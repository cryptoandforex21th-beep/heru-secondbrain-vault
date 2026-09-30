import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

file_path = r'C:\Users\Heru Ardiansyah\Downloads\heru skripsi perancangan solar tube.docx'
doc = docx.Document(file_path)

# Let's find paragraphs
idx_latar = None
idx_rumusan = None
idx_tujuan_sasaran = None
idx_tujuan = None
idx_sasaran = None
idx_batasan = None

for i, p in enumerate(doc.paragraphs):
    t = p.text.strip().upper()
    if t == 'LATAR BELAKANG' and not idx_latar:
        idx_latar = i
    elif t == 'RUMUSAN MASALAH' and not idx_rumusan:
        idx_rumusan = i
    elif t == 'TUJUAN DAN SASARAN PENULISAN' and not idx_tujuan_sasaran:
        idx_tujuan_sasaran = i
    elif t == 'TUJUAN' and idx_tujuan_sasaran and not idx_tujuan:
        idx_tujuan = i
    elif t == 'SASARAN' and idx_tujuan and not idx_sasaran:
        idx_sasaran = i
    elif 'BATASAN PEMBAHASAN DAN LINGKUP' in t and not idx_batasan:
        idx_batasan = i

print(f"Indices: Latar={idx_latar}, Rumusan={idx_rumusan}, TujuanSasaran={idx_tujuan_sasaran}, Tujuan={idx_tujuan}, Sasaran={idx_sasaran}, Batasan={idx_batasan}")

# Helper to remove paragraph from document xml
def delete_paragraph(p):
    p._element.getparent().remove(p._element)

# Helper to set numPr on paragraph
def set_num_pr(p, num_id, ilvl=0):
    pPr = p._p.get_or_add_pPr()
    numPr = pPr.find(qn('w:numPr'))
    if numPr is None:
        numPr = OxmlElement('w:numPr')
        pPr.append(numPr)
    else:
        numPr.clear()
    
    ilvl_el = OxmlElement('w:ilvl')
    ilvl_el.set(qn('w:val'), str(ilvl))
    numPr.append(ilvl_el)
    
    numId_el = OxmlElement('w:numId')
    numId_el.set(qn('w:val'), str(num_id))
    numPr.append(numId_el)

# 1. Update Latar Belakang (paragraphs between idx_latar and idx_rumusan)
# Delete existing body paragraphs between idx_latar and idx_rumusan
body_latar = [doc.paragraphs[k] for k in range(idx_latar + 1, idx_rumusan)]
# Keep first 3, update text, delete remaining
luna_latar_paragraphs = [
    "Kota Makassar, yang berada di kawasan beriklim tropis lembab dengan posisi geografis dekat ekuator, menerima radiasi matahari dengan intensitas tinggi sepanjang tahun. Hal ini menghadirkan tantangan signifikan dalam perancangan bangunan komersial, khususnya tipologi Kantor Sewa (Rental Office). Di satu sisi, bangunan kantor dengan pelat lantai yang dalam (deep floor plan) membutuhkan pasokan pencahayaan alami untuk mengurangi beban energi lampu buatan. Namun di sisi lain, bukaan fasad kaca konvensional sering kali memicu fenomena silau (glare) dan peningkatan beban termal yang drastis di area perimeter bangunan.",
    "Sistem peneduh statis (static shading device) seringkali tidak mampu merespons dinamika pergerakan matahari harian dan musiman. Oleh karena itu, diperlukan intervensi fasad yang lebih responsif. Adaptive Kinetic Facade (Fasad Kinetik Adaptif) menawarkan solusi arsitektural di mana selubung bangunan dapat bertransformasi—membuka, melipat, atau berputar—secara dinamis mengikuti lintasan matahari.",
    "Penelitian ini mengusulkan penerapan Adaptive Kinetic Facade pada bangunan kantor sewa di Makassar. Berbeda dengan pendekatan perancangan konvensional, penelitian ini menggunakan metode Computational Design melalui algoritma parametrik (Rhinoceros & Grasshopper). Fasad kinetik akan dioptimasi kinerjanya menggunakan metrik Climate-Based Daylight Modelling (CBDM), khususnya untuk memaksimalkan Spatial Daylight Autonomy (sDA) dan meminimalkan Annual Sunlight Exposure (ASE) agar tercipta ruang kerja komersial yang terang secara alami namun bebas silau."
]

