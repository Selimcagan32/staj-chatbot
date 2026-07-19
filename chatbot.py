import os
import git
from google import genai
from dotenv import load_dotenv
from vector_db import veritabani_olustur, benzer_parcalari_bul
import re

# Basit bir önbellek: {normalize edilmiş soru: cevap}
soru_cevap_onbellegi = {}

def soruyu_normallestir(soru):
    """Soruyu küçük harfe çevirir, noktalama işaretlerini kaldırır, fazla boşlukları temizler"""
    soru = soru.lower().strip()
    soru = re.sub(r'[^\w\sçğıöşü]', '', soru)  # noktalama işaretlerini kaldır
    soru = re.sub(r'\s+', ' ', soru)  # fazla boşlukları tek boşluğa indir
    return soru

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def cevap_uret(soru, koleksiyon):
    # Önbellekte var mı kontrol et
    normalized_soru = soruyu_normallestir(soru)
    if normalized_soru in soru_cevap_onbellegi:
        return soru_cevap_onbellegi[normalized_soru]

    sonuclar = benzer_parcalari_bul(soru, koleksiyon, sonuc_sayisi=8)
    bulunan_parcalar = sonuclar["documents"][0]
    baglam = "\n\n---\n\n".join(bulunan_parcalar)

    prompt = f"""Sen bir üniversitenin staj süreciyle ilgili sorulara cevap veren, samimi bir asistansın.

Eğer kullanıcı senin kim olduğunu soruyorsa, ne yaptığını soruyorsa veya genel bir selamlaşma/sohbet başlatıyorsa, kısaca kendini tanıt: "Ben staj süreciyle ilgili sorularını cevaplamak için buradayım. Staj süresi, başvuru adımları, staj raporu gibi konularda yardımcı olabilirim." gibi doğal bir şekilde cevap ver.

Eğer soru staj/döküman içeriğiyle ilgiliyse, SADECE aşağıdaki dökümanlardan alınan bilgilere dayanarak cevap ver. Eğer cevap bu bilgilerde yoksa, "Bu konuda dökümanlarda net bir bilgi bulamadım, staj komisyonuyla iletişime geçmenizi öneririm" de. Uydurma bilgi verme.

DÖKÜMANLARDAN ALINAN BİLGİLER:
{baglam}

SORU: {soru}

CEVAP:"""

    try:
        yanit = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )
        cevap = yanit.text
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            cevap = "Şu anda çok yoğunuz, lütfen birkaç dakika sonra tekrar dener misin? 🙏"
        else:
            cevap = "Bir hata oluştu, lütfen tekrar dener misin. Sorun devam ederse staj komisyonuyla iletişime geçebilirsin."


    # Önbelleğe kaydet
    soru_cevap_onbellegi[normalized_soru] = cevap

    return cevap


if __name__ == "__main__":
    koleksiyon = veritabani_olustur()

    while True:
        soru = input("\nSorunuz (çıkmak için 'q'): ")
        if soru.lower() == "q":
            break

        cevap = cevap_uret(soru, koleksiyon)
        print(f"\nCevap: {cevap}")