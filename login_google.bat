@echo off
title Login Google Cloud via Microsoft Edge - SecondBrain
cd /d "d:\SecondBrain"
echo ========================================================
echo   🔐 Menghubungkan Google Cloud ke heruardiansyahtwo003@gmail.com
echo   🌐 Menggunakan Microsoft Edge
echo ========================================================
set BROWSER=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
echo Membuka Microsoft Edge...
echo Silakan pilih akun: heruardiansyahtwo003@gmail.com lalu klik "Izinkan / Allow".
echo ========================================================
"C:\Users\Heru Ardiansyah\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" auth login heruardiansyahtwo003@gmail.com
echo.
echo ========================================================
echo   🔐 Langkah 2: Mengaktifkan Application Default Credentials
echo ========================================================
"C:\Users\Heru Ardiansyah\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" auth application-default login
echo.
echo ========================================================
echo   ✅ Selesai! Anda sudah terhubung.
echo ========================================================
pause
