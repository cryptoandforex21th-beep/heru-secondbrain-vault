import httpx

code = """
schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
for s in schedules:
    if s.Name == "RAB TERPADU MENARA DYNAMO - MAKASSAR 2026":
        defn = s.Definition
        calc_methods = [m for m in dir(defn) if "calc" in m.lower() or "formula" in m.lower()]
        print("Calculated field methods: " + ", ".join(calc_methods))
        break
"""

payload = {
    "code": code,
    "description": "Inspect calculated field methods"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
