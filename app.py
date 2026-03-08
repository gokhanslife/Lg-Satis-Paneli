import streamlit as st
import pandas as pd
from datetime import date
import calendar
import os

# --- VERİ YÜKLEME VE KAYDETME ---
def verileri_yukle():
    satislar = pd.read_csv('satislar.csv') if os.path.exists('satislar.csv') else pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])
    urunler = pd.read_csv('urunler.csv') if os.path.exists('urunler.csv') else pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
    return satislar, urunler

def verileri_kaydet(satislar, urunler):
    satislar.to_csv('satislar.csv', index=False)
    urunler.to_csv('urunler.csv', index=False)

st.set_page_config(page_title="LG Sales Pro", layout="wide")

# Giriş Kontrolü
if "password_correct" not in st.session_state: st.session_state.password_correct = False
if 'satislar' not in st.session_state or 'urunler' not in st.session_state:
    st.session_state.satislar, st.session_state.urunler = verileri_yukle()

if not st.session_state.password_correct:
    st.title("🔐 Giriş")
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if kullanici == "gokhan" and sifre == "825593":
            st.session_state.password_correct = True
            st.rerun()
    st.stop()

# --- CSS ---
st.markdown("""<style>
    div[data-testid="stMetric"] { background-color: #ffffff; border: 2px solid #e0e0e0; border-radius: 12px; padding: 20px; }
    [data-testid="stMetricValue"] { color: #a50034; font-weight: 900; }
</style>""", unsafe_allow_html=True)

# --- MENÜ ---
with st.sidebar:
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📊 Satış Analizleri", "🎯 Hedef Durumu", "📦 Ürün Tanımla"])
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- İŞLEM MANTIKLARI ---
if sekme == "📊 Dashboard & Satış":
    df_s = st.session_state.satislar
    # ... (Metrik hesaplamaları)
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Tarih", date.today())
        marka = st.selectbox("Marka", ["LG", "Rakip"])
        f_fiyat = st.number_input("Satış Fiyatı", value=0.0)
        f_adet = st.number_input("Adet", min_value=1, value=1)
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{"Tarih": f_tarih, "Marka": marka, "Model": "Model", "Ciro": f_fiyat * f_adet, "Prim": 0, "Adet": f_adet, "Not": ""}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            verileri_kaydet(st.session_state.satislar, st.session_state.urunler) # KAYIT
            st.rerun()
    st.dataframe(st.session_state.satislar)

elif sekme == "📦 Ürün Tanımla":
    with st.form("urun_ekle", clear_on_submit=True):
        m = st.text_input("Model İsmi")
        f = st.number_input("Fiyat", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": 0}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            verileri_kaydet(st.session_state.satislar, st.session_state.urunler) # KAYIT
            st.rerun()
    st.dataframe(st.session_state.urunler)
