"""
Edge CDP Bridge (edge_cdp.py) — Microsoft Edge DevTools Protocol Engine
Enables sub-50ms DOM manipulation, JavaScript evaluation, tab management,
and headless/headed automation for SecondBrain without moving the physical mouse.
"""

import sys
import os
import time
import json
import asyncio
import urllib.request
import urllib.parse
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import websockets
except ImportError:
    websockets = None

CDP_PORT = 9222
SYS_DIR = os.path.dirname(os.path.abspath(__file__))
EDGE_DEV_DIR = r"C:\Users\Heru Ardiansyah\.gemini\edge_dev"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def check_cdp_alive(port=CDP_PORT):
    try:
        url = f"http://127.0.0.1:{port}/json/version"
        req = urllib.request.urlopen(url, timeout=1.5)
        data = json.loads(req.read().decode())
        return data
    except Exception:
        return None

def ensure_edge(url="about:blank", port=CDP_PORT):
    alive = check_cdp_alive(port)
    if alive:
        return True, alive

    print(f"⚡ Launching Microsoft Edge with CDP on port {port}...")
    launcher = os.path.join(SYS_DIR, "app_launcher.py")
    edge_cmd = f'"{EDGE_EXE}" --remote-debugging-port={port} --user-data-dir="{EDGE_DEV_DIR}" "{url}"'
    subprocess.run([sys.executable, launcher, edge_cmd], capture_output=True)

    # Wait up to 5 seconds for CDP port to open
    for _ in range(25):
        time.sleep(0.2)
        alive = check_cdp_alive(port)
        if alive:
            print(f"🟢 Connected to Edge CDP! Browser: {alive.get('Browser')}")
            return True, alive

    return False, None

def list_pages(port=CDP_PORT):
    try:
        url = f"http://127.0.0.1:{port}/json/list"
        req = urllib.request.urlopen(url, timeout=2.0)
        tabs = json.loads(req.read().decode())
        return [t for t in tabs if t.get("type") == "page"]
    except Exception as e:
        print(f"Error listing pages: {e}")
        return []

def get_target_page(url_pattern=None, tab_id=None, port=CDP_PORT):
    pages = list_pages(port)
    if not pages:
        return None
    if tab_id:
        for p in pages:
            if p.get("id") == tab_id:
                return p
    if url_pattern:
        for p in pages:
            if url_pattern.lower() in p.get("url", "").lower() or url_pattern.lower() in p.get("title", "").lower():
                return p
    # Return first active page
    return pages[0]

def new_tab(url="about:blank", port=CDP_PORT):
    try:
        encoded_url = urllib.parse.quote(url, safe="")
        req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json/new?{encoded_url}", timeout=2.0)
        return json.loads(req.read().decode())
    except Exception as e:
        print(f"Error opening new tab: {e}")
        return None

def close_tab(tab_id, port=CDP_PORT):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/close/{tab_id}", timeout=2.0)
        return True
    except Exception:
        return False

def activate_tab(tab_id, port=CDP_PORT):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/activate/{tab_id}", timeout=2.0)
        return True
    except Exception:
        return False

async def _send_cdp_cmd(ws_url, method, params=None):
    if not websockets:
        raise RuntimeError("websockets library not installed")
    async with websockets.connect(ws_url) as ws:
        msg_id = int(time.time() * 1000) % 100000
        cmd = {"id": msg_id, "method": method, "params": params or {}}
        await ws.send(json.dumps(cmd))
        while True:
            raw = await ws.recv()
            data = json.loads(raw)
            if data.get("id") == msg_id:
                return data

def run_cdp(method, params=None, url_pattern=None, tab_id=None, port=CDP_PORT):
    page = get_target_page(url_pattern, tab_id, port)
    if not page:
        return {"error": "No matching target page found"}
    ws_url = page.get("webSocketDebuggerUrl")
    if not ws_url:
        return {"error": "Target page has no webSocketDebuggerUrl"}
    return asyncio.run(_send_cdp_cmd(ws_url, method, params))

def eval_js(expression, url_pattern=None, tab_id=None, port=CDP_PORT):
    params = {
        "expression": expression,
        "returnByValue": True,
        "awaitPromise": True
    }
    res = run_cdp("Runtime.evaluate", params, url_pattern, tab_id, port)
    if "result" in res and "result" in res["result"]:
        return res["result"]["result"].get("value")
    return res

def navigate(url, url_pattern=None, tab_id=None, port=CDP_PORT):
    res = run_cdp("Page.navigate", {"url": url}, url_pattern, tab_id, port)
    return res

