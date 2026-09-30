import win32com.client
import sys
import traceback

log_file = r'd:\SecondBrain\00_system\apply_clean_list.log'

try:
    word = win32com.client.GetObject(Class='Word.Application')
    doc = None
    for d in word.Documents:
        if 'heru skripsi' in d.Name.lower():
            doc = d
            break
            
    if not doc:
        with open(log_file, "w") as f: f.write("Doc not found\n")
        sys.exit(1)

    # wdNumberGallery = 2
    num_template = word.ListGalleries(2).ListTemplates(1)

    # 1. Rumusan Masalah: items at 130, 131, 132
    # Ensure text has NO leading numbers
    p130 = doc.Paragraphs(130)
    p131 = doc.Paragraphs(131)
    p132 = doc.Paragraphs(132)

    # Apply to p130 (first item, restart = False for ContinuePreviousList)
    p130.Range.ListFormat.ApplyListTemplate(ListTemplate=num_template, ContinuePreviousList=False, ApplyTo=1)
    p131.Range.ListFormat.ApplyListTemplate(ListTemplate=num_template, ContinuePreviousList=True, ApplyTo=1)
    p132.Range.ListFormat.ApplyListTemplate(ListTemplate=num_template, ContinuePreviousList=True, ApplyTo=1)

    for p in [p130, p131, p132]:
        p.Style = doc.Styles("List Paragraph")
        p.Range.Font.Name = "Arial"
        p.Range.Font.Size = 10.0
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0
        p.Format.Alignment = 3 # Justify
        p.Format.SpaceBefore = 0.0
        p.Format.SpaceAfter = 4.0
        p.Format.LineSpacing = 12.0

    # 2. Tujuan: items at 136, 137
    p136 = doc.Paragraphs(136)
    p137 = doc.Paragraphs(137)

    p136.Range.ListFormat.ApplyListTemplate(ListTemplate=num_template, ContinuePreviousList=False, ApplyTo=1)
    p137.Range.ListFormat.ApplyListTemplate(ListTemplate=num_template, ContinuePreviousList=True, ApplyTo=1)

    for p in [p136, p137]:
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

    with open(log_file, "w", encoding="utf-8") as f:
        f.write("Success!\n")
        for k in range(128, 145):
            pk = doc.Paragraphs(k)
            f.write(f"[{k}] Style={pk.Style.NameLocal} List={repr(pk.Range.ListFormat.ListString)} Left={pk.Format.LeftIndent} First={pk.Format.FirstLineIndent} Text={repr(pk.Range.Text.strip()[:45])}\n")

except Exception as e:
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n{traceback.format_exc()}\n")
