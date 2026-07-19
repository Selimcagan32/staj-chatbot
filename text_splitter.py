def metni_parcala(metin, parca_boyutu=500, ortusme=50):
    """
    Uzun bir metni küçük parçalara böler.

    parca_boyutu: her parçanın yaklaşık karakter sayısı
    ortusme: parçalar arasında ne kadar örtüşme olacağı
             (cümlelerin ortadan bölünmesini azaltmak için)
    """
    parcalar = []
    baslangic = 0

    while baslangic < len(metin):
        bitis = baslangic + parca_boyutu
        parca = metin[baslangic:bitis]
        parcalar.append(parca)
        baslangic = bitis - ortusme  # bir sonraki parça biraz geriden başlasın

    return parcalar


def tum_dokumanlari_parcala(dokumanlar, parca_boyutu=900, ortusme=150):
    """
    document_loader'dan gelen döküman listesini alır,
    her birini parçalara böler.

    Dönen format: [{"dosya_adi": ..., "parca_no": ..., "metin": ...}, ...]
    """
    tum_parcalar = []

    for dokuman in dokumanlar:
        parcalar = metni_parcala(dokuman["metin"], parca_boyutu, ortusme)

        for i, parca in enumerate(parcalar):
            tum_parcalar.append({
                "dosya_adi": dokuman["dosya_adi"],
                "parca_no": i,
                "metin": parca
            })

    return tum_parcalar


# Test etmek için
if __name__ == "__main__":
    from document_loader import tum_dokumanlari_yukle

    dokumanlar = tum_dokumanlari_yukle()
    parcalar = tum_dokumanlari_parcala(dokumanlar)

    print(f"\nToplam {len(parcalar)} parça oluşturuldu.\n")

    # İlk 2 parçayı örnek olarak göster
    for parca in parcalar[:2]:
        print(f"--- {parca['dosya_adi']} - Parça {parca['parca_no']} ---")
        print(parca['metin'])
        print()