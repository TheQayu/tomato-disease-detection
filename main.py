import streamlit as st

# 1. Sayfa Ayarları
st.set_page_config(page_title="Agri-AI | Domates Teşhis", layout="wide", initial_sidebar_state="collapsed")

# 2. Arka Plan ve Modern CSS Tasarımı
# Yazıların okunmasını sağlayan şık karanlık filtre ve GERÇEK bir domates fotoğrafı!
modern_bg = '''
<style>
.stApp {
    background: linear-gradient(rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.8)), url("https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Ana Başlık */
.hero-title {
    color: #ffffff;
    font-size: 70px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 800;
    text-align: center;
    margin-top: 15vh;
    letter-spacing: -1px;
}

/* Alt Başlık */
.hero-subtitle {
    color: #cbd5e1;
    font-size: 22px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 300;
    text-align: center;
    margin-bottom: 50px;
}
</style>
'''
st.markdown(modern_bg, unsafe_allow_html=True)

# 3. İçerik ve Başlıklar
st.markdown('<div class="hero-title">Domates Hastalıkları Tespit Sistemi</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Yapay zeka gücüyle domates yapraklarındaki hastalıkları saniyeler içinde tespit edin.</div>', unsafe_allow_html=True)

# 4. Modern Geçiş Butonu
# Ekranı bölüp butonu tam merkeze oturtuyoruz
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.write("") 
    if st.button("Hemen Taramaya Başla ➔", type="primary", use_container_width=True):
        st.switch_page("pages/analiz.py")