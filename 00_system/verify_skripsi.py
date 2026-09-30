import win32com.client

word = win32com.client.GetObject(Class='Word.Application')
doc = None
for d in word.Documents:
    if 'heru skripsi' in d.Name.lower():
        doc = d
        break

with open(r'd:\SecondBrain\00_system\verify_skripsi.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total Paragraphs: {doc.Paragraphs.Count}\n\n")
    f.write("--- PARAGRAPHS 95 TO 115 ---\n")
    for i in range(95, min(116, doc.Paragraphs.Count + 1)):
        f.write(f"[{i}] {repr(doc.Paragraphs(i).Range.Text.strip())}\n")

    f.write("\n--- PARAGRAPHS 120 TO 145 ---\n")
    for i in range(120, min(145, doc.Paragraphs.Count + 1)):
        f.write(f"[{i}] {repr(doc.Paragraphs(i).Range.Text.strip())}\n")

    f.write("\n--- PARAGRAPHS 380 TO END ---\n")
    for i in range(max(1, doc.Paragraphs.Count - 25), doc.Paragraphs.Count + 1):
        f.write(f"[{i}] {repr(doc.Paragraphs(i).Range.Text.strip())}\n")
