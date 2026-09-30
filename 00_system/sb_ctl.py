"""
SecondBrain Control CLI (sb_ctl.py) — Inspired by Layer5 'mesheryctl'
Unified Management Plane CLI for Heru Ardiansyah's SecondBrain OS.
"""

import sys
import os
import subprocess
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SECONDBRAIN_DIR = r"D:\SecondBrain"
SYS_DIR = os.path.join(SECONDBRAIN_DIR, "00_system")

def print_banner():
    print("""
  ██████╗ ██████╗       ██████╗████████╗██╗     
 ██╔════╝ ██╔══██╗     ██╔════╝╚══██╔══╝██║     
 ╚█████╗  ██████╔╝     ██║        ██║   ██║     
  ╚═══██╗ ██╔══██╗     ██║        ██║   ██║     
 ██████╔╝ ██████╔╝     ╚██████╗   ██║   ███████╗
 ╚═════╝  ╚═════╝       ╚═════╝   ╚═╝   ╚══════╝
 [SecondBrain Layer 5 Management Plane CLI v1.0]
""")

def cmd_status():
    print_banner()
    # Run mesh_sync to get latest state
    try:
        from mesh_sync import run_mesh_sync
        state = run_mesh_sync()
    except Exception:
        subprocess.run([sys.executable, os.path.join(SYS_DIR, "mesh_sync.py")], capture_output=True)
        with open(os.path.join(SYS_DIR, "mesh_state.json"), "r", encoding="utf-8") as f:
            state = json.load(f)

    print(f"⏰ Timestamp: {state['generated_at']}")
    print(f"👑 Management Plane: {state['management_plane']}")
    print("-" * 55)
    
    # 1. Brain Mesh Topology
    print("🧬 [LAYER 2] DIVISION BRAIN MESH:")
    for name, info in state["divisions"].items():
        status_icon = "🟢" if info["status"] == "HEALTHY" else "🔴"
        size_kb = round(info["state_size_bytes"] / 1024, 1)
        print(f"   {status_icon} {name.ljust(25)} : {info['status']} ({size_kb} KB)")
        
    print("-" * 55)
    # 2. Cloud & Storage
    print("☁️ [LAYER 4] CLOUD & VAULT:")
    git_icon = "🟢" if state["git"]["clean"] else "🟡"
    print(f"   {git_icon} GitHub Private Vault    : {state['git']['last_commit']}")
    if state["git"]["uncommitted_changes"] > 0:
        print(f"      └─ Uncommitted files : {state['git']['uncommitted_changes']} (Run 'sb sync' to backup)")
        
    gdrive_icon = "🟢" if state["physical_workspace"]["gdrive_ready"] else "🟡"
    print(f"   {gdrive_icon} Google Drive NotebookLM : {state['physical_workspace']['gdrive_synced_sources']} sources synced (G:\\My Drive)")
    
    print("-" * 55)
    # 3. Active Physical Thesis Docs
    print("📄 [LAYER 0] PHYSICAL THESIS WORKSPACE:")
    for doc in state["physical_workspace"]["physical_thesis_docs"]:
        print(f"   • {doc['name']} ({doc['size_kb']} KB) [Modified: {doc['last_modified']}]")
        
    print("=" * 55)

def cmd_sync(args):
    commit_msg = " ".join(args) if args else None
    sync_script = os.path.join(SYS_DIR, "secondbrain_sync.py")
    cmd = [sys.executable, sync_script]
    if commit_msg:
        cmd.append(commit_msg)
    subprocess.run(cmd)

def cmd_launch(args):
    if not args:
        print("Usage: sb launch <app_name_or_url>")
        return
    launcher = os.path.join(SYS_DIR, "app_launcher.py")
    subprocess.run([sys.executable, launcher] + args)

def cmd_mesh():
    cmd_status()

def cmd_help():
    print_banner()
    print("Commands:")
    print("  sb status         : View live health & topology of all SecondBrain layers")
    print("  sb mesh           : Inspect division mesh states & physical files")
    print("  sb sync [msg]     : Zero-Leak backup & sync to GitHub Private Cloud")
    print("  sb launch <target>: Launch apps, URLs, or scripts in Session 1 in 150ms")
    print("  sb visual         : Open the interactive architecture visualizer in Edge")
    print("=" * 55)

def cmd_visual():
    visual_path = os.path.join(SECONDBRAIN_DIR, "04_app", "static", "blueprint_visualizer.html")
    launcher = os.path.join(SYS_DIR, "app_launcher.py")
    subprocess.run([sys.executable, launcher, visual_path])
    print("🚀 Launched Blueprint Visualizer in Session 1!")

def cmd_cdp(args):
    cdp_script = os.path.join(SYS_DIR, "edge_cdp.py")
    subprocess.run([sys.executable, cdp_script] + args)

def main():
    if len(sys.argv) < 2:
        cmd_help()
        return
        
    action = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if action in ["status", "st"]:
        cmd_status()
    elif action in ["sync", "backup"]:
        cmd_sync(args)
    elif action in ["launch", "open", "run"]:
        cmd_launch(args)
    elif action in ["mesh", "topology"]:
        cmd_mesh()
    elif action in ["visual", "view", "gui"]:
        cmd_visual()
    elif action in ["cdp", "browser", "chrome"]:
        cmd_cdp(args)
    else:
        cmd_help()

if __name__ == "__main__":
    main()
