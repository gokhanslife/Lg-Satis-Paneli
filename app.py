import streamlit as st
import pandas as pd
from datetime import date
import calendar
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- GOOGLE SHEETS BAĞLANTISI ---
def get_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('gizli-anahtar.json', scope)
    return gspread.authorize(creds)

def read_sheet(sheet_name):
    sh = get_sheets_client().open("LG_Satis_Verileri")
    return pd.DataFrame(sh.worksheet(sheet_name).get_all_records())

def write_sheet(df, sheet_name):
    sh = get_sheets_client().open("LG_Satis_Verileri")
    ws = sh.worksheet(sheet_name)
    ws.clear()
    ws.update([df.columns.values.tolist()] + df.values.tolist())

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")

# --- VERİ YÜKLEME ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = read_sheet("Ürünler")
if 'satislar' not in st.session_state:
    st.session_state.satislar = read_sheet("Satışlar")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📊 Satış Analizleri", "🎯 Hedef Durumu", "📦 Ürün Tanımla"])
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- SAYFA 1: DASHBOARD & SATIŞ ---
if sekme == "📊 Dashboard & Satış":
    df_s = st.session_state.satislar
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum() if not df_s.empty else 0
    rk_c = df_s[df_s['Marka'] == "Rakip"]['Ciro'].sum() if not df_s.empty else 0
    top_c = lg_c + rk_c
    p_payi = (lg_c / top_c * 100) if top_c > 0 else 0
    t_prim = df_s['Prim'].sum() if not df_s.empty else 0
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Reyon Cirosu", f"{top_c:,.0f} TL")
    c2.metric("LG Cirosu", f"{lg_c:,.0f} TL")
    c3.metric("Pazar Payı", f"%{p_payi:.1f}")
    c4.metric("Toplam Prim", f"{t_prim:,.0f} TL")
    c5.metric("Hedef Durumu", f"%{(lg_c/aylik_hedef*100):.1f}")

    st.subheader("🖋️ Yeni Satış Kaydı")
    marka_secim = st.selectbox("Marka", ["LG", "Rakip"])
    def_fiyat, def_prim, secilen_model = 0.0, 0.0, "Diğer"
    if marka_secim == "LG" and not st.session_state.urunler.empty:
        secilen_model = st.selectbox("Model Seç", st.session_state.urunler['Model'].tolist())
        bilgi = st.session_state.urunler[st.session_state.urunler['Model'] == secilen_model].iloc[0]
        def_fiyat, def_prim = float(bilgi['Liste_Fiyati']), float(bilgi['Birim_Prim'])
            
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = str(st.date_input("Satış Tarihi", date.today()))
        f_fiyat = st.number_input("Satış Fiyatı (TL)", value=def_fiyat)
        f_prim = st.number_input("Adet Başı Prim (TL)", value=def_prim)
        f_adet = st.number_input("Adet", min_value=1, value=1)
        f_not = st.text_input("Not")
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{"Tarih": f_tarih, "Marka": marka_secim, "Model": secilen_model, "Ciro": f_fiyat * f_adet, "Prim": f_prim * f_adet, "Adet": f_adet, "Not": f_not}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            write_sheet(st.session_state.satislar, "Satışlar") # Sheets'e yazdırdık
            st.rerun()

# --- DİĞER SAYFALAR AYNI MANTIKLA EKlenecek ---
# ... (Diğer sekmeleri de aynı şekilde yaz_sheet ile güncelleyebilirsin)
