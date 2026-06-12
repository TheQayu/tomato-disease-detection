readme_content = """# 🌿 Domates Yaprağı Hastalık Teşhis Sistemi (Agri-AI)

Bu proje, **Bursa Uludağ Üniversitesi Mühendislik Fakültesi Bilgisayar Mühendisliği Bölümü** bünyesinde yürütülen *Python Programlamaya Giriş Dersi (2026)* kapsamında gerçekleştirilen Final Projesidir.

Yapay zeka tabanlı bu web uygulaması, domates üreticilerinin ve ziraat uzmanlarının yaprak fotoğrafları üzerinden saniyeler içerisinde hastalık teşhisi yapabilmesini sağlar. Sistem, hatalı girdileri önlemek amacıyla **iki aşamalı bir doğrulama ve teşhis hattı** (pipeline) kullanmaktadır.

---

## 🚀 Öne Çıkan Özellikler

* **Gelişmiş Ön Filtreleme (OpenAI CLIP):** Sisteme domates yaprağı dışında yüklenebilecek alakasız görsellerin (nesneler, insan, yazı tahtası, araçlar vb.) modeli yanıltmasını önler. Sıfırdan nesne tanıma modeli eğitmek yerine, sıfır-örnekli (zero-shot) öğrenme yeteneğine sahip CLIP mimarisi ile görsel içeriği doğrular.

* **Derin Öğrenme Sınıflandırma Motoru (CNN):** 20.000'den fazla gerçek görüntüyle eğitilmiş derin evrişimli sinir ağı, yaprak üzerindeki mikro belirtileri inceleyerek teşhis koyar.

* **Test-Time Augmentation (TTA):** Görüntünün 5 farklı varyasyonunu (orijinal, yatay çevrilmiş, parlak, karanlık, kırpılmış) eş zamanlı olarak analiz eder ve bu tahminlerin ortalamasını alarak güven skorunu maksimum kararlılığa ulaştırır.

* **Dinamik Excel Raporlama (openpyxl):** Teşhis edilen tüm hastalık olasılık dağılımlarını tek tıkla sütunları düzenlenmiş, profesyonel bir `.xlsx` dosyası olarak indirme imkanı sunar.

* **Gelişmiş Hata Yakalama (Exception Handling):** Bozuk dosya formatları, eksik kütüphaneler, yetersiz hafıza veya kayıp model ağırlıkları durumunda uygulamanın çökmesini engelleyen mimari koruma blokları içerir.

---

## 📊 Desteklenen Hastalık Sınıfları

Modelimiz, domates bitkilerinde en sık görülen aşağıdaki 10 farklı durumu ayırt edebilmektedir:

1. Bakteriyel Leke (Bacterial Spot)

2. Erken Yanıklık (Early Blight)

3. Geç Yanıklık (Late Blight)

4. Yaprak Küfü (Leaf Mold)

5. Septoria Yaprak Lekesi

6. Örümcek Akarı (Spider Mites)

7. Hedef Lekesi (Target Spot)

8. Sarı Yaprak Kıvırcıklık Virüsü (TYLCV)

9. Mozaik Virüsü (Mosaic Virus)

10. Sağlıklı Yaprak (Healthy)

---

## 🛠️ Kurulum ve Çalıştırma Adımları

Projeyi yerel bilgisayarınızda ayağa kaldırmak için aşağıdaki adımları sırasıyla terminalinizde çalıştırabilirsiniz:

### 1. Depoyu Klonlayın
### 2. Gerekli Kütüphaneleri Kurun
Projeye ait tüm bağımlılıklar `requirements.txt` dosyasında listelenmiştir. Python ortamınıza (virtual environment kullanılması tavsiye edilir) yüklemek için:

### 3. Model Ağırlıklarını Yerleştirin

GitHub dosya boyutu sınırları (100MB+) sebebiyle, 20k+ görsel ile eğitilen ana CNN model ağırlık dosyası (`tomato_v4_final.keras`) doğrudan depoda yer almamaktadır.
* Lütfen model dosyasını **Https://drive.google.com/drive/folders/1Ern7Rv1RRpOQ1-OtAOw3J3NNLnmNxdi4?usp=sharing** indirin.

* İndirdiğiniz `tomato_v4_final.keras` dosyasını projenin **ana dizinine** (yani `main.py` dosyasının yanına) yerleştirin.

### 4. Uygulamayı Başlatın
Streamlit sunucusunu çalıştırmak için terminale şu komutu yazın:

Uygulama otomatik olarak tarayıcınızda `http://localhost:8501` adresinde açılacaktır.

## 📂 Proje Dizin Yapısı

tomato-disease-detection/

├── .git/

├── .gitignore # Model ağırlıklarının ve sanal ortamların pushlanmasını engeller

├── main.py # Giriş ve karşılama ekranı (UI)

├── requirements.txt # Proje bağımlılıkları listesi

├── README.md # Proje detaylı kurulum açıklaması

├── tomato_v4_final.keras # Ana Teşhis Modeli (Drive'dan indirilerek buraya atılmalıdır)

└── pages/

└── analiz.py # Analiz laboratuvarı, CLIP ön filtresi, TTA ve Dialog ekranları


## 🧪 Kullanılan Teknolojiler ve Kitaplıklar



* **Streamlit:** Modern ve reaktif web arayüzünün geliştirilmesi.

* **TensorFlow & Keras:** Derin Öğrenme (CNN) modelinin yüklenmesi ve çıkarım işlemleri.

* **PyTorch & Transformers (Hugging Face):** OpenAI CLIP mimarisinin çok modlu (görsel-metin) içerik doğrulaması amacıyla entegrasyonu.

* **Pillow (PIL) & NumPy:** Görüntü ön işleme, matris dönüşümleri ve TTA veri artırımı adımları.

* **Pandas:** Teşhis olasılık verilerinin tablo formatına dönüştürülmesi.

* **OpenPyXL:** Excel veri çıktılarının hücre ve sütun genişliği optimizasyonu ile oluşturulması.


## 🔗 Veri Seti ve Referanslar



* **Eğitim Veri Seti:** Model eğitiminde kullanılan genişletilmiş domates yaprağı veri setine Https://www.kaggle.com/datasets/charuchaudhry/plantvillage-tomato-leaf-dataset üzerinden erişim sağlanabilir.




## 📝 Beyan ve Proje Grubu



Bu proje, Bursa Uludağ Üniversitesi Bilgisayar Mühendisliği Bölümü Python Programlamaya Giriş Dersi kapsamında grup olarak hazırlanmıştır. Proje kodları dahil olmak üzere tüm sistem özgün olarak geliştirilmiş ve teslim edilmiştir.



**Grup Üyeleri ve Akademik Bilgiler:**



* **Ahmet Demirbilek** - [032490045]
* **Mehmet Oğuzhan Tanrıverdi** [032490067]
* **Recep Ali Bayoğlu**  [032490032]
