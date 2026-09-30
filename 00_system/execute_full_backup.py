"""
Full Static File Cloud Backup to Google Drive
Targets: Revit, SketchUp, Twinmotion, Video, Docs, CAD, PDF
Destination: G:\\My Drive\\file laptop heru
Uses multithreaded robocopy for high performance.
"""

import os
import sys
import io
import subprocess
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DEST_ROOT = r"G:\My Drive\file laptop heru"

JOBS = [
    {
        "name": "D: SKETCHUP",
        "src": r"D:\SKETCHUP",
        "dest": os.path.join(DEST_ROOT, "D", "SKETCHUP"),
        "filters": ["*.skp", "*.skb", "*.layout"]
    },
    {
        "name": "D: REVIT LEARN",
        "src": r"D:\REVIT LEARN",
        "dest": os.path.join(DEST_ROOT, "D", "REVIT LEARN"),
        "filters": ["*.rvt", "*.rfa", "*.rte", "*.ifc", "*.dwg"]
    },
    {
        "name": "D: TUGAS KULIAH",
        "src": r"D:\TUGAS KULIAH HERU ARDIANSYAH (D051221073)",
        "dest": os.path.join(DEST_ROOT, "D", "TUGAS KULIAH HERU ARDIANSYAH (D051221073)"),
        "filters": ["*.rvt", "*.skp", "*.skb", "*.docx", "*.doc", "*.pdf", "*.dwg", "*.ifc", "*.xlsx", "*.pptx"]
    },
    {
        "name": "C: DOWNLOADS (Static & Project Media)",
        "src": r"C:\Users\Heru Ardiansyah\Downloads",
        "dest": os.path.join(DEST_ROOT, "C", "Users", "Heru Ardiansyah", "Downloads"),
        "filters": [
            "*.rvt", "*.rfa", "*.rte", "*.skp", "*.skb", "*.layout",
            "*.tm", "*.udsmesh", "*.udatasmith",
            "*.mp4", "*.mov", "*.avi",
            "*.png", "*.jpg", "*.jpeg",
            "*.docx", "*.doc", "*.pdf", "*.pptx", "*.xlsx",
            "*.zip", "*.rar", "*.dwg", "*.ifc"
        ]
    },
    {
        "name": "C: VIDEOS",
        "src": r"C:\Users\Heru Ardiansyah\Videos",
        "dest": os.path.join(DEST_ROOT, "C", "Users", "Heru Ardiansyah", "Videos"),
        "filters": ["*.mp4", "*.mov", "*.avi"]
    }
]

def run_backup():
    print("=" * 65)
    print(f"🚀 MEMULAI PENCADANGAN CLOUD KE GOOGLE DRIVE: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Lokasi Target: {DEST_ROOT}")
    print("=" * 65)
    
    total_jobs = len(JOBS)
    for idx, job in enumerate(JOBS, 1):
        src = job["src"]
        dest = job["dest"]
        name = job["name"]
        filters = job["filters"]
        
        if not os.path.exists(src):
            print(f"[{idx}/{total_jobs}] SKIP: Folder sumber {src} tidak ditemukan.")
            continue
            
        print(f"\n[{idx}/{total_jobs}] Menyinkronkan {name}...")
        print(f"  Sumber : {src}")
        print(f"  Tujuan : {dest}")
        
        os.makedirs(dest, exist_ok=True)
        
        cmd = [
            "robocopy", src, dest
        ] + filters + [
            "/E",           # Salin subfolder termasuk yang kosong
            "/MT:16",       # 16 threads multithreading
            "/R:1",         # Retry 1 kali jika file terkunci
            "/W:1",         # Wait 1 detik antar retry
            "/XD", "node_modules", ".git", ".venv", "appdata", "$recycle.bin", "system volume information",
            "/NJH", "/NJS", # Hilangkan header & summary yang berisik
            "/NDL"          # Hilangkan nama folder yang tidak menyalin file
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        # Robocopy exit codes: 0 = No change, 1 = Successful copy, <= 7 is OK
        if res.returncode <= 7:
            print(f"  [OK] Selesai dengan kode status {res.returncode}")
        else:
            print(f"  [WARNING] Robocopy selesai dengan kode {res.returncode}")

    print("\n" + "=" * 65)
    print("✅ SELURUH PROSES PENCADANGAN CLOUD SELESAI!")
    print(f"Semua file telah tersimpan aman di: {DEST_ROOT}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_backup()
