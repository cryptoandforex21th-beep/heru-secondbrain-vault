# 🏛️ Sakana AI-Scientist-v2: Academic Reviewer Blueprint & Defense Protocol
*Disintesis dari arsitektur Sakana AI-Scientist-v2 (Publikasi Nature, Maret 2026) untuk SecondBrain Heru Ardiansyah & Dewan Penguji Profesor LUNA.*

---

## 1. 🌟 Filosofi Sistem: The Autonomous Peer-Reviewer
Di dalam sistem **Sakana AI-Scientist-v2**, kualitas riset tidak dinilai dengan pujian kosong, melainkan diuji oleh **Automated Meta-Reviewer Agent** yang bertindak sebagai reviewer jurnal ilmiah internasional top-tier (NeurIPS, ICLR, ICML, Elsevier).

Tujuannya adalah menemukan setiap **celah logika, kelemahan metodologi, bias simulasi, dan cacat visual** sebelum naskah diajukan ke hadapan manusia. Bagi skripsi Heru, blueprint ini menjadi instrumen **Profesor LUNA** untuk menguji (*grill*) naskah perancangan Solar Tube sebelum sidang tugas akhir.

```
                    ┌──────────────────────────────────────────┐
                    │      NASKAH SKRIPSI / DATA SIMULASI      │
                    │         (Solar Tube & Daylight)          │
                    └────────────────────┬─────────────────────┘
                                         │
                                         ▼
                    ┌──────────────────────────────────────────┐
                    │      SAKANA v2 REVIEWER ENGINE           │
                    │   (4-Pillar Rubric + VLM Figure Audit)   │
                    └──────┬─────────────┬─────────────┬───────┘
                           │             │             │
              ┌────────────┴──┐   ┌──────┴──────┐   ┌──┴────────────┐
              │   Soundness   │   │ Presentation│   │ Empirical/    │
              │  & Formulasi  │   │  & VLM Art  │   │ Failure Cases │
              └───────────────┘   └─────────────┘   └───────────────┘
                                         │
                                         ▼
                    ┌──────────────────────────────────────────┐
                    │    FEEDBACK PROF LUNA / ACTION MATRIX    │
                    │    (Revisi Target, Nilai Prediksi A)     │
                    └──────────────────────────────────────────┘
```

---

## 2. ⚖️ 4-Pillar Peer-Review Rubric (Skala 1 - 10)

Setiap bab dan klaim perancangan Solar Tube dinilai berdasarkan 4 pilar objektif:

### A. Soundness & Technical Correctness (Bobot 35%)
* **Fokus:** Apakah formulasi matematika, hukum fisika pencahayaan, dan parameter BIM valid?
* **Checklist Solar Tube:**
  1. Apakah transmisi berkas cahaya memperhitungkan reflektansi spekular pipa ($R \ge 99.5\%$) pada sudut datang kritis?
  2. Apakah pemodelan cuaca menggunakan data meteorologi resmi (EPW / TMYx Makassar)?
  3. Apakah perhitungan *Daylight Autonomy* (DA) dan *Useful Daylight Illuminance* (UDI) mematuhi ambang batas SNI 03-6197-2020 dan IES LM-83?

### B. Presentation & VLM Figure Inspection (Bobot 25%)
* **Fokus:** Standar penyajian visual dan tipografi paper kelas dunia (menggunakan skill `scientific-figure-making`).
* **Checklist Visual (VLM Loop):**
  1. Resolusi minimal 300–600 DPI (format vektor PDF/SVG atau TIFF lossless).
  2. Label sumbu $X$ dan $Y$ wajib menyertakan unit satuan ISO yang jelas (misal: `Illuminance (lux)`, `Time of Day (Hours)`, `Power Density (W/m²)`).
  3. Palet warna ramah buta warna (*colorblind-safe*, hindari kombinasi merah-hijau murni tanpa pola pembeda).
  4. Ukuran font pada label grafik terbaca jelas tanpa perlu zoom ekstra (proporsional terhadap naskah).

