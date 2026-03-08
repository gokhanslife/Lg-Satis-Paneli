import streamlit as st
import pandas as pd
from datetime import date
import calendar
from supabase import create_client

# --- SUPABASE BAĞLANTISI ---
# Streamlit Secrets'tan çekiyoruz
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# --- VERİ YÜKLEME (Supabase'den çekip session_state'e aktarma) ---
if 'initialized' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(supabase.table("urunler").select("*").execute().data)
    st.session_state.satislar = pd.DataFrame(supabase.table("satislar").select("*").execute().data)
    st.session_state.initialized = True

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- GİRİŞ KONTROLÜ (Senin kodun) ---
def check_password():
    if "password_correct" not in st.session_state: st.session_state.password_correct = False
    if st.session_state.password_correct: return
    st.title("🔐 LG Sales Pro - Giriş")
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if kullanici == "gokhan" and sifre == "825593":
            st.session_state.password_correct = True
            st.rerun()
        else: st.error("Hatalı!")
    st.stop()

check_password()

# --- CSS (Senin kodun) ---
st.markdown("""<style>... senin CSS kodun ...</style>""", unsafe_allow_html=True)

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📊 Satış Analizleri", "🎯 Hedef Durumu", "📦 Ürün Tanımla"])
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- İŞLEM FONKSİYONLARI ---
def save_to_supabase(tablo, dataframe):
    # Tabloyu temizle ve yeniden yükle (Basit yöntem)
    supabase.table(tablo).delete().neq("id", 0).execute() # Önce eskiyi sil
    if not dataframe.empty:
        supabase.table(tablo).insert(dataframe.to_dict(orient='records')).execute()

# --- SAYFALAR ---
# Buraya senin dashboard, analiz, hedef ve ürün tanımlama sayfalarını aynen yapıştır.
# ÖNEMLİ: Herhangi bir veri ekleme/silme butonundan sonra şu satırı ekle:
# save_to_supabase("satislar", st.session_state.satislar)
# save_to_supabase("urunler", st.session_state.urunler)
