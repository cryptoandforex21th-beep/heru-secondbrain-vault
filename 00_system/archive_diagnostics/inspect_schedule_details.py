import httpx

code = """
schedules = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
for s in schedules:
    if s.IsTemplate: continue
    print("=" * 60)
    print("Schedule: " + s.Name)
    defn = s.Definition
    print("Field Count: " + str(defn.GetFieldCount()))
    for i in range(defn.GetFieldCount()):
        f = defn.GetField(i)
        print("  Field {0}: Name='{1}', FieldType={2}, UnitType={3}, IsHidden={4}".format(
            i, f.GetName(), f.FieldType, f.GetUnitTypeId().TypeId if hasattr(f, 'GetUnitTypeId') else 'N/A', f.IsHidden
        ))
    
    # Check filters
    filter_count = defn.GetFilterCount()
    print("Filter Count: " + str(filter_count))
    for i in range(filter_count):
        flt = defn.GetFilter(i)
        print("  Filter {0}: FieldId={1}, FilterType={2}, Value={3}".format(
            i, flt.FieldId.Value if hasattr(flt.FieldId, 'Value') else flt.FieldId, flt.FilterType, flt.GetStringValue() if hasattr(flt, 'GetStringValue') else 'N/A'
        ))
        
    # Check sorting
    sort_count = defn.GetSortGroupFieldCount()
    print("Sort Count: " + str(sort_count))
    for i in range(sort_count):
        sg = defn.GetSortGroupField(i)
        print("  Sort {0}: FieldId={1}".format(i, sg.FieldId.Value if hasattr(sg.FieldId, 'Value') else sg.FieldId))
"""

payload = {
    "code": code,
    "description": "Inspect schedule definitions in detail"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
