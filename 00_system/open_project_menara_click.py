import os
import subprocess
import sys

cmd_file = r"d:\SecondBrain\00_system\next_launch.cmd"
log_file = r"d:\SecondBrain\00_system\launcher.log"

try:
    if os.path.exists(cmd_file):
        with open(cmd_file, "r", encoding="utf-8-sig") as f:
            target = f.read().strip().lstrip('\ufeff')
        
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Launching: {target}\n")
            
        if os.path.exists(target):
            os.startfile(target)
            with open(log_file, "a", encoding="utf-8") as log:
                log.write("os.startfile executed.\n")
        elif target.startswith("http://") or target.startswith("https://"):
            os.system(f'start "" "{target}"')
            with open(log_file, "a", encoding="utf-8") as log:
                log.write("start URL executed.\n")
        else:
            # Use CREATE_NO_WINDOW so no black box ever pops up!
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(target, shell=True, creationflags=CREATE_NO_WINDOW)
            with open(log_file, "a", encoding="utf-8") as log:
                log.write("subprocess.Popen executed silently.\n")
except Exception as e:
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"Error: {e}\n")
