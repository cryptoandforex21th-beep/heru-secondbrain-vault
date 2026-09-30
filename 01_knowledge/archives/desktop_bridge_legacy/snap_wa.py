import os
import time
import win32gui
import win32con
import win32api
import pyautogui

# Bring WhatsApp to front
def focus_wa():
    hwnds = []
    def cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd)
            if "whatsapp" in t.lower():
                hwnds.append(hwnd)
        return True
    win32gui.EnumWindows(cb, None)
    if hwnds:
        h = hwnds[0]
        win32gui.ShowWindow(h, win32con.SW_RESTORE)
        time.sleep(0.3)
        win32api.keybd_event(18, 0, 0, 0)
        win32gui.SetForegroundWindow(h)
        win32api.keybd_event(18, 0, 2, 0)
        time.sleep(0.5)

focus_wa()
pyautogui.screenshot(r"d:\SecondBrain\00_system\current_wa.png")
