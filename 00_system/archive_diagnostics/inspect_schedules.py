import httpx

code = """
schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
print("Total ViewSchedule elements: " + str(len(schedules)))

for s in schedules:
    if s.IsTemplate:
        continue
    print("=" * 60)
    print("Schedule Name: " + str(s.Name))
    try:
        defn = s.Definition
        cat_id = defn.CategoryId
        print("Category Id: " + str(cat_id.Value))
        print("IsMaterialTakeoff: " + str(defn.IsMaterialTakeoff))
        
        field_count = defn.GetFieldCount()
        field_names = []
        for i in range(field_count):
            f = defn.GetField(i)
            field_names.append(str(f.GetName()))
        print("Fields (" + str(field_count) + "): " + ", ".join(field_names))
        
        table = s.GetTableData()
        section = table.GetSectionData(DB.SectionType.Body)
        print("Rows: " + str(section.NumberOfRows) + ", Cols: " + str(section.NumberOfColumns))
    except Exception as e:
        print("Error: " + str(e))
"""

payload = {
    "code": code,
    "description": "Inspect existing schedules Python 2 compatible"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
