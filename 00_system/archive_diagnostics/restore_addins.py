import shutil
import re

INI_PATH = r"C:\Users\Heru Ardiansyah\AppData\Roaming\Autodesk\Revit\Autodesk Revit 2027\Revit.ini"
BACKUP_PATH = r"C:\Users\Heru Ardiansyah\AppData\Roaming\Autodesk\Revit\Autodesk Revit 2027\Revit.ini.backup_agy"

# Restore from backup
shutil.copy2(BACKUP_PATH, INI_PATH)
print(f"[OK] Revit.ini RESTORED from backup: {BACKUP_PATH}")
