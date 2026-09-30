import win32com.client

word = win32com.client.GetObject(Class='Word.Application')
doc = None
for d in word.Documents:
    if 'heru skripsi' in d.Name.lower():
        doc = d
        break

with open(r'd:\SecondBrain\00_system\final_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"TOTAL PARAGRAPHS: {doc.Paragraphs.Count}\n\n")
    
    f.write("=== 1. TOC (PARAGRAPHS 100-105) ===\n")
    for i in range(100, 106):
        f.write(f"[{i}] {repr(doc.Paragraphs(i).Range.Text.strip())}\n")
        
    f.write("\n=== 2. BAB I (PARAGRAPHS 123-138) ===\n")
    for i in range(123, 139):
        p = doc.Paragraphs(i)
        f.write(f"[{i}] Font={p.Range.Font.Name} Size={p.Range.Font.Size} Bold={p.Range.Font.Bold}\n")
        f.write(f"     Text={repr(p.Range.Text.strip()[:100])}\n")

    f.write("\n=== 3. DAFTAR PUSTAKA (FIRST 6 ENTRIES) ===\n")
    idx_dp = None
    for i in range(300, doc.Paragraphs.Count + 1):
        if doc.Paragraphs(i).Range.Text.strip().upper() == "DAFTAR PUSTAKA":
            idx_dp = i
            break
    if idx_dp:
        for i in range(idx_dp, min(idx_dp + 7, doc.Paragraphs.Count + 1)):
            p = doc.Paragraphs(i)
            f.write(f"[{i}] {repr(p.Range.Text.strip()[:100])}\n")

    f.write("\n=== 4. DOCUMENT END (LAST 5 PARAGRAPHS) ===\n")
    for i in range(doc.Paragraphs.Count - 4, doc.Paragraphs.Count + 1):
        p = doc.Paragraphs(i)
        f.write(f"[{i}] {repr(p.Range.Text.strip()[:100])}\n")
