"""
SecondBrain Zero-Leak Git Synchronizer & GitHub Backup Engine
Author: Ai (Executive PM) for Heru Ardiansyah
"""

import os
import subprocess
import datetime
import sys

# Configure UTF-8 for Windows PowerShell output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SECONDBRAIN_DIR = r"D:\SecondBrain"

def run_git(cmd_args):
    res = subprocess.run(["git"] + cmd_args, cwd=SECONDBRAIN_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def ensure_gitignore():
    gitignore_path = os.path.join(SECONDBRAIN_DIR, ".gitignore")
    essential_rules = [
        "# Security & Vault (ZERO-LEAK GUARANTEE)",
        "00_system/.vault/",
        "*.recovery-codes*",
        "client_secret_*",
        ".env",
        ".env.local",
        "*.env*",
        "",
        "# Dependencies & Temporary caches",
        "node_modules/",
        ".next/",
        ".tmp.driveupload/",
        ".tmp.drivedownload/",
        "__pycache__/",
        "*.pyc",
        "",
        "# Media scratch dumps",
        "01_knowledge/archives/root_scrape_dumps/",
        "00_system/scratch/"
    ]
    
    current_content = ""
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            current_content = f.read()
            
    needs_update = False
    for rule in ["00_system/.vault/", "*.recovery-codes*", "client_secret_*", "node_modules/"]:
        if rule not in current_content:
            needs_update = True
            break
            
    if needs_update or not os.path.exists(gitignore_path):
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write("\n".join(essential_rules) + "\n")
        print("[OK] .gitignore verified and secured with Zero-Leak rules.")
    else:
        print("[OK] .gitignore already verified.")

def sync_repository(commit_msg=None):
    print("=" * 60)
    print("[SECONDBRAIN] AUTO-SYNC & GITHUB BACKUP ENGINE")
    print("=" * 60)
    
    # 1. Check or Init Git
    if not os.path.exists(os.path.join(SECONDBRAIN_DIR, ".git")):
        print("[INFO] Initializing Git repository in D:\\SecondBrain...")
        code, out, err = run_git(["init"])
        if code != 0:
            print("[ERROR] Git init failed:", err)
            return False
        run_git(["config", "user.name", "Heru Ardiansyah"])
        run_git(["config", "user.email", "heruardiansyah2one@gmail.com"])
        run_git(["branch", "-M", "main"])
        print("[OK] Git repository initialized with branch 'main'.")
        
    # 2. Enforce Security
    ensure_gitignore()
    
    # 3. Check Status
    code, status_out, _ = run_git(["status", "--porcelain"])
    if not status_out:
        print("[INFO] SecondBrain is completely clean. No new changes to commit.")
    else:
        # Stage files
        print("[INFO] Staging updated notes and knowledge...")
        run_git(["add", "."])
        
        # Verify no .vault or secret leaked into staging
        code, staged_files, _ = run_git(["diff", "--cached", "--name-only"])
        leaks = [f for f in staged_files.splitlines() if ".vault" in f or "secret" in f.lower() or "recovery" in f.lower()]
        if leaks:
            print("[ALERT] Staged files contain potential leaks:", leaks)
            print("[STOP] Aborting commit to protect privacy!")
            run_git(["reset"])
            return False
            
        wita_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M WITA")
        if not commit_msg:
            commit_msg = f"sync(secondbrain): auto-backup [{wita_time}]"
            
        print(f"[COMMIT] Committing: '{commit_msg}'...")
        code, out, err = run_git(["commit", "-m", commit_msg])
        if code == 0:
            print("[OK] Successfully committed changes to local git history.")
        else:
            print("[WARN] Commit output:", out or err)
            
    # 4. Check Remote
    code, remotes, _ = run_git(["remote", "-v"])
    if remotes:
        print("[INFO] Pushing to remote GitHub repository...")
        code, out, err = run_git(["push", "-u", "origin", "main"])
        if code == 0:
            print("[SUCCESS] SecondBrain successfully backed up to GitHub!")
        else:
            print("[WARN] Push notice (check network/credentials):", err or out)
    else:
        print("\n[NOTE] GitHub Remote belum terhubung!")
        print("Untuk menghubungkan ke private repository di akun GitHub kamu (misal: cryptoandforex21th-beep):")
        print("   1. Buat private repository di GitHub: 'heru-secondbrain-vault'")
        print("   2. Jalankan perintah:")
        print("      git remote add origin https://github.com/cryptoandforex21th-beep/heru-secondbrain-vault.git")
        print("      python d:\\SecondBrain\\00_system\\secondbrain_sync.py")
        
    print("=" * 60)
    return True

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    sync_repository(msg)
