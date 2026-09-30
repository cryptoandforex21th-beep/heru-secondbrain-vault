# Fix 2: Set Microsoft Edge to use NVIDIA RTX 3060 (High Performance GPU)
$edgePath = (Get-Process msedge -ErrorAction SilentlyContinue | Select-Object -First 1).Path
if (-not $edgePath) {
    $edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
}
Write-Host "Edge Path: $edgePath"

if (Test-Path $edgePath) {
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\DirectX\UserGpuPreferences" -Name $edgePath -Value "GpuPreference=2;"
    Write-Host "BERHASIL: Microsoft Edge sekarang dikunci ke High Performance GPU (NVIDIA RTX 3060)!" -ForegroundColor Green
    
    # Verifikasi
    $res = Get-ItemProperty -Path "HKCU:\Software\Microsoft\DirectX\UserGpuPreferences" -Name $edgePath
    Write-Host "Registry Status: $($res.$edgePath)"
} else {
    Write-Host "Edge path tidak ditemukan di $edgePath" -ForegroundColor Red
}

# Fix 1 & 2 helper: Enable Efficiency Mode & Sleeping Tabs settings in Edge if possible
Write-Host "`nMemeriksa Sleeping Tabs Edge..."
$edgePolicy = "HKCU:\Software\Policies\Microsoft\Edge"
if (-not (Test-Path $edgePolicy)) {
    New-Item -Path $edgePolicy -Force | Out-Null
}
# Enable sleeping tabs after 5 minutes of inactivity to save 3+ GB RAM automatically
Set-ItemProperty -Path $edgePolicy -Name "SleepingTabsEnabled" -Value 1 -Type DWord -Force
Set-ItemProperty -Path $edgePolicy -Name "SleepingTabsTimeout" -Value 300 -Type DWord -Force
Write-Host "BERHASIL: Sleeping Tabs Edge diaktifkan otomatis (tab tidak aktif tidur setelah 5 menit)!" -ForegroundColor Green
