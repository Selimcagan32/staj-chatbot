import os
import pdfplumber
from docx import Document

import pdfplumber

def pdf_oku(dosya_yolu):
    """PDF dosyasından metin çıkarır (pdfplumber ile, Türkçe karakter desteği daha iyi)"""
    metin = ""
    with pdfplumber.open(dosya_yolu) as pdf:
        for sayfa in pdf.pages:
            sayfa_metni = sayfa.extract_text()
            if sayfa_metni:
                metin += sayfa_metni + "\n"
    return metin

def word_oku(dosya_yolu):
    """Word (.docx) dosyasından metin çıkarır"""
    doc = Document(dosya_yolu)
    metin = "\n".join([paragraf.text for paragraf in doc.paragraphs])
    return metin

def txt_oku(dosya_yolu):
    """Düz metin dosyasını okur"""
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        return f.read()

def tum_dokumanlari_yukle(klasor_yolu="dokumanlar"):
    """Klasördeki tüm PDF, Word ve metin dosyalarını okuyup birleştirir"""
    tum_dokumanlar = []  # her eleman: {"dosya_adi": ..., "metin": ...}

    for dosya_adi in os.listdir(klasor_yolu):
        dosya_yolu = os.path.join(klasor_yolu, dosya_adi)

        try:
            if dosya_adi.endswith(".pdf"):
                metin = pdf_oku(dosya_yolu)
            elif dosya_adi.endswith(".docx"):
                metin = word_oku(dosya_yolu)
            elif dosya_adi.endswith(".txt"):
                metin = txt_oku(dosya_yolu)
            else:
                continue  # desteklenmeyen format, atla

            tum_dokumanlar.append({
                "dosya_adi": dosya_adi,
                "metin": metin
            })
            print(f"✓ {dosya_adi} okundu ({len(metin)} karakter)")

        except Exception as e:
            print(f"✗ {dosya_adi} okunamadı: {e}")

    return tum_dokumanlar

# Test etmek için
if __name__ == "__main__":
    dokumanlar = tum_dokumanlari_yukle()
    print(f"\nToplam {len(dokumanlar)} döküman yüklendi.")