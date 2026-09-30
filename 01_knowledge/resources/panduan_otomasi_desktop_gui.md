# 🖥️ Panduan & SOP Otomasi Desktop GUI (Antigravity & AI Agent)

> **Catatan Sistem:** Dokumentasi ini adalah standar operasional prosedur (SOP) resmi untuk mengontrol aplikasi desktop (WhatsApp, Edge, Revit, dll.) secara visual di layar fisik Windows tanpa terhalang isolasi sandbox Antigravity.

---

## 1. 🔑 Kunci Rahasia: Bypass Sandbox Antigravity (`Session Isolation`)

### Masalah:
Proses yang dijalankan langsung lewat terminal agent (PowerShell/CMD) berjalan di sesi virtual desktop terisolasi (`Desktop: exebox-...`). Jika agent membuka aplikasi visual seperti WhatsApp atau Edge, jendela aplikasinya tidak muncul di monitor fisik pengguna.

### Solusi Permanen: Windows Task Scheduler (`schtasks`)
Task Scheduler Windows memiliki akses ke **Sesi Interaktif Pengguna (Session 1 / `Desktop: Default`)**.
- Task terdaftar: `AntigravityGUI`
- Principal: `LogonType: Interactive`, `UserId: Heru Ardiansyah`
- Kemampuan: Menjalankan skrip Python langsung di layar monitor fisik pengguna dengan akses penuh ke `pyautogui`, `pywinauto`, `pyperclip`, dan `win32gui`.

### Cara Eksekusi Instan (1 Baris PowerShell):
```powershell
$action = New-ScheduledTaskAction -Execute "C:\Python314\python.exe" -Argument '"d:\SecondBrain\02_skills\desktop_bridge\<nama_script>.py"' -WorkingDirectory "d:\SecondBrain\02_skills\desktop_bridge"
Set-ScheduledTask -TaskName "AntigravityGUI" -Action $action
Start-ScheduledTask -TaskName "AntigravityGUI"
```

---

## 2. 🌐 Standar Buka Microsoft Edge (Profil Pribadi Default)

### Aturan Wajib:
- **DILARANG** menggunakan opsi `--guest` atau `--inprivate`.
- **WAJIB** menyertakan argumen: `--profile-directory="Default"`.
- Lokasi profil: `C:\Users\Heru Ardiansyah\AppData\Local\Microsoft\Edge\User Data\Default`

### Perintah Buka URL Langsung ke Layar:
```powershell
$action = New-ScheduledTaskAction -Execute "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -Argument '--profile-directory="Default" https://www.youtube.com'
Set-ScheduledTask -TaskName "AntigravityGUI" -Action $action
Start-ScheduledTask -TaskName "AntigravityGUI"
```

---

## 3. 💬 Standar Otomasi WhatsApp Desktop

Aplikasi WhatsApp yang digunakan adalah versi UWP / WinUI 3 modern:
- **Package App:** `5319275A.51895FA4EA97F_cv1g1gvanyjgm!App`
- **Cara Launch:** `explorer.exe shell:AppsFolder\5319275A.51895FA4EA97F_cv1g1gvanyjgm!App`

### Alur Eksekusi Cepat (Zero-Failure):
1. **Focus & Bring to Front:**
   ```python
   win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
   win32api.keybd_event(18, 0, 0, 0) # ALT key
   win32gui.SetForegroundWindow(hwnd)
   win32api.keybd_event(18, 0, 2, 0)
   ```
2. **Cari Kontak:**
   - Tekan `Ctrl + F`
   - Paste nama kontak via clipboard: `pyperclip.copy("nama kontak")` lalu `Ctrl + V`
   - Tekan `Down` lalu `Enter` untuk membuka ruang chat.
3. **Ketik & Kirim Pesan:**
   - Gunakan clipboard (`pyperclip.copy(pesan)`) lalu `Ctrl + V` untuk memastikan karakter khusus, spasi, dan emoji tertempel sempurna tanpa delay ketik.
   - Tekan `Enter` untuk mengirim.
4. **Verifikasi Visual:**
   - Selalu ambil tangkapan layar menggunakan `pyautogui.screenshot()` untuk memastikan pesan berstatus centang.

---

## 4. 🏗️ Standar Autodesk Revit & pyRevit (Bebas VendorCode 22)

### Masalah VendorCode 22 (AdskLicensingService):
Mengeksekusi `Revit.exe` secara langsung menyebabkan proses berjalan dalam context terisolasi/background, sehingga Revit gagal berkomunikasi dengan layanan lisensi `AdskLicensingService`.

### Solusi Wajib:
Selalu gunakan `explorer.exe` sebagai perantara agar prosesnya sepenuhnya ditangani oleh sesi desktop Windows interaktif, persis seperti diklik manual oleh pengguna:
```python
import subprocess
# Jalankan Revit via explorer.exe
subprocess.run(['explorer.exe', r'C:\Program Files\Autodesk\Revit 2027\Revit.exe'])

# Buka file proyek via explorer.exe
subprocess.run(['explorer.exe', r'D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt'])
```

---

## 5. ⚡ Direktori & File Pendukung

- Skrip Eksekutor Otomatis: `d:\SecondBrain\02_skills\desktop_bridge\`
- Skrip Peluncur Revit: `d:\SecondBrain\02_skills\desktop_bridge\open_revit.py`
- Log Bukti Eksekusi: `d:\SecondBrain\02_skills\desktop_bridge\*.log`
- Bukti Tangkapan Layar: `d:\SecondBrain\00_system\*.png`
- Scheduled Task Windows: `AntigravityGUI` / `AntigravityWorker`
