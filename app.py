import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Dashboard", layout="wide")

# --- GÖRSEL AYARLAR (CSS) ---
st.markdown("""
    <style>
    /* Arka plan bembeyaz */
    .stApp { background-color: #ffffff !important; }
    
    /* TÜM YAZILAR SİMSİYAH VE OKUNUR */
    html, body, [class*="st-"], label, p, span {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* ÜSTTEKİ RAKAMLAR LG KIRMIZISI */
    [data-testid="stMetricValue"] {
        color: #a50034 !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
    }
    
    /* ÜSTTEKİ BAŞLIKLAR SİYAH */
    [data-testid="stMetricLabel"] p {
        color: #000000 !important;
        font-size: 16px !important;
    }

    /* LG YUVARLAK LOGO */
    .lg-round {
        width: 60px; height: 60px;
        background-color: #a50034;
        border-radius: 50%;
        color: white !important;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 22px;
        margin-bottom: 15px;
        border: 2px solid #7a0026;
    }
    
    /* Input kutularının içindeki yazılar siyah */
    input { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- YAN MENÜ ---
with st.sidebar:
    st.markdown('<div class="lg-round">LG</div>', unsafe_allow_html=True)
    st.title("LG Satış Yönetimi")
    sayfa = st.radio("Menü:", ["📊 Dashboard", "📦 Ürün Tanımla"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- 1. SAYFA: ÜRÜN TANIMLAMA ---
if sayfa == "📦 Ürün Tanımla":
    st.header("Yeni Model Tanımla")
    with st.form("yeni_model_form"):
        m_ad = st.text_input("Model Adı")
        m_fiyat = st.number_input("Liste Fiyatı", min_value=0.0)
        m_prim = st.number_input("Adet Başı Prim", min_value=0.0)
        
        if st.form_submit_button("Modeli Kaydet"):
            yeni_m = pd.DataFrame([{"Model": m_ad, "Liste_Fiyati": m_fiyat, "Birim_Prim": m_prim}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni_m], ignore_index=True)
            st.success("Model başarıyla eklendi!")
    
    st.subheader("Kayıtlı LG Modelleri")
    st.dataframe(st.session_state.urunler, use_container_width=True)

# --- 2. SAYFA: DASHBOARD ---
else:
    df_s = st.session_state.satislar
    # Hesaplamalar
    lg_c = float(df_s[df_s['Marka'] == "LG"]['Ciro'].sum()) if not df_s.empty else 0.0
    rk_c = float(df_s[df_s['Marka'] == "Rakip"]['Ciro'].sum()) if not df_s.empty else 0.0
    toplam_pazar = lg_c + rk_c
    p_payi = (lg_c / toplam_pazar * 100) if toplam_pazar > 0 else 0.0
    toplam_prim = float(df_
