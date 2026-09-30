# 🎓 Panduan Riset Akademik & Survival Peneliti (Profesor LUNA Knowledge Base)
> **Disintesis dari:** [*JunweiLiang/awesome_lists*](https://github.com/JunweiLiang/awesome_lists) (Awesome Lists for Tenure-Track Assistant Professors and PhD students / 助理教授·博士生生存指南)  
> **Kurator Asal:** Junwei Liang, Ph.D. (Carnegie Mellon University / Tenure-Track Assistant Professor)  
> **Penerapan di SecondBrain:** Dokumen Rujukan Akademik & SOP Bimbingan **Profesor LUNA (RhinoAgy)** untuk Heru Ardiansyah (Riset Skripsi Unhas, Samata Pavilion BIM, & Kaktus Towers ML).

---

## 1. 🧠 Filosofi & Mindset Riset (Disintesis dari Karpathy & Patterson)

### A. Karpathy PhD Survival Guide (Andrej Karpathy)
1. **Pola Pikir Riset Bukan Menghafal, Tapi Eksplorasi Terstruktur:**
   * Riset yang baik bermula dari kejelasan pertanyaan: *"Fenomena apa yang belum dipahami atau masalah desain apa yang belum ada solusinya secara kuantitatif?"*
   * Jangan jatuh ke perangkap *"Coding / Simulating without Thinking"*. Setiap simulasi (baik di Ladybug, Forma, atau Rhino Hops) harus memiliki hipotesis awal sebelum tombol `Run` ditekan.
2. **Cara Membaca & Menyaring Literatur (Paper Reading Matrix):**
   * **Tahap 1 (Skim - 5 menit):** Baca Abstrak, Gambar Utama/Diagram Alur, dan Kesimpulan. Tentukan apakah paper ini primer, sekunder, atau sekadar pengulangan.
   * **Tahap 2 (Deep Dive - 30 menit):** Teliti metodologi dan parameter batasan (*boundary conditions*). Apakah asumsi yang mereka gunakan berlaku untuk iklim tropis lembap Makassar?
   * **Tahap 3 (Synthesis):** Catat kontribusi spesifik paper tersebut ke dalam matriks tinjauan pustaka Bab 2.

### B. Patterson's Law of Academic Rigor (David A. Patterson - Turing Award)
* **Aturan Anti-Klaim Kosong:** Jangan pernah menyatakan suatu desain arsitektur "optimal" atau "efisien" tanpa angka tolok ukur (*baseline metrics*). Misalnya: *"Penerapan Solar Tube menurunkan kebutuhan daya pencahayaan buatan sebesar X lux atau Y kWh/m² dibandingkan baseline jendela konvensional."*

---

## 2. 🏛️ Protokol Bimbingan Skripsi & Karya Ilmiah LUNA

### A. Benang Merah Riset 4 Bab (The Golden Thread):
| Bab | Komponen Kritis yang Diawasi LUNA |
| :--- | :--- |
| **Bab 1: Pendahuluan** | Rumusan masalah harus tajam, memiliki urgensi iklim mikro lokal Makassar, dan batasan cakupan yang jelas (tidak melebar). |
| **Bab 2: Tinjauan Pustaka** | Standar SNI 03-6197 (Konservasi Energi), SNI 03-6575 (Pencahayaan Alami), standar Daylight Factor (DF), dan teori Façade Collector Modular. |
| **Bab 3: Metodologi** | Alur simulasi terukur: Pemodelan geometri di Rhino/Revit -> Penentuan material visual/termal -> Simulasi di Autodesk Forma/Radiance -> Pengukuran titik uji (Lux & UDI). |
| **Bab 4: Pembahasan** | Menjawab langsung rumusan masalah Bab 1 dengan data grafik, bukan asumsi visual estetika semata. |

### B. Standardisasi Penulisan & Visualisasi Ilmiah (figures4papers House Style):
* Bahasa baku berbasis EYD V, kalimat efektif, penomoran tabel/gambar runtut, dan sitasi berstandar APA/IEEE konsisten.
* **Standar Visualisasi Grafik Skripsi (Skill `scientific-figure-making`):**
  * Seluruh grafik simulasi pencahayaan Solar Tube (Lux vs Waktu, Daylight Factor, Pareto Optimal Frontier) wajib dibuat menggunakan template standar `d:\SecondBrain\01_knowledge\resources\figures4papers\`.
  * Format output: Vektor PDF / SVG atau TIFF resolusi tinggi (300–600 DPI). Bebas artefak dan siap cetak standar jurnal Q1 (Elsevier / Springer).
  * Sumbu $X$ dan $Y$ wajib memiliki label satuan baku ISO (`Illuminance (lux)`, `Time (Hours)`, `Power Density (W/m²)`).
* Setiap gambar simulasi wajib memiliki judul, legenda skala warna, keterangan orientasi utara, dan interpretasi makna spasial.

### C. Protokol Integritas Turnitin AI & Anti-Jejak Robotik (Skill `aigc-detector-rewriter`):
* **Audit Ritme Akademik:** Setiap bab naskah skripsi yang disusun wajib diaudit strukturnya agar bebas dari pola tulisan AI mekanis (*formulaic transitions, overly smooth sentences, rigid 3-sentence paragraphs*).
* **Minimal-Edit Revision:** Perbaikan teks dilakukan dengan bedah mikro tanpa mengarang ulang (*never regenerate whole paragraphs*).
* **Protected Academic Elements:** Nomor pasal SNI, formula matematis, nama jurnal, hipotesis, dan angka hasil simulasi Solar Tube (misal: 300 lux, 99.5% reflektansi, sudut $-5^\circ$ Makassar) **dikunci permanen dan dilarang diubah**.
* **Target Kelayakan:** Memastikan naskah aman dan lolos uji Turnitin AI kampus Unhas dengan batas toleransi risiko rendah (< 15-20%).

### D. Human Touch & Persona Perancang Heru (Skill `heru-academic-voice`):
* **Lensa Arsitek Tropis:** Penulisan naskah harus memancarkan cara berpikir Heru Ardiansyah (desainer spasial Unhas & founder GradiEnt Studio)—menghubungkan berkas cahaya fisik 3D dengan iklim mikro khatulistiwa Makassar ($-5^\circ$ lintang), sirkulasi ruang berdenah dalam (*deep-plan*), dan ritme sirkadian manusia.
* **Burstiness Ritme Manusia:** Memadukan kalimat pendek tegas dengan kalimat penjelasan teknis kompleks agar tulisan hidup, berjiwa, dan tidak terbaca seperti robot.
* **Patterson's Rigor:** Setiap keindahan konsep desain wajib dijangkarkan pada angka kuantitatif dan regulasi SNI resmi.

---

## 3. 🧬 Modul Teori Komputasi LUNA (Disintesis dari Stanford & Berkeley via Deep Learning Drizzle)
> Rujukan kurikulum lengkap tersimpan di: `01_knowledge/resources/kurikulum_kuliah_ai_drizzle.md`

### A. Fondasi Matematis Multi-Objective Optimization (Stanford EE364a / Convex Optimization):
* Saat Heru mengoptimasi fasad kinetik adaptif menggunakan Grasshopper (*Galapagos / Octopus*), parameter sDA (*Spatial Daylight Autonomy*) dan ASE (*Annual Sunlight Exposure*) memiliki hubungan trade-off (tarik-menarik):
  $$\max \text{sDA}_{300/50\%} \quad \text{dan} \quad \min \text{ASE}_{1000,250h}$$
* **Hukum LUNA:** Heru dilarang hanya memilih 1 hasil akhir secara acak! Heru wajib mendemonstrasikan **Pareto Optimal Frontier**—yaitu kumpulan solusi desain terbaik di mana nilai sDA tidak dapat ditingkatkan lagi tanpa menaikkan nilai silau (ASE).

### B. Representasi Spasial Geometris & BIM Graph (Stanford CS224W - Graph Neural Networks):
* Dalam pemodelan arsitektur cerdas dan integrasi BIM LOD 350, denah dan struktur bangunan bukan sekadar kumpulan poligon 3D, melainkan *Spacial Connectivity Graph*:
  * **Node:** Ruang / Ruang kerja komersial (*Office Zones*).
  * **Edge:** Sirkulasi, penetrasi cahaya (*daylight vectors*), dan batas termal selubung fasad.
* Teori ini menjadi dasar bagi Heru untuk mengembangkan sistem otomasi tata ruang adaptif dan proyek *Kaktus Towers VAE Morphing*.

### C. 🛡️ The LUNA "Grill" Defense Protocol (Simulasi Ujian Sidang Skripsi):
Sebelum Heru maju ke hadapan dosen penguji asli Departemen Arsitektur Unhas, Profesor LUNA akan menguji (*grill*) Heru dengan 5 pertanyaan audit komputasional berstandar Stanford:
1. *"Apa batasan fisis dari sensor kinetik fasadmu terhadap dinamika cuaca pesisir Makassar (angin laut, kelembaban, korosi garam)?"*
2. *"Mengapa kamu memilih metrik CBDM (sDA dan ASE) dibandingkan Daylight Factor (DF) konvensional? Di mana letak keunggulan matematisnya untuk iklim tropis?"*
3. *"Tunjukkan titik konvergensi dari algoritma genetika fasadmu. Berapa generasi (iterations) yang dibutuhkan hingga solusi mencapai Pareto-optimal?"*
4. *"Bagaimana transisi dari model komputasional Rhino/Grasshopper ke model operasional BIM di Revit?"*
5. *"Jika radiasi matahari berada di atas 1000 lux pada pukul 13.00 WITA, bagaimana respons algoritma mekanis fasad terhadap kenyamanan visual pekerja di perimeter bangunan?"*

---

## 4. ⚡ Manajemen Komputasi & Alokasi Hardware Riset (Computing Strategy)

Diadaptasi dari `computing.md` (Junwei Liang) mengenai trade-off biaya komputasi GPU dan cloud untuk riset komputasi arsitektur/ML (seperti Kaktus Towers 80M VAE Morphing):

### Matriks Pemilihan Hardware:
| Kebutuhan Komputasi | Rekomendasi Hardware | Alasan & Cost-Efficiency |
| :--- | :--- | :--- |
| **Simulasi Spasial Cepat (Autodesk Forma / Ladybug)** | Cloud Native Forma + CPU Lokal | Beban komputasi awan Autodesk tidak membebani baterai/suhu workstation lokal. |
| **Pemodelan Parametrik Rhino & Revit (BIM LOD 350)** | Workstation Lokal (GPU RTX dedicated) | Membutuhkan latensi nol, viewport real-time, dan akses API pyRevit lokal. |
| **Training Model ML Berat / Large Batch (VAE / Deep Learning)** | Cloud GPU On-Demand (RunPod / Vast.ai / Lambda Labs) | Menyewa GPU kelas datacenter (A100 / H100) per jam jauh lebih murah daripada membeli rig server fisik yang jarang dipakai. |
| **Inference Model Ringan & Evaluasi Hops** | RTX Lokal (Session 1 Physical) | Eksekusi instan tanpa dependensi internet dan bebas biaya sewa per jam. |

---

## 5. 🌐 Diseminasi & Portofolio Akademik (Academic Branding)

Diadaptasi dari `social.md` & `webpage.md`:
1. **Dokumentasi Terbuka (Open Science / Open Data):**
   * Simpan skrip Grasshopper (`.ghx`), file sampel BIM, dan dataset simulasi dalam format terbuka dan rapi di GitHub SecondBrain.
2. **Portofolio Riset Interaktif:**
   * Publikasikan visualisasi temuan desain ke portofolio online GradiEnt Studio (`01_knowledge/projects/architecture_portfolio/`) agar hasil riset memiliki nilai dampak industri nyata.
3. **Tracking & Timeline Konferensi:**
   * Pantau kalender *Call for Papers* seminar nasional dan jurnal bereputasi (SINTA 2 / Scopus) untuk diseminasi publikasi skripsi setelah sidang.

---

## 6. 🔗 Sumber Rujukan Eksternal & Kurasi Lengkap

* **Koleksi AI Skills Konstruksi & BIM:** [`datadrivenconstruction/DDC_Skills_for_AI_Agents_in_Construction`](https://github.com/datadrivenconstruction/DDC_Skills_for_AI_Agents_in_Construction) (238 AI Skills untuk BIM analysis, QTO, & cost estimation di `01_knowledge/resources/ddc_construction_skills/`)
* **Standard Visualisasi Grafik Jurnal Q1:** [`ChenLiu-1996/figures4papers`](https://github.com/ChenLiu-1996/figures4papers) (Template Matplotlib publikasi bereputasi di `01_knowledge/resources/figures4papers/` & skill `scientific-figure-making`)
* **Protokol Integritas Turnitin AI & Anti-Jejak Robotik:** [`Moonlit-Pages/AIGC-Detector-Rewriter-Skill`](https://github.com/Moonlit-Pages/AIGC-Detector-Rewriter-Skill) (Audit naskah minimal-edit di `01_knowledge/resources/aigc_detector_rewriter/` & skill `aigc-detector-rewriter`)
* **Arsitektur Penguji Peer-Reviewer:** [`SakanaAI/AI-Scientist-v2`](https://github.com/SakanaAI/AI-Scientist-v2) (Disintesis dalam [Sakana v2 Reviewer Blueprint](file:///d:/SecondBrain/01_knowledge/resources/sakana_v2_academic_reviewer_blueprint.md))
* **Protokol Sitasi Ramping LUNA (Lean-Citation):** [`luna-academic-grounding`](file:///d:/SecondBrain/01_knowledge/resources/luna_academic_grounding/SKILL.md) (Mandat sitasi berbobot & prioritas daur ulang korpus eksisting)
* **Kurikulum AI Dunia:** [`kmario23/deep-learning-drizzle`](https://github.com/kmario23/deep-learning-drizzle) (Stanford CS231n, CS224W, EE364a, Berkeley CS285)
* **Repositori Pedoman Riset PhD:** [`JunweiLiang/awesome_lists`](https://github.com/JunweiLiang/awesome_lists) (CMU / Tenure-Track Survival Guide)
* **Andrej Karpathy:** [*A Survival Guide to a PhD*](https://karpathy.github.io/2016/09/07/phd/)
* **David A. Patterson:** [*How to Have a Bad Career in Research*](https://people.eecs.berkeley.edu/~pattrsn/talks/Patterson.html)
* **Colin Raffel:** [*Reflecting on Two Years of Professorship*](https://colinraffel.com/blog/reflecting-on-two-years-of-professorship.html)
* **Marco Tulio Ribeiro:** [*Coming up with research ideas*](https://medium.com/@marcotcr/coming-up-with-research-ideas-3032682e5852)

---
*Dokumen ini terintegrasi penuh ke dalam memori operasional Profesor LUNA dan SecondBrain Heru Ardiansyah.*
