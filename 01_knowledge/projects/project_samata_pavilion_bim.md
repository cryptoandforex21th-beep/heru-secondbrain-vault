# 🏛️ PROJECT BRIEF: Samata Pavilion Villa (BIM Revit Architecture)
> **Client:** Bpk. Hendra Dharmawan  
> **Typology:** Residential Villa (2-Storey Modern Pavilion)  
> **Location:** Samata, Gowa - Makassar, Indonesia  
> **Year:** 2026  
> **Status:** `In Progress` (Design & BIM Modeling)  
> **Notion Tracking:** [Notion Inquiry](https://notion.so) | Database Projects ID: `05`  
> **Web Showcase:** [GradiEnt Studio](https://gradientstudioapp.vercel.app)  

---

## 1. 📐 Spesifikasi Teknis & BIM Protocol
* **Satuan Model (Units):** Millimeters (`mm`), 0 decimal places (ISO 19650 standard).
* **Vertikal Datum (Levels):**
  * `01_Ground Floor` : `0.00 mm`
  * `02_Upper Floor`  : `+4000.00 mm`
  * `03_Roof Plan`    : `+8000.00 mm`
* **Horizontal Datum (Grids):**
  * Sumbu Vertikal (Angka): Grid `1`, `2`, `3` (Bentang: 5000 mm / 5 m).
  * Sumbu Horisontal (Huruf): Grid `A`, `B`, `C` (Bentang: 4000 mm / 4 m).
* **Konstruksi Dinding Utama:**
  * Dinding Luar: Basic Wall Generic 200 mm / Plastered Brick.
  * Constraint: Base `Level 1`, Top `Up to level: Level 2`.

---

## 2. 🏁 Progress & Milestones

### ✅ Phase 1: Setup & Building Envelope (COMPLETED)
- [x] Setting Project Units (`mm`) & Datum Levels (`0.0`, `+4000`, `+8000`).
- [x] Grids 1–3 & A–C.
- [x] Link 3D Site Context (Autodesk Forma IFC via Coordination Model ACC Docs).
- [x] Outer Perimeter Walls ($8000 \times 8000\,\text{mm}$) dengan strict constraints (`Up to Level 2`).

### 🔜 Phase 2: Advanced Detailing & MEP Systems (LOD 300–350)
- [ ] **Structural Tie-ins & Wall Joins:**
  - Penempatan Kolom Praktis (KP $150 \times 150\,\text{mm}$) pada grid.
  - Penerapan `Disallow Join` pada grip ujung bata agar volume beton & pasangan bata terpisah bersih di BoQ.
  - Konfigurasi Compound Wall (Bata Merah 110 mm + Spesi 20 mm + Acian 5 mm) lengkap dengan *Layer Wrapping* pada bukaan kusen.
- [ ] **Sanitary & Plumbing Engineering (MEP):**
  - Pembuatan *Plumbing Chase* (Dinding ganda $200\,\text{mm}$) di belakang WC untuk pipa air kotor $\varnothing 4''$ PVC AW.
  - Routing pipa air kotor (slope gravitasi $1.5\% - 2.0\%$) menuju Shaft Plumbing vertikal.
  - Penempatan & elevasi Fixture Sanitair (Kloset duduk, Lavatory, Floor Drain).
- [ ] **Detail Potongan Skala 1:10 / 1:20 (Construction Details):**
  - Detail sambungan sloof-kolom-dinding bata + DPC (Damp Proof Course).
  - Detail pertemuan ringbalk-plat lantai 2-dinding parapet.

---
*Logged by Ai & Luna for Heru Ardiansyah (GradiEnt Studio).*
