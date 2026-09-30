"""
Client helper untuk memanggil Antigravity Desktop Bridge (Otomatis & Tanpa Jendela Hitam)
"""
import time
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
import httpx

BRIDGE_URL = "http://127.0.0.1:49999"
SERVER_SCRIPT = Path(r"d:\SecondBrain\02_skills\desktop_bridge\bridge_server.py")
PYTHONW_EXE = Path(r"C:\Python314\pythonw.exe")

def ensure_bridge_running():
    """Memastikan bridge berjalan secara hening (silent) tanpa jendela hitam."""
    if not is_bridge_running():
        if PYTHONW_EXE.exists() and SERVER_SCRIPT.exists():
            subprocess.Popen([str(PYTHONW_EXE), str(SERVER_SCRIPT)], creationflags=0x08000000)  # CREATE_NO_WINDOW
            for _ in range(15):
                time.sleep(0.3)
                if is_bridge_running():
                    break

def is_bridge_running() -> bool:
    try:
        r = httpx.get(f"{BRIDGE_URL}/health", timeout=1.0)
        return r.status_code == 200
    except Exception:
        return False

def launch(command: str, args: Optional[List[str]] = None, working_dir: Optional[str] = None) -> Dict[str, Any]:
    ensure_bridge_running()
    r = httpx.post(f"{BRIDGE_URL}/launch", json={"command": command, "args": args or [], "working_dir": working_dir}, timeout=10.0)
    return r.json()

def focus_window(title_pattern: str) -> Dict[str, Any]:
    ensure_bridge_running()
    r = httpx.post(f"{BRIDGE_URL}/focus", json={"title_pattern": title_pattern}, timeout=5.0)
    return r.json()

def screenshot(save_path: Optional[str] = None) -> Dict[str, Any]:
    ensure_bridge_running()
    r = httpx.post(f"{BRIDGE_URL}/screenshot", json={"save_path": save_path}, timeout=10.0)
    return r.json()

def click(x: int, y: int, clicks: int = 1, button: str = "left") -> Dict[str, Any]:
    ensure_bridge_running()
    r = httpx.post(f"{BRIDGE_URL}/click", json={"x": x, "y": y, "clicks": clicks, "button": button}, timeout=5.0)
    return r.json()

def type_text(text: str, press_enter: bool = False) -> Dict[str, Any]:
    ensure_bridge_running()
    r = httpx.post(f"{BRIDGE_URL}/type", json={"text": text, "press_enter": press_enter}, timeout=10.0)
    return r.json()

def press(key: str) -> Dict[str, Any]:
    ensure_bridge_running()
    r = httpx.post(f"{BRIDGE_URL}/press", json={"key": key}, timeout=5.0)
    return r.json()

def list_windows() -> List[Dict[str, Any]]:
    ensure_bridge_running()
    r = httpx.get(f"{BRIDGE_URL}/windows", timeout=5.0)
    return r.json().get("windows", [])

def open_edge(url: Optional[str] = None, profile_dir: str = "Default") -> Dict[str, Any]:
    """Membuka Microsoft Edge dengan profil default Heru (bukan Guest/Tamu)."""
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    args = [f'--profile-directory={profile_dir}']
    if url:
        args.append(url)
    return launch(edge_exe, args=args)