### C. Novelty & Practical Contribution (Bobot 20%)
* **Fokus:** Apa keunggulan signifikan perancangan ini dibanding solusi konvensional?
* **Checklist:**
  1. Seberapa besar penghematan energi listrik (kWh) per tahun untuk pencahayaan buatan?
  2. Bagaimana integrasi arsitektural Solar Tube terhadap struktur atap dan estetika interior gedung?
  3. Apa mitigasi terhadap *heat gain* (beban pendinginan AC)?

### D. Empirical Rigor & Failure-Case Analysis (Bobot 20%)
* **Fokus:** Menguji sistem pada skenario paling buruk (*stress-test*), bukan hanya saat cuaca cerah sempurna.
* **Checklist:**
  1. Performa saat *Overcast Sky* (langit mendung total di musim hujan Makassar)?
  2. Degradasi performa akibat debu pada kubah transparan (*dirt depreciation factor*)?
  3. Analisis *Return on Investment* (ROI) dan masa balik modal perancangan.

---

## 3. 🔥 The Prof Luna "Grill Defense" Matrix: Daftar Serangan Penguji

Gunakan matriks ini untuk gladi bersih simulasi sidang skripsi. Jika Heru bisa menjawab 4 pertanyaan ini dengan data, sidang akan berjalan mulus:

| No | Modul | Pertanyaan Kritis Penguji (Prof Luna Mode) | Argumen Penyelamat (Defense Protocol) |
|---|---|---|---|
| **Q1** | **Optik & Transmisi** | *"Mengapa Anda yakin pipa sepanjang itu tidak kehilangan cahaya sebelum sampai ke lantai bawah?"* | **Bukti:** Tunjukkan grafik transmisi eksponensial $T = R^{n}$ dengan reflektansi 99.5% dari material cermin Alanod/MIRO-SILVER, di mana $n$ adalah jumlah pantulan rata-rata berdasarkan sudut matahari Makassar ($-5^\circ$ lintang). |
| **Q2** | **Kenyamanan Visual (Glare)** | *"Apakah cahaya intens dari Solar Tube di siang terik tidak menyebabkan silau (glare) pada layar komputer pekerja?"* | **Bukti:** Lampirkan analisis *Daylight Glare Probability* (DGP < 0.35) dan penggunaan *diffuser lens prismatic* di ujung pipa yang menyebarkan berkas cahaya secara merata (Lambertian distribution). |
| **Q3** | **Termal & Beban AC** | *"Bukankah memasukkan cahaya matahari sama saja memasukkan radiasi panas yang membebani AC?"* | **Bukti:** Tunjukkan rasio efikasi cahaya (*luminous efficacy*). Cahaya matahari alami memiliki efikasi ~110 lm/W dengan panas lebih rendah per lumen dibanding lampu halogen konvensional, ditambah kubah luar dilengkapi filter UV/IR termal ganda. |
| **Q4** | **Pareto Front Drizzle** | *"Bagaimana Anda membuktikan titik perletakan Solar Tube ini adalah posisi paling optimal?"* | **Bukti:** Tunjukkan grafik *Pareto Frontier* Drizzle (kombinasi `figures4papers`) yang memetakan trade-off antara jumlah unit Solar Tube (biaya instalasi) vs pemerataan lux di atas meja kerja (SNI 300 lux). |

---

## 4. 🛠️ Integrasi Alur Kerja di Antigravity
Saat Heru meminta evaluasi skripsi atau simulasi bab:
1. **Ai Mode:** Menulis narasi, merapikan data, dan menjalankan script `figures4papers` untuk menghasilkan grafik vektor.
2. **Reviewer Mode (Sakana v2 & Prof Luna):** Membaca naskah secara kritis, memberikan skor kelayakan (1-10), dan menunjukkan paragraf mana yang masih lemah argumennya sebelum dicetak.
