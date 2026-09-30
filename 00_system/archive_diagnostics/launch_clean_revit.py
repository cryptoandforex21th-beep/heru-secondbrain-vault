import os
import subprocess
import time
import win32gui
import pyautogui

log_file = r"d:\SecondBrain\00_system\clean_launch.log"
shot_file = r"d:\SecondBrain\00_system\revit_clean_startup.png"

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)

with open(log_file, "w", encoding="utf-8") as f:
    f.write("=== CLEAN LAUNCH REVIT TEST ===\n")

revit_exe = r"C:\Program Files\Autodesk\Revit 2027\Revit.exe"
log(f"Launching Revit cleanly without project file: {revit_exe}")

subprocess.run(["explorer.exe", revit_exe])
log("Explorer.exe executed.")

found = False
revit_hwnd = None
revit_title = ""

for i in range(40):
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
        log(f"Revit window detected after {i+1}s: '{revit_title}' (HWND: {revit_hwnd})")
        break

time.sleep(5)
# Take screenshot
pyautogui.screenshot(shot_file)
log(f"Screenshot captured to {shot_file}")
