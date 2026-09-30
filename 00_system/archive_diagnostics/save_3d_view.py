import httpx
import base64

r = httpx.get('http://127.0.0.1:48884/revit_mcp/get_view/%7B3D%7D', timeout=15)
data = r.json()
img_bytes = base64.b64decode(data['image_data'])

out_path = r"d:\SecondBrain\00_system\revit_live_3d_export.png"
with open(out_path, "wb") as f:
    f.write(img_bytes)

print(f"Successfully saved {len(img_bytes)} bytes to {out_path}")
