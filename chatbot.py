import os
from google import genai
from dotenv import load_dotenv
from vector_db import veritabani_olustur, benzer_parcalari_bul

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def cevap_uret(soru, koleksiyon):
    sonuclar = benzer_parcalari_bul(soru, koleksiyon, sonuc_sayisi=8)
    bulunan_parcalar = sonuclar["documents"][0]
    baglam = "\n\n---\n\n".join(bulunan_parcalar)

    prompt = f"""Sen bir üniversitenin staj süreçleriyle ilgili sorulara cevap veren bir asistansın.
Aşağıda okulun resmi staj dökümanlarından alınmış parçalar var. SADECE bu bilgilere dayanarak soruyu cevapla.
Eğer cevap bu bilgilerde yoksa, "Bu konuda dökümanlarda net bir bilgi bulamadım, staj komisyonuyla iletişime geçmenizi öneririm" de. Uydurma bilgi verme.

DÖKÜMANLARDAN ALINAN BİLGİLER:
{baglam}

SORU: {soru}

CEVAP:"""

    yanit = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return yanit.text


if __name__ == "__main__":
    koleksiyon = veritabani_olustur()

    while True:
        soru = input("\nSorunuz (çıkmak için 'q'): ")
        if soru.lower() == "q":
            break

        cevap = cevap_uret(soru, koleksiyon)
        print(f"\nCevap: {cevap}")