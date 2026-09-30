import win32com.client

word = win32com.client.GetObject(Class='Word.Application')
doc = None
for d in word.Documents:
    if 'heru skripsi' in d.Name.lower():
        doc = d
        break

if doc:
    # wdNumberGallery = 2
    num_template = word.ListGalleries(2).ListTemplates(1)

    # 1. Apply to Rumusan Masalah items (paragraphs 130, 131, 132)
    first = True
    for p_idx in [130, 131, 132]:
        p = doc.Paragraphs(p_idx)
        p.Range.ListFormat.ApplyListTemplate(
            ListTemplate=num_template,
            ContinuePreviousList=not first,
            ApplyTo=1
        )
        first = False
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0

    # 2. Apply to Tujuan items (paragraphs 136, 137) - restart numbering at 1
    first = True
    for p_idx in [136, 137]:
        p = doc.Paragraphs(p_idx)
        p.Range.ListFormat.ApplyListTemplate(
            ListTemplate=num_template,
            ContinuePreviousList=not first,
            ApplyTo=1
        )
        first = False
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0

    doc.Save()

    with open(r'd:\SecondBrain\00_system\numbered_list_result.txt', 'w', encoding='utf-8') as out:
        out.write("--- VERIFICATION ---\n")
        for k in range(123, 146):
            pk = doc.Paragraphs(k)
            out.write(f"[{k}] Style={pk.Style.NameLocal} List={repr(pk.Range.ListFormat.ListString)} Left={pk.Format.LeftIndent} First={pk.Format.FirstLineIndent} Text={repr(pk.Range.Text.strip()[:50])}\n")
