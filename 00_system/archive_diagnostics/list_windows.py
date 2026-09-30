import win32gui
import win32process

log_file = r"d:\SecondBrain\00_system\windows_list.log"

with open(log_file, "w", encoding="utf-8") as f:
    def enum_handler(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                f.write(f"HWND: {hwnd} | PID: {pid} | Title: {title}\n")

    win32gui.EnumWindows(enum_handler, None)
