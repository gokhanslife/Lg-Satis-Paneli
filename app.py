import streamlit as st
import pandas as pd
from datetime import date
import calendar
from supabase import create_client

# --- SUPABASE BAĞLANTISI ---
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def veriyi_cek(tablo):
    response = supabase.table(tablo).select("*").execute()
    return pd.DataFrame(response.data)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# ... (Giriş ekranı fonksiyonun aynı kalıyor) ...

# --- VERİ YÜKLEME ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = veriyi_cek("urunler")
if 'satislar' not in st.session_state:
    st.session_state.satislar = veriyi_cek("satislar")

# --- KODUN GERİ KALANI ---
# ... Senin gönderdiğin CSS ve Yan Menü kısmı aynı kalıyor ...

# --- VERİ EKLEME YERLERİNE BU DOKUNUŞU YAP ---
# Satış Ekleme Butonunun içine:
if st.form_submit_button("SATIŞI GİR"):
    y_satis = {"Tarih": str(f_tarih), "Marka": marka_secim, "Model": secilen_model, "Ciro": f_fiyat * f_adet, "Prim": f_prim * f_adet, "Adet": f_adet, "Not": f_not}
    supabase.table("satislar").insert(y_satis).execute() # Veritabanına gönder
    st.session_state.satislar = pd.concat([st.session_state.satislar, pd.DataFrame([y_satis])], ignore_index=True)
    st.rerun()

# Ürün Ekleme Butonunun içine:
if st.form_submit_button("Sisteme Kaydet"):
    y_urun = {"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}
    supabase.table("urunler").insert(y_urun).execute() # Veritabanına gönder
    st.session_state.urunler = pd.concat([st.session_state.urunler, pd.DataFrame([y_urun])], ignore_index=True)
    st.rerun()
