import time
import win32gui
import win32process
import win32api
import win32con
import pyautogui
import pyperclip
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\pid_revit.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

log("=== Finding Windows for Revit PID 31220 ===")

revit_hwnds = []
def cb(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid == 31220:
            title = win32gui.GetWindowText(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            revit_hwnds.append((hwnd, title, rect))
    return True

win32gui.EnumWindows(cb, None)
log(f"Found windows for PID 31220: {revit_hwnds}")

# Find main window (biggest width)
main_hwnd = None
max_w = 0
for h, t, r in revit_hwnds:
    w = r[2] - r[0]
    if w > max_w:
        max_w = w
        main_hwnd = h

if main_hwnd:
    log(f"Focusing Main Revit HWND {main_hwnd}...")
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(main_hwnd)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(1.0)
    
    # Send Ctrl+O
    log("Pressing Ctrl+O...")
    pyautogui.hotkey('ctrl', 'o')
    time.sleep(2.0)
    
    # Paste path
    proj = r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt"
    pyperclip.copy(proj)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    log("Pressed enter, waiting 10s...")
    time.sleep(10.0)

pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_final_view.png")
log("Screenshot saved!")
