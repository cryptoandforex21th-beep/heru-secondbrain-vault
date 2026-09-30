import sys
import time
import subprocess
import os
import win32gui
import win32con
import win32api
import pyperclip
import pyautogui
from PIL import Image
import win32clipboard
import io

LOG_FILE = r"d:\SecondBrain\00_system\whatsapp_debug.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")
    print(msg)

def find_whatsapp_window():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            cls = win32gui.GetClassName(hwnd).lower()
            if title == "whatsapp beta" or title == "whatsapp":
                hwnds.append((hwnd, title, cls))
    win32gui.EnumWindows(enum_cb, None)
    return hwnds

def bring_to_foreground(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32api.keybd_event(18, 0, 0, 0)
        win32gui.SetForegroundWindow(hwnd)
        win32api.keybd_event(18, 0, 2, 0)
        time.sleep(0.3)
    except Exception as e:
        log(f"Warn: {e}")

def copy_image_to_clipboard(filepath):
    log(f"Loading image from {filepath}")
    image = Image.open(filepath)
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
    log("Image copied to clipboard successfully.")

def send_whatsapp_message(contact, message):
    log(f"--- Starting send to '{contact}' ---")
    log(f"Message: {message}")
    
    windows = find_whatsapp_window()
    if not windows:
        log("WhatsApp window not found, launching...")
        os.system('start whatsapp:')
        time.sleep(2.5)
        windows = find_whatsapp_window()
        
    if not windows:
        log("Fallback launching UWP...")
        os.system(r'explorer.exe shell:AppsFolder\5319275A.51895FA4EA97F_cv1g1gvanyjgm!App')
        time.sleep(2.5)
        windows = find_whatsapp_window()

    if not windows:
        log("ERROR: Could not open WhatsApp.")
        return False

    hwnd = windows[0][0]
    log(f"Found window HWND: {hwnd}")
    bring_to_foreground(hwnd)
    time.sleep(1.0) # increased sleep

    log("Typing ctrl+f")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)

    log("Clearing search and pasting contact")
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(contact)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)

    log("Selecting contact")
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1.5) 

    log("Pasting message")
    if os.path.isfile(message):
        log("Message is a file!")
        try:
            copy_image_to_clipboard(message)
        except Exception as e:
            log(f"Failed to copy image: {e}")
            subprocess.run(["powershell", "-command", f"Set-Clipboard -Path '{message}'"])
        
        time.sleep(0.5)
        log("Pressing ctrl+v")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2.5)
        log("Pressing enter to send image preview")
        pyautogui.press('enter')
        time.sleep(1.0)
    else:
        log("Message is text!")
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)

    screenshot_path = r"d:\SecondBrain\00_system\whatsapp_last_sent.png"
    pyautogui.screenshot(screenshot_path)
    log(f"SUCCESS: Verification saved to {screenshot_path}.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    send_whatsapp_message(sys.argv[1], " ".join(sys.argv[2:]))

