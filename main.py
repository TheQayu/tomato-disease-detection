import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Sayfa yapılandırması
st.set_page_config(page_title="Domates Hastalık Teşhisi", page_icon="🍅")

st.title("🍅 Domates Hastalığı Tespit Sistemi")
st.markdown("""
Bu sistem, tomates bitkisinin fotoğrafını inceleyerek domates fidenizdeki hastalıkları tespit eder.
""")

# Yan panel (Sidebar) bilgileri
st.sidebar.header("Proje Bilgileri")
st.sidebar.info("Bursa Uludağ Üniversitesi - Bilgisayar Mühendisliği")

# Dosya yükleme alanı
uploaded_file = st.file_uploader("Bir domates yaprağı fotoğrafı yükleyin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Görüntüyü aç ve ekranda göster
    image = Image.open(uploaded_file)
    st.image(image, caption='Yüklenen Fotoğraf', use_container_width=True)
    
    st.success("✅ Fotoğraf başarıyla yüklendi ve işlenmeye hazır!")
    
    
    with st.expander("Görüntü İşleme Detaylarını Gör"):
        img_array = np.array(image.resize((224, 224))) / 255.0
        st.write(f"Görüntü Boyutu: {image.size}")
        st.write(f"Model Giriş Formatı: {img_array.shape}")
        st.write("Sistem şu an TensorFlow arka planı ile iletişim kurabiliyor.")

else:
    st.warning("Lütfen analiz için bir fotoğraf yükleyin.")