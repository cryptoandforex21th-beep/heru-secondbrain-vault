import win32gui
import win32con
import win32api
import pyautogui
import time

time.sleep(25)

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
    try:
        win32gui.ShowWindow(target, win32con.SW_RESTORE)
        win32api.keybd_event(18, 0, 0, 0)
        win32gui.SetForegroundWindow(target)
        win32api.keybd_event(18, 0, 2, 0)
    except Exception as e:
        print(f"Focus error: {e}")
    time.sleep(3)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\menara_addins_loaded.png")
    print("Screenshot saved to menara_addins_loaded.png")
else:
    print("Revit main window not found yet. Taking desktop shot.")
    pyautogui.screenshot(r"d:\SecondBrain\00_system\menara_addins_loaded.png")
