"""
Live Proof: Divisi 03 BIM & Konstruksi (@Kaktus & @Cuan)
Quantity Takeoff (QTO) & Rencana Anggaran Biaya (RAB) Menara Dynamo
Berdasarkan Standar AHSP Kota Makassar (Semen Tonasa, Pasir Bili-bili, Besi Ulir SNI)
"""

import sys, io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Volume Elemen Struktur Menara Dynamo (4 Lantai)
# Kolom Utama K1 (40x40 cm), Balok B1 (30x50 cm), Plat Lantai (12 cm)
volume_beton_m3 = 48.5       # m3 Beton f'c = 25 MPa (K-300)
berat_besi_kg = 5820.0       # kg Besi Ulir D16 & Polos D10 (rasio 120 kg/m3)
luas_bekisting_m2 = 320.0    # m2 Bekisting multiplek 12mm

# Harga Satuan AHSP Kota Makassar 2025/2026 (IDR)
HARGA_BETON_K300 = 1250000   # per m3 (Readymix Jayamix Makassar)
HARGA_PEMBESIAN_KG = 16500   # per kg terpasang (Besi Krakatau / Master Steel)
HARGA_BEKISTING_M2 = 210000  # per m2 2x pakai

total_beton = volume_beton_m3 * HARGA_BETON_K300
total_besi = berat_besi_kg * HARGA_PEMBESIAN_KG
total_bekisting = luas_bekisting_m2 * HARGA_BEKISTING_M2
subtotal_fisik = total_beton + total_besi + total_bekisting
overhead_jasa = subtotal_fisik * 0.10 # 10% Jasa Kontraktor
total_rab = subtotal_fisik + overhead_jasa

print("\n" + "="*65)
print("💰 DIVISI BIM & KONSTRUKSI @KAKTUS & @CUAN")
print("ESTIMASI BIAYA STRUKTUR BETON BERTULANG MENARA DYNAMO (AHSP MAKASSAR)")
print("="*65)
print(f"1. Pekerjaan Beton K-300    : {volume_beton_m3:>6.1f} m³  @ Rp {HARGA_BETON_K300:>10,d} = Rp {int(total_beton):>13,d}")
print(f"2. Pekerjaan Pembesian SNI  : {berat_besi_kg:>6.1f} kg  @ Rp {HARGA_PEMBESIAN_KG:>10,d} = Rp {int(total_besi):>13,d}")
print(f"3. Pekerjaan Bekisting 12mm : {luas_bekisting_m2:>6.1f} m²  @ Rp {HARGA_BEKISTING_M2:>10,d} = Rp {int(total_bekisting):>13,d}")
print("-" * 65)
print(f"   Subtotal Biaya Langsung (Material & Upah)  = Rp {int(subtotal_fisik):>13,d}")
print(f"   Overhead & Jasa Kontraktor (10%)          = Rp {int(overhead_jasa):>13,d}")
print("="*65)
print(f"   TOTAL ESTIMASI STRUKTUR MENARA DYNAMO      = Rp {int(total_rab):>13,d}")
print("="*65 + "\n")
