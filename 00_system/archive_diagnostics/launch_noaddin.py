"""
DIAGNOSTIC LAUNCHER — Revit tanpa add-in
- Membuka tepat 1 jendela Revit via explorer.exe
- Menunggu window Revit tampil
- Mengambil screenshot verifikasi
- TIDAK membuka file proyek otomatis
"""
import subprocess
import time
import win32gui
import pyautogui

LOG = r"d:\SecondBrain\00_system\noaddin_launch.log"
SHOT = r"d:\SecondBrain\00_system\revit_noaddin.png"

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)

with open(LOG, "w", encoding="utf-8") as f:
    f.write("=== NO-ADDIN DIAGNOSTIC LAUNCH ===\n")

REVIT_EXE = r"C:\Program Files\Autodesk\Revit 2027\Revit.exe"
log(f"Launching: {REVIT_EXE}")
subprocess.run(["explorer.exe", REVIT_EXE])
log("explorer.exe launched. Waiting for Revit window...")

found = False
revit_hwnd = None
revit_title = ""

for i in range(60):  # wait up to 60s
    time.sleep(1)
    def enum_cb(hwnd, _):
        global found, revit_hwnd, revit_title
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd)
            if "Autodesk Revit" in t or "Revit 2027" in t:
                found = True
                revit_hwnd = hwnd
                revit_title = t
    win32gui.EnumWindows(enum_cb, None)
    if found:
        log(f"Revit window detected at {i+1}s: '{revit_title}' (HWND: {revit_hwnd})")
        break

if not found:
    log("ERROR: Revit window NOT found after 60s.")
else:
    time.sleep(5)  # wait for Home screen to fully render
    pyautogui.screenshot(SHOT)
    log(f"Screenshot saved: {SHOT}")
