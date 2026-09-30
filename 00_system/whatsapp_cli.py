import sys
import subprocess
import time

def trigger_whatsapp_send(contact, message):
    cmd = f'C:\\Python314\\python.exe d:\\SecondBrain\\00_system\\send_whatsapp.py "{contact}" "{message}"'
    
    with open(r"d:\SecondBrain\00_system\next_launch.cmd", "w", encoding="utf-8") as f:
        f.write(cmd)
        
    res = subprocess.run(["schtasks", "/run", "/tn", "AntigravityGUI"], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Triggered WhatsApp message send to '{contact}' in Session 1.")
        return True
    else:
        print(f"Error triggering: {res.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python whatsapp_cli.py <contact> <message>")
        sys.exit(1)
    c = sys.argv[1]
    m = " ".join(sys.argv[2:])
    trigger_whatsapp_send(c, m)
