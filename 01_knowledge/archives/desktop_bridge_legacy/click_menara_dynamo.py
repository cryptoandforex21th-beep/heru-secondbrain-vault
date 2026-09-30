import time
import win32gui
import win32con
import win32api
import pyautogui
from pathlib import Path

# 1. Minimize terminal windows
def enum_terminals(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if "python.exe" in title.lower() or "cmd.exe" in title.lower():
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    return True
win32gui.EnumWindows(enum_terminals, None)
time.sleep(0.5)

# 2. Focus Revit Home Window
revit_hwnd = None
def enum_revit(hwnd, _):
    global revit_hwnd
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if "revit" in title.lower() and "autodesk" in title.lower():
            revit_hwnd = hwnd
            return False
    return True

win32gui.EnumWindows(enum_revit, None)
if revit_hwnd:
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(revit_hwnd)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(1.0)

# 3. Click the first recent model thumbnail (Menara Dynamo at x=185, y=240)
pyautogui.click(185, 240)
time.sleep(12.0)

# 4. Screenshot
pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_menara_dynamo_open.png")
