import streamlit as st
import pandas as pd
from datetime import date
import calendar
from supabase import create_client

# --- SUPABASE BAĞLANTISI ---
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# --- VERİ ÇEKME VE KAYDETME FONKSİYONLARI ---
def veri_ekle(tablo, data):
    # 'data' burada bir sözlük olmalı: {"Model": "LG OLED", "Liste_Fiyati": 1000, "Birim_Prim": 50}
    supabase.table(tablo).insert(data).execute()

def veri_cek(tablo):
    response = supabase.table(tablo).select("*").execute()
    return pd.DataFrame(response.data)

def veri_kaydet(tablo, data):
    supabase.table(tablo).insert(data).execute()

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- ŞİFRE GİRİŞ EKRANI ---
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
            st.error("Kullanıcı adı veya şifre hatalı!")
    st.stop()

check_password()

# --- CSS (Senin Tasarımın) ---
st.markdown("""<style>...</style>""", unsafe_allow_html=True)
elif sekme == "📦 Ürün Tanımla":
    st.header("📦 Yeni Model Ekle")
    with st.form("urun_ekle"):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Adet Başı Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            # Veriyi Supabase'e gönderiyoruz
            veri_ekle("urunler", {"Model": m, "Liste_Fiyati": f, "Birim_Prim": p})
            st.success("Model başarıyla kaydedildi!")
            st.rerun()
            
    st.subheader("Mevcut Modeller")
    df_urunler = veri_cek("urunler") # Veritabanından çek
    st.dataframe(df_urunler) # Listele

# --- YAN MENÜ ---
with st.sidebar:
    st.markdown('<div style="text-align: center;"><img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/LG_logo_%282014%29.svg" width="100"></div>', unsafe_allow_html=True)
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📊 Satış Analizleri", "🎯 Hedef Durumu", "📦 Ürün Tanımla"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- SAYFA 1: DASHBOARD & SATIŞ ---
if sekme == "📊 Dashboard & Satış":
    df_s = veri_cek("satislar")
    urunler = veri_cek("urunler")
    
    # Metrikler ve Satış Girişi burada...
    # (Not: veri_kaydet("satislar", {...}) fonksiyonunu kullanarak verini gönder)
    # ...

# --- DİĞER SAYFALAR AYNI MANTIKLA DEVAM EDER ---
# Tek yapman gereken session_state.satislar yerine veri_cek("satislar") kullanmak!
