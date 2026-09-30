import win32gui
import win32con
import win32api
import pyautogui
import time

hwnd = 398342  # HWND of Revit Home

if win32gui.IsWindow(hwnd):
    print(f"Bringing HWND {hwnd} to top...")
    # Set to TOPMOST temporarily
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    time.sleep(1)
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    time.sleep(1)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_home_top.png")
    print("Screenshot saved to revit_home_top.png")
else:
    print("HWND not valid. Finding current Revit HWND...")
    def enum_cb(h, _):
        if win32gui.IsWindowVisible(h):
            t = win32gui.GetWindowText(h)
            if "Autodesk Revit" in t or "Revit 2027" in t:
                print(f"Found Revit HWND: {h} Title: '{t}'")
                win32gui.ShowWindow(h, win32con.SW_MAXIMIZE)
                win32gui.SetWindowPos(h, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                time.sleep(1)
                win32gui.SetWindowPos(h, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                time.sleep(1)
                pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_home_top.png")
    win32gui.EnumWindows(enum_cb, None)
