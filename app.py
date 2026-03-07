import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- KESİN ÇÖZÜM: TÜM YAZILARI SİYAHA ÇEKİYORUZ ---
st.markdown("""
    <style>
    /* Uygulama Genel Arka Planı */
    .stApp { background-color: #ffffff; }

    /* TÜM FORM ETİKETLERİ VE YAZILAR: Siyah ve Kalın */
    label, p, span, .stMarkdown, .stSelectbox label, .stNumberInput label, .stDateInput label {
        color: #000000 !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    /* ÜST ÖZET BAŞLIKLARI (Metric Labels) */
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }

    /* ÜST ÖZET DEĞERLERİ (Metric Values) - LG KIRMIZISI */
    [data-testid="stMetricValue"] {
        color: #a50034 !important;
        font-weight: 800 !important;
    }
    
    /* Kartların Etrafına Hafif Gri Çerçeve */
    div[data-testid="stMetric"] {
        background-color: #fcfcfc;
        border: 2px solid #eeeeee;
        border-radius: 12px;
        padding: 15px;
    }

    /* Sol Menüdeki LG Logosu (Kırmızı Yuvarlak) */
    .lg-logo {
        width: 60px;
        height: 60px;
        background-color: #a50034;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 20px;
        border: 2px solid #800028;
    }

    /* Input kutularının içindeki yazıların siyah olması */
    input { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.markdown('<div class="lg-logo">LG</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='color:black;'>SATIŞ YÖNETİMİ</h2>", unsafe_allow_html=True)
    
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📦 Ürün Tanımla"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- SAYFA 1: ÜRÜN TANIMLAMA ---
if sekme == "📦 Ürün Tanımla":
    st.markdown("<h1 style='color:black;'>Yeni Model Ekle</h1>", unsafe_allow_html=True)
    with st.form("urun_ekle"):
        m = st.text_input("Model İsmi (Örn: 55QNED81)")
        f = st.number_input("Standart Liste Fiyatı", min_value=0.0)
        p = st.number_input("Adet Başı Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.success("Ürün başarıyla listeye eklendi.")
    
    st.markdown("<h3 style='color:black;'>Mevcut Modeller:</h3>", unsafe_allow_html=True)
    st.table(st.session_state.urunler)

# --- SAYFA 2: DASHBOARD & SATIŞ ---
else:
    # Üst Özet Kartları
    df_s = st.session_state.satislar
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum()
    rk_c = df_s[df_s['Marka'] == "Rakip"]['Ciro'].sum()
    top_c = lg_c + rk_c
    p_payi = (lg_c / top_c * 100) if top_c > 0 else 0
    t_prim = df_s['Prim'].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("LG Cirosu", f"{lg_c:,.0f} TL")
    c2.metric("Pazar Payı", f"%{p_payi:.1f}")
    c3.metric("Toplam Prim", f"{t_prim:,.0f} TL")
    c4.metric("Hedef Durumu", f"%{(lg_c/aylik_hedef*100):.1f}")

    st.divider()

    # SATIŞ GİRİŞ FORMU
    st.markdown("<h2 style='color:black;'>🖋️ Yeni Satış Kaydı</h2>", unsafe_allow_html=True)
    marka_secim = st.selectbox("Marka Seçiniz", ["LG", "Rakip"])
    
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Satış Tarihi", date.today())
        
        if marka_secim == "LG":
            liste = st.session_state.urunler['Model'].tolist()
            if not liste:
                st.warning("Lütfen önce 'Ürün Tanımla' kısmından model ekleyin!")
                final_model, def_fiyat, def_prim = "Yok", 0.0, 0.0
            else:
                secilen = st.selectbox("Model Seçiniz", liste)
                bilgi = st.session_state.urunler[st.session_state.urunler['Model'] == secilen].iloc[0]
