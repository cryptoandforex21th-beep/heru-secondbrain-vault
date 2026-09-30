"""
SecondBrain MeshSync Engine (Inspired by Layer5 MeshSync)
Author: Ai (Management Plane) for Heru Ardiansyah
Discovers and synchronizes state across Physical Win32, Local Knowledge, Brain States, and Cloud Vault.
"""

import os
import sys
import json
import subprocess
import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SECONDBRAIN_DIR = r"D:\SecondBrain"
OUTPUT_STATE_FILE = os.path.join(SECONDBRAIN_DIR, "00_system", "mesh_state.json")

def check_git_status():
    try:
        res = subprocess.run(["git", "status", "--porcelain"], cwd=SECONDBRAIN_DIR, capture_output=True, text=True, encoding="utf-8")
        uncommitted = len(res.stdout.strip().splitlines()) if res.stdout.strip() else 0
        
        # Check last commit
        log_res = subprocess.run(["git", "log", "-1", "--format=%h - %s (%cd)", "--date=relative"], cwd=SECONDBRAIN_DIR, capture_output=True, text=True, encoding="utf-8")
        last_commit = log_res.stdout.strip() if log_res.returncode == 0 else "Unknown"
        
        # Check remote
        rem_res = subprocess.run(["git", "remote", "-v"], cwd=SECONDBRAIN_DIR, capture_output=True, text=True, encoding="utf-8")
        has_remote = "origin" in rem_res.stdout
        
        return {
            "uncommitted_changes": uncommitted,
            "last_commit": last_commit,
            "has_remote": has_remote,
            "clean": uncommitted == 0
        }
    except Exception as e:
        return {"error": str(e), "clean": False}

def inspect_brain_states():
    brains_dir = os.path.join(SECONDBRAIN_DIR, "02_brains")
    divisions = {}
    if not os.path.exists(brains_dir):
        return divisions
        
    for item in sorted(os.listdir(brains_dir)):
        p = os.path.join(brains_dir, item)
        if os.path.isdir(p) and item != "SESSION_ARCHIVES":
            state_file = os.path.join(p, "BRAIN_STATE.md")
            has_state = os.path.exists(state_file)
            size = os.path.getsize(state_file) if has_state else 0
            divisions[item] = {
                "has_brain_state": has_state,
                "state_size_bytes": size,
                "status": "HEALTHY" if has_state else "MISSING_STATE"
            }
    return divisions

def check_physical_workspace():
    ta_dir = r"D:\TugasAkhirHeruArdiansyah"
    gdrive_dir = r"G:\My Drive\NOTEBOOKLM_SKRIPSI_HERU"
    
    active_docs = []
    if os.path.exists(ta_dir):
        for f in os.listdir(ta_dir):
            if f.endswith(".docx") and not f.startswith("~$"):
                full_p = os.path.join(ta_dir, f)
                mtime = os.path.getmtime(full_p)
                active_docs.append({
                    "name": f,
                    "size_kb": round(os.path.getsize(full_p) / 1024, 1),
                    "last_modified": datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                })
                
    gdrive_sources_count = len(os.listdir(gdrive_dir)) if os.path.exists(gdrive_dir) else 0
    
    return {
        "physical_thesis_docs": active_docs,
        "gdrive_synced_sources": gdrive_sources_count,
        "gdrive_ready": gdrive_sources_count >= 20
    }

def run_mesh_sync():
    now_str = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S WITA")
    
    mesh_state = {
        "generated_at": now_str,
        "management_plane": "Ai (00_ai_pm)",
        "architecture_version": "Layer5-Mesh-v1.0",
        "git": check_git_status(),
        "divisions": inspect_brain_states(),
        "physical_workspace": check_physical_workspace()
    }
    
    os.makedirs(os.path.dirname(OUTPUT_STATE_FILE), exist_ok=True)
    with open(OUTPUT_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(mesh_state, f, indent=2, ensure_ascii=False)
        
    return mesh_state

if __name__ == "__main__":
    state = run_mesh_sync()
    print(f"[MESHSYNC] Live State Captured at {state['generated_at']}")
    print(f" - Divisions Healthy: {len([d for d in state['divisions'].values() if d['status'] == 'HEALTHY'])} / {len(state['divisions'])}")
    print(f" - Git Clean: {state['git']['clean']} | Last Commit: {state['git']['last_commit']}")
    print(f" - GDrive NotebookLM Sources: {state['physical_workspace']['gdrive_synced_sources']} files ready")
    print(f" - State saved to: {OUTPUT_STATE_FILE}")
