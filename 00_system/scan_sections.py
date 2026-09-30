import win32com.client

word = win32com.client.GetObject(Class='Word.Application')
doc = None
for d in word.Documents:
    if 'heru skripsi' in d.Name.lower():
        doc = d
        break

with open(r'd:\SecondBrain\00_system\scan_sections.txt', 'w', encoding='utf-8') as f:
    if not doc:
        f.write('Not found\n')
    else:
        for i in range(1, doc.Paragraphs.Count + 1):
            t = doc.Paragraphs(i).Range.Text.strip()
            if any(k in t.upper() for k in ['BAB I', 'BAB II', 'BAB III', 'BAB IV', 'BAB V', 'DAFTAR PUSTAKA', 'PENDAHULUAN', 'LATAR BELAKANG']):
                f.write(f'{i}: {t}\n')
