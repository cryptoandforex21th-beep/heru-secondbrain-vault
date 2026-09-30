import httpx

code = """
old_schedules = [
    "RAB DRAFT Makassar 2026 - Curtain Wall Glass (AHSP PU 8/2023)",
    "RAB DRAFT Makassar 2026 - Curtain Wall Iron (AHSP PU 8/2023)",
    "RAB DRAFT Makassar 2026 - Floors (AHSP Permen PU 8/2023)",
    "RAB DRAFT Makassar 2026 - Walls (AHSP Permen PU 8/2023)"
]

schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
deleted = []

for s in schedules:
    if s.Name in old_schedules:
        doc.Delete(s.Id)
        deleted.append(s.Name)

print("Deleted old fragmented schedules: " + ", ".join(deleted))

# Check remaining schedules
remaining = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
print("Remaining schedules: " + ", ".join([s.Name for s in remaining if not s.IsTemplate]))
"""

payload = {
    "code": code,
    "description": "Delete old fragmented schedules"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
