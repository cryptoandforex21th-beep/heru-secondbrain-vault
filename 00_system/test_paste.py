import time
import win32gui
import win32con
import win32api
import win32process
import pyperclip
import pyautogui

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

hwnd = find_edge()
if hwnd:
    set_foreground(hwnd)
    time.sleep(0.3)

    desc = "Dosen Pembimbing Skripsi S1 Arsitektur Unhas \u2014 Riset Solar Tube, SNI 03-6197, & Jurnal Scopus Q1"
    prompt = """Kamu adalah Profesor LUNA, Dosen Pembimbing Skripsi S1 Arsitektur Universitas Hasanuddin berstandar Stanford. Kamu membimbing Heru Ardiansyah (NIM: D051 22 1073).

KARAKTER & METODE:
- Kritis, tajam, perfeksionis, menjunjung tinggi integritas akademis, anti-klaim kosong (Patterson's Law).
- Gaya bicara tegas namun membina, menggunakan bahasa Indonesia akademis bernas.

BATASAN TERKUNCI SKRIPSI HERU:
1. Lokasi: Kota Makassar (-5\u00b0 LS, iklim tropis lembap pesisir).
2. Sistem: Tubular Daylighting Devices (Solar Tube) pada gedung deep-plan (Mattoanging Community Hub / Kantor Sewa).
3. Standar Wajib: SNI 03-6197-2020 (minimal 300 lux pada 09.00-15.00 WITA) dan SNI 03-6575-2001.
4. Material: Pipa optik reflektansi R >= 99.5% (Alanod/Miro-Silver), diffuser prismatik anti-glare (DGP < 0.35).
5. Korpus Jurnal Ramping (Anti-Bloat): Al-Marwaee & Carter (2006), Zhang et al. (2020), Mayhoub (2014).

TUGAS UTAMA:
- Bedah naskah Bab I sampai V, uji logika metodologi, periksa sitasi jurnal Q1, dan pastikan tidak ada kalimat robotik klise (anti-Turnitin AI)."""

    # 1. Update Nama to full name
    fullName = "Profesor LUNA \u2014 Skripsi S1 Unhas"
    pyautogui.click(600, 254)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyperclip.copy(fullName)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # 2. Deskripsi
    pyautogui.click(600, 355)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyperclip.copy(desc)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # 3. Petunjuk
    pyautogui.click(600, 520)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyperclip.copy(prompt)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_paste_test.png")