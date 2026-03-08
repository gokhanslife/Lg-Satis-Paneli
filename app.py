import streamlit as st
import pandas as pd
from datetime import date
import calendar

st.set_page_config(page_title="LG Sales Pro", layout="wide")

# CSS - Görüntü Ayarı
st.markdown("""
    <style>
    div[data-testid="stMetric"] { background-color: #ffffff; border: 2px solid #e0e0e0; border-radius: 12px; padding: 20px; }
    [data-testid="stMetricLabel"] p { color: #000000; font-weight: 900; }
    [data-testid="stMetricValue"] { color: #a50034; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

# Session State Hazırlığı
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# Yan Menü
with st.sidebar:
    sekme = st.radio("İşlem:", ["📊 Dashboard & Satış", "📦 Ürün Tanımla"])
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# Dashboard Sayfası
if sekme == "📊 Dashboard & Satış":
    st.header("📊 Satış Girişi")
    df_s = st.session_state.satislar
    
    # Metrikler
    top_c = df_s['Ciro'].sum() if not df_s.empty else 0
    c1, c2 = st.columns(2)
    c1.metric("Toplam Ciro", f"{top_c:,.0f} TL")
    c2.metric("Hedef Durumu", f"%{(top_c/aylik_hedef*100):.1f}")

    # Satış Formu
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Tarih", date.today())
        marka = st.selectbox("Marka", ["LG", "Rakip"])
        model = st.text_input("Model")
        fiyat = st.number_input("Toplam Fiyat", min_value=0.0)
        adet = st.number_input("Adet", min_value=1)
        notlar = st.text_input("Not")
        
        submitted = st.form_submit_button("SATIŞI GİR")
        if submitted:
            yeni = pd.DataFrame([{"Tarih": f_tarih, "Marka": marka, "Model": model, "Ciro": fiyat, "Prim": 0, "Adet": adet, "Not": notlar}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, yeni], ignore_index=True)
            st.rerun()

    st.dataframe(st.session_state.satislar, use_container_width=True)

# Ürün Tanımla Sayfası
elif sekme == "📦 Ürün Tanımla":
    st.header("📦 Ürün Tanımla")
    with st.form("urun_ekle", clear_on_submit=True):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı")
        p = st.number_input("Prim")
        if st.form_submit_button("Sisteme Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.rerun()
    st.dataframe(st.session_state.urunler, use_container_width=True)
