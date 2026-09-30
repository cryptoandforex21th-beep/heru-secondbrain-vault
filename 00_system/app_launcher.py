import os
import sys
import subprocess
import difflib

SHORTCUT_DIRS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
]

NEXT_LAUNCH_FILE = r"d:\SecondBrain\00_system\next_launch.cmd"

# Common alias overrides for instant 0ms matching
KNOWN_ALIASES = {
    "rhino": r"C:\Program Files\Rhino 8\System\Rhino.exe",
    "rhino 8": r"C:\Program Files\Rhino 8\System\Rhino.exe",
    "revit": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Autodesk\Revit 2027\Revit 2027.lnk",
    "blender": os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Blender\Blender 5.2.lnk"),
    "code": os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"),
    "vscode": os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"),
    "edge": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "word": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk",
    "excel": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk",
    "calc": "calc.exe",
    "calculator": "calc.exe",
    "notepad": "notepad.exe",
    "explorer": "explorer.exe",
    "youtube": "https://www.youtube.com"
}

def scan_shortcuts():
    shortcuts = {}
    for d in SHORTCUT_DIRS:
        if not os.path.exists(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().endswith(".lnk"):
                    name = f[:-4].lower()
                    shortcuts[name] = os.path.join(root, f)
    return shortcuts

def resolve_target(query):
    q = query.strip().lower()
    
    # 1. Direct path, URL, or script command
    if os.path.exists(query) or q.startswith("http://") or q.startswith("https://"):
        return query
    if q.startswith("python ") or q.startswith("c:\\") or ".py" in q:
        parts = query.split()
        if len(parts) > 1 and (os.path.exists(parts[0]) or parts[0].lower() == "python"):
            return query

    # 2. Known alias table (instant)
    if q in KNOWN_ALIASES:
        return KNOWN_ALIASES[q]
    
    # Check partial alias
    for alias, path in KNOWN_ALIASES.items():
        if alias == q:
            return path
            
    # 3. Scan Start Menu
    shortcuts = scan_shortcuts()
    if q in shortcuts:
        return shortcuts[q]
        
    # Match contains
    for name, path in shortcuts.items():
        if q in name:
            return path
            
    # Fuzzy match
    matches = difflib.get_close_matches(q, shortcuts.keys(), n=1, cutoff=0.4)
    if matches:
        return shortcuts[matches[0]]
        
    # Fallback to query as executable
    return query

def launch(query):
    target = resolve_target(query)
    with open(NEXT_LAUNCH_FILE, "w", encoding="utf-8") as f:
        f.write(target)
        
    res = subprocess.run(["schtasks", "/run", "/tn", "AntigravityGUI"], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS: Launched '{target}' in Session 1.")
        return True
    else:
        print(f"ERROR: {res.stderr.strip()}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app_launcher.py <app_name_or_path_or_url>")
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    launch(query)
