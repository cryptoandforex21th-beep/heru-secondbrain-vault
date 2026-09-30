import win32gui
import win32con
import win32api
import pyautogui
import time

hwnd = 398342  # Revit Home HWND

# Ensure Revit Home is focused and active
def enum_cb(h, _):
    global hwnd
    if win32gui.IsWindowVisible(h):
        t = win32gui.GetWindowText(h)
        if "Autodesk Revit" in t:
            hwnd = h
win32gui.EnumWindows(enum_cb, None)

if hwnd:
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(hwnd)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(2)

# Click on PROJECT MENARA thumbnail (x=265, y=250)
print("Clicking PROJECT MENARA thumbnail at (265, 250)...")
pyautogui.click(265, 250)

print("Waiting 30 seconds for PROJECT MENARA DYNAMO to open...")
time.sleep(30)

# Bring to top and screenshot
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
time.sleep(1)
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
time.sleep(1)

pyautogui.screenshot(r"d:\SecondBrain\00_system\menara_opened_addins.png")
print("Saved screenshot to menara_opened_addins.png")
