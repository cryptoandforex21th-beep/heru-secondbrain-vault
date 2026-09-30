import os
import sys
import time
import traceback
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\mirror_reply.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

try:
    log("=== Starting WhatsApp Mirror Reply (3 Bubbles) ===")
    import pyautogui
    import pyperclip
    import win32gui
    import win32con
    import win32api

    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.3

    # 1. Find and bring WhatsApp window to front
    whatsapp_hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd)
            if "whatsapp" in t.lower():
                rect = win32gui.GetWindowRect(hwnd)
                if rect[2] - rect[0] > 100 and rect[3] - rect[1] > 100:
                    whatsapp_hwnds.append((hwnd, t, rect))
        return True

    win32gui.EnumWindows(enum_cb, None)
    if not whatsapp_hwnds:
        log("No WhatsApp window found!")
        sys.exit(1)

    target_hwnd, title, rect = whatsapp_hwnds[0]
    log(f"Focusing WhatsApp window: '{title}' at {rect}")
    win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
    time.sleep(0.3)
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(target_hwnd)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(0.8)

    # 2. Click in the message input box
    # rect is (left, top, right, bottom)
    left, top, right, bottom = rect
    input_x = left + int((right - left) * 0.6)
    input_y = bottom - 50
    log(f"Clicking message input box at ({input_x}, {input_y})...")
    pyautogui.click(input_x, input_y)
    time.sleep(0.5)

    # 3. 3 Bubble messages to mirror from Glo MBG
    bubbles = [
        "Deh masa poniku nd rata cuy",
        "Baru kuperbaiki",
        "Kek ka orgil"
    ]

    for idx, b in enumerate(bubbles, 1):
        log(f"Sending Bubble {idx}/3: '{b}'")
        pyperclip.copy(b)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1.2)

    # 4. Take confirmation screenshot
    screenshot_path = Path(r"d:\SecondBrain\00_system\whatsapp_mirrored.png")
    pyautogui.screenshot(str(screenshot_path))
    log(f"Screenshot saved to {screenshot_path}")
    log("=== Mirror Reply Finished Successfully ===")

except Exception as ex:
    err = traceback.format_exc()
    log(f"ERROR: {err}")
    sys.exit(1)
