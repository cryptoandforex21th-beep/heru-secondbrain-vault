import pyautogui
import pyperclip
import time
import win32gui
import win32con
import win32api

def bring_wa():
    hwnds = []
    def enum_cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd).lower()
            if 'whatsapp' in t:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    if hwnds:
        h = hwnds[0]
        win32gui.ShowWindow(h, win32con.SW_RESTORE)
        win32api.keybd_event(18, 0, 0, 0)
        win32gui.SetForegroundWindow(h)
        win32api.keybd_event(18, 0, 2, 0)
        time.sleep(0.5)
        return True
    return False

if bring_wa():
    # Press Ctrl+F to search
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy('bot')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\wa_search_bot.png")
