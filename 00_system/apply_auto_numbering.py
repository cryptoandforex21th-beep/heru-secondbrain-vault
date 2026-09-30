import win32com.client
import sys

def apply_auto_numbering():
    word = win32com.client.GetObject(Class='Word.Application')
    doc = None
    for d in word.Documents:
        if 'heru skripsi' in d.Name.lower():
            doc = d
            break
            
    if not doc:
        print("Doc not found")
        return

    # Find the reference list paragraph from Batasan Pembahasan (around 144)
    ref_para = None
    for i in range(135, 155):
        p = doc.Paragraphs(i)
        if p.Range.ListFormat.ListType != 0 and p.Range.ListFormat.ListString.startswith("1"):
            ref_para = p
            print(f"Reference list paragraph found at {i}: {p.Range.Text[:40]}")
            break

    # Find Rumusan Masalah items
    idx_rumusan = None
    idx_tujuan = None
    for i in range(125, 140):
        t = doc.Paragraphs(i).Range.Text.strip().upper()
        if "RUMUSAN MASALAH" in t and not idx_rumusan:
            idx_rumusan = i
        elif "TUJUAN DAN SASARAN" in t and not idx_tujuan:
            idx_tujuan = i

    print(f"Rumusan Masalah heading at {idx_rumusan}, Tujuan heading at {idx_tujuan}")

    # In Rumusan Masalah:
    # idx_rumusan is heading 'Rumusan Masalah'
    # idx_rumusan + 1 is intro 'Berdasarkan latar belakang...'
    # idx_rumusan + 2, 3, 4 are the 3 questions
    rumusan_items = [
        "Bagaimana merancang Adaptive Kinetic Facade pada bangunan kantor sewa di Makassar yang mampu merespons lintasan matahari tropis secara dinamis?\r",
        "Bagaimana mengintegrasikan metode Computational Design (desain komputasional) untuk mengoptimasi pergerakan fasad kinetik agar mencapai nilai Spatial Daylight Autonomy (sDA) dan Annual Sunlight Exposure (ASE) yang memenuhi standar kenyamanan visual?\r",
        "Bagaimana wujud tata ruang dan bentuk arsitektur kantor sewa yang adaptif terhadap integrasi sistem fasad mekanis tersebut?\r"
    ]

    for offset, clean_text in enumerate(rumusan_items):
        p = doc.Paragraphs(idx_rumusan + 2 + offset)
        p.Range.Text = clean_text
        p.Style = doc.Styles("List Paragraph")
        p.Range.Font.Name = "Arial"
        p.Range.Font.Size = 10.0
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0
        p.Format.Alignment = 3 # Justify
        p.Format.SpaceBefore = 0.0
        p.Format.SpaceAfter = 4.0
        p.Format.LineSpacing = 12.0
        if ref_para:
            p.Range.ListFormat.ApplyListTemplateWithLevel(
                ListTemplate=ref_para.Range.ListFormat.ListTemplate,
                ContinuePreviousList=False if offset == 0 else True,
                ApplyTo=1 # wdListApplyToWholeList
            )
        else:
            p.Range.ListFormat.ApplyNumberDefault()

    # In Tujuan:
    # Find heading 'Tujuan' under 'Tujuan dan Sasaran Penulisan'
    idx_sub_tujuan = None
    for i in range(idx_tujuan, idx_tujuan + 6):
        if doc.Paragraphs(i).Range.Text.strip().upper() == "TUJUAN":
            idx_sub_tujuan = i
            break

    print(f"Sub-heading 'Tujuan' found at {idx_sub_tujuan}")

    tujuan_items = [
        "Menghasilkan rancangan bangunan kantor sewa di Makassar yang mengaplikasikan teknologi Adaptive Kinetic Facade.\r",
        "Membuktikan secara komputasional bahwa pergerakan fasad kinetik yang dirancang mampu meningkatkan penetrasi cahaya alami yang berguna (sDA) sekaligus mereduksi silau berlebih (ASE).\r"
    ]

    for offset, clean_text in enumerate(tujuan_items):
        p = doc.Paragraphs(idx_sub_tujuan + 1 + offset)
        p.Range.Text = clean_text
        p.Style = doc.Styles("List Paragraph")
        p.Range.Font.Name = "Arial"
        p.Range.Font.Size = 10.0
        p.Format.LeftIndent = 36.0
        p.Format.FirstLineIndent = -18.0
        p.Format.Alignment = 3 # Justify
        p.Format.SpaceBefore = 0.0
        p.Format.SpaceAfter = 4.0
        p.Format.LineSpacing = 12.0
        if ref_para:
            p.Range.ListFormat.ApplyListTemplateWithLevel(
                ListTemplate=ref_para.Range.ListFormat.ListTemplate,
                ContinuePreviousList=False if offset == 0 else True,
                ApplyTo=1
            )
        else:
            p.Range.ListFormat.ApplyNumberDefault()

    # Save
    doc.Save()
    print("Auto-numbering applied and saved!")

    # Check results
    with open(r"d:\SecondBrain\00_system\auto_numbering_result.txt", "w", encoding="utf-8") as out:
        out.write("--- RUMUSAN MASALAH ITEMS ---\n")
        for k in range(idx_rumusan + 1, idx_rumusan + 5):
            pk = doc.Paragraphs(k)
            out.write(f"[{k}] ListString={repr(pk.Range.ListFormat.ListString)} LeftIndent={pk.Format.LeftIndent} Text={repr(pk.Range.Text[:60])}\n")

        out.write("\n--- TUJUAN ITEMS ---\n")
        for k in range(idx_sub_tujuan, idx_sub_tujuan + 3):
            pk = doc.Paragraphs(k)
            out.write(f"[{k}] ListString={repr(pk.Range.ListFormat.ListString)} LeftIndent={pk.Format.LeftIndent} Text={repr(pk.Range.Text[:60])}\n")

        out.write("\n--- BATASAN ITEMS ---\n")
        for k in range(idx_sub_tujuan + 3, min(idx_sub_tujuan + 12, doc.Paragraphs.Count + 1)):
            pk = doc.Paragraphs(k)
            if pk.Range.ListFormat.ListString:
                out.write(f"[{k}] ListString={repr(pk.Range.ListFormat.ListString)} LeftIndent={pk.Format.LeftIndent} Text={repr(pk.Range.Text[:60])}\n")

if __name__ == '__main__':
    apply_auto_numbering()
