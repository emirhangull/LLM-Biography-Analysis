import os
import json

def turkce_key_to_ingilizce(json_data):
    char_map = {
        'ş': 's',
        'Ş': 'S',
        'ğ': 'g',
        'Ğ': 'G',
        'ç': 'c',
        'Ç': 'C',
        'ı': 'i',
        'İ': 'I',
        'ö': 'o',
        'Ö': 'O',
        'ü': 'u',
        'Ü': 'U'
    }

    def turkce_to_ingilizce(text):
        for key, value in char_map.items():
            text = text.replace(key, value)
        return text

    # SADECE anahtarları İngilizce karakterlere dönüştürme (value'lar aynı kalacak)
    updated_json = {}
    for key, value in json_data.items():
        new_key = turkce_to_ingilizce(key)
        # Value'ları olduğu gibi bırak, sadece key'leri çevir
        updated_json[new_key] = value

    return updated_json

def convert_json_keys_to_english(input_file, output_file):
    """
    JSON dosyasındaki Türkçe karakterli key'leri İngilizce karakterlere çevirir.
    
    Args:
        input_file (str): Giriş JSON dosyasının yolu
        output_file (str): Çıkış JSON dosyasının yolu
    """
    try:
        # JSON dosyasını oku
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Eğer data bir liste ise (birden fazla nesne içeriyorsa)
        if isinstance(data, list):
            converted_data = []
            for item in data:
                if isinstance(item, dict):
                    converted_data.append(turkce_key_to_ingilizce(item))
                else:
                    converted_data.append(item)
        elif isinstance(data, dict):
            converted_data = turkce_key_to_ingilizce(data)
        else:
            converted_data = data
        
        # Dönüştürülmüş veriyi yeni dosyaya yaz
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(converted_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Başarılı! {input_file} -> {output_file}")
        print(f"📊 Key'ler İngilizce karakterlere dönüştürüldü.")
        
    except FileNotFoundError:
        print(f"❌ Hata: {input_file} dosyası bulunamadı!")
    except json.JSONDecodeError:
        print(f"❌ Hata: {input_file} geçerli bir JSON dosyası değil!")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

def main():
    """Ana fonksiyon - komut satırından kullanım için"""
    import sys
    
    if len(sys.argv) != 3:
        print("Kullanım: python to_english.py <input_file.json> <output_file.json>")
        print("Örnek: python to_english.py structured_bios_all.json structured_bios_english.json")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_json_keys_to_english(input_file, output_file)

if __name__ == "__main__":
    main()