import time
import httpx
from pathlib import Path

log_file = Path(r"d:\SecondBrain\02_skills\desktop_bridge\monitor_revit.log")
def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

log("=== Monitoring Revit and pyRevit MCP Status ===")
API_URL = "http://127.0.0.1:48884/revit_mcp/status/"

start_time = time.time()
connected = False

while time.time() - start_time < 120: # wait up to 2 minutes
    try:
        r = httpx.get(API_URL, timeout=2.0)
        log(f"Status Code: {r.status_code}, Response: {r.text}")
        if r.status_code == 200:
            data = r.json()
            log(f"SUCCESS! Connected to pyRevit: {data}")
            connected = True
            break
        elif r.status_code == 503:
            log("pyRevit routes online! Loading document...")
    except Exception as e:
        # Not yet listening
        pass
    time.sleep(3)

if not connected:
    log("Timed out waiting for pyRevit status 200 (Revit might still be loading plugins/file).")
