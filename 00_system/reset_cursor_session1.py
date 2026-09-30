import ctypes
import os
import winreg
import subprocess

user32 = ctypes.windll.user32

# Standard Windows Default Cursors (Clean Normal Size)
STANDARD_CURSORS = {
    "(Default)": "Windows Default",
    "Arrow": r"%SystemRoot%\cursors\aero_arrow.cur",
    "Help": r"%SystemRoot%\cursors\aero_helpsel.cur",
    "AppStarting": r"%SystemRoot%\cursors\aero_working.ani",
    "Wait": r"%SystemRoot%\cursors\aero_busy.ani",
    "Crosshair": "",
    "IBeam": "",
    "NWPen": r"%SystemRoot%\cursors\aero_pen.cur",
    "No": r"%SystemRoot%\cursors\aero_unavail.cur",
    "SizeNS": r"%SystemRoot%\cursors\aero_ns.cur",
    "SizeWE": r"%SystemRoot%\cursors\aero_ew.cur",
    "SizeNWSE": r"%SystemRoot%\cursors\aero_nwse.cur",
    "SizeNESW": r"%SystemRoot%\cursors\aero_nesw.cur",
    "SizeAll": r"%SystemRoot%\cursors\aero_move.cur",
    "UpArrow": r"%SystemRoot%\cursors\aero_up.cur",
    "Hand": r"%SystemRoot%\cursors\aero_link.cur",
    "Pin": r"%SystemRoot%\cursors\aero_pin.cur",
    "Person": r"%SystemRoot%\cursors\aero_person.cur"
}

# 1. Update Registry
try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, winreg.KEY_SET_VALUE) as key:
        for name, val in STANDARD_CURSORS.items():
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ if "%" in val else winreg.REG_SZ, val)
        winreg.SetValueEx(key, "Scheme Source", 0, winreg.REG_DWORD, 2)
except Exception as e:
    print("Reg error:", e)

# 2. Reload System Cursors in memory
OCR_MAPPING = {
    32512: r"C:\Windows\Cursors\aero_arrow.cur",      # OCR_NORMAL
    32513: r"C:\Windows\Cursors\aero_helpsel.cur",    # OCR_IBEAM / HELP
    32514: r"C:\Windows\Cursors\aero_busy.ani",       # OCR_WAIT
    32515: r"C:\Windows\Cursors\aero_ew.cur",
    32516: r"C:\Windows\Cursors\aero_ns.cur",
    32640: r"C:\Windows\Cursors\aero_nwse.cur",
    32641: r"C:\Windows\Cursors\aero_nesw.cur",
    32644: r"C:\Windows\Cursors\aero_move.cur",       # OCR_SIZEALL
    32648: r"C:\Windows\Cursors\aero_unavail.cur",    # OCR_NO
    32649: r"C:\Windows\Cursors\aero_link.cur",       # OCR_HAND
    32650: r"C:\Windows\Cursors\aero_working.ani",    # OCR_APPSTARTING
}

user32.LoadCursorFromFileW.restype = ctypes.c_void_p
user32.LoadCursorFromFileW.argtypes = [ctypes.c_wchar_p]

for ocr_id, path in OCR_MAPPING.items():
    if os.path.exists(path):
        hcur = user32.LoadCursorFromFileW(path)
        if hcur:
            user32.SetSystemCursor(hcur, ocr_id)

# 3. SPI_SETCURSORS broadcast
SPI_SETCURSORS = 0x0057
user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, 0x01 | 0x02)

# 4. Trigger system update
subprocess.run(["rundll32.exe", "user32.dll,UpdatePerUserSystemParameters", "1,", "True"], capture_output=True)

print("SUCCESS: Cursor restored to standard clean Windows Default!")
