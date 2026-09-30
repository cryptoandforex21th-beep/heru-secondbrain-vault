import time
import win32gui
import win32con
import win32api
import win32process
import pyperclip
import pyautogui

def set_foreground(hwnd):
    cur_thread = win32api.GetCurrentThreadId()
    target_thread, _ = win32process.GetWindowThreadProcessId(hwnd)
    win32process.AttachThreadInput(cur_thread, target_thread, True)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    win32process.AttachThreadInput(cur_thread, target_thread, False)

def find_edge():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "gemini" in title or "edge" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    return hwnds[0] if hwnds else None

hwnd = find_edge()
if hwnd:
    set_foreground(hwnd)
    time.sleep(0.3)
    # Click Console tab in DevTools
    pyautogui.click(1555, 95)
    time.sleep(0.5)

    # Click in the console area (e.g. at x=1550, y=300) to ensure focus
    pyautogui.click(1550, 300)
    time.sleep(0.3)

    # Write a test command
    js = """console.log("DEVTOOLS CONSOLE IS READY");"""
    pyperclip.copy(js)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1.0)

    pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_console_active.png")