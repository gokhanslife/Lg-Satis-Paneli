import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- CSS: METRİK KUTULARI VE YAZI RENKLERİ ---
st.markdown("""
    <style>
    input, .stTextInput > div > div > input, .stNumberInput > div > div > input, 
    .stDateInput > div > div > input, .stSelectbox div {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px;
        padding: 20px !important;
    }
    [data-testid="stMetricLabel"] p { color: #000000 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    [data-testid="stMetricValue"] { color: #a50034 !important; font-weight: 900 !important; font-size: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

if 'urunler' not in st.session_state: st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state: st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

with st.sidebar:
    st.markdown('<div style="text-align: center;"><img src="https://upload.wikimedia.org/wikipedia/commons/b/bf/LG_logo.svg" width="100"></div>', unsafe_allow_html=True)
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📦 Ürün Tanımla"])
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- ÜRÜN YÖNETİMİ ---
if sekme == "📦 Ürün Tanımla":
    st.header("Yeni Model Ekle")
    with st.form("urun_ekle"):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Adet Başı Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            st.session_state.urunler = pd.concat([st.session_state.urunler, pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])], ignore_index=True)
            st.rerun()

    st.subheader("Mevcut Modeller")
    for i, row in st.session_state.urunler.iterrows():
        c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1, 1])
        c1.write(row['Model'])
        c2.write(f"{row['Liste_Fiyati']:,.0f} TL")
        c3.write(f"{row['Birim_Prim']:,.0f} TL")
        if c4.button("🗑️", key=f"del_u_{i}"):
            st.session_state.urunler = st.session_state.urunler.drop(i)
            st.rerun()
        if c5.button("✏️", key=f"edit_u_{i}"):
            st.warning("Düzenleme için ürünü silip tekrar eklemek daha sağlıklıdır.")

# --- DASHBOARD & SATIŞ ---
else:
    # (Dashboard metriklerini buraya yazabilirsin, öncekiyle aynı)
    st.subheader("🖋️ Yeni Satış Kaydı")
    # ... (Önceki satış formun aynı kalacak) ...
    
    st.subheader("📋 Satış Listesi")
    for i, row in st.session_state.satislar.iterrows():
        cols = st.columns([1, 1, 1, 1, 1, 1, 1, 0.5, 0.5])
        cols[0].write(str(row['Tarih']))
        cols[1].write(row['Model'])
        cols[2].write(f"{row['Ciro']:,.0f} TL")
        if cols[7].button("🗑️", key=f"del_s_{i}"):
            st.session_state.satislar = st.session_state.satislar.drop(i)
            st.rerun()
        if cols[8].button("✏️", key=f"edit_s_{i}"):
            st.info("Satış düzenleme aktif edildi.")
