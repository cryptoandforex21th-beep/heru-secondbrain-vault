import sys
import subprocess
import os
import psutil

REVIT_EXE = r"C:\Program Files\Autodesk\Revit 2027\Revit.exe"
PROJECT_MAP = {
    "menara": r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt",
    "project menara": r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt",
    "menara dynamo": r"D:\REVIT LEARN\REVIT FILE\PROJECT MENARA DYNAMO.rvt"
}

def trigger_session1(target):
    # Uses app_launcher to guarantee Session 1 interactive launch
    cmd = f'python d:\\SecondBrain\\00_system\\app_launcher.py "{target}"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(res.stdout.strip())
    return res.returncode == 0

def status():
    found = False
    for p in psutil.process_iter(['pid', 'name']):
        if 'revit' in p.info['name'].lower():
            print(f"Revit is RUNNING: PID {p.info['pid']} ({p.info['name']})")
            found = True
    if not found:
        print("Revit is NOT running.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python revit_cli.py [open|open-project <name>|status]")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    if action == "open":
        trigger_session1(REVIT_EXE)
    elif action == "open-project":
        name = sys.argv[2].lower() if len(sys.argv) > 2 else "menara"
        target = PROJECT_MAP.get(name, name)
        trigger_session1(target)
    elif action == "status":
        status()
    else:
        print(f"Unknown action: {action}")
