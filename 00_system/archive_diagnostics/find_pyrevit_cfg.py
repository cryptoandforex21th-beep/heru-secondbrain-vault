import os

BASE = r"C:\Users\Heru Ardiansyah\AppData\Roaming\pyRevit"

for dirpath, dirnames, filenames in os.walk(BASE):
    dirnames[:] = [d for d in dirnames if d not in ['Extensions', '__pycache__', '.venv']]
    for fname in filenames:
        if fname.lower().endswith(('.cfg', '.ini', '.json', '.toml', '.yaml', '.yml')):
            full = os.path.join(dirpath, fname)
            rel = full[len(BASE):]
            print(rel)
