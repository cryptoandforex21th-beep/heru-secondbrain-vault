import win32com.client
import sys
import traceback

log_file = r"d:\SecondBrain\00_system\word_update_result.log"

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

try:
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("Starting Word Update...\n")

    word = win32com.client.GetObject(Class='Word.Application')
    doc = None
    for d in word.Documents:
        if 'heru skripsi' in d.Name.lower():
            doc = d
            break
            
    if not doc:
        log("ERROR: Document 'heru skripsi' not found in Word.")
        sys.exit(1)

    log(f"Connected to document: {doc.Name}")
    log(f"Initial Paragraph Count: {doc.Paragraphs.Count}")

    # Verify Prof Luna's message exists at the bottom
    last_text = doc.Paragraphs(doc.Paragraphs.Count).Range.Text.strip()
    log(f"Last Paragraph snippet: {repr(last_text[:60])}")
    if "PROF LUNA" not in last_text.upper():
        # Check previous 3 paragraphs
        found_luna = False
        for k in range(doc.Paragraphs.Count, max(1, doc.Paragraphs.Count - 5), -1):
            if "PROF LUNA" in doc.Paragraphs(k).Range.Text.upper():
                found_luna = True
                log(f"Found Prof Luna message at paragraph {k}")
                break
        if not found_luna:
            log("WARNING: Prof Luna message not found near end!")
    else:
        log("Prof Luna message verified at document end.")

    # 1. Locate Bab I bounds: Latar Belakang to Batasan
    idx_latar = None
    idx_batasan = None
    idx_pustaka = None
    idx_logbook = None

    for i in range(1, doc.Paragraphs.Count + 1):
        t = doc.Paragraphs(i).Range.Text.strip()
        u = t.upper()
        if i >= 120 and i <= 130 and "LATAR BELAKANG" in u and not idx_latar:
            idx_latar = i
        elif i >= 135 and i <= 155 and "BATASAN" in u and not idx_batasan:
            idx_batasan = i
        elif i >= 350 and "DAFTAR PUSTAKA" in u and not idx_pustaka:
            idx_pustaka = i
        elif i >= 390 and "LOGBOOK PENELITIAN" in u and not idx_logbook:
            idx_logbook = i

    log(f"Detected indices: Latar={idx_latar}, Batasan={idx_batasan}, Pustaka={idx_pustaka}, Logbook={idx_logbook}")

    if not idx_latar or not idx_batasan:
        log("ERROR: Could not safely find Bab I boundaries.")
        sys.exit(1)

    # Content to insert into Bab I
    bab1_elements = [
        ("h", "1.1 Latar Belakang"),
        ("p", "Kota Makassar, yang berada di kawasan beriklim tropis lembab dengan posisi geografis dekat ekuator, menerima radiasi matahari dengan intensitas tinggi sepanjang tahun. Hal ini menghadirkan tantangan signifikan dalam perancangan bangunan komersial, khususnya tipologi Kantor Sewa (Rental Office). Di satu sisi, bangunan kantor dengan pelat lantai yang dalam (deep floor plan) membutuhkan pasokan pencahayaan alami untuk mengurangi beban energi lampu buatan. Namun di sisi lain, bukaan fasad kaca konvensional sering kali memicu fenomena silau (glare) dan peningkatan beban termal yang drastis di area perimeter bangunan."),
        ("p", "Sistem peneduh statis (static shading device) seringkali tidak mampu merespons dinamika pergerakan matahari harian dan musiman. Oleh karena itu, diperlukan intervensi fasad yang lebih responsif. Adaptive Kinetic Facade (Fasad Kinetik Adaptif) menawarkan solusi arsitektural di mana selubung bangunan dapat bertransformasi—membuka, melipat, atau berputar—secara dinamis mengikuti lintasan matahari."),
        ("p", "Penelitian ini mengusulkan penerapan Adaptive Kinetic Facade pada bangunan kantor sewa di Makassar. Berbeda dengan pendekatan perancangan konvensional, penelitian ini menggunakan metode Computational Design melalui algoritma parametrik (Rhinoceros & Grasshopper). Fasad kinetik akan dioptimasi kinerjanya menggunakan metrik Climate-Based Daylight Modelling (CBDM), khususnya untuk memaksimalkan Spatial Daylight Autonomy (sDA) dan meminimalkan Annual Sunlight Exposure (ASE) agar tercipta ruang kerja komersial yang terang secara alami namun bebas silau."),
        ("h", "1.2 Rumusan Masalah"),
        ("p", "Berdasarkan latar belakang di atas, rumusan masalah dalam perancangan ini adalah:"),
        ("l", "1. Bagaimana merancang Adaptive Kinetic Facade pada bangunan kantor sewa di Makassar yang mampu merespons lintasan matahari tropis secara dinamis?"),
        ("l", "2. Bagaimana mengintegrasikan metode Computational Design (desain komputasional) untuk mengoptimasi pergerakan fasad kinetik agar mencapai nilai Spatial Daylight Autonomy (sDA) dan Annual Sunlight Exposure (ASE) yang memenuhi standar kenyamanan visual?"),
        ("l", "3. Bagaimana wujud tata ruang dan bentuk arsitektur kantor sewa yang adaptif terhadap integrasi sistem fasad mekanis tersebut?"),
        ("h", "1.3 Tujuan Perancangan"),
        ("p", "Adapun tujuan perancangan ini yakni sebagai berikut:"),
        ("l", "1. Menghasilkan rancangan bangunan kantor sewa di Makassar yang mengaplikasikan teknologi Adaptive Kinetic Facade."),
        ("l", "2. Membuktikan secara komputasional bahwa pergerakan fasad kinetik yang dirancang mampu meningkatkan penetrasi cahaya alami yang berguna (sDA) sekaligus mereduksi silau berlebih (ASE).")
    ]

    # Replace section range: from start of idx_latar to start of idx_batasan
    rng_bab1 = doc.Range(Start=doc.Paragraphs(idx_latar).Range.Start, End=doc.Paragraphs(idx_batasan).Range.Start)
    
    # We will construct the formatted text string
    full_text = "\n".join([item[1] for item in bab1_elements]) + "\n"
    rng_bab1.Text = full_text

    # Re-apply exact formatting to the newly inserted paragraphs
    cur_p = idx_latar
    for kind, text in bab1_elements:
        p = doc.Paragraphs(cur_p)
        p.Range.Font.Name = "Arial"
        if kind == "h":
            p.Range.Font.Size = 10.0
            p.Range.Font.Bold = True
            p.Format.Alignment = 3 # Justify
            p.Format.SpaceBefore = 18.0
            p.Format.SpaceAfter = 12.0
            p.Format.LineSpacing = 12.0
            p.Format.FirstLineIndent = 0.0
        elif kind == "p":
            p.Range.Font.Size = 10.0
            p.Range.Font.Bold = False
            p.Format.Alignment = 3 # Justify
            p.Format.SpaceBefore = 0.0
            p.Format.SpaceAfter = 8.0
            p.Format.LineSpacing = 12.95
            p.Format.FirstLineIndent = 21.3
        elif kind == "l":
            p.Range.Font.Size = 10.0
            p.Range.Font.Bold = False
            p.Format.Alignment = 3 # Justify
            p.Format.SpaceBefore = 0.0
            p.Format.SpaceAfter = 4.0
            p.Format.LineSpacing = 13.0
            p.Format.FirstLineIndent = 0.0
        cur_p += 1

    log("Successfully replaced Bab I content with Luna's text and formatted.")

    # 2. Add the 4 journals into DAFTAR PUSTAKA
    # Find DAFTAR PUSTAKA index again
    new_idx_pustaka = None
    new_idx_logbook = None
    for i in range(1, doc.Paragraphs.Count + 1):
        u = doc.Paragraphs(i).Range.Text.strip().upper()
        if "DAFTAR PUSTAKA" in u and not new_idx_pustaka:
            new_idx_pustaka = i
        elif "LOGBOOK PENELITIAN" in u and not new_idx_logbook:
            new_idx_logbook = i

    log(f"Refreshed indices: Pustaka={new_idx_pustaka}, Logbook={new_idx_logbook}")

    journals = [
        "Al-Masrani, S. M., Al-Obaidi, K. M., Zalin, N. A., & Isma, M. I. (2018). Design optimisation of solar shading systems for tropical office buildings: Challenges and future trends. Solar Energy, 170, 849-872.",
        "Eltaweel, A., & Su, Y. (2017). Parametric design and daylighting: A literature review. Renewable and Sustainable Energy Reviews, 73, 1086-1103.",
        "Reinhart, C. F. (2014). Daylighting Handbook I: Fundamentals, Designing with the Sun.",
        "Tabadkani, A., Roetzel, A., Li, H. X., & Tsangrassoulis, A. (2020). Design of adaptive shading patterns for visual comfort and energy efficiency. Automation in Construction, 112, 103096."
    ]

    # Insert right after DAFTAR PUSTAKA heading
    target_p_insert = new_idx_pustaka + 1
    for j in reversed(journals):
        # Insert a paragraph after DAFTAR PUSTAKA
        r = doc.Paragraphs(new_idx_pustaka).Range
        r.Collapse(0) # Collapse to end of heading paragraph
        # Insert after heading
        new_para = doc.Paragraphs.Add(r)
        new_para.Range.Text = j
        new_para.Range.Font.Name = "Arial"
        new_para.Range.Font.Size = 10.0
        new_para.Range.Font.Bold = False
        new_para.Format.Alignment = 3
        new_para.Format.SpaceBefore = 0.0
        new_para.Format.SpaceAfter = 6.0
        new_para.Format.LineSpacing = 12.0
        new_para.Format.FirstLineIndent = -18.0
        new_para.Format.LeftIndent = 18.0

    log("Successfully inserted 4 journal citations into DAFTAR PUSTAKA.")

    # 3. Final verification of Prof Luna's message
    last_p = doc.Paragraphs(doc.Paragraphs.Count)
    log(f"Final paragraph {doc.Paragraphs.Count}: {repr(last_p.Range.Text.strip()[:80])}")
    
    # Save the document!
    doc.Save()
    log("Document saved successfully!")

except Exception as e:
    log(f"ERROR: {e}\n{traceback.format_exc()}")
