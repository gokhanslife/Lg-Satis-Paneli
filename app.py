import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- CSS: HER TÜR AYARA RAĞMEN BEYAZ ARKA PLAN VE SİYAH YAZI ---
st.markdown("""
    <style>
    /* Uygulama Arka Planını Zorla Beyaz Yap */
    .stApp, .stApp > header, .stApp > footer { 
        background-color: #ffffff !important; 
    }
    
    /* Yan Menü (Sidebar) Arka Planını Beyaz Yap */
    [data-testid="stSidebar"] { 
        background-color: #f0f2f6 !important; 
    }

    /* TÜM YAZILARI SİYAH YAP */
    body, p, label, span, div, h1, h2, h3, .stMarkdown, 
    .stSelectbox label, .stNumberInput label, .stDateInput label, .stTextInput label {
        color: #000000 !important;
    }
    
    /* Input Alanlarını Beyaz Arka Plan ve Siyah Yazı Yap */
    input, .st-ar, .st-as, .st-at, .st-au, .st-av, .st-aw {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }

    /* ÜST ÖZET BAŞLIKLARI (Koyu Siyah ve Kalın) */
    [data-testid="stMetricLabel"] p {
        color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: 900 !important;
    }

    /* ÜST ÖZET DEĞERLERİ (LG Kırmızısı) */
    [data-testid="stMetricValue"] {
        color: #a50034 !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
    }
    
    /* Kartların Etrafına Hafif Gri Çerçeve */
    div[data-testid="stMetric"] {
        background-color: #fcfcfc;
        border: 2px solid #eeeeee;
        border-radius: 12px;
        padding: 15px;
    }
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
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📦 Ürün Tanımla"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- SAYFA 1 ---
if sekme == "📦 Ürün Tanımla":
    st.header("Yeni Model Ekle")
    with st.form("urun_ekle"):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Adet Başı Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.success("Ürün eklendi.")
    st.table(st.session_state.urunler)

# --- SAYFA 2 ---
else:
    df_s = st.session_state.satislar
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum() if not df_s.empty else 0
    rk_c = df_s[df_s['Marka'] == "Rakip"]['Ciro'].sum() if not df_s.empty else 0
    top_c = lg_c + rk_c
    p_payi = (lg_c / top_c * 100) if top_c > 0 else 0
    t_prim = df_s['Prim'].sum() if not df_s.empty else 0
    
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
            final_ciro, final_prim, final_model = f_fiyat * f_adet, f_prim * f_adet, secilen
        else:
            final_model, final_ciro, final_prim = "Diğer", st.number_input("Rakip Toplam Ciro", min_value=0.0), 0.0
            f_adet = st.number_input("Adet", min_value=1, value=1)
            
        f_not = st.text_input("Not")
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{"Tarih": f_tarih, "Marka": marka_secim, "Model": final_model, "Ciro": final_ciro, "Prim": final_prim, "Adet": f_adet, "Not": f_not}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            st.rerun()

    st.subheader("📋 Satış Listesi")
    st.dataframe(df_s, use_container_width=True)
