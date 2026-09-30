import time
import win32gui
import win32con
import win32api
import pyperclip
import pyautogui

def bring_edge():
    hwnds = []
    def enum_cb(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "edge" in title or "gemini" in title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    if hwnds:
        hwnd = hwnds[0]
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32api.keybd_event(18, 0, 0, 0)
        win32gui.SetForegroundWindow(hwnd)
        win32api.keybd_event(18, 0, 2, 0)
        time.sleep(0.5)
        return True
    return False

def test_fill_gem1():
    if not bring_edge():
        print("Edge not found")
        return

    name = "Profesor LUNA \u2014 Skripsi S1 Unhas"
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

    # 1. Click Nama
    pyautogui.click(300, 254)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    # 2. Click Deskripsi
    pyautogui.click(300, 355)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(desc)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    # 3. Click Petunjuk
    pyautogui.click(300, 520)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(prompt)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)

    # Capture preview before save
    pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_filled_test.png")
    
    # 4. Click Simpan (x=819, y=147)
    pyautogui.click(819, 147)
    time.sleep(4.0)

    # Capture after save
    pyautogui.screenshot(r"d:\SecondBrain\00_system\gemini_saved_test.png")
    with open(r"d:\SecondBrain\00_system\gemini_diag.log", "w", encoding="utf-8") as f:
        f.write("Gem 1 filled and clicked save.\n")

test_fill_gem1()