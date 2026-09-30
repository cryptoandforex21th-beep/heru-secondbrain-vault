# 🎨 Referensi Desain UI/UX & AI Artifacts (cult/ui)
> **Disintesis dari:** [*nolly-studio/cult-ui*](https://github.com/nolly-studio/cult-ui)  
> **Kategori:** Frontend Engineering, Micro-Interactions, & AI Agent Interfaces  
> **Target Implementasi:** GradiEnt Studio Web App ([`gradientstudioapp.vercel.app`](https://gradientstudioapp.vercel.app)) & Antarmuka SecondBrain Web.

---

## 📌 Ringkasan Teknologi
* **Teknologi Dasar:** React, Next.js, Tailwind CSS, Framer Motion, TypeScript.
* **Arsitektur:** 100% kompatibel dengan **Shadcn/ui** (menggunakan arsitektur *copy-paste components* tanpa dependensi npm yang membebani bundle).
* **Spesialisasi:** Dibuat khusus untuk *Design Engineers* dan pengembang aplikasi AI modern.

---

## 🛠️ Komponen Prioritas untuk GradiEnt Studio ([`gradient_studio_app`](file:///d:/SecondBrain/01_knowledge/projects/gradient_studio_app/))

Berikut komponen-komponen unggulan dari `cult-ui` yang direncanakan untuk diintegrasikan ke platform digital GradiEnt Studio:

### 1. 🏛️ Showcase Proyek Arsitektur (Project Cards & Gallery)
* **3D Tilt & Glowing Border Cards:** Menampilkan render proyek *Samata Pavilion* dan *Menara Dynamo* dengan efek hover 3D dan pendaran gradien mewah saat kursor mouse bergerak di atas kartu proyek.
* **Fluid Tabs & Category Filters:** Transisi animasi mulus saat calon klien menyaring portofolio (misal: *Residensial*, *Komersial*, *BIM Engineering*).

### 2. 🤖 AI Chat & Interactive Artifacts (Studio AI Consultant)
* **Side-by-Side Artifacts Canvas:** Saat calon klien atau pengguna berkonsultasi dengan asisten AI GradiEnt Studio, hasil estimasi RAB atau tabel spesifikasi material BIM akan muncul di jendela samping (*Artifact panel*) interaktif yang bisa di-unduh atau diedit real-time.
* **Streaming Chart Visualizer:** Menampilkan grafik perbandingan efisiensi pencahayaan (sDA/ASE) atau perkiraan biaya proyek secara dinamis.

### 3. ✨ Landing Page Hero & Micro-Interactions
* **Animated Gradient Typography:** Efek teks shimmer halus untuk tagline *"Pioneering Computational Architecture & High-Performance Design"*.
* **Magnetic Action Buttons:** Tombol *"Konsultasi Proyek"* yang bereaksi secara magnetik terhadap pergerakan kursor pengguna.

---

## 🚀 Panduan Cepat Integrasi ke Next.js (Shadcn Ecosystem)

1. Pastikan proyek Next.js memiliki Tailwind CSS dan Framer Motion:
   ```bash
   npm install framer-motion clsx tailwind-merge lucide-react
   ```
2. Salin kode komponen yang diinginkan langsung dari direktori `apps/www/src/components/cult/` ke dalam folder `@/components/ui/` di proyek `gradient_studio_app`.
3. Komponen langsung siap digunakan tanpa konfigurasi kompleks tambahan.

---
*Dokumen ini terdaftar dalam indeks aset digital SecondBrain Heru Ardiansyah.*
