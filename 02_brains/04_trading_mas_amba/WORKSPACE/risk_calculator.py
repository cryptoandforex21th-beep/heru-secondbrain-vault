"""
Risk & Position Sizing Calculator - Divisi Trading Mas Amba (@Rem)
Protokol manajemen risiko ketat untuk menghitung lot/position size dan R:R.
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def calculate_trade(equity: float, risk_pct: float, entry: float, stop_loss: float, asset_type: str = "crypto"):
    """
    asset_type: 'crypto' atau 'forex_gold' (1 standard lot = 100 oz gold / 100k currency)
    """
    if entry == stop_loss:
        raise ValueError("Entry dan Stop Loss tidak boleh sama!")
    
    direction = "LONG (BUY)" if entry > stop_loss else "SHORT (SELL)"
    stop_distance = abs(entry - stop_loss)
    risk_dollar = equity * (risk_pct / 100.0)
    
    # Target R:R
    tp_1_2 = entry + (2 * stop_distance) if direction.startswith("LONG") else entry - (2 * stop_distance)
    tp_1_3 = entry + (3 * stop_distance) if direction.startswith("LONG") else entry - (3 * stop_distance)
    
    position_units = risk_dollar / stop_distance
    position_value = position_units * entry
    
    print("\n" + "="*60)
    print("🛑 PROTOKOL RISK MANAGEMENT @REM (MAS AMBA DIVISION)")
    print("="*60)
    print(f"💰 Total Modal (Equity)    : ${equity:,.2f}")
    print(f"🎯 Risiko per Trade         : {risk_pct:.1f}% (${risk_dollar:,.2f})")
    print(f"🧭 Arah Posisi              : {direction}")
    print(f"📍 Entry Price              : ${entry:,.4f}")
    print(f"🛑 Stop Loss Price          : ${stop_loss:,.4f} (Jarak: ${stop_distance:,.4f})")
    print("-" * 60)
    print(f"🎯 Take Profit 1 (R:R 1:2)  : ${tp_1_2:,.4f} (Profit: +${risk_dollar*2:,.2f})")
    print(f"🎯 Take Profit 2 (R:R 1:3)  : ${tp_1_3:,.4f} (Profit: +${risk_dollar*3:,.2f})")
    print("-" * 60)
    
    if asset_type == "crypto":
        print(f"📦 Rekomendasi Ukuran Posisi: {position_units:.6f} koin (${position_value:,.2f} Notional)")
    else:
        # Untuk Gold / Forex standar (1 lot XAUUSD = 100 oz)
        lot_size = position_units / 100.0
        print(f"📦 Rekomendasi Lot (Gold/FX): {lot_size:.2f} Lot standar")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Kalkulator Risk & Position Size @Rem")
    parser.add_argument("--equity", type=float, default=1000.0, help="Total modal dalam USD (default: 1000)")
    parser.add_argument("--risk", type=float, default=1.5, help="Persentase risiko (default: 1.5%%)")
    parser.add_argument("--entry", type=float, default=83500.0, help="Harga entry")
    parser.add_argument("--sl", type=float, default=82000.0, help="Harga stop loss")
    parser.add_argument("--type", type=str, default="crypto", choices=["crypto", "forex"], help="Tipe aset")
    
    args = parser.parse_args()
    calculate_trade(args.equity, args.risk, args.entry, args.sl, args.type)
