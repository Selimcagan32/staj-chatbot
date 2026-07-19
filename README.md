# 🎓 AI Staj Asistanı

Üniversite öğrencilerinin staj süreciyle ilgili sorularını, okulun resmi staj dökümanlarına dayanarak yanıtlayan bir **RAG (Retrieval-Augmented Generation)** tabanlı yapay zeka chatbot'u.

🔗 **Canlı Demo:** [ai-staj-asistan.streamlit.app](https://ai-staj-asistan.streamlit.app/)

## 📌 Proje Hakkında

Staj sürecine dair güncel bilgiler (başvuru adımları, staj süresi, gerekli belgeler, İSG sertifikası vb.) genellikle dağınık PDF ve Word dökümanlarında yer alıyor. Bu proje, öğrencilerin bu bilgilere doğal bir sohbet arayüzü üzerinden, saniyeler içinde ve doğru kaynaktan erişebilmesini sağlıyor.

Sistem, kullanıcının sorusuna cevap üretirken **sadece okulun resmi dökümanlarındaki bilgilere dayanır**, böylece yanlış veya uydurma bilgi verme riski minimize edilir.

## 🛠️ Kullanılan Teknolojiler

- **Python** – Ana geliştirme dili
- **Streamlit** – Web arayüzü
- **ChromaDB** – Vector database
- **Sentence Transformers** (multilingual embedding) – Türkçe metinler için anlamsal arama
- **Google Gemini API** – Doğal dilde cevap üretimi (LLM)
- **pdfplumber / python-docx** – PDF ve Word dökümanlarından metin çıkarma

## ⚙️ Nasıl Çalışıyor?

1. **Döküman İşleme** – Okulun staj dökümanları (PDF/Word) okunup metne çevrilir
2. **Parçalama (Chunking)** – Metinler, bağlamı koruyacak şekilde küçük parçalara bölünür
3. **Embedding & Vector Database** – Her parça, anlamsal aramaya uygun hale getirilip ChromaDB'ye kaydedilir
4. **Retrieval** – Kullanıcı bir soru sorduğunda, en alakalı parçalar veritabanından bulunur
5. **Generation** – Bulunan parçalar, Gemini API'ye bağlam olarak verilir ve doğal bir cevap üretilir
6. **Arayüz** – Tüm süreç, Streamlit ile oluşturulan sohbet arayüzünde kullanıcıya sunulur

```
Kullanıcı Sorusu → Vector Search (ChromaDB) → İlgili Döküman Parçaları → Gemini API → Cevap
```

## ✨ Özellikler

- 🔍 Anlamsal arama (kelime eşleşmesi değil, anlam bazlı sonuç bulma)
- 🌐 Türkçe dil desteği için multilingual embedding modeli
- ⚡ Sık sorulan sorular için önbellekleme (caching), hız ve API kotası tasarrufu
- 🛡️ Hata durumlarında kullanıcı dostu geri bildirim
- 💬 Gerçek zamanlı, akıcı sohbet arayüzü

## 🚀 Yerel Kurulum

```bash
# Repoyu klonla
git clone https://github.com/Selimcagan32/ai-staj-asistan.git
cd ai-staj-asistan

# Sanal ortam oluştur ve aktive et
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Mac/Linux

# Gerekli kütüphaneleri kur
pip install -r requirements.txt

# .env dosyası oluştur ve API key'ini ekle
echo GEMINI_API_KEY=senin_api_keyin > .env

# Uygulamayı çalıştır
streamlit run app.py
```

## 📂 Proje Yapısı

```
ai-staj-asistan/
├── app.py                  # Streamlit arayüzü
├── chatbot.py               # RAG mantığı ve Gemini API entegrasyonu
├── document_loader.py       # PDF/Word/txt döküman okuma
├── text_splitter.py         # Metin parçalama (chunking)
├── vector_db.py              # ChromaDB entegrasyonu
├── dokumanlar/                # Staj ile ilgili resmi dökümanlar
├── requirements.txt
└── README.md
```

## 🎯 Gelecek Geliştirmeler

- [ ] Kullanıcı geri bildirimi (👍/👎) ile cevap kalitesini takip etme
- [ ] Sık sorulan soruların analitiği
- [ ] Çoklu döküman kaynağı desteği (farklı bölümler için)

## 👤 Geliştirici

**Selim Çağan**
[GitHub](https://github.com/Selimcagan32)