import streamlit as st
import pandas as pd
from datetime import date
from supabase import create_client

# --- BAĞLANTI ---
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

def veri_cek(tablo):
    response = supabase.table(tablo).select("*").execute()
    return pd.DataFrame(response.data)

def veri_kaydet(tablo, data):
    supabase.table(tablo).insert(data).execute()

st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- GİRİŞ KONTROLÜ ---
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

if not st.session_state.password_correct:
    st.title("🔐 Giriş")
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if kullanici == "gokhan" and sifre == "825593":
            st.session_state.password_correct = True
            st.rerun()
    st.stop()

# --- YAN MENÜ ---
with st.sidebar:
    sekme = st.radio("İşlem:", ["📊 Satış Girişi", "📦 Ürün Tanımla"])

# --- SAYFA: DASHBOARD & SATIŞ ---
if sekme == "📊 Satış Girişi":
    st.header("📊 Satış Girişi")
    df_urunler = veri_cek("urunler")
    
    # Sütun isimlerini Supabase'den geldiği gibi kontrol et (genelde küçük harf olur)
    # Eğer hata alırsan Supabase'deki sütun ismine göre burayı değiştir (model, liste_fiyati, birim_prim)
    secilen_model = st.selectbox("Model Seç", df_urunler['model'].tolist())
    model_bilgi = df_urunler[df_urunler['model'] == secilen_model].iloc[0]
    
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Tarih", value=date.today())
        f_adet = st.number_input("Adet", min_value=1, step=1)
        f_not = st.text_input("Not")
        
        if st.form_submit_button("SATIŞI GİR"):
            veri = {
                "tarih": str(f_tarih), 
                "marka": "LG", 
                "model": secilen_model,
                "ciro": float(model_bilgi['liste_fiyati']) * f_adet,
                "prim": float(model_bilgi['birim_prim']) * f_adet,
                "adet": int(f_adet), 
                "not": f_not
            }
            veri_kaydet("satislar", veri)
            st.success("Kaydedildi!")
            st.rerun()

# --- SAYFA: ÜRÜN TANIMLA ---
elif sekme == "📦 Ürün Tanımla":
    st.header("📦 Yeni Model")
    with st.form("urun_ekle"):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Birim Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            veri_kaydet("urunler", {"model": m, "liste_fiyati": f, "birim_prim": p})
            st.rerun()
    st.dataframe(veri_cek("urunler"))
