@echo off
title SecondBrain Portal Launcher
cd /d "d:\SecondBrain"
echo ========================================================
echo   🧠 Menjalankan SecondBrain Antigravity Portal
echo ========================================================
echo Akses lokal di laptop : http://localhost:8000
echo Akses dari HP (Wi-Fi) : Cari IP laptop Anda (misal: http://192.168.1.X:8000)
echo ========================================================
python -m uvicorn 04_app.server:app --host 0.0.0.0 --port 8000 --reload
pause
