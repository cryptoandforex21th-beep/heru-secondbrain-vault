import time
import sys
import traceback

log_path = r"d:\SecondBrain\00_system\gemini_diag.log"

try:
    import win32gui
    import win32con
    import win32api
    import win32process
    import pyautogui

    def set_foreground(hwnd):
        cur_thread = win32api.GetCurrentThreadId()
        target_thread, _ = win32process.GetWindowThreadProcessId(hwnd)
        win32process.AttachThreadInput(cur_thread, target_thread, True)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        win32process.AttachThreadInput(cur_thread, target_thread, False)

    def find_edge():
        hwnds = []
        def enum_cb(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).lower()
                if "gemini" in title or "edge" in title:
                    hwnds.append(hwnd)
        win32gui.EnumWindows(enum_cb, None)
        return hwnds[0] if hwnds else None

    hwnd = find_edge()
    if hwnd:
        set_foreground(hwnd)
        time.sleep(0.5)

        pos_before = pyautogui.position()
        pyautogui.moveTo(350, 250, duration=0.2)
        pos_after = pyautogui.position()
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.typewrite("Profesor LUNA", interval=0.05)
        time.sleep(0.5)
        pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_clean_test.png")
        
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"SUCCESS: Pos before: {pos_before}, after moveTo: {pos_after}\n")
    else:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("ERROR: Edge not found\n")
except Exception as e:
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("EXCEPTION: " + traceback.format_exc() + "\n")