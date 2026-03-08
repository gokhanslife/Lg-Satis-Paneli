import streamlit as st
import pandas as pd
from datetime import date
import calendar
import math
from supabase import create_client

# --- SUPABASE BAĞLANTISI ---
# Bilgileri artık Streamlit Secrets'tan çekiyoruz (Güvenli)
URL = st.secrets["https://nnvgedsfgjilbpsnlufx.supabase.co"]
KEY = st.secrets["sb_secret_aCfd4l2njislCFox5nBRpA_VaItpbPq"]
supabase = create_client(URL, KEY)

# --- VERİ İŞLEMLERİ ---
def veri_cek():
    response = supabase.table("satislar").select("*").execute()
    return pd.DataFrame(response.data)

def veri_kaydet(tarih, marka, model, ciro, prim, adet, not_):
    data = {"tarih": str(tarih), "marka": marka, "model": model, 
            "ciro": float(ciro), "prim": float(prim), "adet": int(adet), "not": not_}
    supabase.table("satislar").insert(data).execute()

# --- ARAYÜZ AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "🎯 Hedef Durumu"])

# --- SAYFALAR ---
if sekme == "📊 Dashboard & Satış":
    st.header("📊 Dashboard & Satış Girişi")
    
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Satış Tarihi", value=date.today())
        col1, col2 = st.columns(2)
        marka_secim = col1.selectbox("Marka", ["LG", "Diğer"])
        secilen_model = col2.text_input("Model")
        
        c1, c2, c3 = st.columns(3)
        f_fiyat = c1.number_input("Birim Fiyat", min_value=0.0)
        f_prim = c2.number_input("Birim Prim", min_value=0.0)
        f_adet = c3.number_input("Adet", min_value=1, step=1)
        f_not = st.text_area("Not")
        
        if st.form_submit_button("SATIŞI GİR"):
            veri_kaydet(f_tarih, marka_secim, secilen_model, f_fiyat * f_adet, f_prim * f_adet, f_adet, f_not)
            st.success("Satış başarıyla kaydedildi!")
            st.rerun()

elif sekme == "🎯 Hedef Durumu":
    st.header("🎯 Hedef Gerçekleştirme Projeksiyonu")
    df = veri_cek()
    
    if not df.empty:
        aylik_hedef = 100000 # Kendi hedefini buraya girebilirsin
        bugun = date.today()
        guncel_gun = max(1, bugun.day)
        ay_gun_sayisi = calendar.monthrange(bugun.year, bugun.month)[1]
        
        df_lg = df[df['marka'] == "LG"]
        lg_ciro = df_lg['ciro'].sum()
        tahmini_ciro = (lg_ciro / guncel_gun) * ay_gun_sayisi
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Şu Ana Kadar", f"{lg_ciro:,.0f} TL")
        c2.metric("Ay Sonu Tahmini", f"{tahmini_ciro:,.0f} TL")
        
        st.subheader("💰 Model Bazlı Prim Projeksiyonu")
        proj_list = []
        for model in df_lg['model'].unique():
            m_df = df_lg[df_lg['model'] == model]
            top_adet = m_df['adet'].sum()
            birim_prim = m_df['prim'].sum() / top_adet if top_adet > 0 else 0
            
            tahmin_adet_net = int((top_adet / guncel_gun) * ay_gun_sayisi)
            tahmin_prim_net = tahmin_adet_net * birim_prim
            
            proj_list.append({
                "Model": model, 
                "Mevcut Adet": top_adet,
                "Tahmini Adet": tahmin_adet_net,
                "Tahmini Prim (TL)": round(tahmin_prim_net, 2)
            })
        
        if proj_list:
            proj_df = pd.DataFrame(proj_list)
            st.table(proj_df)
    else:
        st.info("Henüz veri girişi yapılmamış.")
