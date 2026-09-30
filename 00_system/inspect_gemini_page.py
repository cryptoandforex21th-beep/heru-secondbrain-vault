import subprocess
import json

cu_exe = r"C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe"
res = subprocess.run([cu_exe, "observe", "-Handle", "1313626"], capture_output=True, text=True)

try:
    data = json.loads(res.stdout)
    controls = data.get("controls", [])
    print(f"Total controls observed: {len(controls)}")
    for c in controls:
        name = c.get("name", "")
        aid = c.get("automationId", "")
        ctype = c.get("controlType", "")
        x = c.get("x", 0)
        y = c.get("y", 0)
        w = c.get("width", 0)
        h = c.get("height", 0)
        
        lower_name = name.lower()
        lower_aid = aid.lower()
        
        matches = ["heru", "@", "simpan", "save", "gem", "petunjuk", "deskripsi", "batal", "cancel", "nama"]
        if any(m in lower_name or m in lower_aid for m in matches):
            print(f"[{ctype}] name='{name}' | aid='{aid}' | ({x}, {y}, {w}x{h})")
except Exception as e:
    print("Error parsing json:", e)
    print(res.stdout[:500])
