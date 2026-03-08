import streamlit as st
import pandas as pd
from datetime import date
import calendar
from supabase import create_client

# --- SUPABASE BAĞLANTISI ---
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# --- VERİ İŞLEMLERİ ---
def veri_cek(tablo):
    response = supabase.table(tablo).select("*").execute()
    return pd.DataFrame(response.data)

def veri_kaydet(tablo, data):
    supabase.table(tablo).insert(data).execute()

# --- GİRİŞ EKRANI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

if not st.session_state.password_correct:
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

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📦 Ürün Tanımla"])
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- SAYFA: DASHBOARD & SATIŞ ---
if sekme == "📊 Dashboard & Satış":
    st.header("📊 Satış Girişi")
    urunler_df = veri_cek("urunler")
    
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Satış Tarihi", value=date.today())
        secilen_model = st.selectbox("Model Seç", urunler_df['Model'].tolist())
        model_bilgi = urunler_df[urunler_df['Model'] == secilen_model].iloc[0]
        f_adet = st.number_input("Adet", min_value=1, step=1)
        f_not = st.text_input("Not")
        
        if st.form_submit_button("SATIŞI GİR"):
            veri = {
                "tarih": str(f_tarih), "marka": "LG", "model": secilen_model,
                "ciro": float(model_bilgi['Liste_Fiyati']) * f_adet,
                "prim": float(model_bilgi['Birim_Prim']) * f_adet,
                "adet": int(f_adet), "not": f_not
            }
            veri_kaydet("satislar", veri)
            st.success("Kaydedildi!")
            st.rerun()

# --- SAYFA: ÜRÜN TANIMLA ---
elif sekme == "📦 Ürün Tanımla":
    st.header("📦 Yeni Model Ekle")
    with st.form("urun_ekle"):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Birim Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            veri_kaydet("urunler", {"Model": m, "Liste_Fiyati": f, "Birim_Prim": p})
            st.rerun()
    
    st.subheader("Mevcut Modeller")
    st.dataframe(veri_cek("urunler"))
