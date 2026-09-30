import sys
import time
import win32gui
import win32con
import win32api
from pathlib import Path
from pywinauto import Desktop

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\find_messages_2.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

try:
    log("=== Finding WinUI 3 Elements ===")
    app = Desktop(backend="uia")
    wins = [x for x in app.windows() if "whatsapp" in x.window_text().lower()]
    if not wins:
        log("No WhatsApp window found")
        sys.exit(1)
        
    wa = wins[0]
    hwnd = wa.handle
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32api.keybd_event(18, 0, 0, 0)
    win32gui.SetForegroundWindow(hwnd)
    win32api.keybd_event(18, 0, 2, 0)
    time.sleep(1)

    bridge = None
    for c in wa.children():
        if "DesktopChildSiteBridge" in c.element_info.class_name:
            bridge = c
            break

    if not bridge:
        log("Bridge not found, checking direct wa children")
        bridge = wa

    log(f"Bridge element: {bridge.element_info.class_name}, children count: {len(bridge.children())}")
    for idx, c in enumerate(bridge.children()):
        info = c.element_info
        log(f"L1 Child {idx}: {info.control_type} | Name: '{info.name}' | Class: {info.class_name}")
        for jdx, cc in enumerate(c.children()):
            cinfo = cc.element_info
            log(f"  L2 Child {jdx}: {cinfo.control_type} | Name: '{cinfo.name}' | Class: {cinfo.class_name}")

except Exception as ex:
    import traceback
    log(f"Error: {traceback.format_exc()}")
