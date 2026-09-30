import win32com.client
import sys

def run():
    word = win32com.client.GetObject(Class='Word.Application')
    doc = None
    for d in word.Documents:
        if 'heru skripsi' in d.Name.lower():
            doc = d
            break
            
    if not doc:
        print("Doc not found")
        return

    # 1. Update Section 6 (BAB I PENDAHULUAN)
    s6 = doc.Sections(6)
    for h in [s6.Headers(1), s6.Headers(2), s6.Headers(3)]:
        try:
            h.PageNumbers.RestartNumberingAtSection = True
            h.PageNumbers.StartingNumber = 1
            h.PageNumbers.NumberStyle = 0 # wdPageNumberStyleArabic
        except Exception as e:
            print("Header err:", e)

    for f in [s6.Footers(1), s6.Footers(2), s6.Footers(3)]:
        try:
            f.PageNumbers.RestartNumberingAtSection = True
            f.PageNumbers.StartingNumber = 1
            f.PageNumbers.NumberStyle = 0 # wdPageNumberStyleArabic
        except Exception as e:
            print("Footer err:", e)

    # 2. Update Section 7 (LOGBOOK PENELITIAN) to continue numbering
    if doc.Sections.Count >= 7:
        s7 = doc.Sections(7)
        for h in [s7.Headers(1), s7.Headers(2)]:
            try:
                h.PageNumbers.RestartNumberingAtSection = False
            except:
                pass
        for f in [s7.Footers(1), s7.Footers(2)]:
            try:
                f.PageNumbers.RestartNumberingAtSection = False
            except:
                pass

    # 3. Update Table of Contents
    try:
        for toc in doc.TablesOfContents:
            toc.UpdatePageNumbers()
    except Exception as e:
        print("TOC update err:", e)

    # 4. Check Bab I page number
    # Paragraph 124 is 1.1 Latar Belakang
    p_babi = doc.Sections(6).Range.Paragraphs(1)
    page_num = p_babi.Range.Information(1) # wdActiveEndPageNumber

    # 5. Check first 10 paragraphs of TOC in Section 3
    s3 = doc.Sections(3)
    toc_lines = []
    for i in range(1, min(18, s3.Range.Paragraphs.Count + 1)):
        toc_lines.append(s3.Range.Paragraphs(i).Range.Text.strip())

    # Save
    doc.Save()
    print("Page number reset to 1 and document saved!")

    with open(r"d:\SecondBrain\00_system\page_number_result.txt", "w", encoding="utf-8") as out:
        out.write(f"Section 6 starting page in Information(1): {page_num}\n\n")
        out.write("--- TOC PREVIEW ---\n")
        for line in toc_lines:
            out.write(line + "\n")

if __name__ == '__main__':
    run()
