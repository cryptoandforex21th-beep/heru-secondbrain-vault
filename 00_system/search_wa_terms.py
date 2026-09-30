import win32gui
import win32con
import pyautogui
import time
import pyperclip

def find_whatsapp():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "whatsapp" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    return hwnds

hwnds = find_whatsapp()
if hwnds:
    hwnd = hwnds[0]
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    
    # Search for "office" or "brain" or "ai"
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy("office")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\wa_search_office.png")
    
    # Search for "grup" or "group"
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy("group")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\wa_search_group.png")

    # Search for "ai"
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy("ai")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)
    pyautogui.screenshot(r"d:\SecondBrain\00_system\wa_search_ai.png")
    
    pyautogui.press('esc')
    pyautogui.press('esc')
    print("Done searches")
