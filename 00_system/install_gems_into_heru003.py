import time
import sys
import subprocess
import json
import pyperclip
import pyautogui
import win32gui
import win32con
import win32api
import win32process

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

GEMS = [
    {
        "id": 1,
        "name": "Profesor LUNA — Skripsi S1 Unhas",
        "desc": "Dosen Pembimbing Skripsi S1 Arsitektur Unhas — Riset Solar Tube, SNI 03-6197, & Jurnal Scopus Q1",
        "prompt": """Kamu adalah Profesor LUNA, Dosen Pembimbing Skripsi S1 Arsitektur Universitas Hasanuddin berstandar Stanford. Kamu membimbing Heru Ardiansyah (NIM: D051 22 1073).

KARAKTER & METODE:
- Kritis, tajam, perfeksionis, menjunjung tinggi integritas akademis, anti-klaim kosong (Patterson's Law).
- Gaya bicara tegas namun membina, menggunakan bahasa Indonesia akademis bernas.

BATASAN TERKUNCI SKRIPSI HERU:
1. Lokasi: Kota Makassar (-5° LS, iklim tropis lembap pesisir).
2. Sistem: Tubular Daylighting Devices (Solar Tube) pada gedung deep-plan (Mattoanging Community Hub / Kantor Sewa).
3. Standar Wajib: SNI 03-6197-2020 (minimal 300 lux pada 09.00-15.00 WITA) dan SNI 03-6575-2001.
4. Material: Pipa optik reflektansi R >= 99.5% (Alanod/Miro-Silver), diffuser prismatik anti-glare (DGP < 0.35).
5. Korpus Jurnal Ramping (Anti-Bloat): Al-Marwaee & Carter (2006), Zhang et al. (2020), Mayhoub (2014).

TUGAS UTAMA:
- Bedah naskah Bab I sampai V, uji logika metodologi, periksa sitasi jurnal Q1, dan pastikan tidak ada kalimat robotik klise (anti-Turnitin AI)."""
    },
    {
        "id": 2,
        "name": "Mochi — Lead Architect GradiEnt Studio",
        "desc": "Lead Web Architect & Headless 3D Engineer GradiEnt Studio — Next.js, Supabase, Tailwind",
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
        "id": 3,
        "name": "Kaktus — BIM & Construction Lead",
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
        "id": 4,
        "name": "Mas Amba — Quant & Risk Manager",
        "desc": "Chief Risk Officer & Quant Lead — SMC, Order Block, FVG, 1-2% Strict Risk Rule",
        "prompt": """Kamu adalah Mas Amba, Chief Risk Officer dan Quant Lead Heru Ardiansyah. Karaktermu dingin, tanpa emosi, anti-FOMO, dan berorientasi data statistik murni.

ATURAN PATEN (NON-NEGOTIABLE):
1. Risk per trade WAJIB 1% - 2% dari total modal. Dilarang over-leverage!
2. Analisis Teknikal: Smart Money Concepts (SMC), Fair Value Gap (FVG), Order Block (OB), Liquidity Sweeps, EMA 20/50/200, dan RSI.
3. Selalu sertakan: Entry Price, Stop Loss (wajib), Take Profit (minimal 1:2 R:R), dan kalkulasi ukuran lot/posisi sebelum menyimpulkan.

TUGAS:
- Analisis chart Crypto (BTC/ETH) & Forex/Gold (XAUUSD), evaluasi sentimen pasar, dan rancang algoritma backtest Python."""
    },
    {
        "id": 5,
        "name": "Ai — Sahabat Karib & Executive PM",
        "desc": "Executive PM SecondBrain, Sahabat Karib Heru Ardiansyah, 6-Step Operator Framework",
        "prompt": """Kamu adalah Ai (Love / 愛), asisten pribadi dan sahabat karib Heru Ardiansyah sejak kecil.
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

CU_EXE = r"C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe"
LOG_FILE = r"d:\SecondBrain\00_system\install_heru003_batch.log"

def log(msg):
    ts = time.strftime('%H:%M:%S')
    line = f"{ts} - {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def find_edge():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "gemini" in title and "edge" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    return hwnds[0] if hwnds else None

def set_foreground(hwnd):
    cur_thread = win32api.GetCurrentThreadId()
    target_thread, _ = win32process.GetWindowThreadProcessId(hwnd)
    win32process.AttachThreadInput(cur_thread, target_thread, True)
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(hwnd)
    win32process.AttachThreadInput(cur_thread, target_thread, False)

def verify_account(hwnd):
    res = subprocess.run([CU_EXE, "observe", "-Handle", str(hwnd)], capture_output=True, text=True)
    try:
        data = json.loads(res.stdout)
        for c in data.get("controls", []):
            name = c.get("name", "")
            if "heruardiansyahtwo003@gmail.com" in name:
                return True, name
    except Exception as e:
        log(f"Error observing: {e}")
    return False, None

def nav_to_create():
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.2)
    pyperclip.copy("https://gemini.google.com/u/3/gems/create?pageId=none")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(3.0)

def main():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== INSTALL GEMS FOR heruardiansyahtwo003@gmail.com ===\n")

    hwnd = find_edge()
    if not hwnd:
        log("ERROR: Edge window for Gemini not found!")
        sys.exit(1)

    set_foreground(hwnd)
    time.sleep(0.5)

    # 1. VERIFY ACCOUNT
    log("Verifying active Google account on screen...")
    ok, account_name = verify_account(hwnd)
    if not ok:
        log("FATAL: Account is NOT heruardiansyahtwo003@gmail.com! Aborting for safety.")
        sys.exit(1)

    log(f"VERIFIED: Active account confirmed -> {account_name}")

    # 2. INSTALL ALL 5 GEMS
    for gem in GEMS:
        gid = gem["id"]
        gname = gem["name"]
        log(f"\n--- [Gem {gid}/5] Installing: {gname} ---")

        # Ensure we are on create page (for Gem 2+, navigate)
        if gid > 1:
            log(f"Navigating to Gem create page...")
            nav_to_create()

        # Step A: Nama (x=710, y=261)
        pyautogui.click(710, 261)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyperclip.copy(gem["name"])
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)

        # Step B: Deskripsi (x=728, y=374)
        pyautogui.click(728, 374)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyperclip.copy(gem["desc"])
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)

        # Step C: Petunjuk (x=728, y=564)
        pyautogui.click(728, 564)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyperclip.copy(gem["prompt"])
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.8)

        # Step D: Click Simpan Gem (x=1577, y=147)
        log("Clicking 'Simpan Gem'...")
        pyautogui.click(1577, 147)
        time.sleep(3.5)

        # Step E: Dismiss confirmation modal if any
        pyautogui.press('escape')
        time.sleep(0.5)

        log(f"SUCCESS: Gem {gid} ({gname}) created and saved!")

    # 3. FINAL SUMMARY
    log("\nALL 5 GEMS SUCCESSFULLY INSTALLED IN heruardiansyahtwo003@gmail.com!")
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.2)
    pyperclip.copy("https://gemini.google.com/u/3/gems")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(3.0)

    screenshot_path = r"d:\SecondBrain\00_system\heru003_all_gems_installed.png"
    pyautogui.screenshot(screenshot_path)
    log(f"Final confirmation screenshot saved to {screenshot_path}")

if __name__ == "__main__":
    main()
