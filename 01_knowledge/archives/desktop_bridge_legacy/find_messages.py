import sys
import time
from pathlib import Path
from pywinauto import Desktop

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\find_messages.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

try:
    log("=== Finding Messages in WhatsApp ===")
    app = Desktop(backend="uia")
    wins = [x for x in app.windows() if "whatsapp" in x.window_text().lower()]
    if not wins:
        log("No WhatsApp window found")
        sys.exit(1)
        
    wa = wins[0]
    log(f"Window: {wa.window_text()}")
    
    # Check direct children
    for idx, c in enumerate(wa.children()):
        info = c.element_info
        log(f"Child {idx}: {info.control_type} | Name: '{info.name}' | Class: {info.class_name} | Rect: {info.rectangle}")

except Exception as ex:
    import traceback
    log(f"Error: {traceback.format_exc()}")
