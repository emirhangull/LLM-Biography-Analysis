import json
import pandas as pd

# JSON dosyasını oku
with open('automated_relationships.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# DataFrame'e çevir
df = pd.DataFrame(data)

# CSV olarak kaydet
df.to_csv('output.csv', index=False, encoding='utf-8')