import time
import win32gui
import win32con
import win32api
import pyperclip
import pyautogui

def bring_edge():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "gemini" in title or "edge" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    if hwnds:
        hwnd = hwnds[0]
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32api.keybd_event(18, 0, 0, 0)
        win32gui.SetForegroundWindow(hwnd)
        win32api.keybd_event(18, 0, 2, 0)
        time.sleep(0.5)
        return True
    return False

def test_input():
    bring_edge()
    time.sleep(0.5)
    
    # Click Nama box
    pyautogui.click(350, 254)
    time.sleep(0.5)
    
    # Try typing directly
    pyautogui.write("Profesor LUNA", interval=0.03)
    time.sleep(0.5)

    pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_type_test.png")
    with open(r"d:\SecondBrain\00_system\gemini_diag.log", "w", encoding="utf-8") as f:
        f.write("Typed directly.\n")

test_input()