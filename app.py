import streamlit as st
import pandas as pd
from datetime import date
import calendar

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- GİRİŞ KONTROLÜ ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if st.session_state.password_correct:
        return
    st.title("🔐 LG Sales Pro - Giriş")
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if kullanici == "gokhan" and sifre == "825593":
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Hatalı!")
    st.stop()

check_password()

# --- CSS ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] { background-color: #ffffff !important; border: 2px solid #e0e0e0 !important; border-radius: 12px; padding: 20px !important; }
    [data-testid="stMetricLabel"] p { color: #000000 !important; font-weight: 900 !important; }
    [data-testid="stMetricValue"] { color: #a50034 !important; font-weight: 900 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📦 Ürün Tanımla"])
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- SAYFA 1: DASHBOARD & SATIŞ ---
if sekme == "📊 Dashboard & Satış":
    st.header("📊 Dashboard")
    df = st.session_state.satislar
    c1, c2 = st.columns(2)
    c1.metric("Toplam Ciro", f"{df['Ciro'].sum():,.0f} TL")
    c2.metric("Hedef (%)", f"{(df['Ciro'].sum()/aylik_hedef*100):.1f}")
    
    st.subheader("🖋️ Yeni Satış")
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Tarih", date.today())
        marka = st.selectbox("Marka", ["LG", "Rakip"])
        fiyat = st.number_input("Tutar", min_value=0.0)
        adet = st.number_input("Adet", min_value=1)
        
        if st.form_submit_button("KAYDET"):
            yeni = pd.DataFrame([{"Tarih": f_tarih, "Marka": marka, "Model": "Model", "Ciro": fiyat, "Prim": 0, "Adet": adet, "Not": ""}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, yeni], ignore_index=True)
            st.rerun()
    st.dataframe(st.session_state.satislar)

# --- SAYFA 2: ÜRÜN TANIMLAMA ---
elif sekme == "📦 Ürün Tanımla":
    st.header("📦 Ürün Tanımla")
    with st.form("urun_ekle", clear_on_submit=True):
        m = st.text_input("Model Adı")
        f = st.number_input("Fiyat")
        if st.form_submit_button("Ekle"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": 0}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.rerun()
    st.dataframe(st.session_state.urunler)
