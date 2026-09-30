import os
import sys
import time
import win32gui
import win32con
import win32api
import pyautogui
import pyperclip
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\open_ctrl_o.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

log("=== Opening Project via Revit Ctrl+O ===")

# 1. Minimize cmd/python terminal windows
def enum_terminals(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if "python.exe" in title.lower() or "cmd.exe" in title.lower():
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    return True
win32gui.EnumWindows(enum_terminals, None)
time.sleep(0.5)

# 2. Focus Revit Main Window
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
if not revit_main:
    log("Revit main window not found!")
    sys.exit(1)

log(f"Focusing Revit Main Window: {revit_main}")
win32api.keybd_event(18, 0, 0, 0)
win32gui.SetForegroundWindow(revit_main)
win32api.keybd_event(18, 0, 2, 0)
time.sleep(1.0)

# 3. Trigger Ctrl + O
log("Pressing Ctrl + O...")
pyautogui.hotkey('ctrl', 'o')
time.sleep(2.0)

# 4. Paste file path and press Enter
project_path = r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt"
log(f"Pasting project path: {project_path}")
pyperclip.copy(project_path)
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)
log("Pressing Enter to Open...")
pyautogui.press('enter')
time.sleep(8.0)

# 5. Screenshot
screenshot_path = Path(r"d:\SecondBrain\00_system\revit_opened_final.png")
pyautogui.screenshot(str(screenshot_path))
log(f"Saved screenshot to {screenshot_path}")
