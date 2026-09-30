import httpx

code = """
materials = DB.FilteredElementCollector(doc).OfClass(DB.Material).ToElements()
print("Total Materials in Project: " + str(len(materials)))
for m in materials:
    name = m.Name
    # Look for relevant materials like glass, iron, concrete, wall, floor
    if any(k in name.lower() for k in ["glass", "iron", "kaca", "besi", "baja", "beton", "floor", "wall", "lantai", "dinding", "curtain", "panel"]):
        cost_param = m.LookupParameter("Cost")
        cost_val = cost_param.AsString() if cost_param and cost_param.HasValue else (str(cost_param.AsDouble()) if cost_param else "None")
        print("Material: " + name + " | Cost param: " + str(cost_val))

print("=" * 60)
# Check all elements and their materials
collector = DB.FilteredElementCollector(doc).WhereElementIsNotElementType()
cats = [DB.BuiltInCategory.OST_Floors, DB.BuiltInCategory.OST_Walls, DB.BuiltInCategory.OST_CurtainWallPanels, DB.BuiltInCategory.OST_CurtainWallMullions]
for cat in cats:
    elems = DB.FilteredElementCollector(doc).OfCategory(cat).WhereElementIsNotElementType().ToElements()
    print("Category: " + str(cat) + " -> Count: " + str(len(elems)))
    mat_names = set()
    for e in elems:
        mat_ids = e.GetMaterialIds(False)
        for mid in mat_ids:
            mat = doc.GetElement(mid)
            if mat:
                mat_names.add(mat.Name)
    print("  Used Materials: " + ", ".join(list(mat_names)))
"""

payload = {
    "code": code,
    "description": "Inspect materials and elements in project"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
