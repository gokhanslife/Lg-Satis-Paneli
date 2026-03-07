import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- CSS: HÜCRELERİ VE METİNLERİ YÖNETME ---
st.markdown("""
    <style>
    /* Uygulama Genel */
    .stApp { background-color: #ffffff !important; }
    
    /* GENEL YAZILAR SİYAH */
    html, body, p, label, span, div, h1, h2, h3, .stMarkdown, 
    .stSelectbox label, .stNumberInput label, .stDateInput label, .stTextInput label {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* ÜST ÖZET BAŞLIKLARI */
    [data-testid="stMetricLabel"] p {
        color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: 900 !important;
    }
    
    /* ÜST ÖZET DEĞERLERİ */
    [data-testid="stMetricValue"] {
        color: #a50034 !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
    }

    /* DATAFRAME HÜCRELERİ: BEYAZ YAZI */
    [data-testid="stDataFrameResizable"] div[data-testid="stDataFrameView"] {
        color: #ffffff !important;
        background-color: #333333 !important; /* Arka planı koyulaştırdık ki beyaz yazı okunsun */
    }

    .lg-logo {
        width: 60px; height: 60px;
        background-color: #a50034;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: white !important;
        font-weight: bold; margin-bottom: 20px; font-size: 20px;
    }
    input { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- YAN MENÜ ---
with st.sidebar:
    st.markdown('<div class="lg-logo">LG</div>', unsafe_allow_html=True)
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📦 Ürün Tanımla"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- SAYFA 1 ---
if sekme == "📦 Ürün Tanımla":
    st.header("Yeni Model Ekle")
    with st.form("urun_ekle"):
        m = st.text_input("Model İsmi (Örn: 55QNED81)")
        f = st.number_input("Standart Liste Fiyatı", min_value=0.0)
        p = st.number_input("Adet Başı Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.success("Ürün başarıyla listeye eklendi.")
    st.dataframe(st.session_state.urunler, use_container_width=True)

# --- SAYFA 2 ---
else:
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
    st.subheader("🖋️ Yeni Satış Kaydı")
    
    with st.form("satis_form", clear_on_submit=True):
        marka_secim = st.selectbox("Marka", ["LG", "Rakip"])
        f_tarih = st.date_input("Satış Tarihi", date.today())
        
        if marka_secim == "LG":
            liste = st.session_state.urunler['Model'].tolist()
            if liste:
                secilen = st.selectbox("Model Seç", liste)
                bilgi = st.session_state.urunler[st.session_state.urunler['Model'] == secilen].iloc[0]
                def_fiyat, def_prim = float(bilgi['Liste_Fiyati']), float(bilgi['Birim_Prim'])
            else:
                secilen, def_fiyat, def_prim = "Yok", 0.0, 0.0
            
            f_fiyat = st.number_input("Satış Fiyatı (TL)", value=def_fiyat)
            f_prim = st.number_input("Adet Başı Prim (TL)", value=def_prim)
            f_adet = st.number_input("Adet", min_value=1, value=1)
            
            final_ciro = f_fiyat * f_adet
            final_prim = f_prim * f_adet
            final_model = secilen
        else:
            final_model = "Diğer"
            final_ciro = st.number_input("Rakip Toplam Satış Cirosu", min_value=0.0)
            f_adet = st.number_input("Adet", min_value=1, value=1)
            final_prim = 0.0
            
        f_not = st.text_input("Not")
        
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{
                "Tarih": f_tarih, "Marka": marka_secim, "Model": final_model, 
                "Ciro": final_ciro, "Prim": final_prim, "Adet": f_adet, "Not": f_not
            }])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            st.rerun()

    st.subheader("📋 Satış Listesi")
    st.dataframe(df_s, use_container_width=True)
