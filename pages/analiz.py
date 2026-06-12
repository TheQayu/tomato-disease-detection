import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import tensorflow as tf
import io

# 1. Sayfa Ayarları
st.set_page_config(page_title="Analiz Laboratuvarı", layout="wide", initial_sidebar_state="collapsed")

# --- DOSYA YÜKLEYİCİ SIFIRLAMA ANAHTARI ---
if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0

# --- YAPAY ZEKA MODELLERİNİ YÜKLEME ---
@st.cache_resource
def Mehmet_load_model():
    try:
        return tf.keras.models.load_model("tomato_v4_final.keras")
    except Exception as e:
        st.error("Sistem Hatası: CNN teşhis modeli bulunamadı. Lütfen 'tomato_v4_final.keras' dosyasını kontrol edin.")
        st.stop()

cnn_model = Mehmet_load_model()

# --- HASTALIK SINIFLARI ---
class_labels = [
    'Bakteriyel Leke (Bacterial Spot)',
    'Erken Yanıklık (Early Blight)',
    'Geç Yanıklık (Late Blight)',
    'Yaprak Küfü (Leaf Mold)',
    'Septoria Yaprak Lekesi',
    'Örümcek Akarı (Spider Mites)',
    'Hedef Lekesi (Target Spot)',
    'Sarı Yaprak Kıvırcıklık Virüsü (TYLCV)',
    'Mozaik Virüsü (Mosaic Virus)',
    'Sağlıklı Yaprak (Healthy)',
]

# --- TTA FONKSİYONU ---
def tta_tahmin(model, image):
    img = image.resize((224, 224)).convert('RGB')
    img_array = np.array(img, dtype=np.float32)

    tahminler = []
    tahminler.append(model.predict(np.expand_dims(img_array, 0), verbose=0)[0])

    flipped = np.fliplr(img_array)
    tahminler.append(model.predict(np.expand_dims(flipped, 0), verbose=0)[0])

    img_bright = np.clip(img_array * 1.2, 0, 255)
    tahminler.append(model.predict(np.expand_dims(img_bright, 0), verbose=0)[0])

    img_dark = np.clip(img_array * 0.8, 0, 255)
    tahminler.append(model.predict(np.expand_dims(img_dark, 0), verbose=0)[0])

    h, w = img_array.shape[:2]
    margin = 20
    cropped = img_array[margin:h-margin, margin:w-margin]
    cropped_resized = np.array(Image.fromarray(cropped.astype(np.uint8)).resize((224, 224)), dtype=np.float32)
    tahminler.append(model.predict(np.expand_dims(cropped_resized, 0), verbose=0)[0])

    return np.mean(tahminler, axis=0)

