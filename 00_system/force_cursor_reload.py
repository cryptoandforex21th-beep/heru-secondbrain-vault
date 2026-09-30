import ctypes
import os
import subprocess
import winreg

user32 = ctypes.windll.user32

# 1. Ensure registry has standard aero_arrow.cur
try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Arrow", 0, winreg.REG_EXPAND_SZ, r"%SystemRoot%\cursors\aero_arrow.cur")
        winreg.SetValueEx(key, "(Default)", 0, winreg.REG_SZ, "Windows Default")
except Exception as e:
    print("Reg set error:", e)

# 2. SetSystemCursor directly to standard arrow
arrow_path = r"C:\Windows\Cursors\aero_arrow.cur"
if os.path.exists(arrow_path):
    user32.LoadCursorFromFileW.restype = ctypes.c_void_p
    user32.LoadCursorFromFileW.argtypes = [ctypes.c_wchar_p]
    hcur = user32.LoadCursorFromFileW(arrow_path)
    if hcur:
        user32.SetSystemCursor(hcur, 32512)

# 3. SPI_SETCURSORS
user32.SystemParametersInfoW(0x0057, 0, None, 0x01 | 0x02)

# 4. Trigger system update
subprocess.run(["rundll32.exe", "user32.dll,UpdatePerUserSystemParameters", "1,", "True"], capture_output=True)

print("Cursor fully refreshed!")