def fill_input(selector, text, url_pattern=None, tab_id=None, port=CDP_PORT):
    clean_text = json.dumps(text)
    js = f"""
    (() => {{
        const el = document.querySelector({json.dumps(selector)});
        if (!el) return {{success: false, error: 'Element not found: ' + {json.dumps(selector)}}};
        el.focus();
        el.value = {clean_text};
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return {{success: true, value: el.value}};
    }})();
    """
    return eval_js(js, url_pattern, tab_id, port)

def click_element(selector, url_pattern=None, tab_id=None, port=CDP_PORT):
    js = f"""
    (() => {{
        const el = document.querySelector({json.dumps(selector)});
        if (!el) return {{success: false, error: 'Element not found: ' + {json.dumps(selector)}}};
        el.click();
        return {{success: true}};
    }})();
    """
    return eval_js(js, url_pattern, tab_id, port)

def capture_screenshot(output_path, url_pattern=None, tab_id=None, port=CDP_PORT):
    import base64
    res = run_cdp("Page.captureScreenshot", {"format": "png"}, url_pattern, tab_id, port)
    if "result" in res and "data" in res["result"]:
        raw_b64 = res["result"]["data"]
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(raw_b64))
        return True, output_path
    return False, res

# --- CLI Interface ---
def print_help():
    print("""
Edge CDP Bridge CLI:
  python edge_cdp.py status                 : Check if Edge CDP port is active
  python edge_cdp.py launch [url]           : Launch Edge with CDP enabled in Session 1
  python edge_cdp.py list                   : List all open tabs with IDs and URLs
  python edge_cdp.py new <url>              : Open a new tab instantly (<15ms)
  python edge_cdp.py nav <url> [pattern]    : Navigate current or matching tab to URL
  python edge_cdp.py eval <js_code>         : Execute JavaScript directly in page
  python edge_cdp.py click <css_selector>   : Click DOM element directly via CSS selector
  python edge_cdp.py fill <selector> <text> : Fill input field and trigger React events
  python edge_cdp.py shot <output.png>      : High-speed screenshot directly via CDP (<50ms)
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    if cmd == "status":
        info = check_cdp_alive()
        if info:
            print(f"🟢 Edge CDP is ACTIVE on port {CDP_PORT}")
            print(f"   Browser : {info.get('Browser')}")
            print(f"   Protocol: {info.get('Protocol-Version')}")
        else:
            print(f"🔴 Edge CDP is NOT active on port {CDP_PORT}")

    elif cmd == "launch":
        url = args[0] if args else "about:blank"
        ok, info = ensure_edge(url)
        if ok:
            print(f"🚀 Edge ready with CDP: {info.get('Browser')}")
        else:
            print("❌ Failed to connect to Edge CDP.")

    elif cmd == "list":
        pages = list_pages()
        print(f"📑 Open Tabs ({len(pages)}):")
        for i, p in enumerate(pages, 1):
            print(f"   [{i}] {p.get('title')[:45].ljust(45)} | {p.get('url')[:45]}")
            print(f"       ID: {p.get('id')}")

    elif cmd == "new":
        url = args[0] if args else "about:blank"
        res = new_tab(url)
        if res:
            print(f"🟢 New Tab Opened (ID: {res.get('id')}): {url}")
        else:
            print("❌ Failed to open new tab.")

    elif cmd in ["nav", "navigate"]:
        if not args:
            print("Usage: python edge_cdp.py nav <url> [pattern]")
            sys.exit(1)
        target_url = args[0]
        pat = args[1] if len(args) > 1 else None
        res = navigate(target_url, url_pattern=pat)
        print(f"🌐 Navigated to {target_url} (Response: {res})")

    elif cmd == "eval":
        if not args:
            print("Usage: python edge_cdp.py eval <js_code>")
            sys.exit(1)
        js = " ".join(args)
        val = eval_js(js)
        print(f"✨ JS Evaluation Result:\n{json.dumps(val, indent=2) if isinstance(val, (dict, list)) else val}")

    elif cmd == "click":
        if not args:
            print("Usage: python edge_cdp.py click <css_selector>")
            sys.exit(1)
        sel = args[0]
        val = click_element(sel)
        print(f"🖱️ Clicked '{sel}': {val}")

    elif cmd == "fill":
        if len(args) < 2:
            print("Usage: python edge_cdp.py fill <css_selector> <text>")
            sys.exit(1)
        sel = args[0]
        text = " ".join(args[1:])
        val = fill_input(sel, text)
        print(f"⌨️ Filled '{sel}': {val}")

    elif cmd in ["shot", "screenshot"]:
        out = args[0] if args else r"d:\SecondBrain\00_system\cdp_screenshot.png"
        ok, res = capture_screenshot(out)
        if ok:
            print(f"📸 Screenshot saved to {out} via CDP (<50ms)!")
        else:
            print(f"❌ Screenshot failed: {res}")
    else:
        print_help()
