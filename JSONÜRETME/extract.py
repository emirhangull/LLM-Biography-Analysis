# extract_final.py - Tüm dosyalar için Google Gemini 2.5 Flash API ile
import os
import json
import time
from dotenv import load_dotenv
from google import genai

# .env dosyasını yükle
load_dotenv()

DATASET_PATH = "C:\\Users\\emirhan.gul\\Desktop\\LLM_proje\\LLM-Biography-Analysis\\dataset_new"
OUTPUT_JSON = "C:\\Users\\emirhan.gul\\Desktop\\LLM_proje\\LLM-Biography-Analysis\\structured_bios_new.json"

# Google Gemini client'ı başlat (GEMINI_API_KEY ortam değişkenini otomatik alır)
client = genai.Client()

def extract_structured_data(md_text):
    prompt = f"""
    Aşağıdaki detaylı biyografiden yapılandırılmış JSON formatında bilgi çıkar. Kurallara dikkatli uyun:

    KURALLAR:
    - Bilgi yoksa null yaz (tırnaksız)
    - Tarihler: "GG.AA.YYYY" formatında (örn: "15.09.1988")
    - Yıl aralıkları: "YYYY-YYYY" (örn: "2006-2010")
    - Tek yıl: "YYYY" (örn: "2013")
    - Şehirler: Sadece şehir adı (örn: "İzmir", "Ankara")
    - Hobiler: Sade ifadeler listesi
    - Eş ve çocuk yoksa null yaz
    - Çocuklar: Sadece isimler listesi
    - Boş listeler için [] kullan
    - Yaş: Doğum tarihine göre 2025 yılı baz alınarak hesapla
    - Çalışma yılları: Hala çalışıyorsa "YYYY-devam ediyor", çıktıysa "YYYY-YYYY"
    - Çalıştığı kurumlar ve çalışma yılları aynı sırada olmalı
    - Akademik yayınlar: Sadece makale/kitap isimleri

    ÇIKTIYI SADECE JSON OLARAK VER. AÇIKLAMA, MARKDOWN, KOD BLOĞU EKLEMEYİN.

    İstenen JSON formatı:
    {{
    "ad": "Kişi Adı",
    "doğum_yeri": "Şehir",
    "doğum_tarihi": "GG.AA.YYYY",
    "yaş": sayı,
    "ilkokul": "Okul adı veya null",
    "ilkokul_yılları": "YYYY-YYYY veya null",
    "lise": "Lise adı veya null",
    "lise_yılları": "YYYY-YYYY veya null",
    "üniversite": "Üniversite adı veya null",
    "üniversite_yılları": "YYYY-YYYY veya null",
    "bölüm": "Bölüm adı veya null",
    "yüksek_lisans": "Üniversite adı veya null",
    "yüksek_lisans_yılları": "YYYY-YYYY veya null",
    "doktora": "Üniversite adı veya null",
    "doktora_yılları": "YYYY-YYYY veya null",
    "çalıştığı_kurumlar": ["Kurum1", "Kurum2"] veya [],
    "çalışma_yılları": ["YYYY-YYYY", "YYYY-devam ediyor"] veya [],
    "kurduğu_girişim_ve_dernekler": ["Girişim1"] veya [],
    "girişim_kuruluş_yılları": ["YYYY"] veya [],
    "yaşadığı_şehir": "Şehir",
    "hobiler": ["hobi1", "hobi2"] veya [],
    "eş": "Eş adı veya null",
    "çocuklar": ["Çocuk1", "Çocuk2"] veya [],
    "akademik_yayınlar": ["Makale1", "Makale2"] veya [],
    "yayın_yılları": ["YYYY", "YYYY"] veya []
    }}

    Biyografi:
    {md_text}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        json_text = response.text.strip()
        
        # JSON'u temizle (markdown kod bloklarını kaldır)
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()
        elif "```" in json_text:
            json_text = json_text.split("```")[1].strip()
            
        return json_text
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print(f"❌ Rate limit hatası - 30 saniye bekleniyor...")
            time.sleep(30)
            return None
        elif "quota" in error_msg.lower():
            print(f"❌ Günlük kota doldu: {e}")
            return None
        else:
            print(f"❌ LLM hatası: {e}")
            return None

def run():
    all_data = []
    files = [f for f in os.listdir(DATASET_PATH) if f.endswith(".md")]
    
    print(f"Toplam {len(files)} dosya işlenecek...")
    
    for i, file in enumerate(files, 1):
        try:
            print(f"İşleniyor ({i}/{len(files)}): {file}")
            
            with open(os.path.join(DATASET_PATH, file), "r", encoding="utf-8") as f:
                text = f.read()
            
            json_str = extract_structured_data(text)
            
            if json_str:
                try:
                    parsed = json.loads(json_str)
                    parsed["dosya_adı"] = file  # Dosya adını da ekleyelim
                    all_data.append(parsed)
                    print(f"✅ Başarılı: {parsed.get('ad', 'Bilinmeyen')}")
                    
                    # Her dosya sonrası JSON'u hemen kaydet
                    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
                        json.dump(all_data, f, ensure_ascii=False, indent=2)
                    print(f"📁 Ara kayıt yapıldı - Toplam: {len(all_data)} kişi")
                    
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parse hatası: {e}")
                    print(f"Raw output: {json_str[:200]}...")
            else:
                print(f"❌ Başarısız: {file}")
            
            # Rate limiting - API quota'sını aşmamak için bekleme (dakikada 15 istek limiti)
            if i < len(files):  # Son dosya değilse bekle
                print("⏳ 3 saniye bekleniyor...")
                time.sleep(3)
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Kullanıcı tarafından durduruldu. {len(all_data)} dosya işlendi.")
            break
        except Exception as e:
            print(f"❌ Hata ({file}): {e}")
    
    # Final sonuçları kaydet (zaten her adımda kaydediliyor ama gene de)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 İşlem tamamlandı! {len(all_data)} dosya başarıyla işlendi.")
    print(f"📁 Final sonuçlar: {OUTPUT_JSON}")
    print(f"📊 Başarı oranı: {len(all_data)}/{len(files)} ({len(all_data)/len(files)*100:.1f}%)")

if __name__ == "__main__":
    run()
