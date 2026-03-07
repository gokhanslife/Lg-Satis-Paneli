import streamlit as st
import pandas as pd
from datetime import date
import calendar
import math
from supabase import create_client

# --- SUPABASE BAĞLANTISI ---
URL = "sb_publishable_n2K_RddMLWThF0VGTxmTVQ_ISuUtQQs"
KEY = "sb_secret_aCfd4l2njislCFox5nBRpA_VaItpbPq"
supabase = create_client(URL, KEY)

# --- VERİ ÇEKME VE KAYDETME FONKSİYONLARI ---
def veri_cek():
    response = supabase.table("satislar").select("*").execute()
    return pd.DataFrame(response.data)

def veri_kaydet(tarih, marka, model, ciro, prim, adet, not_):
    data = {"tarih": str(tarih), "marka": marka, "model": model, 
            "ciro": float(ciro), "prim": float(prim), "adet": int(adet), "not": not_}
    supabase.table("satislar").insert(data).execute()

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# ... [DİĞER AYARLAR VE GİRİŞ KONTROLÜ AYNI KALACAK] ...

# --- DASHBOARD & SATIŞ ---
if sekme == "📊 Dashboard & Satış":
    df_s = veri_cek() # Artık veriyi Supabase'den çekiyoruz
    
    # ... (Metrik hesaplamaları aynı) ...

    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Satış Tarihi", value=date.today())
        # ... (Diğer inputlar aynı) ...
        if st.form_submit_button("SATIŞI GİR"):
            veri_kaydet(f_tarih, marka_secim, secilen_model, f_fiyat * f_adet, f_prim * f_adet, f_adet, f_not)
            st.success("Satış başarıyla kaydedildi!")
            st.rerun()

# --- HEDEF DURUMU (MODEL BAZLI PRİM) ---
elif sekme == "🎯 Hedef Durumu":
    # ... (Buradaki hesaplamalar aynı, sadece 'df = veri_cek()' kullan) ...
    df = veri_cek()
    df_lg = df[df['marka'] == "LG"] # Not: Supabase'de sütun isimleri küçük harf olabilir, kontrol et!
    
    # ... (İstediğin o yuvarlama mantığı ile çalışan kod buraya) ...
    # Tahmini adet hesaplaması
    tahmin_adet_raw = (top_adet / guncel_gun) * ay_gun_sayisi
    tahmin_adet_net = int(tahmin_adet_raw)
    tahmin_prim_net = tahmin_adet_net * birim_prim
    
    # ... (Tabloya basarken kullan) ...
