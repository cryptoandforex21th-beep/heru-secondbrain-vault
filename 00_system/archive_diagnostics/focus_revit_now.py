import win32gui
import win32con
import win32api
import pyautogui
import time

time.sleep(1)

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
    print(f"Found Revit: '{target_title}' (HWND: {target})")
    win32gui.ShowWindow(target, win32con.SW_RESTORE)
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(target)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(2)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_foreground_addins.png")
    print("Screenshot saved to revit_foreground_addins.png")
else:
    print("Revit window not found.")
