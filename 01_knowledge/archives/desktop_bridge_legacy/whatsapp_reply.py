import os
import sys
import time
import subprocess
import traceback
from pathlib import Path

# Setup logging
log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\whatsapp_reply.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

try:
    log("=== Starting WhatsApp Automated Reply ===")
    import pyautogui
    import pyperclip
    import win32gui
    import win32con
    import win32process
    import win32api

    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.2

    # 1. Launch WhatsApp
    log("Step 1: Launching / Bringing WhatsApp to front...")
    os.system('explorer.exe shell:AppsFolder\\5319275A.51895FA4EA97F_cv1g1gvanyjgm!App')
    time.sleep(2.5)

    # 2. Find WhatsApp Window
    log("Step 2: Searching for WhatsApp window...")
    whatsapp_hwnds = []
    
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "whatsapp" in title.lower():
                rect = win32gui.GetWindowRect(hwnd)
                # Ignore zero-size or minimized windows
                if rect[2] - rect[0] > 100 and rect[3] - rect[1] > 100:
                    whatsapp_hwnds.append((hwnd, title, rect))
        return True

    win32gui.EnumWindows(enum_cb, None)
    log(f"Found {len(whatsapp_hwnds)} potential WhatsApp windows: {whatsapp_hwnds}")

    target_hwnd = None
    if whatsapp_hwnds:
        target_hwnd = whatsapp_hwnds[0][0]

    if target_hwnd:
        log(f"Targeting window HWND: {target_hwnd}")
        try:
            win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
            time.sleep(0.5)
            # Alt trick to allow SetForegroundWindow
            win32api.keybd_event(18, 0, 0, 0)
            win32gui.SetForegroundWindow(target_hwnd)
            win32api.keybd_event(18, 0, 2, 0)
            time.sleep(0.8)
        except Exception as e:
            log(f"Warning setting foreground: {e}")
    else:
        log("No specific WhatsApp HWND identified; proceeding with global foreground.")

    # 3. Search for contact "glo mbg"
    log("Step 3: Triggering Search with Ctrl+F...")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.8)

    # Clear any previous search text
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.2)

    log("Typing contact name 'glo mbg'...")
    pyperclip.copy("glo mbg")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)

    # Press Enter to select search result or Down arrow + Enter
    log("Selecting search result...")
    pyautogui.press('down')
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(1.0)

    # 4. Paste message and take pre-send screenshot
    message = "iya sayang, aamiin. kamu sekarang lagi apa?"
    log(f"Step 4: Pasting reply message: '{message}'")
    pyperclip.copy(message)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.8)

    screenshot_pre = Path(r"d:\SecondBrain\00_system\whatsapp_pre_send.png")
    pyautogui.screenshot(str(screenshot_pre))
    log(f"Pre-send screenshot saved to {screenshot_pre}")

    # 5. Send message
    log("Step 5: Pressing Enter to send message...")
    pyautogui.press('enter')
    time.sleep(1.0)

    screenshot_post = Path(r"d:\SecondBrain\00_system\whatsapp_post_send.png")
    pyautogui.screenshot(str(screenshot_post))
    log(f"Post-send screenshot saved to {screenshot_post}")

    log("=== WhatsApp Automated Reply Finished Successfully ===")

except Exception as ex:
    err = traceback.format_exc()
    log(f"ERROR: {err}")
    sys.exit(1)
