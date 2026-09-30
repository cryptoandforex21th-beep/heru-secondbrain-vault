import time
import win32gui
import win32con
import win32api
import win32process
import pyautogui

def set_foreground(hwnd):
    cur_thread = win32api.GetCurrentThreadId()
    target_thread, _ = win32process.GetWindowThreadProcessId(hwnd)
    win32process.AttachThreadInput(cur_thread, target_thread, True)
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(hwnd)
    win32process.AttachThreadInput(cur_thread, target_thread, False)

def find_edge():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "edge" in title or "chess" in title or "gemini" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    return hwnds[0] if hwnds else None

hwnd = find_edge()
if hwnd:
    set_foreground(hwnd)
    time.sleep(0.3)
    # Ctrl + 9 switches to the last tab in Edge
    pyautogui.hotkey('ctrl', '9')
    time.sleep(1.5)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_tab_active.png")