# --- POP-UP (DIALOG) FONKSİYONU ---
@st.dialog("🔬 Analiz Sonuçları Raporu", width="large")
def show_results_dialog(image):
    with st.spinner("Yapay Zeka (CNN) hastalığı analiz ediyor..."):
        try:
            tahminler = tta_tahmin(cnn_model, image)
            en_yuksek_indeks = np.argmax(tahminler)
            teshis = class_labels[en_yuksek_indeks]
            guven_skoru = tahminler[en_yuksek_indeks] * 100
        except Exception as e:
            st.error("⚠️ Analiz motoru bu görseli işlerken bir sorun yaşadı.")
            if st.button("Pencereyi Kapat", use_container_width=True):
                st.rerun()
            return 

    # CNN Güvenlik filtresi (Görsel çok bulanıksa veya alakasızsa)
    if guven_skoru < 60.0:
        st.error("⚠️ HATA: Analiz yapılamayacak kadar düşük güven skoru.")
        st.info("Fotoğraf çok bulanık veya hastalık belirtileri net değil. Lütfen uygun bir görsel ile tekrar deneyin.")
        
        if st.button("Pencereyi Kapat", use_container_width=True):
            st.rerun()
        return

    st.markdown("#### 📊 Teşhis Olasılık Dağılımı")
    
    chart_data = pd.DataFrame(
        {"Olasılık (%)": tahminler * 100},
        index=class_labels
    )
    
    st.bar_chart(chart_data, color="#e11d48")
    st.success(f"🎯 **Kesin Teşhis:** {teshis} \n\n **Güven Skoru:** %{guven_skoru:.2f}")
    st.divider()
    
    # --- EXCEL OLUŞTURMA VE İNDİRME KISMI ---
    try:
        df_indir = pd.DataFrame({
            "Hastalık Sınıfı": class_labels,
            "Tahmin Olasılığı (%)": np.round(tahminler * 100, 2)
        })
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_indir.to_excel(writer, index=False, sheet_name='Analiz Sonuçları')
            worksheet = writer.sheets['Analiz Sonuçları']
            worksheet.column_dimensions['A'].width = 35  
            worksheet.column_dimensions['B'].width = 20  

        excel_data = buffer.getvalue()
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.download_button(
                label="📥 Sonuçları Excel Olarak İndir",
                data=excel_data,
                file_name="domates_analiz_raporu.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with col_btn2:
            if st.button("Pencereyi Kapat", use_container_width=True):
                st.rerun()
    except ImportError:
        st.error("❌ Excel oluşturma modülü eksik. Lütfen sisteme 'openpyxl' kütüphanesini kurun.")
    except Exception as e:
        st.error("❌ Rapor oluşturulurken beklenmeyen bir hata oluştu.")

# 2. Ortak Tasarım Dili (CSS)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), url("https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
html, body, [class*="css"], .stMarkdown p, h1, h2, h3, h4 {
    color: #f8fafc !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
}
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
    try:
        if st.button("⬅️ Ana Sayfa"):
            st.switch_page("main.py")
    except Exception:
        pass 

st.markdown('<h2 style="font-weight: 700; margin-top: -10px;">🌿 Yaprak Analiz Laboratuvarı</h2>', unsafe_allow_html=True)
st.divider()

# 4. Modern Kart Tasarımı
image = None

col_upload, col_result = st.columns([1, 1], gap="large")

with col_upload:
    with st.container(border=True):
        st.markdown("#### Görüntü Yükleme")
        st.write("Analiz etmek istediğiniz domates yaprağını yükleyin.")
        st.write("")
        
        uploaded_file = st.file_uploader(
            "Dosya seçin veya sürükleyip bırakın", 
            type=["jpg", "jpeg", "png"], 
            label_visibility="collapsed",
            key=f"uploader_{st.session_state.file_uploader_key}"
        )

        if uploaded_file is None:
            st.info("Sistem, analize başlamak için yüksek çözünürlüklü bir yaprak görseli bekliyor.")
        else:
            try:
                image = Image.open(uploaded_file)
                image.verify() 
                image = Image.open(uploaded_file) 
                
                st.write("") 
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("🔄 Yeni Görüntü Ekle", use_container_width=True):
                        st.session_state.file_uploader_key += 1
                        st.rerun()
                        
                with col_btn2:
                    if st.button("Sonuçları Göster 📊", type="primary", use_container_width=True):
                        show_results_dialog(image)
                        
            except Exception as e:
                st.error("❌ Hata: Yüklenen dosya okunamadı. Lütfen geçerli bir görsel dosyası yükleyin.")
                if st.button("🔄 Tekrar Dene", use_container_width=True):
                    st.session_state.file_uploader_key += 1
                    st.rerun()

with col_result:
    with st.container(border=True):
        st.markdown("#### Analiz Çıktısı")

        if uploaded_file is not None and image is not None:
            try:
                st.image(image, use_container_width=True)
                st.success("✅ Görüntü algılandı ve yapay zeka motoruna aktarıldı.")

                st.markdown("**Sistem Verileri:**")
                col_m1, col_m2 = st.columns(2)
                col_m1.metric(label="Model Giriş Boyutu", value="224x224")
                col_m2.metric(label="Renk Kanalları", value="3 (RGB)")
                    
            except Exception:
                st.warning("Görsel önizlemesi yüklenemedi.")
        else:
            st.write("")
            st.write("")
            st.write("Veri bekleniyor...")
            st.progress(0)