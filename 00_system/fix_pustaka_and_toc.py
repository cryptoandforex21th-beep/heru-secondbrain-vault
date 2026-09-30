import win32com.client
import sys

def fix():
    word = win32com.client.GetObject(Class='Word.Application')
    doc = None
    for d in word.Documents:
        if 'heru skripsi' in d.Name.lower():
            doc = d
            break
            
    if not doc:
        print("Doc not found")
        return

    # 1. Restore paragraph 103 in DAFTAR ISI
    p103 = doc.Paragraphs(103)
    p103.Range.Text = "LOGBOOK PENELITIAN\t114\r"
    p103.Range.Font.Name = "Arial"
    p103.Range.Font.Size = 10.0
    p103.Range.Font.Bold = False
    p103.Format.Alignment = 0 # Left
    p103.Format.SpaceBefore = 0.0
    p103.Format.SpaceAfter = 0.0
    p103.Format.FirstLineIndent = 0.0
    p103.Format.LeftIndent = 0.0

    # 2. Find the real DAFTAR PUSTAKA in the body (after paragraph 300)
    real_pustaka_idx = None
    for i in range(300, doc.Paragraphs.Count + 1):
        t = doc.Paragraphs(i).Range.Text.strip().upper()
        if t == "DAFTAR PUSTAKA":
            real_pustaka_idx = i
            break

    if not real_pustaka_idx:
        print("Real DAFTAR PUSTAKA not found!")
        return

    print(f"Real DAFTAR PUSTAKA found at index {real_pustaka_idx}")

    journals = [
        "Al-Masrani, S. M., Al-Obaidi, K. M., Zalin, N. A., & Isma, M. I. (2018). Design optimisation of solar shading systems for tropical office buildings: Challenges and future trends. Solar Energy, 170, 849-872.",
        "Eltaweel, A., & Su, Y. (2017). Parametric design and daylighting: A literature review. Renewable and Sustainable Energy Reviews, 73, 1086-1103.",
        "Reinhart, C. F. (2014). Daylighting Handbook I: Fundamentals, Designing with the Sun.",
        "Tabadkani, A., Roetzel, A., Li, H. X., & Tsangrassoulis, A. (2020). Design of adaptive shading patterns for visual comfort and energy efficiency. Automation in Construction, 112, 103096."
    ]

    # Insert after real DAFTAR PUSTAKA
    for j in reversed(journals):
        r = doc.Paragraphs(real_pustaka_idx).Range
        r.Collapse(0) # End of heading paragraph
        # Insert paragraph
        r.InsertParagraphAfter()
        # The new paragraph is at real_pustaka_idx + 1
        p_new = doc.Paragraphs(real_pustaka_idx + 1)
        p_new.Range.Text = j + "\r"
        p_new.Range.Font.Name = "Arial"
        p_new.Range.Font.Size = 10.0
        p_new.Range.Font.Bold = False
        p_new.Range.Font.Italic = False
        p_new.Format.Alignment = 3 # Justify
        p_new.Format.SpaceBefore = 0.0
        p_new.Format.SpaceAfter = 6.0
        p_new.Format.LineSpacing = 12.0
        p_new.Format.FirstLineIndent = -18.0
        p_new.Format.LeftIndent = 18.0

    # Verify Prof Luna's message at the end
    last_text = doc.Paragraphs(doc.Paragraphs.Count).Range.Text.strip()
    print("Final last paragraph:", repr(last_text[:60]))

    doc.Save()
    print("Fixed and saved successfully!")

    with open(r"d:\SecondBrain\00_system\fix_result.txt", "w", encoding="utf-8") as f:
        f.write("Fixed successfully! Last par: " + last_text[:60] + "\n")

if __name__ == '__main__':
    fix()
