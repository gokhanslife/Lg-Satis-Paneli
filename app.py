import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide", initial_sidebar_state="expanded")

# --- STİL DOKUNUŞU (LG KIRMIZISI) ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Satis_Cirosu", "Prim", "Adet", "Not"])

# --- YAN MENÜ: AYARLAR & GİRİŞ ---
with st.sidebar:
    st.title("🔴 LG Satış Paneli")
    aylik_hedef = st.number_input("Aylık Ciro Hedefin (TL)", value=1000000, step=10000)
    st.divider()
    
    st.subheader("➕ Yeni Kayıt")
    islem_tipi = st.radio("İşlem Türü", ["LG Satışı", "Rakip Satışı"])
    
    with st.form("kayit_formu", clear_on_submit=True):
        tarih = st.date_input("Satış Tarihi", date.today())
        
        if islem_tipi == "LG Satışı":
            marka = "LG"
            model = st.text_input("Model (Örn: OLED65G4)")
            liste_fiyati = st.number_input("Liste Fiyatı", min_value=0)
            satis_fiyati = st.number_input("Gerçek Satış Fiyatı", value=liste_fiyati)
            prim = st.number_input("Kazanılan Prim (Adet Başı)", min_value=0)
            adet = st.number_input("Adet", min_value=1, value=1)
            toplam_ciro = satis_fiyati * adet
        else:
            marka = "Rakip"
            model = "Diğer"
            toplam_ciro = st.number_input("Toplam Rakip Satış Cirosu (TL)", min_value=0)
            prim = 0
            adet = st.number_input("Tahmini Adet", min_value=1, value=1)

        notlar = st.text_input("Not")
        submit = st.form_submit_button("Sisteme İşle")

if submit:
    yeni_satir = {
        "Tarih": tarih, "Marka": marka, "Model": model, 
        "Satis_Cirosu": toplam_ciro, "Prim": prim * (adet if marka=="LG" else 1), 
        "Adet": adet, "Not": notlar
    }
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([yeni_satir])], ignore_index=True)
    st.success("Kayıt Başarılı!")

# --- HESAPLAMALAR ---
df = st.session_state.data
lg_ciro = df[df['Marka'] == "LG"]['Satis_Cirosu'].sum()
rakip_ciro = df[df['Marka'] == "Rakip"]['Satis_Cirosu'].sum()
toplam_pazar_ciro = lg_ciro + rakip_ciro
pazar_payi = (lg_ciro / toplam_pazar_ciro * 100) if toplam_pazar_ciro > 0 else 0
toplam_prim = df['Prim'].sum()
hedef_yuzde = (lg_ciro / aylik_hedef * 100) if aylik_hedef > 0 else 0

# --- ANA DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("LG Toplam Ciro", f"{lg_ciro:,.0f} TL")
col2.metric("Pazar Payı (Ciro)", f"%{pazar_payi:.1f}")
col3.metric("Toplam Primin", f"{toplam_prim:,.0f} TL")
col4.metric("Hedef Gerçekleşme", f"%{hedef_yuzde:.1f}")

st.progress(min(hedef_yuzde/100, 1.0), text=f"Hedef Yolculuğu: %{hedef_yuzde:.1f}")

st.divider()

# --- LİSTELEME ---
st.subheader("📋 Son İşlemler")
st.dataframe(df.sort_values(by="Tarih", ascending=False), use_container_width=True)
