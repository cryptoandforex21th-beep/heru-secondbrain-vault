import os
import time
import pyautogui
import win32gui

os.system('start whatsapp:')
time.sleep(3)

pyautogui.screenshot(r"d:\SecondBrain\00_system\screen_whatsapp.png")

windows = []
def enum_cb(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        t = win32gui.GetWindowText(hwnd)
        if t:
            windows.append(t)
win32gui.EnumWindows(enum_cb, None)

with open(r"d:\SecondBrain\00_system\wa_windows.log", "w", encoding="utf-8") as f:
    f.write("\n".join(windows))
