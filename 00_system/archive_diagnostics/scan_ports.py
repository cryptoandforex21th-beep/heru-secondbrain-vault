"""
Scan semua port lokal aktif dan coba request HTTP ke /revit_mcp/status/
untuk menemukan port pyRevit Routes yang sesungguhnya.
"""
import socket
import httpx
import json

# Daftar port yang perlu diperiksa
# pyRevit Routes default port: 48884 (dari dokumentasi pyRevit)
# Tapi bisa juga di port lain jika dikonfigurasi berbeda
CANDIDATES = [
    # pyRevit Routes defaults:
    48884, 48885, 48886, 48887,
    # Port lokal yang aktif berdasarkan netstat:
    18100, 49438, 49675, 49696, 49697, 49999,
    # Common alternatives:
    5000, 5001, 8000, 8080, 8888, 3000, 4000,
]

def try_port(port, path="/revit_mcp/status/"):
    url = f"http://127.0.0.1:{port}{path}"
    try:
        r = httpx.get(url, timeout=2.0)
        return port, r.status_code, r.text[:300]
    except httpx.ConnectError:
        return port, "REFUSED", None
    except httpx.ConnectTimeout:
        return port, "TIMEOUT", None
    except Exception as e:
        return port, f"ERROR: {type(e).__name__}", str(e)[:100]

print("=== PORT SCAN FOR pyRevit Routes ===\n")
for port in CANDIDATES:
    p, code, body = try_port(port)
    if code not in ("REFUSED",):
        print(f"Port {p}: status={code}")
        if body:
            print(f"  Body: {body[:200]}")
    else:
        print(f"Port {p}: REFUSED")

# Also try root of each port that isn't refused
print("\n=== ALSO TRY ROOT '/' ON NON-REFUSED PORTS ===")
for port in CANDIDATES:
    p, code, body = try_port(port, "/")
    if code not in ("REFUSED",):
        print(f"Port {p} /: status={code} body={str(body)[:200]}")
