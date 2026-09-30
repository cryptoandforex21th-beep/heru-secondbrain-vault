# 🧭 ROUTING POLICY: Mas Amba (Divisi Trading)

## Aturan Komunikasi & Rute Perintah
1. **Trigger Callout:** Jika Heru memanggil `@Amba`, `@MasAmba`, atau meminta cek market crypto/forex, kalkulasi lot size, backtest script, atau jalankan bot trading, perintah langsung dialihkan ke Mas Amba.
2. **Koordinasi dengan Divisi Lain:**
   * Jika Mas Amba butuh database pencatatan riwayat trading: koordinasi dengan `@Kunci` (Supabase).
   * Jika Mas Amba butuh dashboard visualisasi portofolio: koordinasi dengan `@Mochi` & `@Piksel` (GradiEnt Studio App).
   * Jika Heru butuh notifikasi trading darurat via WhatsApp: gunakan `whatsapp_cli.py` via `@Ai`.
