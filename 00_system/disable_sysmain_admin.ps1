# Elevated Script to Disable SysMain & DiagTrack
Write-Host "Menghentikan dan menonaktifkan SysMain (Superfetch)..." -ForegroundColor Cyan
sc.exe stop SysMain
sc.exe config SysMain start= disabled

Write-Host "`nMenghentikan dan menonaktifkan DiagTrack (Windows Telemetry)..." -ForegroundColor Cyan
sc.exe stop DiagTrack
sc.exe config DiagTrack start= disabled

Write-Host "`nMerapikan Working Set RAM..." -ForegroundColor Cyan
[System.GC]::Collect()

Write-Host "`nBERHASIL! SysMain dan Telemetri berhasil dinonaktifkan." -ForegroundColor Green
Start-Sleep -Seconds 3
