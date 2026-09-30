import time
import win32gui
import win32con
import pyautogui

def cb(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title == "pyRevit":
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    return True

win32gui.EnumWindows(cb, None)
time.sleep(1.5)

pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_final_clean.png")
