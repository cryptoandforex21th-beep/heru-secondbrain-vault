import win32gui
import win32con
import pyautogui
import time

def find_edge():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "edge" in title or "secondbrain" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    return hwnds

hwnds = find_edge()
if hwnds:
    hwnd = hwnds[0]
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'f5')
    print("Edge refreshed with Ctrl+F5")