for idx, text in enumerate(luna_latar_paragraphs):
    body_latar[idx].text = text
    body_latar[idx].style = 'Normal'
    # remove any numPr
    pPr = body_latar[idx]._p.pPr
    if pPr is not None:
        numPr = pPr.find(qn('w:numPr'))
        if numPr is not None: pPr.remove(numPr)

# Delete excess paragraphs in Latar Belakang
for k in range(len(luna_latar_paragraphs), len(body_latar)):
    delete_paragraph(body_latar[k])

# Refresh document paragraph list
doc.save(file_path)
doc = docx.Document(file_path)

# Re-find indices
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip().upper()
    if t == 'RUMUSAN MASALAH': idx_rumusan = i
    elif t == 'TUJUAN DAN SASARAN PENULISAN': idx_tujuan_sasaran = i
    elif t == 'TUJUAN' and idx_tujuan_sasaran and not idx_tujuan: idx_tujuan = i
    elif t == 'SASARAN' and idx_tujuan: idx_sasaran = i
    elif 'BATASAN PEMBAHASAN DAN LINGKUP' in t: idx_batasan = i

# 2. Rumusan Masalah: intro is idx_rumusan + 1
# Items are between idx_rumusan + 2 and idx_tujuan_sasaran
doc.paragraphs[idx_rumusan + 1].text = "Berdasarkan latar belakang di atas, rumusan masalah dalam perancangan ini adalah:"
rumusan_items_p = [doc.paragraphs[k] for k in range(idx_rumusan + 2, idx_tujuan_sasaran)]

luna_rumusan = [
    "Bagaimana merancang Adaptive Kinetic Facade pada bangunan kantor sewa di Makassar yang mampu merespons lintasan matahari tropis secara dinamis?",
    "Bagaimana mengintegrasikan metode Computational Design (desain komputasional) untuk mengoptimasi pergerakan fasad kinetik agar mencapai nilai Spatial Daylight Autonomy (sDA) dan Annual Sunlight Exposure (ASE) yang memenuhi standar kenyamanan visual?",
    "Bagaimana wujud tata ruang dan bentuk arsitektur kantor sewa yang adaptif terhadap integrasi sistem fasad mekanis tersebut?"
]

for idx, text in enumerate(luna_rumusan):
    rumusan_items_p[idx].text = text
    rumusan_items_p[idx].style = 'List Paragraph'
    set_num_pr(rumusan_items_p[idx], num_id=1, ilvl=0)

# Delete excess
for k in range(len(luna_rumusan), len(rumusan_items_p)):
    delete_paragraph(rumusan_items_p[k])

doc.save(file_path)
doc = docx.Document(file_path)

# Re-find indices
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip().upper()
    if t == 'TUJUAN DAN SASARAN PENULISAN': idx_tujuan_sasaran = i
    elif t == 'TUJUAN' and idx_tujuan_sasaran and not idx_tujuan: idx_tujuan = i
    elif t == 'SASARAN' and idx_tujuan: idx_sasaran = i
    elif 'BATASAN PEMBAHASAN DAN LINGKUP' in t: idx_batasan = i

# 3. Tujuan: intro is idx_tujuan + 1
doc.paragraphs[idx_tujuan + 1].text = "Adapun tujuan dari penulisan tugas akhir ini yakni sebagai berikut:"
tujuan_items_p = [doc.paragraphs[k] for k in range(idx_tujuan + 2, idx_sasaran)]

luna_tujuan = [
    "Menghasilkan rancangan bangunan kantor sewa di Makassar yang mengaplikasikan teknologi Adaptive Kinetic Facade.",
    "Membuktikan secara komputasional bahwa pergerakan fasad kinetik yang dirancang mampu meningkatkan penetrasi cahaya alami yang berguna (sDA) sekaligus mereduksi silau berlebih (ASE)."
]

for idx, text in enumerate(luna_tujuan):
    tujuan_items_p[idx].text = text
    tujuan_items_p[idx].style = 'List Paragraph'
    set_num_pr(tujuan_items_p[idx], num_id=2, ilvl=0)

for k in range(len(luna_tujuan), len(tujuan_items_p)):
    delete_paragraph(tujuan_items_p[k])

doc.save(file_path)

print("Docx file on disk successfully updated with exact original numId=1 and numId=2!")
