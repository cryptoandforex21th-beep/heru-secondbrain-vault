import win32gui
import win32con
import win32api
import time
import pyautogui

def bring_to_front(target_hwnd):
    win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(target_hwnd)
    win32api.keybd_event(18, 0, 2, 0)

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
    print(f"Bringing Revit to front: {target_title} (HWND: {target})")
    bring_to_front(target)
    time.sleep(2)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_foreground_verified.png")
    print("Screenshot saved to d:\\SecondBrain\\00_system\\revit_foreground_verified.png")
else:
    print("Revit window not found!")
