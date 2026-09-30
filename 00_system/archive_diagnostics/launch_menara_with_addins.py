"""
Launch PROJECT MENARA DYNAMO.rvt via explorer.exe with all add-ins enabled.
Wait for loading, bring window to front, and take verification screenshot.
"""
import subprocess
import time
import win32gui
import win32con
import win32api
import pyautogui

LOG = r"d:\SecondBrain\00_system\menara_launch.log"
SHOT = r"d:\SecondBrain\00_system\menara_with_addins.png"
PROJECT_FILE = r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt"

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)

with open(LOG, "w", encoding="utf-8") as f:
    f.write("=== LAUNCH PROJECT MENARA DYNAMO WITH ADDINS ===\n")

log(f"Launching project: {PROJECT_FILE}")
subprocess.run(["explorer.exe", PROJECT_FILE])
log("explorer.exe launched. Waiting 40s for Revit and add-ins to load...")

time.sleep(40)

# Detect Revit window
target = None
target_title = None

def enum_cb(hwnd, _):
    global target, target_title
    if win32gui.IsWindowVisible(hwnd):
        t = win32gui.GetWindowText(hwnd)
        if "Autodesk Revit" in t or "PROJECT MENARA" in t:
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
        log(f"Focus warning: {e}")
    time.sleep(3)
    pyautogui.screenshot(SHOT)
    log(f"Screenshot saved: {SHOT}")
else:
    log("ERROR: Revit window NOT found after 40s.")
    # Take screenshot anyway to see desktop state
    pyautogui.screenshot(SHOT)
    log(f"Desktop screenshot saved: {SHOT}")
