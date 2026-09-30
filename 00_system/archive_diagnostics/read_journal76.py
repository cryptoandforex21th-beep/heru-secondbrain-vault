journal_path = r"C:\Users\Heru Ardiansyah\AppData\Local\Autodesk\Revit\Autodesk Revit 2027\Journals\journal.0076.txt"

with open(journal_path, encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("=== LAST 60 LINES OF JOURNAL 0076 ===")
for l in lines[-60:]:
    print(l.rstrip())
