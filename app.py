import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# 1. Veri tanımlama (Session state yoksa oluştur)
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Fiyat", "Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Model", "Adet", "Ciro"])

# 2. Yan Menü
menu = st.sidebar.radio("Sayfalar", ["Satış", "Ürün Ekle"])

# 3. Ürün Ekle Sayfası (Basit)
if menu == "Ürün Ekle":
    st.header("Ürün Ekle")
    with st.form("yeni_urun"):
        model = st.text_input("Model Adı")
        fiyat = st.number_input("Fiyat")
        prim = st.number_input("Prim")
        if st.form_submit_button("Kaydet"):
            yeni = pd.DataFrame([[model, fiyat, prim]], columns=["Model", "Fiyat", "Prim"])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.rerun()
    st.write(st.session_state.urunler)

# 4. Satış Sayfası (Basit)
elif menu == "Satış":
    st.header("Satış Yap")
    if not st.session_state.urunler.empty:
        model_sec = st.selectbox("Model Seç", st.session_state.urunler["Model"].tolist())
        adet = st.number_input("Adet", min_value=1)
        if st.button("Satışı Kaydet"):
            # Basit hesaplama
            ciro = adet * 100 # Burayı istediğin gibi değiştir
            yeni_satis = pd.DataFrame([[model_sec, adet, ciro]], columns=["Model", "Adet", "Ciro"])
            st.session_state.satislar = pd.concat([st.session_state.satislar, yeni_satis], ignore_index=True)
            st.rerun()
    else:
        st.warning("Önce ürün ekle!")
    st.write(st.session_state.satislar)
