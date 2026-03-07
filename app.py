import streamlit as st
import pandas as pd
from datetime import date, timedelta
import calendar

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    input, .stTextInput > div > div > input, .stNumberInput > div > div > input, 
    .stDateInput > div > div > input, .stSelectbox div { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    div[data-testid="stMetric"] { background-color: #ffffff !important; border: 2px solid #e0e0e0 !important; border-radius: 12px; padding: 20px !important; }
    [data-testid="stMetricLabel"] p { color: #000000 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    [data-testid="stMetricValue"] { color: #a50034 !important; font-weight: 900 !important; font-size: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA ---
if 'urunler' not in st.session_state: st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state: st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- YAN MENÜ ---
with st.sidebar:
    st.markdown('<div style="text-align: center;"><img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/LG_logo_%282014%29.svg" width="100"></div>', unsafe_allow_html=True)
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📈 Satış Analizleri", "🎯 Hedef Durumu", "📦 Ürün Tanımla"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- 1. DASHBOARD ---
if sekme == "📊 Dashboard & Satış":
    df_s = st.session_state.satislar.copy()
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum() if not df_s.empty else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("LG Cirosu", f"{lg_c:,.0f} TL")
    c4.metric("Hedef Durumu", f"%{(lg_c/aylik_hedef*100):.1f}")
    
    st.subheader("🖋️ Yeni Satış Kaydı")
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Satış Tarihi", date.today())
        f_fiyat = st.number_input("Satış Fiyatı (TL)", value=0.0)
        f_adet = st.number_input("Adet", min_value=1, value=1)
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{"Tarih": f_tarih, "Marka": "LG", "Model": "Model", "Ciro": f_fiyat * f_adet, "Prim": 0, "Adet": f_adet, "Not": ""}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            st.rerun()

# --- 2. ANALİZLER ---
elif sekme == "📈 Satış Analizleri":
    st.header("📈 Satış Analizleri")
    if not st.session_state.satislar.empty:
        df = st.session_state.satislar.copy()
        df['Tarih'] = pd.to_datetime(df['Tarih'])
        def al(data): return data.groupby('Model')['Adet'].sum().reset_index().sort_values(by='Adet', ascending=False)
        col1, col2 = st.columns(2)
        col1.write("Tüm Zamanlar"); col1.dataframe(al(df), use_container_width=True)
        col2.write("Son 30 Gün"); col2.dataframe(al(df[df['Tarih'] >= (pd.Timestamp.now() - timedelta(days=30))]), use_container_width=True)

# --- 3. HEDEF DURUMU (PROJEKSİYON) ---
elif sekme == "🎯 Hedef Durumu":
    st.header("🎯 Hedef Gerçekleştirme Analizi")
    if not st.session_state.satislar.empty:
        df = st.session_state.satislar.copy()
        df['Tarih'] = pd.to_datetime(df['Tarih'])
        lg_ciro = df[df['Marka'] == "LG"]['Ciro'].sum()
        
        bugun = date.today()
        gun_sayisi = bugun.day
        ay_gun_sayisi = calendar.monthrange(bugun.year, bugun.month)[1]
        
        tahmini_ciro = (lg_ciro / gun_sayisi) * ay_gun_sayisi
        projeksiyon_yuzde = (tahmini_ciro / aylik_hedef) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gerçekleşen", f"{lg_ciro:,.0f} TL")
        c2.metric("Ay Sonu Tahmini", f"{tahmini_ciro:,.0f} TL")
        c3.metric("Projeksiyon (%)", f"%{projeksiyon_yuzde:.1f}")
        
        st.info(f"Ayın {gun_sayisi}. günündeyiz. Bu hızla devam edilirse, ay sonu hedef gerçekleşme oranınız %{projeksiyon_yuzde:.1f} olacaktır.")
    else:
        st.info("Henüz satış verisi yok.")

# --- 4. ÜRÜN TANIMLAMA ---
else:
    st.header("📦 Ürün Tanımla")
    # (Ürün tanımlama kodun buraya gelecek)
    st.session_state.urunler = st.data_editor(st.session_state.urunler, use_container_width=True)
