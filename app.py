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
    if not st.session_state.password_correct:
        st.stop()

check_password()

# --- CSS ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] { background-color: #ffffff !important; border: 2px solid #e0e0e0 !important; border-radius: 12px; padding: 20px !important; }
    [data-testid="stMetricLabel"] p { color: #000000 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    [data-testid="stMetricValue"] { color: #a50034 !important; font-weight: 900 !important; font-size: 2rem !important; }
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

# --- SAYFA 1: DASHBOARD & SATIŞ ---
if sekme == "📊 Dashboard & Satış":
    df_s = st.session_state.satislar.copy()
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum() if not df_s.empty else 0
    top_c = df_s['Ciro'].sum() if not df_s.empty else 0
    t_prim = df_s['Prim'].sum() if not df_s.empty else 0
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Reyon Cirosu", f"{top_c:,.0f} TL")
    c2.metric("LG Cirosu", f"{lg_c:,.0f} TL")
    c3.metric("Pazar Payı", f"%{(lg_c/top_c*100) if top_c > 0 else 0:.1f}")
    c4.metric("Toplam Prim", f"{t_prim:,.0f} TL")
    c5.metric("Hedef Durumu", f"%{(lg_c/aylik_hedef*100):.1f}")

    st.divider()
    st.subheader("🖋️ Yeni Satış Kaydı")
    marka_secim = st.selectbox("Marka", ["LG", "Rakip"])
    def_fiyat, def_prim, secilen_model = 0.0, 0.0, "Diğer"
    
    if marka_secim == "LG" and not st.session_state.urunler.empty:
        secilen_model = st.selectbox("Model Seç", st.session_state.urunler['Model'].tolist())
        bilgi = st.session_state.urunler[st.session_state.urunler['Model'] == secilen_model].iloc[0]
        def_fiyat, def_prim = float(bilgi['Liste_Fiyati']), float(bilgi['Birim_Prim'])
            
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Satış Tarihi", date.today())
        f_fiyat = st.number_input("Satış Fiyatı (TL)", value=def_fiyat)
        f_prim = st.number_input("Adet Başı Prim (TL)", value=def_prim)
        f_adet = st.number_input("Adet", min_value=1, value=1)
        f_not = st.text_input("Not")
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{"Tarih": f_tarih, "Marka": marka_secim, "Model": secilen_model, "Ciro": f_fiyat * f_adet, "Prim": f_prim * f_adet, "Adet": f_adet, "Not": f_not}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            st.rerun()

    st.subheader("📋 Satış Listesi")
    st.session_state.satislar = st.data_editor(st.session_state.satislar, use_container_width=True)
    if st.button("Satırı Sil"):
        if not st.session_state.satislar.empty:
            st.session_state.satislar = st.session_state.satislar.iloc[:-1]
            st.rerun()

# --- SAYFA 4: ÜRÜN TANIMLAMA ---
elif sekme == "📦 Ürün Tanımla":
    st.header("Yeni Model Ekle")
    with st.form("urun_ekle", clear_on_submit=True):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Adet Başı Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.rerun()
    st.dataframe(st.session_state.urunler, use_container_width=True)

# (Diğer sayfaları buraya aynı mantıkla ekleyebilirsin)
