import streamlit as st
from PIL import Image
import numpy as np

# 1. Sayfa Ayarları
st.set_page_config(page_title="Analiz Laboratuvarı", layout="wide", initial_sidebar_state="collapsed")

# 2. Ortak Tasarım Dili (Giriş sayfasıyla aynı arka plan, karanlık laboratuvar havası)
st.markdown("""
<style>
/* Ana arka plan (Giriş sayfasıyla aynı görsel, işlem alanına odaklanmak için biraz daha karartıldı) */
.stApp {
    background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), url("https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Tüm metin renklerini beyaz/açık gri tonlara çekiyoruz */
html, body, [class*="css"], .stMarkdown p, h1, h2, h3, h4 {
    color: #f8fafc !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Bölücü çizginin rengini karanlık temaya uydurma */
hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
}

/* Metrik kutularını (Boyut ve Kanal yazan yerler) daha modern gösterme */
[data-testid="stMetric"] {
    background-color: rgba(255, 255, 255, 0.05);
    padding: 15px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

# 3. Üst Navigasyon ve Başlık
col_back, col_title = st.columns([1, 10])
with col_back:
    if st.button("⬅️ Ana Sayfa"):
        st.switch_page("main.py")

st.markdown('<h2 style="font-weight: 700; margin-top: -10px;">🌿 Yaprak Analiz Laboratuvarı</h2>', unsafe_allow_html=True)
st.divider()

# 4. Modern Kart Tasarımı (Karanlık temaya uyumlu sınır çizgileri)
col_upload, col_result = st.columns([1, 1], gap="large")

with col_upload:
    # Sol Kart: Yükleme Alanı
    with st.container(border=True):
        st.markdown("#### Görüntü Yükleme")
        st.write("Analiz etmek istediğiniz domates yaprağını yükleyin.")
        st.write("")
        uploaded_file = st.file_uploader("Dosya seçin veya sürükleyip bırakın", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        if uploaded_file is None:
            st.info("Sistem, analize başlamak için yüksek çözünürlüklü bir yaprak görseli bekliyor.")

with col_result:
    # Sağ Kart: Analiz Sonuçları
    with st.container(border=True):
        st.markdown("#### Analiz Çıktısı")
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            st.success("Görüntü algılandı ve ön işleme adımları tamamlandı.")
            
            img_array = np.array(image.resize((224, 224))) / 255.0
            
            st.markdown("**Sistem Verileri:**")
            col_m1, col_m2 = st.columns(2)
            col_m1.metric(label="Model Giriş Boyutu", value="224x224")
            col_m2.metric(label="Renk Kanalları", value="3 (RGB)")
            
            st.caption("Not: Tahmin motoru entegre edildikten sonra sonuçlar burada listelenecektir.")
        else:
            st.write("")
            st.write("")
            st.write("Veri bekleniyor...")
            st.progress(0) 