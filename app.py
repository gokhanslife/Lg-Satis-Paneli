import streamlit as st
import pandas as pd
from datetime import date
import calendar
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- GOOGLE SHEETS BAĞLANTISI ---
def get_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    # GitHub'a yüklediğin json dosyasının adı 'gizli-anahtar.json' olmalı
    creds = ServiceAccountCredentials.from_json_keyfile_name('gizli-anahtar.json', scope)
    return gspread.authorize(creds)

def read_sheet(sheet_name):
    try:
        sh = get_sheets_client().open("LG_Satis_Verileri")
        df = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())
        return df
    except:
        return pd.DataFrame()

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
    st.markdown('<div style="text-align: center;"><img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/LG_logo_%282014%29.svg" width="100"></div>', unsafe_allow_html=True)
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
            write_sheet(st.session_state.satislar, "Satışlar")
            st.rerun()

    st.subheader("📋 Satış Listesi")
    st.dataframe(st.session_state.satislar, use_container_width=True)

# --- SAYFA 2: ANALİZLER ---
elif sekme == "📊 Satış Analizleri":
    st.header("📈 Satış Analizleri")
    df_lg = st.session_state.satislar[st.session_state.satislar['Marka'] == "LG"].copy()
    if not df_lg.empty:
        df_lg['Tarih'] = pd.to_datetime(df_lg['Tarih'])
        bugun = pd.Timestamp.now()
        def al(data): return data.groupby('Model')['Adet'].sum().reset_index().sort_values(by='Adet', ascending=False)
        c1, c2, c3 = st.columns(3)
        c1.write("**Tüm Zamanlar**"); c1.table(al(df_lg))
        c2.write("**Son 30 Gün**"); c2.table(al(df_lg[df_lg['Tarih'] >= (bugun - pd.Timedelta(days=30))]))
        c3.write("**Son 7 Gün**"); c3.table(al(df_lg[df_lg['Tarih'] >= (bugun - pd.Timedelta(days=7))]))
    else:
        st.info("Kayıt bulunamadı.")

# --- SAYFA 3: HEDEF DURUMU ---
elif sekme == "🎯 Hedef Durumu":
    st.header("🎯 Hedef Projeksiyonu")
    df_lg = st.session_state.satislar[st.session_state.satislar['Marka'] == "LG"]
    if not df_lg.empty:
        lg_ciro = df_lg['Ciro'].sum()
        gun_sayisi = date.today().day
        ay_gun = calendar.monthrange(date.today().year, date.today().month)[1]
        tahmin = (lg_ciro / gun_sayisi) * ay_gun
        c1, c2, c3 = st.columns(3)
        c1.metric("Mevcut Ciro", f"{lg_ciro:,.0f} TL")
        c2.metric("Ay Sonu Tahmin", f"{tahmin:,.0f} TL")
        c3.metric("Hedef Başarı", f"%{(tahmin/aylik_hedef*100):.1f}")
    else:
        st.info("Kayıt yok.")

# --- SAYFA 4: ÜRÜN TANIMLAMA ---
else:
    st.header("📦 Ürün Tanımla")
    with st.form("urun_ekle"):
        m = st.text_input("Model")
        f = st.number_input("Fiyat", min_value=0.0)
        p = st.number_input("Prim", min_value=0.0)
        if st.form_submit_button("Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            write_sheet(st.session_state.urunler, "Ürünler")
            st.rerun()
    st.table(st.session_state.urunler)
