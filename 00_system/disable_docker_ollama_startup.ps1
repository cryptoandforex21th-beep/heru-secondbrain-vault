# Disable Docker and Ollama Auto-Start
Write-Host "Disabling Ollama from Startup folder..." -ForegroundColor Cyan
$ollamaLnk = "$([Environment]::GetFolderPath('Startup'))\Ollama.lnk"
if (Test-Path $ollamaLnk) {
    Rename-Item -Path $ollamaLnk -NewName "Ollama.lnk.disabled" -Force
    Write-Host "BERHASIL: Ollama.lnk dinonaktifkan (di-rename ke .disabled)!" -ForegroundColor Green
} else {
    Write-Host "Ollama.lnk tidak ditemukan di Startup folder (mungkin sudah nonaktif)."
}

Write-Host "`nDisabling Docker Desktop from Registry Run..." -ForegroundColor Cyan
$runKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$dockerVal = Get-ItemProperty -Path $runKey -Name "Docker Desktop" -ErrorAction SilentlyContinue
if ($dockerVal) {
    Remove-ItemProperty -Path $runKey -Name "Docker Desktop" -Force
    Write-Host "BERHASIL: Docker Desktop dihapus dari Registry Run Startup!" -ForegroundColor Green
} else {
    Write-Host "Docker Desktop tidak ada di Registry Run."
}

# Also check Docker settings.json if exists
$dockerSettings = "$env:APPDATA\Docker\settings.json"
if (Test-Path $dockerSettings) {
    try {
        $json = Get-Content $dockerSettings | ConvertFrom-Json
        $json.openAtLogin = $false
        $json | ConvertTo-Json -Depth 10 | Set-Content $dockerSettings
        Write-Host "BERHASIL: Docker Desktop openAtLogin diset ke false!" -ForegroundColor Green
    } catch {
        Write-Host "Gagal update settings.json Docker: $_"
    }
}
