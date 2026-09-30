import win32com.client
import time

word = win32com.client.GetObject(Class='Word.Application')
file_path = r'C:\Users\Heru Ardiansyah\Downloads\heru skripsi perancangan solar tube.docx'

doc = None
for d in word.Documents:
    if 'heru skripsi' in d.Name.lower():
        doc = d
        break

if doc:
    # Close without saving memory buffer so Word loads the updated file from disk
    doc.Close(SaveChanges=False)
    time.sleep(0.5)

# Open fresh
new_doc = word.Documents.Open(file_path)

# 1. Ensure Section 6 starts at 1
s6 = new_doc.Sections(6)
for h in [s6.Headers(1), s6.Headers(2)]:
    try:
        h.PageNumbers.RestartNumberingAtSection = True
        h.PageNumbers.StartingNumber = 1
        h.PageNumbers.NumberStyle = 0
    except: pass
for f in [s6.Footers(1), f.Footers(2)]:
    try:
        f.PageNumbers.RestartNumberingAtSection = True
        f.PageNumbers.StartingNumber = 1
        f.PageNumbers.NumberStyle = 0
    except: pass

# 2. Section 7 continues
if new_doc.Sections.Count >= 7:
    s7 = new_doc.Sections(7)
    for h in [s7.Headers(1), s7.Headers(2)]:
        try: h.PageNumbers.RestartNumberingAtSection = False
        except: pass
    for f in [s7.Footers(1), f.Footers(2)]:
        try: f.PageNumbers.RestartNumberingAtSection = False
        except: pass

# 3. Update TOC
for toc in new_doc.TablesOfContents:
    try: toc.UpdatePageNumbers()
    except: pass

# 4. Scroll to Bab I Latar Belakang
word.Visible = True
word.Activate()
new_doc.Activate()

target_p = None
for i in range(120, 135):
    if "LATAR BELAKANG" in new_doc.Paragraphs(i).Range.Text.upper():
        target_p = new_doc.Paragraphs(i)
        break

if target_p:
    target_p.Range.Select()
    word.ActiveWindow.ScrollIntoView(target_p.Range, True)

new_doc.Save()
print("Word reloaded, TOC updated, scrolled to Bab I successfully!")
