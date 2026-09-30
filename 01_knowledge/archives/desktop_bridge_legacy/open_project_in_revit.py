import os
import sys
import time
import win32gui
import win32con
import win32api
import pyautogui
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\open_project.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

log("=== Opening Project Menara Dynamo in Revit ===")

# 1. Close/hide pyRevit popup windows
def enum_pyrevit(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title == "pyRevit":
            log(f"Closing pyRevit console window: {hwnd}")
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    return True

win32gui.EnumWindows(enum_pyrevit, None)
time.sleep(1.0)

# 2. Find Revit Main Window
revit_main = None
def enum_revit(hwnd, _):
    global revit_main
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if "revit" in title.lower() and title != "pyRevit":
            rect = win32gui.GetWindowRect(hwnd)
            if rect[2] - rect[0] > 500:
                revit_main = hwnd
                return False
    return True

win32gui.EnumWindows(enum_revit, None)
if revit_main:
    log(f"Focusing Revit Main Window: {revit_main}")
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(revit_main)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(1.0)

# 3. Open project via os.startfile
project_path = r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt"
log(f"Opening project: {project_path}")
os.startfile(project_path)
time.sleep(6.0)

# 4. Screenshot
screenshot_path = Path(r"d:\SecondBrain\00_system\revit_project_opening.png")
pyautogui.screenshot(str(screenshot_path))
log(f"Saved screenshot to {screenshot_path}")
