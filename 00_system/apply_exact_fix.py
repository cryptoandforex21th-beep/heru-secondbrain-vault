import win32com.client
import sys

def apply_exact_fix():
    word = win32com.client.GetObject(Class='Word.Application')
    doc = None
    for d in word.Documents:
        if 'heru skripsi' in d.Name.lower():
            doc = d
            break
            
    if not doc:
        print("Doc not found")
        return

    # Find where Bab I starts (Heading 2: PENDAHULUAN)
    idx_pendahuluan = None
    idx_batasan = None

    for i in range(120, 150):
        t = doc.Paragraphs(i).Range.Text.strip().upper()
        if "PENDAHULUAN" in t and not idx_pendahuluan:
            idx_pendahuluan = i
        elif "BATASAN PEMBAHASAN DAN LINGKUP" in t and not idx_batasan:
            idx_batasan = i

    print(f"PENDAHULUAN at {idx_pendahuluan}, BATASAN at {idx_batasan}")

    # The region to replace is from right after PENDAHULUAN (i.e. idx_pendahuluan + 1)
    # up to the start of BATASAN (idx_batasan)
    start_pos = doc.Paragraphs(idx_pendahuluan + 1).Range.Start
    end_pos = doc.Paragraphs(idx_batasan).Range.Start

    rng = doc.Range(Start=start_pos, End=end_pos)

    # Let's define the exact structure
    # tuple: (style_name, text, space_before, space_after, first_indent, left_indent)
    elements = [
        # 1.1 Latar Belakang Header (Word will auto-number as 1.1)
        ("Heading 3", "Latar Belakang\r", 18.0, 12.0, 0.0, 0.0),
        
        # 3 Body Paragraphs (Normal style, indent 21.3 pt, justified)
        ("Normal", "Kota Makassar, yang berada di kawasan beriklim tropis lembab dengan posisi geografis dekat ekuator, menerima radiasi matahari dengan intensitas tinggi sepanjang tahun. Hal ini menghadirkan tantangan signifikan dalam perancangan bangunan komersial, khususnya tipologi Kantor Sewa (Rental Office). Di satu sisi, bangunan kantor dengan pelat lantai yang dalam (deep floor plan) membutuhkan pasokan pencahayaan alami untuk mengurangi beban energi lampu buatan. Namun di sisi lain, bukaan fasad kaca konvensional sering kali memicu fenomena silau (glare) dan peningkatan beban termal yang drastis di area perimeter bangunan.\r", 0.0, 8.0, 21.3, 0.0),
        
        ("Normal", "Sistem peneduh statis (static shading device) seringkali tidak mampu merespons dinamika pergerakan matahari harian dan musiman. Oleh karena itu, diperlukan intervensi fasad yang lebih responsif. Adaptive Kinetic Facade (Fasad Kinetik Adaptif) menawarkan solusi arsitektural di mana selubung bangunan dapat bertransformasi—membuka, melipat, atau berputar—secara dinamis mengikuti lintasan matahari.\r", 0.0, 8.0, 21.3, 0.0),
        
        ("Normal", "Penelitian ini mengusulkan penerapan Adaptive Kinetic Facade pada bangunan kantor sewa di Makassar. Berbeda dengan pendekatan perancangan konvensional, penelitian ini menggunakan metode Computational Design melalui algoritma parametrik (Rhinoceros & Grasshopper). Fasad kinetik akan dioptimasi kinerjanya menggunakan metrik Climate-Based Daylight Modelling (CBDM), khususnya untuk memaksimalkan Spatial Daylight Autonomy (sDA) dan meminimalkan Annual Sunlight Exposure (ASE) agar tercipta ruang kerja komersial yang terang secara alami namun bebas silau.\r", 0.0, 8.0, 21.3, 0.0),
        
        # 1.2 Rumusan Masalah Header (Word will auto-number as 1.2)
        ("Heading 3", "Rumusan Masalah\r", 18.0, 12.0, 0.0, 0.0),
        
        # Intro text (Normal style)
        ("Normal", "Berdasarkan latar belakang di atas, rumusan masalah dalam perancangan ini adalah:\r", 0.0, 6.0, 21.3, 0.0),
        
        # 3 items under Rumusan Masalah (List Paragraph)
        ("List Paragraph", "1. Bagaimana merancang Adaptive Kinetic Facade pada bangunan kantor sewa di Makassar yang mampu merespons lintasan matahari tropis secara dinamis?\r", 0.0, 4.0, -18.0, 18.0),
        ("List Paragraph", "2. Bagaimana mengintegrasikan metode Computational Design (desain komputasional) untuk mengoptimasi pergerakan fasad kinetik agar mencapai nilai Spatial Daylight Autonomy (sDA) dan Annual Sunlight Exposure (ASE) yang memenuhi standar kenyamanan visual?\r", 0.0, 4.0, -18.0, 18.0),
        ("List Paragraph", "3. Bagaimana wujud tata ruang dan bentuk arsitektur kantor sewa yang adaptif terhadap integrasi sistem fasad mekanis tersebut?\r", 0.0, 6.0, -18.0, 18.0),
        
        # 1.3 Tujuan dan Sasaran Penulisan Header (Word will auto-number as 1.3)
        ("Heading 3", "Tujuan dan Sasaran Penulisan\r", 18.0, 12.0, 0.0, 0.0),
        
        # Intro text
        ("Normal", "Adapun tujuan dan sasaran dari penulisan tugas akhir ini yakni sebagai berikut:\r", 0.0, 6.0, 21.3, 0.0),
        
        # Subheader 1.3.1 Tujuan (Heading 4)
        ("Heading 4", "Tujuan\r", 12.0, 6.0, 0.0, 0.0),
        
        # 2 items under Tujuan (List Paragraph)
        ("List Paragraph", "1. Menghasilkan rancangan bangunan kantor sewa di Makassar yang mengaplikasikan teknologi Adaptive Kinetic Facade.\r", 0.0, 4.0, -18.0, 18.0),
        ("List Paragraph", "2. Membuktikan secara komputasional bahwa pergerakan fasad kinetik yang dirancang mampu meningkatkan penetrasi cahaya alami yang berguna (sDA) sekaligus mereduksi silau berlebih (ASE).\r", 0.0, 6.0, -18.0, 18.0),
        
        # Subheader 1.3.2 Sasaran (Heading 4)
        ("Heading 4", "Sasaran\r", 12.0, 6.0, 0.0, 0.0),
        
        # Sasaran text (List Paragraph)
        ("List Paragraph", "Sasaran penelitian dan perancangan ini adalah menghasilkan konsep rancangan bangunan kantor sewa di Makassar yang mengintegrasikan sistem Adaptive Kinetic Facade secara fungsional dan estetis, dengan fokus pada optimalisasi pencahayaan alami dan kenyamanan visual ruang kerja.\r", 0.0, 8.0, 0.0, 0.0)
    ]

    # Combine text
    combined_text = "".join([el[1] for el in elements])
    rng.Text = combined_text

    # Now apply formatting to each paragraph
    cur_p = idx_pendahuluan + 1
    for style_name, text, sb, sa, fli, li in elements:
        p = doc.Paragraphs(cur_p)
        try:
            p.Style = doc.Styles(style_name)
        except Exception as e:
            print(f"Style error for {style_name}: {e}")
        p.Range.Font.Name = "Arial"
        p.Range.Font.Size = 10.0
        p.Format.SpaceBefore = sb
        p.Format.SpaceAfter = sa
        p.Format.LineSpacing = 12.0
        p.Format.Alignment = 3 # Justify
        if fli != 0.0:
            p.Format.FirstLineIndent = fli
        if li != 0.0:
            p.Format.LeftIndent = li
        cur_p += 1

    # Scroll into view
    doc.Paragraphs(idx_pendahuluan + 1).Range.Select()
    word.ActiveWindow.ScrollIntoView(doc.Paragraphs(idx_pendahuluan + 1).Range, True)

    doc.Save()
    print("Exact fix applied and saved successfully!")

    with open(r"d:\SecondBrain\00_system\exact_fix_result.txt", "w", encoding="utf-8") as f:
        f.write("Success! Paragraphs updated.\n")
        for k in range(idx_pendahuluan, cur_p + 3):
            pk = doc.Paragraphs(k)
            f.write(f"[{k}] Style={pk.Style.NameLocal} List={pk.Range.ListFormat.ListString} Text={repr(pk.Range.Text.strip()[:60])}\n")

if __name__ == '__main__':
    apply_exact_fix()
