# 🛡️ Panduan Arena Skill & Token-Shield Protocol

> **Sumber Asli:** [*Jakeschincariol/arena-skill*](https://github.com/Jakeschincariol/arena-skill) (The Arena Skill for Claude Code / Antigravity)  
> **Lokasi Pemasangan:**  
> - Repositori SecondBrain: `D:\SecondBrain\02_skills\arena\`  
> - Direktori Global Semua Agen: `C:\Users\Heru Ardiansyah\.gemini\config\skills\arena\`

---

## 1. 🔍 Apa Itu Arena Skill?

Arena Skill adalah mekanisme pemecahan masalah berbasis **turnamen eliminasi multi-strategi (*adversarial tournament bracket*)**:
* Ketika AI memberikan jawaban yang kurang memuaskan untuk masalah yang sangat rumit (misalnya bug koding yang bandel, desain sistem arsitektur yang kontradiktif, atau optimasi formula matematika), skill ini membuat beberapa versi sub-agen berkompetisi.
* Setiap agen dibekali **Kartu Strategi unik** (kombinasi dari 15 pola penalaran, 12 alur kerja, dan 12 strategi = 2.160 kombinasi unik dari `strategies.json`).
* Agen saling mengkritisi solusi (*attack*), merevisi kelemahan (*defend*), dan dinilai oleh agen juri independen (*judge*) berdasarkan [rubrik penilaian objektif](rubric.md) hingga tersisa **1 solusi juara terbaik**.

---

## 2. ⚠️ Peringatan Risiko: Mengapa Versi Bawaan Berbahaya untuk Kuota Token?

Versi asli dari repo tersebut memiliki setelan bawaan yang **sangat agresif dan berpotensi menghabiskan kuota token secara masif (*token drain*)**:

| Parameter Asli | Dampak Token & Panggilan | Risiko |
| :--- | :--- | :--- |
| **Default 100 Agen** | Menghasilkan **595 panggilan sub-agent** dalam 7 ronde eliminasi! | Menghabiskan **1.800.000 – 3.500.000 token** dalam satu kali jalan! |
| **Quick Mode (16 Agen)** | Menghasilkan **91 panggilan sub-agent** dalam 4 ronde. | Menghabiskan **~250.000 – 400.000 token**. |
| **Auto-Trigger Agresif** | Terpicu otomatis jika user berkata *"try again"*, *"bad answer"*, atau *"salah"*. | Bisa berjalan tanpa disengaja dan membakar limit harian. |

---

## 3. 🛡️ 4 Lapisan Perlindungan Kuota (*Token-Shield Protocol*)

Ai telah memodifikasi dan mengamankan skill ini sebelum diaktifkan untuk seluruh agen kamu:

### A. Nonaktifkan Auto-Trigger (Anti-Spam)
* Skill ini **TIDAK AKAN PERNAH** berjalan otomatis hanya karena kamu bilang *"coba lagi"*, *"salah"*, atau *"ulang"*.
* **Hanya aktif jika Heru secara sadar memanggil:** `/arena` atau memberikan perintah eksplisit: *"jalankan arena tournament"*.

### B. Ukuran Default Aman (Micro-Bracket 4 Agen)
Ai mengubah konfigurasi default menjadi mode **Micro-Bracket**:
* **Default (`--micro`):** 4 Agen, 2 Ronde = **19 total panggilan** (~40.000–60.000 token). Sangat aman dan terjangkau!
* **Quick (`--quick`):** 8 Agen, 3 Ronde = **43 total panggilan** (~100.000 token).
* **Standard (`--standard`):** 16 Agen, 4 Ronde = **91 total panggilan** (~250.000 token).
* **Extreme (`--agents 100`):** 100 Agen (595 panggilan). **Wajib konfirmasi eksplisit dari Heru** sebelum dieksekusi.

### C. Pembatasan Model Subagent (`flash_lite` / `flash`)
* Sub-agen yang bertarung diwajibkan menggunakan model ringan dan super cepat (`flash_lite` atau `flash`), sehingga biaya per panggilan **95% lebih murah** dibanding model `pro`.

### D. Kalkulasi & Persetujuan di Awal (Pre-Flight Budget Gate)
* Sebelum satu pun sub-agen dibuat, sistem wajib melaporkan estimasi ke Heru:
  > *"Turnamen Arena: 4 agen, 2 ronde, estimasi ~19 panggilan subagent (~50k token). Lanjutkan?"*

---

## 4. 🚀 Cara Menggunakan

Kapan pun kamu ingin mengadu beberapa strategi untuk satu masalah yang sangat rumit:
```text
/arena selesaikan optimasi distribusi daylighting Solar Tube di lantai dalam gedung
```
Atau tentukan jumlah agen secara aman:
```text
/arena --micro rancang arsitektur caching database Supabase
/arena --quick evaluasi clash detection balok vs pipa MEP
```

Dengan sistem ini, kamu mendapatkan kekuatan penuh turnamen penalaran multi-strategi **tanpa khawatir kuota token tersedot diam-diam!**
