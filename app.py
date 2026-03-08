import streamlit as st
import pandas as pd
from datetime import date
from supabase import create_client

# --- SUPABASE BAĞLANTISI ---
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# --- VERİ İŞLEMLERİ ---
def veri_cek(tablo):
    response = supabase.table(tablo).select("*").execute()
    # Supabase veriyi küçük harfli sütun isimleriyle getirir
    df = pd.DataFrame(response.data)
    # Sütun isimlerini kodunla eşleşecek şekilde düzeltiyoruz
    if not df.empty:
        df.columns = [c.capitalize() for c in df.columns] 
    return df

def veri_kaydet(tablo, data):
    supabase.table(tablo).insert(data).execute()

# --- GİRİŞ VE DİĞER KISIMLAR (Aynı) ---
# ... (Giriş ekranı ve st.set_page_config buraya gelecek) ...

# --- SAYFA: DASHBOARD & SATIŞ ---
if sekme == "📊 Dashboard & Satış":
    st.header("📊 Satış Girişi")
    urunler_df = veri_cek("urunler")
    
    # 1. Model seçimi formun DIŞINDA olmalı ki veriler otomatik gelsin
    secilen_model = st.selectbox("Model Seç", urunler_df['Model'].unique())
    model_bilgi = urunler_df[urunler_df['Model'] == secilen_model].iloc[0]
    
    st.write(f"Birim Fiyat: {model_bilgi['Liste_fiyati']} TL")

    with st.form("satis_form"):
        f_tarih = st.date_input("Satış Tarihi", value=date.today())
        f_adet = st.number_input("Adet", min_value=1, step=1)
        f_not = st.text_input("Not")
        
        # 2. Submit butonu burada
        if st.form_submit_button("SATIŞI GİR"):
            veri = {
                "tarih": str(f_tarih), "marka": "LG", "model": secilen_model,
                "ciro": float(model_bilgi['Liste_fiyati']) * f_adet,
                "prim": float(model_bilgi['Birim_prim']) * f_adet,
                "adet": int(f_adet), "not": f_not
            }
            veri_kaydet("satislar", veri)
            st.success("Kaydedildi!")
            st.rerun()
