"""
Safely clean Drive C after verified Google Drive backup
Targets:
1. Backed-up static files in Downloads (only if verified in G:\My Drive\file laptop heru)
2. Windows Temporary files (%TEMP%)
Reports exact disk space freed.
"""

import os
import sys
import io
import shutil
import ctypes

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GDRIVE_BACKUP_ROOT = r"G:\My Drive\file laptop heru"
DOWNLOADS_DIR = os.path.expanduser(r"~\Downloads")
TEMP_DIR = os.environ.get("TEMP", os.path.expanduser(r"~\AppData\Local\Temp"))

STATIC_EXTS = {
    '.rvt', '.rfa', '.rte', '.ifc', '.skp', '.skb', '.layout', '.dwg', '.dxf',
    '.tm', '.udsmesh', '.udatasmith',
    '.mp4', '.mov', '.avi', '.png', '.jpg', '.jpeg',
    '.docx', '.doc', '.pdf', '.pptx', '.xlsx', '.zip', '.rar'
}

def get_free_space_gb(drive="C:"):
    free_bytes = ctypes.c_ulonglong(0)
    total_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        drive,
        ctypes.byref(free_bytes),
        ctypes.byref(total_bytes),
        None
    )
    return free_bytes.value / (1024**3), total_bytes.value / (1024**3)

def clean_downloads():
    print(f"\n📂 Memeriksa file Downloads yang sudah terverifikasi di Google Drive...")
    deleted_files = 0
    deleted_bytes = 0
    
    for root, dirs, files in os.walk(DOWNLOADS_DIR, topdown=False):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in STATIC_EXTS:
                src_path = os.path.join(root, f)
                rel_path = os.path.relpath(src_path, os.path.expanduser("~"))
                # Path di Google Drive: G:\My Drive\file laptop heru\C\Users\Heru Ardiansyah\<rel_path>
                cloud_path = os.path.join(GDRIVE_BACKUP_ROOT, "C", "Users", "Heru Ardiansyah", rel_path)
                
                # VERIFIKASI KETAT: Hanya hapus jika file ada di cloud dengan ukuran yang sama
                try:
                    if os.path.exists(cloud_path):
                        src_sz = os.path.getsize(src_path)
                        cloud_sz = os.path.getsize(cloud_path)
                        if src_sz == cloud_sz:
                            os.remove(src_path)
                            deleted_files += 1
                            deleted_bytes += src_sz
                except Exception as e:
                    pass
        
        # Bersihkan direktori kosong
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
            except:
                pass
                
    print(f"  [OK] Berhasil menghapus {deleted_files} file statis terverifikasi ({deleted_bytes / (1024**3):.2f} GB)")
    return deleted_bytes

def clean_temp():
    print(f"\n🧹 Membersihkan file cache sementara (%TEMP%)...")
    deleted_count = 0
    deleted_bytes = 0
    
    if not os.path.exists(TEMP_DIR):
        return 0
        
    for item in os.listdir(TEMP_DIR):
        p = os.path.join(TEMP_DIR, item)
        try:
            if os.path.isfile(p) or os.path.islink(p):
                sz = os.path.getsize(p)
                os.remove(p)
                deleted_bytes += sz
                deleted_count += 1
            elif os.path.isdir(p):
                # Calculate size before rmtree
                for r, _, fs in os.walk(p):
                    for f in fs:
                        try:
                            deleted_bytes += os.path.getsize(os.path.join(r, f))
                        except:
                            pass
                shutil.rmtree(p, ignore_errors=True)
                deleted_count += 1
        except Exception:
            # File sedang dipakai proses aktif, lewati secara aman
            pass
            
    print(f"  [OK] Berhasil membersihkan sampah temporary ({deleted_bytes / (1024**3):.2f} GB)")
    return deleted_bytes

def main():
    print("=" * 65)
    print("🚀 PEMBERSIHAN PENYIMPANAN DRIVE C LAPTOP")
    print("=" * 65)
    
    free_before, total_c = get_free_space_gb("C:")
    print(f"Kapasitas Drive C Sebelum Pembersihan: {free_before:.2f} GB Free dari {total_c:.2f} GB")
    
    dl_bytes = clean_downloads()
    temp_bytes = clean_temp()
    
    free_after, _ = get_free_space_gb("C:")
    freed_gb = free_after - free_before
    
    print("\n" + "=" * 65)
    print("🎉 PEMBERSIHAN SELESAI DENGAN SUKSES!")
    print(f"Total Ruang Baru yang Berhasil Diberikan: +{freed_gb:.2f} GB")
    print(f"Kapasitas Bebas Drive C Sekarang: {free_after:.2f} GB Free")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
