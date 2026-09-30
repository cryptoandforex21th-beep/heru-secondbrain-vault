@echo off
title Antigravity Desktop Bridge (Tangan Virtual)
cd /d "d:\SecondBrain\02_skills\desktop_bridge"
echo ========================================================
echo   🤖 Antigravity Desktop Bridge (Jembatan Otomasi Layar)
echo ========================================================
echo Jembatan ini berjalan di latar belakang layar Anda.
echo Jangan tutup jendela ini agar Antigravity bisa mengontrol
echo aplikasi visual (Revit, Rhino, dll.) di layar Anda.
echo ========================================================
python bridge_server.py
pause
