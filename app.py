import streamlit as st
import pandas as pd
from datetime import date
import calendar

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LG Sales Pro", layout="wide")
# --- GÜNCELLENMİŞ GİRİŞ EKRANI (BENİ HATIRLA ÖZELLİKLİ) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    # Eğer daha önce giriş başarılıysa ve "Beni Hatırla" işaretliyse şifre sorma
    if st.session_state.password_correct:
        return

    st.title("🔐 LG Sales Pro - Giriş")
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    beni_hatirla = st.checkbox("Beni Hatırla")
    
    if st.button("Giriş Yap"):
        if kullanici == "gokhan" and sifre == "825593": # Burayı değiştir!
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")
    
    # Giriş yapılmadıysa uygulamanın devamını durdur
    if not st.session_state.password_correct:
        st.stop()

# --- CSS ---
st.markdown("""
    <style>
    input, .stTextInput > div > div > input, .stNumberInput > div > div > input, 
    .stDateInput > div > div > input, .stSelectbox div {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px;
        padding: 20px !important;
    }
    [data-testid="stMetricLabel"] p { color: #000000 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    [data-testid="stMetricValue"] { color: #a50034 !important; font-weight: 900 !important; font-size: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SAKLAMA ---
if 'urunler' not in st.session_state:
    st.session_state.urunler = pd.DataFrame(columns=["Model", "Liste_Fiyati", "Birim_Prim"])
if 'satislar' not in st.session_state:
    st.session_state.satislar = pd.DataFrame(columns=["Tarih", "Marka", "Model", "Ciro", "Prim", "Adet", "Not"])

# --- YAN MENÜ ---
with st.sidebar:
    st.markdown('<div style="text-align: center;"><img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/LG_logo_%282014%29.svg" width="100"></div>', unsafe_allow_html=True)
    st.subheader("SATIŞ YÖNETİMİ")
    sekme = st.radio("İşlem Seçin:", ["📊 Dashboard & Satış", "📊 Satış Analizleri", "🎯 Hedef Durumu", "📦 Ürün Tanımla"])
    st.divider()
    aylik_hedef = st.number_input("Aylık Hedef (TL)", value=1000000)

# --- SAYFA 1: DASHBOARD & SATIŞ ---

if sekme == "📊 Dashboard & Satış":
    df_s = st.session_state.satislar.copy()
    lg_c = df_s[df_s['Marka'] == "LG"]['Ciro'].sum() if not df_s.empty else 0
    rk_c = df_s[df_s['Marka'] == "Rakip"]['Ciro'].sum() if not df_s.empty else 0
    top_c = lg_c + rk_c  # Burası senin istediğin "Reyon Cirosu"
    p_payi = (lg_c / top_c * 100) if top_c > 0 else 0
    t_prim = df_s['Prim'].sum() if not df_s.empty else 0
    
    # 5 sütun olarak güncelledim
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Reyon Cirosu", f"{top_c:,.0f} TL") # Yeni eklenen metrik
    c2.metric("LG Cirosu", f"{lg_c:,.0f} TL")
    c3.metric("Pazar Payı", f"%{p_payi:.1f}")
    c4.metric("Toplam Prim", f"{t_prim:,.0f} TL")
    c5.metric("Hedef Durumu", f"%{(lg_c/aylik_hedef*100):.1f}")

    st.divider()
    st.subheader("🖋️ Yeni Satış Kaydı")
    marka_secim = st.selectbox("Marka", ["LG", "Rakip"])
    def_fiyat, def_prim, secilen_model = 0.0, 0.0, "Diğer"
    if marka_secim == "LG" and not st.session_state.urunler.empty:
        secilen_model = st.selectbox("Model Seç", st.session_state.urunler['Model'].tolist())
        bilgi = st.session_state.urunler[st.session_state.urunler['Model'] == secilen_model].iloc[0]
        def_fiyat, def_prim = float(bilgi['Liste_Fiyati']), float(bilgi['Birim_Prim'])
            
    with st.form("satis_form", clear_on_submit=True):
        f_tarih = st.date_input("Satış Tarihi", date.today())
        f_fiyat = st.number_input("Satış Fiyatı (TL)", value=def_fiyat)
        f_prim = st.number_input("Adet Başı Prim (TL)", value=def_prim)
        f_adet = st.number_input("Adet", min_value=1, value=1)
        f_not = st.text_input("Not")
        if st.form_submit_button("SATIŞI GİR"):
            y_satis = pd.DataFrame([{"Tarih": f_tarih, "Marka": marka_secim, "Model": secilen_model, "Ciro": f_fiyat * f_adet, "Prim": f_prim * f_adet, "Adet": f_adet, "Not": f_not}])
            st.session_state.satislar = pd.concat([st.session_state.satislar, y_satis], ignore_index=True)
            st.rerun()

    st.subheader("📋 Satış Listesi")
    st.session_state.satislar = st.data_editor(st.session_state.satislar, use_container_width=True)
    c1, c2 = st.columns([3, 1])
    idx_sil = c1.number_input("Silinecek Satır No", min_value=0, max_value=len(st.session_state.satislar)-1 if not st.session_state.satislar.empty else 0)
    if c2.button("Satırı Sil"):
        st.session_state.satislar = st.session_state.satislar.drop(idx_sil).reset_index(drop=True)
        st.rerun()


# --- SAYFA 2: ANALİZLER ---
elif sekme == "📊 Satış Analizleri":
    st.header("📈 Satış Analizleri")
    df_s = st.session_state.satislar.copy()
    
    # Sadece LG satışlarını filtrele
    df_lg = df_s[df_s['Marka'] == "LG"].copy()
    
    if not df_lg.empty:
        df_lg['Tarih'] = pd.to_datetime(df_lg['Tarih'])
        bugun = pd.Timestamp.now()
        
        # Sadece LG modellerini gruplayan fonksiyon
        def al(data): 
            return data.groupby('Model')['Adet'].sum().reset_index().sort_values(by='Adet', ascending=False)
            
        col1, col2, col3 = st.columns(3)
        col1.write("**Tüm Zamanlar**"); col1.dataframe(al(df_lg), use_container_width=True)
        col2.write("**Son 30 Gün**"); col2.dataframe(al(df_lg[df_lg['Tarih'] >= (bugun - pd.Timedelta(days=30))]), use_container_width=True)
        col3.write("**Son 7 Gün**"); col3.dataframe(al(df_lg[df_lg['Tarih'] >= (bugun - pd.Timedelta(days=7))]), use_container_width=True)
    else:
        st.info("Analiz edilecek LG satış kaydı bulunamadı.")

# --- SAYFA 3: HEDEF DURUMU (PROJEKSİYON) ---
elif sekme == "🎯 Hedef Durumu":
    st.header("🎯 Hedef Gerçekleştirme Projeksiyonu")
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
        c1.metric("Şu Ana Kadar", f"{lg_ciro:,.0f} TL")
        c2.metric("Ay Sonu Tahmini", f"{tahmini_ciro:,.0f} TL")
        c3.metric("Tahmini Hedef (%)", f"%{projeksiyon_yuzde:.1f}")
        
        st.info(f"Ayın {gun_sayisi}. günündeyiz. Bu performansla gidilirse ay sonu toplam ciro tahmini {tahmini_ciro:,.0f} TL olup, hedefin %{projeksiyon_yuzde:.1f}'i gerçekleşmiş olacaktır.")
        
   # --- MODEL BAZLI PRİM PROJEKSİYONU ---
        st.subheader("💰 Model Bazlı Prim Projeksiyonu")
        df_lg = df[df['Marka'] == "LG"]
        if not df_lg.empty:
            proj_list = []
            for model in df_lg['Model'].unique():
                if model == "Diğer": continue
                m_df = df_lg[df_lg['Marka'] == model]
                top_adet = m_df['Adet'].sum()
                top_prim = m_df['Prim'].sum()
                birim_prim = top_prim / top_adet if top_adet > 0 else 0
                
                # Tahmini adet hesaplaması
                tahmin_adet = (top_adet / gun_sayisi) * ay_gun_sayisi
                tahmin_prim = tahmin_adet * birim_prim
                
                proj_list.append({
                    "Model": model, 
                    "Mevcut Adet": top_adet,
                    "Tahmini Ay Sonu Adet": int(tahmin_adet), # int() ile küsuratı tamamen attık, tam sayıya çevirdik
                    "Tahmini Prim (TL)": round(tahmin_prim, 2)
                })
            
            if proj_list:
                proj_df = pd.DataFrame(proj_list)
                st.table(proj_df)
                st.write(f"### **Toplam Tahmini Prim Kazancı: {proj_df['Tahmini Prim (TL)'].sum():,.2f} TL**")

# --- SAYFA 4: ÜRÜN TANIMLAMA ---
else:
    st.header("Yeni Model Ekle")
    with st.form("urun_ekle"):
        m = st.text_input("Model İsmi")
        f = st.number_input("Liste Fiyatı", min_value=0.0)
        p = st.number_input("Adet Başı Prim", min_value=0.0)
        if st.form_submit_button("Sisteme Kaydet"):
            yeni = pd.DataFrame([{"Model": m, "Liste_Fiyati": f, "Birim_Prim": p}])
            st.session_state.urunler = pd.concat([st.session_state.urunler, yeni], ignore_index=True)
            st.rerun()
    st.subheader("Mevcut Modeller")
    st.session_state.urunler = st.data_editor(st.session_state.urunler, use_container_width=True)
    c1, c2 = st.columns([3, 1])
    silinecek = c1.selectbox("Silinecek Model", st.session_state.urunler['Model'].unique())
    if c2.button("Ürünü Sil"):
        st.session_state.urunler = st.session_state.urunler[st.session_state.urunler['Model'] != silinecek]
        st.rerun()
