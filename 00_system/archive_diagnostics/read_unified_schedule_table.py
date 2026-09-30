import httpx

code = """
schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
for s in schedules:
    if s.Name == "RAB TERPADU MENARA DYNAMO - MAKASSAR 2026":
        table = s.GetTableData()
        section = table.GetSectionData(DB.SectionType.Body)
        rows = section.NumberOfRows
        cols = section.NumberOfColumns
        print("Schedule: " + s.Name + " | Rows: " + str(rows) + " | Cols: " + str(cols))
        
        for r in range(rows):
            row_vals = []
            for c in range(cols):
                text = s.GetCellText(DB.SectionType.Body, r, c)
                row_vals.append(str(text))
            print("Row " + str(r) + ": " + " | ".join(row_vals))
        break
"""

payload = {
    "code": code,
    "description": "Inspect unified schedule table rows"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
