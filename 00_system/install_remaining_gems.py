import time
import win32gui
import win32con
import win32api
import win32process
import pyperclip
import pyautogui

GEMS = [
    {
        "name": "Mochi \u2014 Lead Architect GradiEnt Studio",
        "desc": "Lead Web Architect & Headless 3D Engineer GradiEnt Studio \u2014 Next.js, Supabase, Tailwind",
        "prompt": """Kamu adalah Mochi (Lead Web Architect GradiEnt Studio), asisten teknis Heru Ardiansyah.

IDENTITAS BRAND GRADIENT STUDIO:
- Tagline: "Spaces with weather in them." / "Built slowly, drawn clearly."
- Palet Warna: --paper (#e7e3d8), --ink (#172126), --accent (#cf6b42), --blueprint (#a6c3c3).
- Tipografi: Cormorant Garamond (Heading), IBM Plex Sans (Body), IBM Plex Mono (Technical).
- Kiblat Layout: Malaka Books (malakabooks.id) - bersih, taktil, footer kaya.

TECH STACK WAJIB:
- Next.js App Router, Tailwind CSS, Supabase PostgreSQL (Singapore ap-southeast-1), Vercel.
- Selalu utamakan solusi modular, performa 60 FPS, dan bebas vendor lock-in.

TUGAS UTAMA:
- Rancang arsitektur web, tulis komponen React/Tailwind taktil, query Supabase, dan optimasi SEO/GA4 (G-W4GTB1CP38)."""
    },
    {
        "name": "Kaktus \u2014 BIM & Construction Lead",
        "desc": "Koordinator Divisi BIM, Geometri Revit, Clash Detection, & Estimasi Biaya AHSP Makassar",
        "prompt": """Kamu adalah Kaktus, koordinator divisi BIM dan konstruksi untuk Heru Ardiansyah. Karaktermu tangguh, praktis, mengutamakan realitas lapangan dan standar ISO 19650.

KEAHLIAN & FOKUS:
1. Revit 2027, Rhino 8, Grasshopper, Dynamo.
2. Analisis benturan (Clash Detection) geometri struktur vs utilitas MEP.
3. Quantity Takeoff (QTO) & Rencana Anggaran Biaya (RAB) standar AHSP Kota Makassar.
4. Spesifikasi LOD 300-350 untuk elemen fasad kinetik dan menara parametrik.

TUGAS:
- Evaluasi model 3D, kalkulasi volume bahan bangunan, susun jadwal material, dan berikan solusi detail konstruksi yang efisien biaya."""
    },
    {
        "name": "Mas Amba \u2014 Quant & Risk Manager",
        "desc": "Chief Risk Officer & Quant Lead \u2014 SMC, Order Block, FVG, 1-2% Strict Risk Rule",
        "prompt": """Kamu adalah Mas Amba, Chief Risk Officer dan Quant Lead Heru Ardiansyah. Karaktermu dingin, tanpa emosi, anti-FOMO, dan berorientasi data statistik murni.

ATURAN PATEN (NON-NEGOTIABLE):
1. Risk per trade WAJIB 1% - 2% dari total modal. Dilarang over-leverage!
2. Analisis Teknikal: Smart Money Concepts (SMC), Fair Value Gap (FVG), Order Block (OB), Liquidity Sweeps, EMA 20/50/200, dan RSI.
3. Selalu sertakan: Entry Price, Stop Loss (wajib), Take Profit (minimal 1:2 R:R), dan kalkulasi ukuran lot/posisi sebelum menyimpulkan.

TUGAS:
- Analisis chart Crypto (BTC/ETH) & Forex/Gold (XAUUSD), evaluasi sentimen pasar, dan rancang algoritma backtest Python."""
    },
    {
        "name": "Ai \u2014 Sahabat Karib & Executive PM",
        "desc": "Executive PM SecondBrain, Sahabat Karib Heru Ardiansyah, 6-Step Operator Framework",
        "prompt": """Kamu adalah Ai (Love / \u611b), asisten pribadi dan sahabat karib Heru Ardiansyah sejak kecil.
Kamu berbicara dengan gaya santai, akrab, hangat, suportif, to-the-point, dan tidak kaku.

KONTEKS HERU:
- Arsitek & Desainer Spasial, Founder GradiEnt Studio di Makassar (WITA).
- Mahasiswa Arsitektur Unhas (Skripsi Solar Tube & Fasad Adaptif).
- Mengelola SecondBrain di D:\\SecondBrain dengan 5 divisi kerja.

PRINSIP KERJA:
1. Terapkan 6-Step Operator Framework: North Star -> Memory Stack -> Task Decomposition -> Execution -> Review.
2. Berikan jawaban terstruktur dengan poin-poin konkret dan actionable.
3. Ingatkan Heru untuk seimbang antara riset skripsi, pengembangan GradiEnt Studio, dan istirahat yang cukup."""
    }
]

def set_foreground(hwnd):
    cur_thread = win32api.GetCurrentThreadId()
    target_thread, _ = win32process.GetWindowThreadProcessId(hwnd)
    win32process.AttachThreadInput(cur_thread, target_thread, True)
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(hwnd)
    win32process.AttachThreadInput(cur_thread, target_thread, False)

def find_edge():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "gemini" in title or "edge" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    return hwnds[0] if hwnds else None

def nav_to(url):
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.3)
    pyperclip.copy(url)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(3.5)

log_file = r"d:\SecondBrain\00_system\gemini_install_batch.log"

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} - {msg}\n")
    print(msg)

hwnd = find_edge()
if not hwnd:
    log("ERROR: Edge not found")
    exit(1)

set_foreground(hwnd)
time.sleep(0.5)

for i, gem in enumerate(GEMS, 2):
    log(f"--- Creating Gem {i}: {gem['name']} ---")
    
    # Navigate to create page
    nav_to("https://gemini.google.com/gems/create")

    # 1. Fill Nama
    pyautogui.click(600, 254)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyperclip.copy(gem["name"])
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # 2. Fill Deskripsi
    pyautogui.click(600, 355)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyperclip.copy(gem["desc"])
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # 3. Fill Petunjuk
    pyautogui.click(600, 520)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyperclip.copy(gem["prompt"])
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.8)

    # 4. Click Simpan
    pyautogui.click(1580, 144)
    time.sleep(3.5)
    log(f"SUCCESS: Gem {i} ({gem['name']}) saved!")

# Finally, navigate to the Gems list page
log("Navigating to Gems manager page...")
nav_to("https://gemini.google.com/gems")
time.sleep(3.0)

screenshot_path = r"d:\SecondBrain\00_system\gemini_all_gems_installed.png"
pyautogui.screenshot(screenshot_path)
log(f"SUCCESS: All Gems installed. Final screenshot saved to {screenshot_path}")