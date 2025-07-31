📌 LLM Biyografi Analizi Projesi

• Bu proje, Yapay Zeka (LLM) kullanarak biyografi belgelerinden özet bilgiler çıkarmayı ve kişiler arasındaki ortak özelliklere dayalı ilişkileri belirlemeyi amaçlar.

📌 Neler Yapabilir?

Ortak Özelliklere Göre Bağlantı Kurma:

• Doğum yeri, eğitim geçmişi, çalışma hayatı ve yaşadığı şehir gibi veriler üzerinden kişiler arasındaki bağlantıları oluşturur.

• Eğitim ve iş geçmişinde tarih kesişmelerini kontrol ederek gerçekten aynı dönemde bulunup bulunmadıklarını belirler.

Otomatik İlişki Haritaları:

• Aynı okulda okuyan, aynı kurumda çalışan veya aynı şehirde yaşayan kişiler arasındaki ilişkileri otomatik görselleştirir.

Kolay Veri İşleme:

• Markdown biyografi dosyalarını işler, JSON formatında yapılandırılmış veri üretir ve bu verileri grafik tabanlı ilişki haritalarına dönüştürür.

Kişisel Sorgulara Cevap Verme:

Örneğin:

İster 1: “Ben Gülnur Yıldız, ASELSAN’da çalışan Ahmet Doğan adlı kişiye nasıl ulaşabilirim?”
→ Sistem, ortak okul, iş yeri veya şehir bağlantıları üzerinden dolaylı ilişki yollarını bulur.

<img width="692" height="605" alt="image" src="https://github.com/user-attachments/assets/0b7b7c63-d3bf-49c0-a0c3-5116e8d207f0" />


İster 2: “Ben Nefise Aydın, ilkokul arkadaşlarımın tüm üniversite arkadaşlarını bulmak istiyorum.”
→ Sistem, Nefise Aydın’ın ilkokul arkadaşlarını bulur ve bu kişilerin üniversite bağlantılarını listeler.

<img width="573" height="675" alt="image" src="https://github.com/user-attachments/assets/5e5271e1-86a7-4fd8-85a2-3900e4d9c66c" />

📌 Örnek Kullanım Alanları

• Aynı okulda aynı dönemde okuyan kişileri bulma

• Aynı şirkette aynı dönemde çalışan kişileri tespit etme

• Aynı memleketten olan insanları listeleme

• Aynı şehirde yaşayan insanları keşfetme 

🛠️ Teknolojiler

• Python (veri işleme, analiz)

• LLM API (biyografi analizi)

• Neo4j (graph veri tabanı ve görselleştirme)

• Pandas / JSON (veri formatlama ve entegrasyon)

• Cypher (Neo4j sorgularında kullanıldı)

📌 Yol Haritası

• Verileri Markdown'dan otomatik JSON formatına dönüştürme

• Ortak özelliklere göre ilişkileri çıkarma

• Tarih kesişmesi algoritması geliştirme

• Neo4j graph görselleştirme entegrasyonu


Örneğin:
{

  "source": "Zehra Ermiş",
  
  "target": "Zeynep Uzun",
  
  "relations": [
  
    "AYNI_MEMLEKETTEN",
    
    "LISE_ARKADASI",
    
    "UNIVERSITE_ARKADASI",
    
    "MESLEKTAS",
    
    "AYNI_KURUMDA_CALISMIS"
    
  ]
  
}


  ![alt text](image.png)
