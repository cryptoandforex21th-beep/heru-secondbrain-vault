INI_PATH = r"C:\Users\Heru Ardiansyah\AppData\Roaming\Autodesk\Revit\Autodesk Revit 2027\Revit.ini"
BACKUP_PATH = r"C:\Users\Heru Ardiansyah\AppData\Roaming\Autodesk\Revit\Autodesk Revit 2027\Revit.ini.backup_agy"

# Read as bytes to detect encoding and print key sections
with open(INI_PATH, 'rb') as f:
    raw = f.read()

# Try UTF-16-LE with BOM
if raw[:2] == b'\xff\xfe':
    content = raw.decode('utf-16-le', errors='replace')
elif raw[:2] == b'\xfe\xff':
    content = raw.decode('utf-16-be', errors='replace')
else:
    content = raw.decode('utf-8', errors='replace')

# Print [API], [Misc], [Applications], [System] sections
import re
sections_of_interest = ['API', 'Misc', 'Applications', 'System', 'Graphics', 'Revit.ini']
current_section = None
for line in content.splitlines():
    m = re.match(r'^\[(.+)\]', line.strip())
    if m:
        current_section = m.group(1)
    if current_section in sections_of_interest:
        print(line)
