---
name: desktop-gui-automation
description: "Mengontrol aplikasi desktop Windows secara visual (WhatsApp, Edge default profile, Revit, dll.) langsung di layar fisik pengguna dengan menembus isolasi sandbox Antigravity menggunakan Windows Task Scheduler."
---

# Desktop GUI Automation Skill

Gunakan skill ini setiap kali ada instruksi untuk mengontrol, membuka, membaca, atau mengetik pada aplikasi desktop Windows di monitor fisik pengguna.

## 🚀 Prosedur Standar Eksekusi Instan

### 1. Bypass Sandbox Antigravity
Perintah bawaan agent berjalan di sesi terisolasi (`exebox`). Untuk berinteraksi dengan layar fisik, jalankan skrip Python melalui task scheduler `AntigravityGUI`:
```powershell
$action = New-ScheduledTaskAction -Execute "C:\Python314\python.exe" -Argument '"d:\SecondBrain\02_skills\desktop_bridge\<nama_script>.py"' -WorkingDirectory "d:\SecondBrain\02_skills\desktop_bridge"
Set-ScheduledTask -TaskName "AntigravityGUI" -Action $action
Start-ScheduledTask -TaskName "AntigravityGUI"
```

### 2. WhatsApp Desktop Automation
- Template eksekutor: `d:\SecondBrain\02_skills\desktop_bridge\whatsapp_reply.py`
- Template mirroring: `d:\SecondBrain\02_skills\desktop_bridge\mirror_reply.py`
- Alur:
  1. Bring to front dengan `win32gui.SetForegroundWindow` (pakai Alt-key trick).
  2. Tekan `Ctrl + F` untuk mencari kontak.
  3. Gunakan `pyperclip` untuk copy-paste nama kontak dan teks pesan agar emoji & teks panjang tidak error.
  4. Tekan `Enter` untuk mengirim pesan.
  5. Ambil tangkapan layar `pyautogui.screenshot()` untuk verifikasi visual ke `00_system/`.

### 3. Microsoft Edge Personal Profile
- Path: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- Parameter Wajib: `--profile-directory="Default"` (Dilarang `--guest`).

### 4. Autodesk Revit & pyRevit (Mencegah VendorCode 22)
- Software Autodesk memerlukan `AdskLicensingService` yang hanya bisa berkomunikasi normal dalam User Context Windows Explorer.
- **DILARANG** mengeksekusi `Revit.exe` secara langsung via shell biasa.
- **WAJIB** meluncurkan melalui `explorer.exe`:
  ```python
  import subprocess
  subprocess.run(['explorer.exe', r'C:\Program Files\Autodesk\Revit 2027\Revit.exe'])
  subprocess.run(['explorer.exe', r'D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt'])
  ```
- Skrip siap pakai: `d:\SecondBrain\02_skills\desktop_bridge\open_revit.py`

