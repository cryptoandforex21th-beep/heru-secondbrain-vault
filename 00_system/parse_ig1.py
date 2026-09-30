import re
import json

with open(r'd:\SecondBrain\00_system\ig_reel1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Cari pola text komentar atau caption
all_texts = re.findall(r'"text":"(.*?)"', text)
print(f"Total text tokens found: {len(all_texts)}")

interesting = []
for t in all_texts:
    # decode escaped unicode
    try:
        clean_t = t.encode('utf-8').decode('unicode_escape')
    except:
        clean_t = t
    
    if any(k in clean_t.lower() for k in ['orchestrator', 'bos ai', 'karyawan', 'ruang', 'pantry', 'nama', 'app', 'aplikasi', 'software', 'pake', 'link', 'buatnya']):
        if len(clean_t) < 300:
            interesting.append(clean_t)

print("\n--- TEMUAN MENARIK ---")
for item in set(interesting[:40]):
    print("•", item)
