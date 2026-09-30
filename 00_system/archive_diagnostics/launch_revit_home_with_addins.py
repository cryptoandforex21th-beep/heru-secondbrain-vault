"""
Launch Revit 2027 cleanly to Home Screen with pyRevit and Rhino.Inside.Revit enabled.
Wait for loading, bring window to front, and take screenshot.
"""
import subprocess
import time
import win32gui
import win32con
import win32api
import pyautogui

LOG = r"d:\SecondBrain\00_system\home_launch.log"
SHOT = r"d:\SecondBrain\00_system\revit_home_addins.png"
REVIT_EXE = r"C:\Program Files\Autodesk\Revit 2027\Revit.exe"

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)

with open(LOG, "w", encoding="utf-8") as f:
    f.write("=== CLEAN LAUNCH REVIT WITH ALL ADDINS ===\n")

log(f"Launching Revit Home: {REVIT_EXE}")
subprocess.run(["explorer.exe", REVIT_EXE])
log("explorer.exe launched. Waiting 35s for Revit, pyRevit & Rhino.Inside.Revit...")

time.sleep(35)

target = None
target_title = None

def enum_cb(hwnd, _):
    global target, target_title
    if win32gui.IsWindowVisible(hwnd):
        t = win32gui.GetWindowText(hwnd)
        if "Autodesk Revit" in t or "Revit 2027" in t:
            target = hwnd
            target_title = t

win32gui.EnumWindows(enum_cb, None)

if target:
    log(f"Found Revit window: '{target_title}' (HWND: {target})")
    try:
        win32gui.ShowWindow(target, win32con.SW_RESTORE)
        win32api.keybd_event(18, 0, 0, 0)
        win32gui.SetForegroundWindow(target)
        win32api.keybd_event(18, 0, 2, 0)
    except Exception as e:
        log(f"Focus info: {e}")
    time.sleep(3)
    pyautogui.screenshot(SHOT)
    log(f"Screenshot saved: {SHOT}")
else:
    log("ERROR: Revit window NOT found after 35s.")
    pyautogui.screenshot(SHOT)
