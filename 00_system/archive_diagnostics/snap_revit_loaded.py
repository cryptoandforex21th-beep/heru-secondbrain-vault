"""
Foto ulang setelah Revit selesai loading - tunggu 45s dari sekarang
lalu bawa Revit ke depan dan ambil screenshot
"""
import win32gui
import win32con
import win32api
import pyautogui
import time

time.sleep(20)  # tunggu loading selesai

# Cari window Revit
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
    print(f"Found Revit: '{target_title}' (HWND: {target})")
    win32gui.ShowWindow(target, win32con.SW_RESTORE)
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(target)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(2)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_noaddin_loaded.png")
    print("Screenshot saved: revit_noaddin_loaded.png")
else:
    print("ERROR: Revit window NOT found!")
    # List all windows for debugging
    def list_cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd)
            if t:
                print(f"  HWND: {hwnd} Title: {t}")
    win32gui.EnumWindows(list_cb, None)
