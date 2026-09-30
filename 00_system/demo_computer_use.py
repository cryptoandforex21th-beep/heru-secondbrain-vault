import os
import sys
import time
import subprocess
import pyautogui

CU_EXE = r"C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe"

def run_full_demo():
    # 0. Clear any emergency latch stop.flag from previous ESC presses
    stop_flag = os.path.expandvars(r"%LOCALAPPDATA%\AntigravityComputerUse\stop.flag")
    if os.path.exists(stop_flag):
        try:
            os.remove(stop_flag)
        except Exception:
            pass

    # 1. Clean stop any existing session
    subprocess.run([CU_EXE, "session-stop"], capture_output=True)
    time.sleep(0.5)
    
    # 2. Start Computer Use session (HUD + Cosmic Cyan Side Glow appear)
    print("Launching Antigravity Computer Use HUD...")
    res = subprocess.run([CU_EXE, "session-start"], capture_output=True, text=True)
    print("Session Start Result:", res.stdout)
    time.sleep(1.5)
    
    # 3. Perform a gentle smooth mouse movement to demonstrate live control
    width, height = pyautogui.size()
    centerX, centerY = width // 2, height // 2
    
    # Move cursor gently in a smooth pattern
    pyautogui.moveTo(centerX, centerY, duration=0.6)
    time.sleep(0.3)
    pyautogui.moveTo(centerX + 200, centerY, duration=0.6)
    pyautogui.moveTo(centerX + 200, centerY - 150, duration=0.6)
    pyautogui.moveTo(centerX - 200, centerY - 150, duration=0.6)
    pyautogui.moveTo(centerX - 200, centerY, duration=0.6)
    pyautogui.moveTo(centerX, centerY, duration=0.6)
    
    # 4. Hold the HUD and Cosmic Cyan Glow visible for 10 seconds so Heru can inspect
    print("Holding HUD for 10 seconds...")
    time.sleep(8.0)
    
    # 5. Cleanly stop session
    subprocess.run([CU_EXE, "session-stop"])
    print("Demo completed!")

if __name__ == "__main__":
    run_full_demo()
