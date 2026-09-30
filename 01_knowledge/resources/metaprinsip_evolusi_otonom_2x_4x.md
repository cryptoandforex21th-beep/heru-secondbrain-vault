# 🧬 Metaprinsip Evolusi Otonom (The 2x Skill & 4x Automation Rule)

> **Status:** Aktif Permanen di Seluruh Workspace Antigravity & SecondBrain  
> **Master Tracker:** `d:\SecondBrain\00_system\task_frequency.json`  
> **Tracker Engine:** `d:\SecondBrain\00_system\task_tracker.py`  

---

## 1. 🎯 Filosofi Inti
Asisten AI (Ai) bukan sekadar bot pasif penjawab teks, melainkan agen yang aktif mengamati pola instruksi berulang pengguna (Heru Ardiansyah), lalu **secara otonom mengubah pola tersebut menjadi kapabilitas permanen**.

```
[Permintaan Berulang] 
        │
        ├── 2x Pola Sama ────────► [KRISTALISASI SKILL (SKILL.md)]
        │                           Membungkus SOP, parameter, dan teknik eksekusi standar.
        │
        └── 4x Pola Sama ────────► [FULL AUTOMATION PIPELINE]
                                    Meningkatkan ke CLI 1-baris, Scheduled Task, atau Daemon.
```

---

## 2. ⚡ Rincian Aturan

### A. Aturan 2x — Kristalisasi Skill (*Skill Crystallization*)
* **Kapan Aktif:** Saat suatu tugas/perintah diminta sebanyak **2 kali atau lebih**.
* **Tindakan AI:** 
  1. AI dilarang mengulang raba-raba atau eksperimen manual dari nol.
  2. AI langsung membuat folder skill baru di `~/.gemini/config/skills/<nama-skill>/` atau workspace `.agents/skills/`.
  3. Menulis file `SKILL.md` yang merinci:
     - Kapan skill ini dipicu (*trigger keywords*).
     - SOP langkah kerja tercepat.
     - Penanganan error (*troubleshooting*).
  4. Mendaftarkan skill ke `task_frequency.json` dengan status `skill_crystallized`.

### B. Aturan 4x — Otomasi Penuh (*Full Automation Pipeline*)
* **Kapan Aktif:** Saat tugas tersebut diminta berulang kali hingga **~4 kali berturut-turut**.
* **Tindakan AI:**
  1. AI dilarang meminta konfirmasi multi-langkah lagi ke pengguna.
  2. AI langsung menaikkan skill tersebut menjadi pipeline mandiri:
     - Skrip eksekutor kilat 1 baris (contoh: `app_launcher.py`, `whatsapp_cli.py`, `revit_cli.py`).
     - Trigger otomatis via Windows Task Scheduler (`AntigravityGUI`).
     - Script sinkronisasi background (contoh: `sync_gdrive.py`).
  3. Memastikan waktu eksekusi turun ke level sub-detik (< 1 detik).
  4. Mendaftarkan statusnya sebagai `fully_automated` di `task_frequency.json`.

---

## 3. 📊 Status Inventaris Histori Saat Ini (Audit Retroaktif)

| Kategori Tugas | Jumlah Histori | Status | Implementasi & File Terkait |
| :--- | :---: | :---: | :--- |
| **Revit, Dynamo & pyRevit** | 15x | `fully_automated` | `d:\SecondBrain\00_system\revit_cli.py`<br>`~/.gemini/config/skills/revit-bim-connector/` |
| **Membuka Aplikasi Desktop** | 14x | `fully_automated` | `d:\SecondBrain\00_system\app_launcher.py`<br>Task Scheduler `AntigravityGUI` (Session 1) |
| **Buka Tab / Web Edge** | 9x | `fully_automated` | `app_launcher.py` + Profil Default Edge |
| **Sinkronisasi Google Drive** | 6x | `fully_automated` | `d:\SecondBrain\00_system\sync_gdrive.py`<br>Mirror ke `G:\My Drive\` |
| **Otomasi Pesan WhatsApp** | 2x | `skill_crystallized` | `d:\SecondBrain\00_system\whatsapp_cli.py`<br>`~/.gemini/config/skills/whatsapp-automator/` |
| **Publikasi Portfolio Portabel** | 3x | `skill_crystallized` | `~/.gemini/config/skills/safe-showcase-publisher/` |
| **Pengisian Formulir Kilat** | 3x | `skill_crystallized` | `~/.gemini/config/skills/fast-form-filler/` |

---

## 4. 🛠️ Cara Kerja Pemantau Otomatis di Masa Depan
Setiap kali AI mengeksekusi instruksi dari Heru, sistem menjalankan pencatatan ke tracker:
```powershell
python d:\SecondBrain\00_system\task_tracker.py log "<nama_tugas>" "<catatan/deskripsi>"
```
Untuk melihat ringkasan seluruh tugas yang telah dipelajari:
```powershell
python d:\SecondBrain\00_system\task_tracker.py summary
```
