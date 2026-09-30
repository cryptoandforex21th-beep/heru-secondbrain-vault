import time
import win32gui
import win32api
import win32con
import win32process
import pyautogui
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\revit_clean.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

log("=== Checking Revit Status in Session 1 ===")
revit_hwnds = []
def cb(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if "revit" in title.lower():
            rect = win32gui.GetWindowRect(hwnd)
            revit_hwnds.append((hwnd, title, rect))
    return True

win32gui.EnumWindows(cb, None)
log(f"Visible Revit windows: {revit_hwnds}")

main_win = None
for h, t, r in revit_hwnds:
    if "autodesk revit" in t.lower() or "project menara dynamo" in t.lower():
        main_win = h
        break
if not main_win and revit_hwnds:
    main_win = revit_hwnds[0][0]

if main_win:
    log(f"Bringing Revit window {main_win} to foreground gently...")
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(main_win)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(1.0)

pyautogui.screenshot(r"d:\SecondBrain\00_system\revit_foreground.png")
log("Saved screenshot to revit_foreground.png")
