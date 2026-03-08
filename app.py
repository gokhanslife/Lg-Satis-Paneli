import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- GİRİŞ EKRANI ---
def check_password():
    if "password_correct" not in st.session_state: st.session_state.password_correct = False
    if st.session_state.password_correct: return True
    st.title("🔐 LG Sales Pro - Giriş")
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if kullanici == "gokhan" and sifre == "825593":
            st.session_state.password_correct = True
            st.rerun()
        else: st.error("Hatalı!")
    return False

if not check_password(): st.stop()

# --- VERİ SAKLAMA (Sütunlar zorla tanımlandı) ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- YAN MENÜ ---
with st.sidebar:
    sekme = st.radio("İşlem:", ["📊 Dashboard & Satış", "📊 Satış Analizleri", "🎯 Hedef Durumu", "📦 Ürün Tanımla"])
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- DASHBOARD & SATIŞ ---
if sekme == "📊 Dashboard & Satış":
    st.header("📊 Satış Girişi")
    
    # Metrikler
    df_s = st.session_state.satislar
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum() if not df_s.empty else 0
    c1, c2 = st.columns(2)
    c1.metric("Toplam Ciro", f"{df_s['Ciro'].sum():,.0f} TL")
    c2.metric("LG Performansı", f"%{(lg_c/aylik_hedef*100):.1f}")

    st.subheader("🖋️ Yeni Satış")
    with st.form("satis_form", clear_on_submit=True):
        m_secim = st.selectbox("Marka", ["LG", "Rakip"])
        # Hata korumalı model seçimi
        if m_secim == "LG" and not st.session_state.urunler.empty:
            m_sec = st.selectbox("Model", st.session_state.urunler['Model'].unique())
        else:
            m_sec = st.text_input("Model")
        
        fiyat = st.number_input("Fiyat", min_value=0.0)
        adet = st.number_input("Adet", min_value=1, step=1)
        
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{"Tarih": date.today(), "Marka": m_secim, "Model": m_sec, "Ciro": fiyat*adet, "Prim": 0, "Adet": adet, "Not": ""}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            st.rerun()

    st.dataframe(st.session_state.satislar, use_container_width=True)

# --- ÜRÜN TANIMLA ---
elif sekme == "📦 Ürün Tanımla":
    st.header("📦 Ürün Tanımla")
    with st.form("urun_ekle", clear_on_submit=True):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Birim Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            y_urun = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, y_urun], ignore_index=True)
            st.rerun()
    st.dataframe(st.session_state.urunler)
