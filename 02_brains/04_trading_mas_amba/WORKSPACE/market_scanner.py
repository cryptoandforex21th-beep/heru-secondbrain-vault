"""
Market Scanner - Divisi Trading Mas Amba (@Amba, @Lilin, @Bandar)
Mengambil data harga pasar crypto (Binance) dan komoditas/forex secara live.
"""

import requests
import json
from datetime import datetime

def scan_crypto():
    symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT']
    results = []
    for s in symbols:
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={s}"
            res = requests.get(url, timeout=5).json()
            results.append({
                "symbol": s.replace("USDT", "/USDT"),
                "price": float(res["lastPrice"]),
                "change_pct": float(res["priceChangePercent"]),
                "high": float(res["highPrice"]),
                "low": float(res["lowPrice"]),
                "volume": float(res["quoteVolume"])
            })
        except Exception as e:
            results.append({"symbol": s, "error": str(e)})
    return results

def scan_macro():
    tickers = [
        ("GC=F", "Gold (XAU/USD)"),
        ("SI=F", "Silver (XAG/USD)"),
        ("EURUSD=X", "EUR/USD"),
        ("DX-Y.NYB", "US Dollar Index (DXY)")
    ]
    results = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for ticker, name in tickers:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                meta = r.json()['chart']['result'][0]['meta']
                price = meta.get('regularMarketPrice')
                prev = meta.get('chartPreviousClose')
                change_pct = ((price - prev) / prev * 100) if prev else 0.0
                results.append({
                    "name": name,
                    "symbol": ticker,
                    "price": price,
                    "change_pct": change_pct
                })
        except Exception as e:
            results.append({"name": name, "symbol": ticker, "error": str(e)})
    return results

import sys
import io

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_dashboard():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*65}")
    print(f"📊 MAS AMBA QUANTITATIVE TERMINAL | {now}")
    print(f"{'='*65}")
    
    print("\n💎 [CRYPTO MARKET - BINANCE FEED]")
    print(f"{'Pair':<12} | {'Price':<12} | {'24h Change':<12} | {'24h High':<10} | {'24h Low':<10}")
    print("-" * 65)
    for c in scan_crypto():
        if "error" in c:
            print(f"{c['symbol']:<12} | Error fetching data")
        else:
            chg = f"{c['change_pct']:+.2f}%"
            print(f"{c['symbol']:<12} | ${c['price']:<11,.2f} | {chg:<12} | ${c['high']:<9,.2f} | ${c['low']:<9,.2f}")

    print("\n🌍 [COMMODITY & FOREX - MACRO FEED]")
    print(f"{'Asset':<24} | {'Price':<14} | {'Change %':<10}")
    print("-" * 65)
    for m in scan_macro():
        if "error" in m:
            print(f"{m['name']:<24} | Error: {m['error']}")
        else:
            chg = f"{m['change_pct']:+.2f}%"
            print(f"{m['name']:<24} | ${m['price']:<13,.2f} | {chg:<10}")
    print(f"{'='*65}\n")

if __name__ == "__main__":
    print_dashboard()
