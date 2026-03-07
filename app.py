import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Master", layout="wide")

# --- KOYU TEMA VE OKUNABİLİRLİK AYARI (CSS) ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #a50034 !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #333333 !important; font-size: 1.1rem; }
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #a50034;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA (Session State) ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- SOL PANEL: YÖNETİM ---
with st.sidebar:
    st.title("🔴 LG YÖNETİM")
    sekme = st.radio("Git:", ["📊 Dashboard & Satış Gir", "📦 Ürün Kütüphanesi"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Ciro Hedefin (TL)", value=1000000)

# --- SAYFA 1: ÜRÜN KÜTÜPHANESİ ---
if sekme == "📦 Ürün Kütüphanesi":
    st.header("Yeni Model Tanımla")
    with st.form("urun_ekle"):
        y_model = st.text_input("Model Adı (Örn: 65C5)")
        y_fiyat = st.number_input("Liste Fiyatı", min_value=0)
        y_prim = st.number_input("Adet Başı Prim", min_value=0)
        if st.form_submit_button("Kütüphaneye Ekle"):
            yeni_u = pd.DataFrame([{"Model": y_model, "Liste_Fiyati": y_fiyat, "Birim_Prim": y_prim}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni_u], ignore_index=True)
            st.success("Model eklendi!")
    
    st.subheader("Kayıtlı Modeller")
    st.table(st.session_state.urunler)

# --- SAYFA 2: DASHBOARD & SATIŞ ---
else:
    # Üst Özet Kartları
    df_s = st.session_state.satislar
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum()
    rk_c = df_s[df_s['Marka'] == "Rakip"]['Ciro'].sum()
    top_p = lg_c + rk_c
    p_payi = (lg_c / top_p * 100) if top_p > 0 else 0
    t_prim = df_s['Prim'].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("LG Toplam Ciro", f"{lg_c:,.0f} TL")
    c2.metric("Pazar Payı", f"%{p_payi:.1f}")
    c3.metric("Toplam Prim", f"{t_prim:,.0f} TL")
    c4.metric("Hedef Durumu", f"%{(lg_c/aylik_hedef*100):.1f}")

    st.divider()

    # Satış Giriş Formu
    st.subheader("➕ Yeni Satış Girişi")
    islem = st.selectbox("Marka Seç", ["LG", "Rakip"])
    
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Tarih", date.today())
        
        if islem == "LG":
            # Kütüphanedeki modelleri getir
            modeller = st.session_state.urunler['Model'].tolist()
            secilen_model = st.selectbox("Model Seç", ["Manuel Gir"] + modeller)
            
            # Otomatik Değerleri Çek
            varsayilan_fiyat = 0
            varsayilan_prim = 0
            if secilen_model != "Manuel Gir":
                row = st.session_state.urunler[st.session_state.urunler['Model'] == secilen_model].iloc[0]
                varsayilan_fiyat = row['Liste_Fiyati']
                varsayilan_prim = row['Birim_Prim']
            
            f_model = st.text_input("Model Teyit/Manuel", value=secilen_model)
            f_fiyat = st.number_input("Satış Fiyatı", value=float(varsayilan_fiyat))
            f_prim = st.number_input("Birim Prim", value=float(varsayilan_prim))
            f_adet = st.number_input("Adet", min_value=1, value=1)
            f_ciro = f_fiyat * f_adet
            f_toplam_prim = f_prim * f_adet
        else:
            f_model = "Diğer"
            f_ciro = st.number_input("Toplam Ciro (TL)", min_value=0)
            f_adet = st.number_input("Adet", min_value=1, value=1)
            f_toplam_prim = 0
            
        f_not = st.text_input("Not")
        
        if st.form_submit_button("Kaydet"):
            yeni_s = pd.DataFrame([{
                "Tarih": f_tarih, "Marka": islem, "Model": f_model, 
                "Ciro": f_ciro, "Prim": f_toplam_prim, "Adet": f_adet, "Not": f_not
            }])
            st.session_state.satislar = pd.concat([st.session_state.satislar, yeni_s], ignore_index=True)
            st.rerun()

    st.subheader("📋 Satış Geçmişi")
    st.dataframe(df_s, use_container_width=True)
