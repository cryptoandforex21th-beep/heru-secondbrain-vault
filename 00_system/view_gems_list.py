import time
import pyautogui

# Click Edge window
pyautogui.click(1200, 300)
time.sleep(0.3)

# Click Gems icon on left sidebar (x=52, y=334)
# In split screen, if Edge is on right half (x starts at 953):
# Wait, look at gemini_u3_home.png:
# Edge is occupying from x=960 to 1920!
# So the Gems icon on Edge's sidebar is at x = 960 + 52 = 1012, y = 334!
pyautogui.click(980, 260)
time.sleep(1.0)
pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_gems_list_eruuu.png")
