import subprocess
import time
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\launch_revit_explorer.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

log("=== Launching Revit 2027 via explorer.exe (Full User Shell Context) ===")

REVIT_EXE = r"C:\Program Files\Autodesk\Revit 2027\Revit.exe"
PROJECT_RVT = r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt"

log(f"Step 1: Running explorer.exe with {REVIT_EXE}...")
subprocess.run(['explorer.exe', REVIT_EXE])

time.sleep(4)

log(f"Step 2: Running explorer.exe with {PROJECT_RVT}...")
subprocess.run(['explorer.exe', PROJECT_RVT])

log("=== Both commands dispatched successfully via explorer.exe ===")
