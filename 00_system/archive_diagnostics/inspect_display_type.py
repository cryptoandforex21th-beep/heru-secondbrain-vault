import httpx

code = """
import clr
print([e.ToString() for e in System.Enum.GetValues(DB.ScheduleFieldDisplayType)])
"""

payload = {
    "code": code,
    "description": "Inspect ScheduleFieldDisplayType enum"
}

r = httpx.post("http://127.0.0.1:48884/revit_mcp/execute_code/", json=payload, timeout=20)
print(r.status_code)
res = r.json()
print(res.get("output", res))
