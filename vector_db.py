import chromadb
from chromadb.utils import embedding_functions

turkce_embedding = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-mpnet-base-v2"
)

def veritabani_olustur():
    client = chromadb.PersistentClient(path="./chroma_db")
    koleksiyon = client.get_or_create_collection(
        name="staj_dokumanlari",
        embedding_function=turkce_embedding
    )
    return koleksiyon


def parcalari_veritabanina_ekle(parcalar, koleksiyon):
    """
    text_splitter'dan gelen parçaları ChromaDB'ye ekler.
    ChromaDB embedding işlemini otomatik olarak kendi yapıyor.
    """
    metinler = [p["metin"] for p in parcalar]
    id_listesi = [f"{p['dosya_adi']}_{p['parca_no']}" for p in parcalar]
    metadata_listesi = [{"dosya_adi": p["dosya_adi"], "parca_no": p["parca_no"]} for p in parcalar]

    koleksiyon.add(
        documents=metinler,
        ids=id_listesi,
        metadatas=metadata_listesi
    )

    print(f"✓ {len(parcalar)} parça veritabanına eklendi.")


def benzer_parcalari_bul(soru, koleksiyon, sonuc_sayisi=3):
    """
    Verilen soruya en çok benzeyen parçaları veritabanından bulur.
    """
    sonuclar = koleksiyon.query(
        query_texts=[soru],
        n_results=sonuc_sayisi
    )
    return sonuclar


# Test etmek için
if __name__ == "__main__":
    from document_loader import tum_dokumanlari_yukle
    from text_splitter import tum_dokumanlari_parcala

    print("Dökümanlar yükleniyor...")
    dokumanlar = tum_dokumanlari_yukle()
    parcalar = tum_dokumanlari_parcala(dokumanlar)

    print("\nVeritabanı oluşturuluyor...")
    koleksiyon = veritabani_olustur()

    # Eğer koleksiyon boşsa parçaları ekle
    if koleksiyon.count() == 0:
        parcalari_veritabanina_ekle(parcalar, koleksiyon)
    else:
        print(f"Veritabanında zaten {koleksiyon.count()} parça var, tekrar eklenmedi.")

    # Test sorusu
    test_sorusu = "staj süresi ne kadar"
    print(f"\nTest sorusu: '{test_sorusu}'")
    sonuclar = benzer_parcalari_bul(test_sorusu, koleksiyon)

    print("\nEn alakalı parçalar:")
    for i, metin in enumerate(sonuclar["documents"][0]):
        print(f"\n--- Sonuç {i+1} ---")
        print(metin)