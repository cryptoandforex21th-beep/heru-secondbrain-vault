import httpx

code = """
# Test reading and setting Material: Cost for the 4 materials
ahsp_makassar = {
    "Default Floor": 1150000.0,                    # Rp 1.150.000 / m2 (Plat Lantai Beton Bertulang K-300 + Pembesian + Bekisting)
    "Brick, Common": 210000.0,                     # Rp 210.000 / m2 (Pasangan Dinding Bata 1/2 camp 1:4 + Plester + Aci)
    "Glass, Clear Glazing, Tempered": 1150000.0,   # Rp 1.150.000 / m2 (Kaca Tempered 10-12mm Curtain Wall + Sealant)
    "Iron, Ductile": 680000.0                      # Rp 680.000 / m2 (Rangka Besi/Baja Struktur Fasad Curtain Wall)
}

materials = DB.FilteredElementCollector(doc).OfClass(DB.Material).ToElements()
updated = []

for m in materials:
    if m.Name in ahsp_makassar:
        cost_param = m.get_Parameter(DB.BuiltInParameter.ALL_MODEL_COST)
        if not cost_param:
            cost_param = m.LookupParameter("Cost")
        
        if cost_param and not cost_param.IsReadOnly:
            val = ahsp_makassar[m.Name]
            # In Revit API, Currency / Cost parameter can be double or string depending on version
            try:
                cost_param.Set(val)
                updated.append(m.Name + " -> " + str(val))
            except Exception as e:
                # Try setting as string if double fails
                cost_param.Set(str(val))
                updated.append(m.Name + " (str) -> " + str(val))

print("Updated Materials Cost: " + ", ".join(updated))
"""

payload = {
    "code": code,
    "description": "Set AHSP Makassar Cost on Materials"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
