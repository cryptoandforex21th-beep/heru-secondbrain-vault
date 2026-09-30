import win32gui
import win32con
import pyautogui
import time
import os
import traceback

LOG_FILE = r"d:\SecondBrain\00_system\switch_youtube.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg)

pyautogui.FAILSAFE = False

try:
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("--- Starting Tab Switcher ---\n")

    def get_edge_main_window():
        edge_hwnds = []
        def enum_cb(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "edge" in title.lower() and win32gui.GetWindowRect(hwnd)[2] > 500:
                    edge_hwnds.append((hwnd, title))
        win32gui.EnumWindows(enum_cb, None)
        return edge_hwnds

    windows = get_edge_main_window()
    log(f"Found {len(windows)} main Edge windows:")
    for h, t in windows:
        log(f" - {h}: {t}")

    if windows:
        target_hwnd = windows[0][0]
        log(f"Targeting Edge HWND: {target_hwnd}")
        
        # Bring Edge to front
        win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
        pyautogui.press("alt")
        time.sleep(0.05)
        win32gui.SetForegroundWindow(target_hwnd)
        time.sleep(0.3)
        
        # 1. Search for YouTube tab (Ctrl+Shift+A)
        log("Opening Tab Search (Ctrl+Shift+A)...")
        pyautogui.hotkey("ctrl", "shift", "a")
        time.sleep(0.4)
        
        # 2. Type 'youtube' and enter
        log("Searching 'youtube' tab...")
        pyautogui.write("youtube", interval=0.02)
        time.sleep(0.3)
        pyautogui.press("enter")
        time.sleep(0.6)
        
        # 3. Pause the video (press 'k')
        log("Pausing video (pressing 'k')...")
        pyautogui.press("k")
        time.sleep(0.3)
        
        # 4. Focus address bar (Ctrl+L) and navigate to Jokowi video
        log("Navigating to Jokowi video...")
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.2)
        pyautogui.write("https://www.youtube.com/watch?v=sO2g0Uv-V58", interval=0.01)
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(0.5)
        
        log("SUCCESS: Replaced YouTube tab with Jokowi video!")
    else:
        log("No Edge window found, launching direct...")
        os.system('start "" "https://www.youtube.com/watch?v=sO2g0Uv-V58"')
except Exception as e:
    log(f"Fatal error: {e}\n{traceback.format_exc()}")
