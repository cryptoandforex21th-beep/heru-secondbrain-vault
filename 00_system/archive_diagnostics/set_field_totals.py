import httpx

code = """
schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
for s in schedules:
    if s.Name == "RAB TERPADU MENARA DYNAMO - MAKASSAR 2026":
        defn = s.Definition
        for i in range(defn.GetFieldCount()):
            f = defn.GetField(i)
            fname = f.GetName()
            if "Area" in fname or "Volume" in fname or "Count" in fname:
                try:
                    f.IsCalculateTotals = True
                    print("Set IsCalculateTotals on " + fname)
                except Exception as e:
                    print("Error setting totals on " + fname + ": " + str(e))
        break
"""

payload = {
    "code": code,
    "description": "Enable Calculate Totals on Area and Volume"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
