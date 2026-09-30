import win32com.client

word = win32com.client.GetObject(Class='Word.Application')
doc = None
for d in word.Documents:
    if 'heru skripsi' in d.Name.lower():
        doc = d
        break

if doc:
    # 1. Rumusan Masalah range: paragraph 130 to 132
    r1 = doc.Range(Start=doc.Paragraphs(130).Range.Start, End=doc.Paragraphs(132).Range.End)
    r1.ListFormat.RemoveNumbers()
    r1.ListFormat.ApplyNumberDefault()
    for k in [130, 131, 132]:
        p = doc.Paragraphs(k)
        p.Style = doc.Styles("List Paragraph")
        p.Range.Font.Name = "Arial"
        p.Range.Font.Size = 10.0
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0
        p.Format.Alignment = 3 # Justify
        p.Format.SpaceBefore = 0.0
        p.Format.SpaceAfter = 4.0
        p.Format.LineSpacing = 12.0

    # 2. Tujuan range: paragraph 136 to 137
    r2 = doc.Range(Start=doc.Paragraphs(136).Range.Start, End=doc.Paragraphs(137).Range.End)
    r2.ListFormat.RemoveNumbers()
    r2.ListFormat.ApplyNumberDefault()
    for k in [136, 137]:
        p = doc.Paragraphs(k)
        p.Style = doc.Styles("List Paragraph")
        p.Range.Font.Name = "Arial"
        p.Range.Font.Size = 10.0
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0
        p.Format.Alignment = 3 # Justify
        p.Format.SpaceBefore = 0.0
        p.Format.SpaceAfter = 4.0
        p.Format.LineSpacing = 12.0

    doc.Save()

    with open(r'd:\SecondBrain\00_system\range_numbering_result.txt', 'w', encoding='utf-8') as out:
        out.write("--- FINAL RANGE NUMBERING CHECK ---\n")
        for k in range(123, 146):
            pk = doc.Paragraphs(k)
            out.write(f"[{k}] Style={pk.Style.NameLocal} List={repr(pk.Range.ListFormat.ListString)} Left={pk.Format.LeftIndent} First={pk.Format.FirstLineIndent} Text={repr(pk.Range.Text.strip()[:50])}\n")
