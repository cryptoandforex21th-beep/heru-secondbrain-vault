import httpx

code = """
# Compute total area and volume per material for Floors, Walls, CurtainWallPanels
materials_summary = {}

for cat in [DB.BuiltInCategory.OST_Floors, DB.BuiltInCategory.OST_Walls, DB.BuiltInCategory.OST_CurtainWallPanels]:
    elems = DB.FilteredElementCollector(doc).OfCategory(cat).WhereElementIsNotElementType().ToElements()
    for e in elems:
        mat_ids = e.GetMaterialIds(False)
        for mid in mat_ids:
            mat = doc.GetElement(mid)
            if not mat: continue
            mname = mat.Name
            area = e.GetMaterialArea(mid, False) # in sq ft
            vol = e.GetMaterialVolume(mid)      # in cu ft
            
            # convert to m2 and m3 (1 ft2 = 0.092903 m2, 1 ft3 = 0.0283168 m3)
            area_m2 = area * 0.092903
            vol_m3 = vol * 0.0283168
            
            if mname not in materials_summary:
                materials_summary[mname] = {"category": str(cat).replace("OST_", ""), "count": 0, "area_m2": 0.0, "vol_m3": 0.0, "mat_id": mid}
            materials_summary[mname]["count"] += 1
            materials_summary[mname]["area_m2"] += area_m2
            materials_summary[mname]["vol_m3"] += vol_m3

print("=== MATERIAL QUANTITIES IN PROJECT (METRIC) ===")
for mname, data in materials_summary.items():
    print("Material: '{0}' (Cat: {1}) | Count: {2} | Area: {3:.2f} m2 | Volume: {4:.2f} m3".format(
        mname, data["category"], data["count"], data["area_m2"], data["vol_m3"]
    ))
"""

payload = {
    "code": code,
    "description": "Calculate material quantities in metric"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
