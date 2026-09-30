import httpx

code = """
schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
for s in schedules:
    if s.Name == "RAB TERPADU MENARA DYNAMO - MAKASSAR 2026":
        defn = s.Definition
        f = defn.GetField(3) # Material: Area
        attrs = [a for a in dir(f) if not a.startswith("__")]
        print("ScheduleField attributes: " + ", ".join(attrs))
        break
"""

payload = {
    "code": code,
    "description": "Inspect ScheduleField methods"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
