import streamlit as st
from vector_db import veritabani_olustur
from chatbot import cevap_uret

st.set_page_config(page_title="Staj Chatbot", page_icon="🎓")

st.title("🎓 Staj Asistanı")
st.write("Staj süreciyle ilgili merak ettiğin her şeyi sorabilirsin!")

# Veritabanını sadece bir kere yükle (her mesajda tekrar yüklememek için)
@st.cache_resource
def veritabani_yukle():
    return veritabani_olustur()

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