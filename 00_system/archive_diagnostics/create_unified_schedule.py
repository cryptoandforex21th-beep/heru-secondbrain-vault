import httpx

code = """
import clr
import System

# Check if schedule with this name already exists and remove/replace it
sched_name = "RAB TERPADU MENARA DYNAMO - MAKASSAR 2026"
existing = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
for s in existing:
    if s.Name == sched_name:
        doc.Delete(s.Id)
        print("Deleted old schedule with same name.")
        break

# Create Multi-Category Material Takeoff (InvalidElementId = multi-category)
multi_cat_id = DB.ElementId.InvalidElementId
schedule = DB.ViewSchedule.CreateMaterialTakeoff(doc, multi_cat_id)
schedule.Name = sched_name

defn = schedule.Definition
schedulable_fields = defn.GetSchedulableFields()

# Target fields to add
target_field_names = ["Category", "Material: Name", "Count", "Material: Area", "Material: Volume", "Material: Cost"]
added_fields = []

for target in target_field_names:
    for sf in schedulable_fields:
        try:
            fname = sf.GetName(doc)
            if fname == target:
                field = defn.AddField(sf)
                added_fields.append(fname)
                
                # Enable calculation of totals for Area, Volume, Count
                if target in ["Material: Area", "Material: Volume", "Count"]:
                    field.IsCalculateTotals = True
                break
        except Exception as e:
            pass

# Group by Material: Name so it does not list all 3000 instances individually
defn.IsItemized = False

# Add Sort/Group by Material: Name (field index 1)
try:
    # Find field index for Material: Name
    mat_field_id = None
    for i in range(defn.GetFieldCount()):
        f = defn.GetField(i)
        if f.GetName() == "Material: Name":
            mat_field_id = f.FieldId
            break
    if mat_field_id is not None:
        sort_field = DB.ScheduleSortGroupField(mat_field_id)
        sort_field.ShowHeader = False
        sort_field.ShowFooter = True
        defn.AddSortGroupField(sort_field)
except Exception as e:
    print("SortGroup notice: " + str(e))

# Enable Grand Totals
defn.ShowGrandTotal = True
defn.ShowGrandTotalTitle = True
defn.ShowGrandTotalCount = True

# Update Material Cost values according to AHSP Makassar 2026
ahsp_makassar = {
    "Default Floor": 1150000.0,                    # Rp 1.150.000 / m2 (Plat Lantai Beton K-300 + Pembesian + Bekisting)
    "Brick, Common": 210000.0,                     # Rp 210.000 / m2 (Pasangan Dinding Bata 1/2 camp 1:4 + Plesteran & Acian)
    "Glass, Clear Glazing, Tempered": 1150000.0,   # Rp 1.150.000 / m2 (Kaca Tempered 10-12mm Curtain Wall + Sealant)
    "Iron, Ductile": 680000.0                      # Rp 680.000 / m2 (Rangka Besi/Baja Struktur Fasad Curtain Wall)
}

mats = DB.FilteredElementCollector(doc).OfClass(DB.Material).ToElements()
for m in mats:
    if m.Name in ahsp_makassar:
        cost_p = m.get_Parameter(DB.BuiltInParameter.ALL_MODEL_COST)
        if not cost_p:
            cost_p = m.LookupParameter("Cost")
        if cost_p and not cost_p.IsReadOnly:
            cost_p.Set(ahsp_makassar[m.Name])
            print("Set Cost for " + m.Name + " = " + str(ahsp_makassar[m.Name]))

print("SUCCESS: Created unified schedule '" + sched_name + "' with fields: " + ", ".join(added_fields))
"""

payload = {
    "code": code,
    "description": "Create Unified Multi-Category Material Takeoff Schedule with AHSP Makassar"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=25)
print("STATUS CODE:", r.status_code)
res = r.json()
print("OUTPUT:\n", res.get("output", res))
