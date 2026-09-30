import ctypes
import os
import winreg

user32 = ctypes.windll.user32

SPI_SETCURSORS = 0x0057
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02
OCR_NORMAL = 32512

log_lines = []

# 1. Read registry
arrow_path = r"C:\WINDOWS\cursors\aero_arrow_l.cur"
try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors") as key:
        val, _ = winreg.QueryValueEx(key, "Arrow")
        if val and os.path.exists(val):
            arrow_path = val
    log_lines.append(f"Registry Arrow: {arrow_path}")
except Exception as e:
    log_lines.append(f"Reg error: {e}")

# 2. Explicit SetSystemCursor if file exists
if os.path.exists(arrow_path):
    # LoadCursorFromFileW
    user32.LoadCursorFromFileW.restype = ctypes.c_void_p
    user32.LoadCursorFromFileW.argtypes = [ctypes.c_wchar_p]
    hcur = user32.LoadCursorFromFileW(arrow_path)
    log_lines.append(f"hcur loaded: {hcur}")
    if hcur:
        res = user32.SetSystemCursor(hcur, OCR_NORMAL)
        log_lines.append(f"SetSystemCursor result: {res}")

# 3. Broadcast SystemParametersInfoW SPI_SETCURSORS
spi_res = user32.SystemParametersInfoW(SPI_SETCURSORS, 0, 0, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
log_lines.append(f"SystemParametersInfoW SPI_SETCURSORS result: {spi_res}")

with open(r"d:\SecondBrain\00_system\restore_cursor_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines) + "\n")
