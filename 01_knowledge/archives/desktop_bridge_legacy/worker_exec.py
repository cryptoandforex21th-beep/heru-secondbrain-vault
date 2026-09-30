import os
import sys
import pyautogui
from PIL import ImageGrab

log_file = r"d:\SecondBrain\00_system\worker.log"

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")

try:
    log("Worker started.")
    pyautogui.FAILSAFE = False
    img = pyautogui.screenshot()
    save_path = r"d:\SecondBrain\00_system\current_state_before.png"
    img.save(save_path)
    log(f"Screenshot saved to {save_path}, size: {img.size}")
except Exception as e:
    log(f"Error: {e}")
