import streamlit as st
from vector_db import veritabani_olustur
from chatbot import cevap_uret
from PIL import Image

logo = Image.open("gorseller/okul_logo.png")

st.set_page_config(page_title="AI Staj Asistanı", page_icon=logo)

# Başlığın yanında da logoyu göstermek için
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=80)
with col2:
    st.title("AI Staj Asistanı")

st.write("Staj süreciyle ilgili merak ettiğin her şeyi sorabilirsin!")

@st.cache_resource
def veritabani_yukle():
    from document_loader import tum_dokumanlari_yukle
    from text_splitter import tum_dokumanlari_parcala
    from vector_db import veritabani_olustur, parcalari_veritabanina_ekle

    koleksiyon = veritabani_olustur()

    # Eğer veritabanı boşsa (ilk çalıştırma), dökümanları işleyip ekle
    if koleksiyon.count() == 0:
        dokumanlar = tum_dokumanlari_yukle()
        parcalar = tum_dokumanlari_parcala(dokumanlar)
        parcalari_veritabanina_ekle(parcalar, koleksiyon)

    return koleksiyon
koleksiyon = veritabani_yukle()

# Sohbet geçmişini hafızada tut
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# Geçmiş mesajları ekrana yazdır
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"]):
        st.write(mesaj["icerik"])

# Kullanıcıdan yeni mesaj al
kullanici_sorusu = st.chat_input("Sorunuzu yazın...")

if kullanici_sorusu:
    # Kullanıcının mesajını ekrana ve geçmişe ekle
    st.session_state.mesajlar.append({"rol": "user", "icerik": kullanici_sorusu})
    with st.chat_message("user"):
        st.write(kullanici_sorusu)

    # Cevabı üret ve göster
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            cevap = cevap_uret(kullanici_sorusu, koleksiyon)
            st.write(cevap)

    # Cevabı geçmişe ekle
    st.session_state.mesajlar.append({"rol": "assistant", "icerik": cevap})