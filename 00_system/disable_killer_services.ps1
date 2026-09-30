# Safely stop and disable Killer Network bloat services
$killerServices = @(
    "Killer Analytics Service",
    "Killer Network Service",
    "Killer Provider Data Helper Service",
    "KAPSService",
    "KNDBWM"
)

foreach ($s in $killerServices) {
    try {
        Stop-Service -Name $s -Force -ErrorAction SilentlyContinue
        Set-Service -Name $s -StartupType Disabled -ErrorAction SilentlyContinue
        Write-Host "Service '$s' dinonaktifkan (Disabled) & dihentikan!" -ForegroundColor Green
    } catch {
        Write-Host "Gagal update service '$s': $_" -ForegroundColor Red
    }
}

# Verify Wi-Fi connectivity
Start-Sleep -Seconds 2
$ping = Test-Connection -ComputerName 8.8.8.8 -Count 1 -Quiet
Write-Host "`nStatus Internet Wi-Fi: $(if ($ping) { 'LANCAR & TERKONEKSI (OK)' } else { 'TERPUTUS' })" -ForegroundColor Cyan
