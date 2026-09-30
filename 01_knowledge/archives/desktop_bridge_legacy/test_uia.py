import os
import sys
import time
import win32gui
import win32con
import win32api
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\uia_test.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

try:
    log("=== Testing UIA on WhatsApp ===")
    from pywinauto import Desktop

    # Bring WhatsApp to front
    os.system('explorer.exe shell:AppsFolder\\5319275A.51895FA4EA97F_cv1g1gvanyjgm!App')
    time.sleep(2)

    app = Desktop(backend="uia")
    # Find window with title containing WhatsApp
    wa_win = None
    for win in app.windows():
        title = win.window_text()
        if "whatsapp" in title.lower():
            wa_win = win
            break
            
    if not wa_win:
        log("WhatsApp window not found via pywinauto Desktop")
        sys.exit(1)

    log(f"Found WhatsApp window: '{wa_win.window_text()}'")
    wa_win.set_focus()
    time.sleep(1)

    # Let's inspect descendants
    descendants = wa_win.descendants()
    log(f"Total descendants: {len(descendants)}")
    
    # Filter for Text or ListItem or Edit controls
    items = []
    for d in descendants:
        try:
            ctrl_type = d.element_info.control_type
            text = d.window_text()
            if text and len(text.strip()) > 0:
                items.append(f"[{ctrl_type}] {text.strip()}")
        except Exception:
            pass

    log(f"Total named elements found: {len(items)}")
    with open(r"d:\SecondBrain\02_skills\desktop_bridge\wa_elements.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(items))

    log("Saved elements to wa_elements.txt")
except Exception as ex:
    import traceback
    log(f"Error: {traceback.format_exc()}")
