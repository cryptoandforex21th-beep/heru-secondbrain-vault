import sys
import time
from pathlib import Path
from pywinauto import Desktop

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\find_messages_3.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

try:
    log("=== Inspecting BrowserRootView ===")
    app = Desktop(backend="uia")
    wins = [x for x in app.windows() if "whatsapp" in x.window_text().lower()]
    wa = wins[0]
    
    # Find BrowserRootView
    root_view = None
    for d in wa.descendants(depth=4):
        if d.element_info.class_name == "BrowserRootView":
            root_view = d
            break
            
    if not root_view:
        log("BrowserRootView not found")
        sys.exit(1)
        
    log(f"Found BrowserRootView: {root_view.element_info.name}")
    
    # Find all text elements inside root_view
    texts = []
    for el in root_view.descendants():
        info = el.element_info
        if info.control_type in ["Text", "ListItem", "Edit", "Button"]:
            name = info.name.strip()
            if name:
                texts.append(f"[{info.control_type}] {name}")
                if len(texts) > 200: # prevent infinite loop
                    break

    log(f"Found {len(texts)} text/list elements. Samples:")
    for t in texts[-40:]:
        log(f"  {t}")

except Exception as ex:
    import traceback
    log(f"Error: {traceback.format_exc()}")
