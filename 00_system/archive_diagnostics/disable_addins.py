import shutil
import re

INI_PATH = r"C:\Users\Heru Ardiansyah\AppData\Roaming\Autodesk\Revit\Autodesk Revit 2027\Revit.ini"
BACKUP_PATH = r"C:\Users\Heru Ardiansyah\AppData\Roaming\Autodesk\Revit\Autodesk Revit 2027\Revit.ini.backup_agy"

# --- STEP 1: Create backup ---
shutil.copy2(INI_PATH, BACKUP_PATH)
print(f"[OK] Backup created: {BACKUP_PATH}")

# --- STEP 2: Read original content ---
with open(INI_PATH, 'rb') as f:
    raw = f.read()

if raw[:2] == b'\xff\xfe':
    encoding = 'utf-16-le'
    bom = b'\xff\xfe'
elif raw[:2] == b'\xfe\xff':
    encoding = 'utf-16-be'
    bom = b'\xfe\xff'
else:
    encoding = 'utf-8'
    bom = b''

content = raw[len(bom):].decode(encoding, errors='replace') if bom else raw.decode(encoding, errors='replace')

print("=== ORIGINAL [API] section ===")
in_api = False
for line in content.splitlines():
    if line.strip() == '[API]':
        in_api = True
    elif in_api and re.match(r'^\[', line.strip()):
        in_api = False
    if in_api:
        print(line)

# --- STEP 3: Add/update DisableUserAddinsAndMacros=1 in [API] section ---
if '[API]' not in content:
    # Add [API] section with the setting
    content = content.rstrip() + '\n\n[API]\nDisableUserAddinsAndMacros=1\n'
    print("\n[OK] Added new [API] section with DisableUserAddinsAndMacros=1")
else:
    # Check if key already exists
    if 'DisableUserAddinsAndMacros' in content:
        # Replace value
        content = re.sub(
            r'(DisableUserAddinsAndMacros\s*=\s*)\d+',
            r'\g<1>1',
            content
        )
        print("\n[OK] Updated existing DisableUserAddinsAndMacros to 1")
    else:
        # Insert key after [API] header
        content = content.replace('[API]', '[API]\nDisableUserAddinsAndMacros=1', 1)
        print("\n[OK] Inserted DisableUserAddinsAndMacros=1 after [API]")

# --- STEP 4: Write modified file back ---
new_raw = bom + content.encode(encoding if encoding != 'utf-8' else 'utf-8')
with open(INI_PATH, 'wb') as f:
    f.write(new_raw)
print(f"[OK] Modified Revit.ini written.")
