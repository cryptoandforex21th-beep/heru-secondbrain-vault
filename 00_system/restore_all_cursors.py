import ctypes
import os
import winreg

user32 = ctypes.windll.user32
user32.LoadCursorFromFileW.restype = ctypes.c_void_p
user32.LoadCursorFromFileW.argtypes = [ctypes.c_wchar_p]

OCR_MAPPING = {
    "Arrow": 32512,       # OCR_NORMAL
    "IBeam": 32513,       # OCR_IBEAM
    "Wait": 32514,        # OCR_WAIT
    "Crosshair": 32515,   # OCR_CROSS
    "UpArrow": 32516,     # OCR_UP
    "SizeNWSE": 32642,    # OCR_SIZENWSE
    "SizeNESW": 32643,    # OCR_SIZENESW
    "SizeWE": 32644,      # OCR_SIZEWE
    "SizeNS": 32645,      # OCR_SIZENS
    "SizeAll": 32646,     # OCR_SIZEALL
    "No": 32648,          # OCR_NO
    "Hand": 32649,        # OCR_HAND
    "AppStarting": 32650  # OCR_APPSTARTING
}

restored = []
try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors") as key:
        for name, ocr_id in OCR_MAPPING.items():
            try:
                val, _ = winreg.QueryValueEx(key, name)
                if val and os.path.exists(val):
                    hcur = user32.LoadCursorFromFileW(val)
                    if hcur:
                        res = user32.SetSystemCursor(hcur, ocr_id)
                        restored.append(f"{name}: {res}")
            except Exception as e:
                pass
except Exception as e:
    restored.append(f"Reg err: {e}")

with open(r"d:\SecondBrain\00_system\restore_all_cursors.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(restored) + "\n")
