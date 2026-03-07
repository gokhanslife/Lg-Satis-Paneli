import streamlit as st
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- GÖRÜNÜRLÜK VE STİL AYARLARI (TAM OKUNABİLİRLİK) ---
st.markdown("""
    <style>
    /* Metin Renkleri Fix */
    label, p, span, div { color: #1e1e1e !important; font-weight: 500; }
    .stMetric label { color: #555555 !important; }
    [data-testid="stMetricValue"] { color: #a50034 !important; font-size: 2rem !important; }
    
    /* Kart Tasarımları */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Giriş Kutuları Arka Planı */
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
        color: #000000 !important;
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
    st.header("🔴 LG MENÜ")
    sekme = st.radio("Sayfa Değiştir:", ["📊 Satış Dashboard", "📦 Model Ekle/Sil"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Ciro Hedefin (TL)", value=1000000)

# --- 1. SAYFA: MODEL YÖNETİMİ ---
if sekme == "📦 Model Ekle/Sil":
    st.subheader("Yeni Model Tanımla")
    with st.form("yeni_urun"):
        m = st.text_input("Model İsmi")
        f = st.number_input("Standart Fiyat", min_value=0)
        p = st.number_input("Adet Başı Prim", min_value=0)
        if st.form_submit_button("Kütüphaneye Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.success(f"{m} başarıyla eklendi.")
    
    st.write("Kayıtlı Modellerin:")
    st.dataframe(st.session_state.urunler, use_container_width=True)

# --- 2. SAYFA: DASHBOARD & SATIŞ ---
else:
    # Üst Özet Kartları
    df_s = st.session_state.satislar
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum()
    rk_c = df_s[df_s['Marka'] == "Rakip"]['Ciro'].sum()
    p_payi = (lg_c / (lg_c + rk_c) * 100) if (lg_c + rk_c) > 0 else 0
    t_prim = df_s['Prim'].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("LG Cirosu", f"{lg_c:,.0f} TL")
    c2.metric("Pazar Payı", f"%{p_payi:.1f}")
    c3.metric("Toplam Prim", f"{t_prim:,.0f} TL")
    c4.metric("Hedef Durumu", f"%{(lg_c/aylik_hedef*100):.1f}")

    st.divider()

    # SATIŞ GİRİŞ FORMU
    st.subheader("🖋️ Satış Kaydı Oluştur")
    marka_secim = st.selectbox("Satılan Marka", ["LG", "Rakip"])
    
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Satış Tarihi", date.today())
        
        if marka_secim == "LG":
            # Kütüphaneden modelleri çek
            liste = st.session_state.urunler['Model'].tolist()
            secilen = st.selectbox("Model Seç", liste if liste else ["Lütfen önce model ekleyin"])
            
            # Otomatik Değerleri Bul
            if liste:
                bilgi = st.session_state.urunler[st.session_state.urunler['Model'] == secilen].iloc[0]
                def_fiyat = float(bilgi['Liste_Fiyati'])
                def_prim = float(bilgi['Birim_Prim'])
            else:
                def_fiyat, def_prim = 0.0, 0.0
            
            # Form Alanları
            f_fiyat = st.number_input("Satış Fiyatı (TL)", value=def_fiyat)
            f_prim = st.number_input("Birim Prim (TL)", value=def_prim)
            f_adet = st.number_input("Adet", min_value=1, value=1)
            
            final_ciro = f_fiyat * f_adet
            final_prim = f_prim * f_adet
            final_model = secilen
        else:
            final_model = "Rakip TV"
            final_ciro = st.number_input("Toplam Rakip Satış Cirosu", min_value=0)
            f_adet = st.number_input("Adet", min_value=1, value=1)
            final_prim = 0
            
        f_not = st.text_input("Notlar")
        
        if st.form_submit_button("SATIŞI KAYDET"):
            y_satis = pd.DataFrame([{
                "Tarih": f_tarih, "Marka": marka_secim, "Model": final_model, 
                "Ciro": final_ciro, "Prim": final_prim, "Adet": f_adet, "Not": f_not
            }])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            st.rerun()

    st.subheader("📋 Kayıt Geçmişi")
    st.dataframe(df_s.sort_values(by="Tarih", ascending=False), use_container_width=True)
