import time
import win32gui
import win32con
import win32api
import pyautogui
import pyperclip
from pathlib import Path

# 1. Bring Revit to front
revit_hwnd = None
def cb(hwnd, _):
    global revit_hwnd
    if win32gui.IsWindowVisible(hwnd):
        t = win32gui.GetWindowText(hwnd)
        if "revit" in t.lower() and "autodesk" in t.lower():
            revit_hwnd = hwnd
            return False
    return True

win32gui.EnumWindows(cb, None)
if revit_hwnd:
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(revit_hwnd)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(0.8)

# 2. Click "Open..." button under Models (x=55, y=140)
pyautogui.click(55, 140)
time.sleep(2.0)

# 3. Paste file path and press Enter
project_path = r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt"
pyperclip.copy(project_path)
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)
pyautogui.press('enter')
time.sleep(15.0)

# 4. Take confirmation screenshot
pyautogui.screenshot(r"d:\SecondBrain\00_system\menara_dynamo_loaded.png")
