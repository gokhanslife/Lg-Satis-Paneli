st.markdown("""
    <style>
    /* Uygulama Genel Arka Planı Beyaz */
    .stApp { background-color: #ffffff; }

    /* TÜM YAZILAR: Siyah, Kalın ve Net */
    label, p, span, h1, h2, h3, .stMarkdown, .stSelectbox label, .stNumberInput label, .stDateInput label {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* ÜST ÖZET KART BAŞLIKLARI: Siyah ve Belirgin */
    [data-testid="stMetricLabel"] p {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: 800 !important;
    }

    /* ÜST ÖZET DEĞERLERİ: LG Kırmızısı */
    [data-testid="stMetricValue"] {
        color: #a50034 !important;
        font-weight: 800 !important;
    }
    
    /* Kartların Etrafına Hafif Gri Çerçeve */
    div[data-testid="stMetric"] {
        background-color: #fcfcfc;
        border: 2px solid #eeeeee;
        border-radius: 12px;
        padding: 15px;
    }

    /* Sol Menüdeki LG Logosu (Kırmızı Yuvarlak) */
    .lg-logo {
        width: 60px; height: 60px;
        background-color: #a50034;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: white !important;
        font-weight: bold; font-family: Arial;
        margin-bottom: 20px;
        font-size: 20px;
    }
    
    /* Giriş kutularının içindeki yazıları siyah yap */
    input { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)
