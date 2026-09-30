import re

journal_path = r"C:\Users\Heru Ardiansyah\AppData\Local\Autodesk\Revit\Autodesk Revit 2027\Journals\journal.0074.txt"

with open(journal_path, encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Print area around lines 3280-3370 (crash sequence context)
print("=== CRASH SEQUENCE CONTEXT (lines 3270-3380) ===\n")
for i in range(3270, min(3380, len(lines))):
    print(f"[{i:05d}] {lines[i].rstrip()}")

# Print the opening sequence at start
print("\n=== SESSION OPEN SEQUENCE (first 60 lines) ===\n")
for i, l in enumerate(lines[:60]):
    print(f"[{i:05d}] {l.rstrip()}")
