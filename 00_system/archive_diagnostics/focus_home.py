import win32gui
import win32con
import win32api
import pyautogui
import time

hwnd = 398342  # HWND for Revit 2027.3 Home

print(f"Bringing HWND {hwnd} to front...")
try:
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(hwnd)
    win32api.keybd_event(18, 0, 2, 0)
except Exception as e:
    print(f"Focus error: {e}")

time.sleep(2)
pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_home_verified.png")
print("Saved screenshot to revit_home_verified.png")
