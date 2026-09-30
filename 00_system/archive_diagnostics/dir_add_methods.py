import httpx

code = """
schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
for s in schedules:
    if s.Name == "RAB TERPADU MENARA DYNAMO - MAKASSAR 2026":
        defn = s.Definition
        add_methods = [m for m in dir(defn) if any(k in m.lower() for k in ["add", "insert", "create"])]
        print("Add/Insert/Create methods: " + ", ".join(add_methods))
        break
"""

payload = {
    "code": code,
    "description": "Inspect Add/Insert methods on ScheduleDefinition"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
