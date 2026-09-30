"""
Cloud Storage Manager for Heru's Laptop
Mencadangkan file statis (Revit, SketchUp, Docs) ke Google Drive:
Destination: G:\\My Drive\\file laptop heru\\<Drive>\\<OriginalPath>
Tidak menyentuh SecondBrain, mempertahankan hierarki folder asli laptop.
"""

import os
import sys
import io
import shutil
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GDRIVE_DEST_ROOT = r"G:\My Drive\file laptop heru"
STATIC_EXTENSIONS = ('.rvt', '.skp', '.docx', '.rfa')

# Folder sumber yang dipindai
SOURCES = [
    r"D:\TUGAS KULIAH HERU ARDIANSYAH (D051221073)",
    r"D:\REVIT LEARN",
    r"D:\SKETCHUP",
    r"C:\Users\Heru Ardiansyah\Downloads",
    r"C:\Users\Heru Ardiansyah\Documents",
    r"C:\Users\Heru Ardiansyah\Desktop"
]

EXCLUDE_DIRS = {
    'node_modules', '.git', '.venv', 'appdata', '$recycle.bin',
    'system volume information', 'windows', 'secondbrain', '.next'
}

def get_destination_path(source_path):
    # D:\folder\file.ext -> G:\My Drive\file laptop heru\D\folder\file.ext
    drive, path_without_drive = os.path.splitdrive(source_path)
    drive_letter = drive.replace(":", "").upper()
    rel_path = path_without_drive.lstrip("\\/")
    return os.path.join(GDRIVE_DEST_ROOT, drive_letter, rel_path)

def scan_files():
    found_files = []
    for src in SOURCES:
        if not os.path.exists(src):
            continue
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d.lower() not in EXCLUDE_DIRS]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in STATIC_EXTENSIONS:
                    p = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(p)
                        found_files.append((p, sz, ext))
                    except:
                        pass
    return found_files

def dry_run_summary():
    files = scan_files()
    total_size = sum(f[1] for f in files)
    print("=" * 65)
    print("📦 PREVIEW PENYIMPANAN KE GOOGLE DRIVE")
    print(f"Target Google Drive: {GDRIVE_DEST_ROOT}")
    print("=" * 65)
    print(f"Total file terdeteksi: {len(files)} file")
    print(f"Total ukuran: {total_size / (1024**3):.2f} GB ({total_size / (1024**2):.1f} MB)")
    
    # Rangkuman per ekstensi
    by_ext = {}
    for _, sz, ext in files:
        by_ext[ext] = by_ext.get(ext, [0, 0])
        by_ext[ext][0] += 1
        by_ext[ext][1] += sz
    
    print("\nRincian per jenis file:")
    for ext, (cnt, sz) in sorted(by_ext.items(), key=lambda x: x[1][1], reverse=True):
        print(f"  • {ext.upper():<6} : {cnt:>3} file | {sz / (1024**2):>8.1f} MB")
    
    print("\nContoh pemetaan path ke Google Drive:")
    for p, sz, ext in sorted(files, key=lambda x: x[1], reverse=True)[:5]:
        dest = get_destination_path(p)
        print(f"  [Asli]   {p} ({sz / (1024**2):.1f} MB)")
        print(f"  [Target] {dest}\n")
    print("=" * 65)
    return files

def execute_backup():
    files = scan_files()
    total_files = len(files)
    total_size = sum(f[1] for f in files)
    copied_count = 0
    copied_bytes = 0
    skipped_count = 0
    
    print(f"\n🚀 Memulai pencadangan {total_files} file ({total_size / (1024**3):.2f} GB) ke Google Drive...")
    for idx, (src, sz, ext) in enumerate(files, 1):
        dest = get_destination_path(src)
        dest_dir = os.path.dirname(dest)
        
        # Cek jika file sudah ada dengan ukuran sama
        if os.path.exists(dest) and os.path.getsize(dest) == sz:
            skipped_count += 1
            continue
        
        try:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(src, dest)
            copied_count += 1
            copied_bytes += sz
            if copied_count % 10 == 0 or copied_count == total_files:
                print(f"[{idx}/{total_files}] Tersimpan: {os.path.basename(src)} ({sz / (1024**2):.1f} MB)")
        except Exception as e:
            print(f"[ERROR] Gagal menyalin {src}: {e}")
            
    print("\n" + "=" * 65)
    print("✅ PENCADANGAN KE GOOGLE DRIVE SELESAI!")
    print(f"File baru tersalin : {copied_count} file ({copied_bytes / (1024**2):.1f} MB)")
    print(f"File sudah ada     : {skipped_count} file")
    print(f"Lokasi Cloud       : {GDRIVE_DEST_ROOT}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        execute_backup()
    else:
        dry_run_summary()
