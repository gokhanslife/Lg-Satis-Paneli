import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- CSS: TÜM YAZILARI SİYAHA SABİTLEME ---
st.markdown("""
    <style>
    /* Arka plan beyaz */
    .stApp { background-color: white !important; }
    
    /* Tüm metinler siyah */
    html, body, [class*="st-"] {
        color: black !important;
        font-family: sans-serif;
    }

    /* Üst kartlardaki başlıklar siyah ve kalın */
    [data-testid="stMetricLabel"] p {
        color: black !important;
        font-weight: 900 !important;
        font-size: 18px !important;
    }

    /* Üst kartlardaki rakamlar kırmızı */
    [data-testid="stMetricValue"] {
        color: #a50034 !important;
        font-weight: bold !important;
    }

    /* Form etiketleri siyah */
    .stWidgetForm label p {
        color: black !important;
        font-weight: bold !important;
    }
    
    /* Sol menü logosu */
    .lg-round {
        width: 60px; height: 60px;
        background-color: #a50034;
        border-radius: 50%;
        color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA ÜNİTESİ ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="lg-round">LG</div>', unsafe_allow_html=True)
    st.title("YÖNETİM")
    sayfa = st.radio("Sekmeler", ["📊 Dashboard", "📦 Ürün Tanımla"])
    st.divider()
    hedef = st.number_input("Aylık Hedef TL", value=1000000)

# --- ÜRÜN TANIMLAMA SAYFASI ---
if sayfa == "📦 Ürün Tanımla":
    st.subheader("Yeni Ürün Ekle")
    with st.form("yeni_u_form"):
        m_ad = st.text_input("Model")
        m_fiyat =
