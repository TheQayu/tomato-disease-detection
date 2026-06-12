
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import tensorflow as tf

# --- YAPAY ZEKA MODELİNİ YÜKLEME ---
# Sistemi yormamak için modeli sadece ilk açılışta önbelleğe (cache) alıyoruz.
@st.cache_resource
def load_model():
    # domates_modeli.h5 dosyasının main.py ile aynı klasörde olduğundan emin olun.
    return tf.keras.models.load_model("domates_modeli.h5")

model = load_model()

# 1. Sayfa Ayarları
st.set_page_config(page_title="Analiz Laboratuvarı", layout="wide", initial_sidebar_state="collapsed")

# 2. Ortak Tasarım Dili 
st.markdown("""
<style>
/* Ana arka plan */
.stApp {
    background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), url("https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Tüm metin renkleri */
html, body, [class*="css"], .stMarkdown p, h1, h2, h3, h4 {
    color: #f8fafc !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Bölücü çizginin rengi */
hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
}

/* Metrik kutuları */
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

# 4. Modern Kart Tasarımı
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
    # Sağ Kart: Analiz Sonuçları ve Yapay Zeka Entegrasyonu
    with st.container(border=True):
        st.markdown("#### Analiz Çıktısı")
        
        if uploaded_file is not None:
            # 1. Resmi ekranda göster
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            st.success("✅ Görüntü algılandı ve yapay zeka motoruna aktarıldı.")
            
            # 2. Ara Çıktılar (Hocanın istediği metrikler)
            st.markdown("**Sistem Verileri:**")
            col_m1, col_m2 = st.columns(2)
            col_m1.metric(label="Model Giriş Boyutu", value="224x224")
            col_m2.metric(label="Renk Kanalları", value="3 (RGB)")
            
            # 3. Yapay Zeka Hazırlığı ve Tahmin İşlemi
            with st.spinner("Yapay Zeka (CNN) görüntüyü analiz ediyor..."):
                # Resmi modelin istediği formata getir
                img_resized = image.resize((224, 224))
                img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
                img_array = np.expand_dims(img_array, axis=0) # Matris boyutunu ayarla
                
                # Tahmini yap!
                tahminler = model.predict(img_array)[0]
                
                # Klasör isimlerine göre alfabetik sınıf sıralaması
                siniflar = ["Erken Yanıklık", "Sağlıklı", "Geç Yanıklık"] 
                
                # En yüksek ihtimalli sonucu bul
                en_yuksek_indeks = np.argmax(tahminler)
                teshis = siniflar[en_yuksek_indeks]
                guven_skoru = tahminler[en_yuksek_indeks] * 100
                
            # 4. Sonuçları Grafik Olarak Göster (Hocanın istediği Grafik/Tablo şartı)
            st.divider()
            st.markdown("#### 📊 Teşhis Olasılık Dağılımı")
            
            chart_data = pd.DataFrame(
                {"Olasılık (%)": tahminler * 100},
                index=siniflar
            )
            
            st.bar_chart(chart_data, color="#e11d48")
            st.success(f"🎯 **Kesin Teşhis:** {teshis} (Güven Skoru: %{guven_skoru:.2f})")
            
        else:
            st.write("")
            st.write("")
            st.write("Veri bekleniyor...")
            st.progress(0)



