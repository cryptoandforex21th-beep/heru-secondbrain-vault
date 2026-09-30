import sys
import time
import httpx
import win32gui
import win32con
import win32api
import pyautogui
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\check_revit.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

log("=== Checking Revit Window and pyRevit Status ===")

# 1. Check Window Title
revit_hwnds = []
def cb(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd):
        t = win32gui.GetWindowText(hwnd)
        if "revit" in t.lower():
            revit_hwnds.append((hwnd, t))
    return True

win32gui.EnumWindows(cb, None)
log(f"Found Revit windows: {revit_hwnds}")

target_hwnd = None
if revit_hwnds:
    target_hwnd = revit_hwnds[0][0]
    title = revit_hwnds[0][1]
    log(f"Focusing Revit window: '{title}'")
    win32gui.ShowWindow(target_hwnd, win32con.SW_MAXIMIZE)
    time.sleep(0.3)
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(target_hwnd)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(1.0)

# Take screenshot
screenshot_path = Path(r"d:\SecondBrain\00_system\revit_active.png")
pyautogui.screenshot(str(screenshot_path))
log(f"Saved screenshot to {screenshot_path}")

# 2. Check pyRevit status endpoint
try:
    r = httpx.get("http://127.0.0.1:48884/revit_mcp/status/", timeout=3.0)
    log(f"pyRevit Status Code: {r.status_code}, Body: {r.text}")
except Exception as e:
    log(f"pyRevit Status Error: {e}")
