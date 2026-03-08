import streamlit as st
import pandas as pd
from supabase import create_client

URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

def veri_cek(tablo):
    response = supabase.table(tablo).select("*").execute()
    return pd.DataFrame(response.data)

# Sütun isimleri ne olursa olsun ilk gelenleri kullanması için güvenli hale getirdik
def get_model_list(df):
    # Tablodaki ilk sütunu model listesi olarak al
    return df.iloc[:, 1].tolist() if df.shape[1] > 1 else []

st.set_page_config(layout="wide")

# ... Giriş kodu buraya ...

tab = st.radio("Seçim:", ["Satış", "Ürün"])

if tab == "Satış":
    df = veri_cek("urunler")
    if not df.empty:
        # Sütun ismine takılmadan veriyi çekiyoruz
        secilen_model = st.selectbox("Model:", df.iloc[:, 1].unique())
        # ... (Satış kayıt işlemi) ...
    else:
        st.error("Önce ürün ekle!")

elif tab == "Ürün":
    # ... (Ürün ekleme formu) ...
