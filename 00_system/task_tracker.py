import json
import os
import sys
from datetime import datetime

TRACKER_FILE = r"d:\SecondBrain\00_system\task_frequency.json"
SKILLS_DIR = os.path.expandvars(r"%USERPROFILE%\.gemini\config\skills")

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": {}, "rules": {"skill_threshold": 2, "automation_threshold": 4}}

def save_tracker(data):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def log_task(task_key, description=None, artifact=None):
    data = load_tracker()
    tasks = data.setdefault("tasks", {})
    rules = data.setdefault("rules", {"skill_threshold": 2, "automation_threshold": 4})
    
    task = tasks.setdefault(task_key, {
        "count": 0,
        "status": "one_off",
        "description": description or task_key,
        "artifact": artifact or "",
        "history": []
    })
    
    task["count"] += 1
    task.setdefault("history", [])
    task["history"].append({
        "timestamp": datetime.now().isoformat(),
        "note": description or ""
    })
    
    skill_thresh = rules.get("skill_threshold", 2)
    auto_thresh = rules.get("automation_threshold", 4)
    
    evolution_event = None
    if task["count"] >= auto_thresh and task["status"] != "fully_automated":
        task["status"] = "fully_automated"
        evolution_event = f"🔥 [4X PIPELINE UPGRADE] Task '{task_key}' reached {task['count']}x! Upgraded to Full Automation Pipeline."
    elif task["count"] >= skill_thresh and task["status"] == "one_off":
        task["status"] = "skill_crystallized"
        evolution_event = f"⚡ [2X SKILL CRYSTALLIZATION] Task '{task_key}' reached {task['count']}x! Crystallized into Skill."
        
    save_tracker(data)
    
    print(f"Logged task: '{task_key}' (Total: {task['count']}x, Status: {task['status']})")
    if evolution_event:
        print(evolution_event)
    return task

def summary():
    data = load_tracker()
    tasks = data.get("tasks", {})
    print(f"\n{'TASK KEY':<25} | {'COUNT':<5} | {'STATUS':<20} | {'ARTIFACT'}")
    print("-" * 80)
    for k, v in sorted(tasks.items(), key=lambda x: x[1].get('count', 0), reverse=True):
        print(f"{k:<25} | {v.get('count', 0):<5} | {v.get('status', ''):<20} | {v.get('artifact', '')}")
    print("-" * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        summary()
    elif sys.argv[1] == "log" and len(sys.argv) > 2:
        k = sys.argv[2]
        desc = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None
        log_task(k, description=desc)
    elif sys.argv[1] == "summary":
        summary()
    else:
        print("Usage: python task_tracker.py [summary | log <task_key> [desc]]")
