import os
import subprocess
import time
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import win32gui
import win32con
import win32process
import pyautogui

app = FastAPI(title="Antigravity Desktop Bridge", version="1.0.0")

# Safety settings for pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

class LaunchRequest(BaseModel):
    command: str
    args: Optional[List[str]] = []
    working_dir: Optional[str] = None

class FocusRequest(BaseModel):
    title_pattern: str

class ClickRequest(BaseModel):
    x: int
    y: int
    clicks: int = 1
    button: str = "left"

class TypeRequest(BaseModel):
    text: str
    press_enter: bool = False

class PressRequest(BaseModel):
    key: str

class ScreenshotRequest(BaseModel):
    save_path: Optional[str] = None

@app.get("/health")
def health():
    size = pyautogui.size()
    return {"status": "running", "screen_width": size.width, "screen_height": size.height}

@app.get("/windows")
def list_windows():
    """Mengembalikan daftar semua jendela aktif yang terlihat."""
    windows = []
    def enum_handler(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title and not win32gui.IsIconic(hwnd):
                rect = win32gui.GetWindowRect(hwnd)
                windows.append({
                    "hwnd": hwnd,
                    "title": title,
                    "rect": {"left": rect[0], "top": rect[1], "right": rect[2], "bottom": rect[3]}
                })
        return True
    win32gui.EnumWindows(enum_handler, None)
    return {"windows": windows}

@app.post("/launch")
def launch_app(req: LaunchRequest):
    """Membuka aplikasi atau dokumen secara visual di layar desktop."""
    try:
        cmd_list = [req.command] + (req.args or [])
        cwd = req.working_dir if req.working_dir else os.path.dirname(req.command) if os.path.exists(req.command) else None
        
        # Menggunakan explorer.exe atau start untuk memunculkan antarmuka grafis
        if os.path.isfile(req.command) and not req.command.lower().endswith(".exe"):
            os.startfile(req.command)
        else:
            subprocess.Popen(cmd_list, cwd=cwd, shell=True)
            
        return {"status": "launched", "command": req.command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/focus")
def focus_window(req: FocusRequest):
    """Mencari jendela berdasarkan nama dan membawanya ke layar paling depan."""
    pattern = req.title_pattern.lower()
    target_hwnd = None
    target_title = None

    def enum_handler(hwnd, extra):
        nonlocal target_hwnd, target_title
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title and pattern in title.lower():
                target_hwnd = hwnd
                target_title = title
                return False
        return True

    try:
        win32gui.EnumWindows(enum_handler, None)
    except Exception:
        pass

    if target_hwnd:
        try:
            import win32gui, win32con, win32api
            win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
            win32api.keybd_event(18, 0, 0, 0)
            win32gui.SetForegroundWindow(target_hwnd)
            win32api.keybd_event(18, 0, 2, 0)
        except Exception:
            pass
        return {"status": "focused", "title": target_title, "hwnd": target_hwnd}
    
    raise HTTPException(status_code=404, detail=f"Jendela dengan kata '{req.title_pattern}' tidak ditemukan.")

@app.post("/screenshot")
def take_screenshot(req: ScreenshotRequest):
    """Mengambil tangkapan layar monitor."""
    default_dir = Path("d:/SecondBrain/00_system")
    default_dir.mkdir(parents=True, exist_ok=True)
    save_file = Path(req.save_path) if req.save_path else default_dir / f"screenshot_{int(time.time())}.png"
    
    screenshot = pyautogui.screenshot()
    screenshot.save(str(save_file))
    return {"status": "saved", "path": str(save_file)}

@app.post("/click")
def click(req: ClickRequest):
    """Menggerakkan mouse dan mengeklik koordinat tertentu di layar."""
    pyautogui.click(req.x, req.y, clicks=req.clicks, button=req.button)
    return {"status": "clicked", "x": req.x, "y": req.y}

@app.post("/type")
def type_text(req: TypeRequest):
    """Mengetik teks pada jendela yang sedang aktif."""
    pyautogui.write(req.text, interval=0.03)
    if req.press_enter:
        pyautogui.press("enter")
    return {"status": "typed", "text": req.text}

@app.post("/press")
def press_key(req: PressRequest):
    """Menekan tombol keyboard tertentu (misal: 'enter', 'esc', 'tab')."""
    pyautogui.press(req.key)
    return {"status": "pressed", "key": req.key}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=49999, log_level="info")
