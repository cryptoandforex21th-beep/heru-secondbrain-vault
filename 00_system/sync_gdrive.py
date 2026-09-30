"""
Sync D:\\SecondBrain to G:\\My Drive\\SecondBrain
Automatically syncs notes, knowledge, and system instructions to Google Drive cloud.
"""
import subprocess
import sys

def sync():
    cmd = [
        "robocopy",
        r"D:\SecondBrain",
        r"G:\My Drive\SecondBrain",
        "/MIR",
        "/XD", ".git", ".venv", "__pycache__", "node_modules", "archive_diagnostics",
        "/XF", "*.exe", "*.tmp", "*.log", "*.png",
        "/R:1", "/W:1", "/NFL", "/NDL", "/NJH", "/NJS"
    ]
    # Robocopy return codes <= 7 mean successful copy or no changes
    res = subprocess.run(cmd)
    if res.returncode <= 7:
        print("[OK] SecondBrain successfully synced to Google Drive My Drive!")
        return 0
    else:
        print(f"[ERROR] Sync exited with code {res.returncode}")
        return res.returncode

if __name__ == "__main__":
    sys.exit(sync())
