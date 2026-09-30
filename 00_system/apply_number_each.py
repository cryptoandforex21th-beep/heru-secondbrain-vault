import win32com.client

word = win32com.client.GetObject(Class='Word.Application')
doc = None
for d in word.Documents:
    if 'heru skripsi' in d.Name.lower():
        doc = d
        break

if doc:
    # Paragraphs 130, 131, 132: Rumusan Masalah
    for i in [130, 131, 132]:
        p = doc.Paragraphs(i)
        p.Range.ListFormat.ApplyNumberDefault()
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0

    # Paragraphs 136, 137: Tujuan (restart numbering)
    for i in [136, 137]:
        p = doc.Paragraphs(i)
        p.Range.ListFormat.ApplyNumberDefault()
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0

    # Ensure paragraph 136 restarts at 1
    doc.Paragraphs(136).Range.ListFormat.RestartNumbering()

    doc.Save()

    with open(r'd:\SecondBrain\00_system\apply_number_result.txt', 'w', encoding='utf-8') as out:
        for k in range(128, 146):
            pk = doc.Paragraphs(k)
            out.write(f"[{k}] Style={pk.Style.NameLocal} List={repr(pk.Range.ListFormat.ListString)} Left={pk.Format.LeftIndent} Text={repr(pk.Range.Text[:50])}\n")
