import os

EXT_ROOT = r"C:\Users\Heru Ardiansyah\AppData\Roaming\pyRevit\Extensions\mcp-server-for-revit-python.extension"

# Walk and collect files (exclude .venv)
for dirpath, dirnames, filenames in os.walk(EXT_ROOT):
    # Skip .venv
    dirnames[:] = [d for d in dirnames if d not in ['.venv', '__pycache__', 'node_modules']]
    for fname in filenames:
        if fname.endswith(('.py', '.json', '.yaml', '.yml', '.toml', '.txt', '.md')):
            full = os.path.join(dirpath, fname)
            rel = full[len(EXT_ROOT):]
            print(rel)
