"""
Skrip Peluncur Tunggal Revit 2027 & PROJECT MENARA DYNAMO via Windows Explorer Shell.
Hanya membuka TEPAT 1 jendela Revit langsung bersama file proyeknya.
"""
import subprocess
from pathlib import Path

PROJECT_FILE = r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt"

def launch_single_revit_window():
    print(f"Membuka 1 jendela Revit dengan proyek: {PROJECT_FILE}")
    # Membuka langsung file .rvt via explorer.exe membuka tepat 1 instance Revit dengan context user utuh
    subprocess.run(['explorer.exe', PROJECT_FILE])
    print("Perintah explorer.exe berhasil dikirim!")

if __name__ == "__main__":
    launch_single_revit_window()
