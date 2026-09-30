import time
import win32gui
import win32con
import win32api
import pyautogui

def log_info():
    fore_hwnd = win32gui.GetForegroundWindow()
    fore_title = win32gui.GetWindowText(fore_hwnd)
    
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "edge" in title.lower():
                hwnds.append((hwnd, title, win32gui.GetWindowRect(hwnd)))
    win32gui.EnumWindows(enum_cb, None)

    with open(r"d:\SecondBrain\00_system\gemini_diag.log", "w", encoding="utf-8") as f:
        f.write(f"Foreground: HWND={fore_hwnd}, Title='{fore_title}'\n")
        f.write(f"Edge windows: {hwnds}\n")

log_info()