import streamlit as st
import pandas as pd
from datetime import date
import calendar

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- GİRİŞ EKRANI ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if st.session_state.password_correct:
        return True
    
    st.title("🔐 LG Sales Pro - Giriş")
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if kullanici == "gokhan" and sifre == "825593":
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")
    return False

if not check_password():
    st.stop()

# --- CSS ---
st.markdown("""
    <style>
    [data-testid="stMetric"] { background-color: #ffffff; border: 2px solid #e0e0e0; border-radius: 12px; padding: 20px; }
    [data-testid="stMetricLabel"] p { color: #000000; font-weight: 900; font-size: 1.1rem; }
    [data-testid="stMetricValue"] { color: #a50034; font-weight: 900; font-size: 2rem; }
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
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📊 Satış Analizleri", "🎯 Hedef Durumu", "📦 Ürün Tanımla"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- DASHBOARD ---
if sekme == "📊 Dashboard & Satış":
    st.header("📊 Dashboard & Satış Girişi")
    df_s = st.session_state.satislar
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum() if not df_s.empty else 0
    top_c = df_s['Ciro'].sum() if not df_s.empty else 0
    t_prim = df_s['Prim'].sum() if not df_s.empty else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Ciro", f"{top_c:,.0f} TL")
    c2.metric("LG Cirosu", f"{lg_c:,.0f} TL")
    c3.metric("Toplam Prim", f"{t_prim:,.0f} TL")
    c4.metric("Hedef Durumu", f"%{(lg_c/aylik_hedef*100):.1f}")

    st.subheader("🖋️ Yeni Satış Kaydı")
    with st.form("satis_form", clear_on_submit=True):
        m_secim = st.selectbox("Marka", ["LG", "Rakip"])
        model_sec = st.selectbox("Model", st.session_state.urunler['Model'].tolist()) if m_secim=="LG" else st.text_input("Model")
        fiyat = st.number_input("Fiyat", value=0.0)
        adet = st.number_input("Adet", min_value=1, value=1)
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{"Tarih": date.today(), "Marka": m_secim, "Model": model_sec, "Ciro": fiyat*adet, "Prim": 0, "Adet": adet, "Not": ""}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            st.rerun()

    st.subheader("📋 Satış Listesi")
    st.dataframe(st.session_state.satislar, use_container_width=True)

# --- ÜRÜN TANIMLA ---
elif sekme == "📦 Ürün Tanımla":
    st.header("📦 Yeni Model Ekle")
    with st.form("urun_ekle", clear_on_submit=True):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Birim Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            st.session_state.urunler = pd.concat([st.session_state.urunler, pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])], ignore_index=True)
            st.rerun()
    st.dataframe(st.session_state.urunler)
