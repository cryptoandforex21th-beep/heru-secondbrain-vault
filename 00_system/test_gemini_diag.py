import time
import win32gui
import win32con
import win32api
import pyperclip
import pyautogui

def nav_to_gemini():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "edge" in title or "gemini" in title or "chess" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    if hwnds:
        hwnd = hwnds[0]
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32api.keybd_event(18, 0, 0, 0)
        win32gui.SetForegroundWindow(hwnd)
        win32api.keybd_event(18, 0, 2, 0)
        time.sleep(0.5)

        # Open new tab with Ctrl+T
        pyautogui.hotkey('ctrl', 't')
        time.sleep(0.5)

        # Paste URL
        pyperclip.copy("https://gemini.google.com/gems/create")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        pyautogui.press('enter')

        # Wait for page to load
        time.sleep(4.0)

        # Capture screenshot
        pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_create_screen.png")
        with open(r"d:\SecondBrain\00_system\gemini_diag.log", "w") as f:
            f.write("Navigated to gemini gems create and captured.\n")

nav_to_gemini()