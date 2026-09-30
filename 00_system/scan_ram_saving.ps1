# Detailed RAM Optimization Opportunities
Write-Host "================ 1. CURRENT MEMORY STATE ================" -ForegroundColor Cyan
$os = Get-CimInstance Win32_OperatingSystem
$total = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$free = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$used = [math]::Round($total - $free, 2)
$pct = [math]::Round(($used / $total) * 100, 1)
Write-Host "RAM Terpakai: $used GB / $total GB ($pct %) | RAM Bebas: $free GB"

Write-Host "`n================ 2. BACKGROUND SERVICES CANDIDATES ================" -ForegroundColor Cyan
$services = Get-Service | Where-Object { 
    $_.Status -eq 'Running' -and (
        $_.Name -match 'SysMain|DiagTrack|WSearch|OneDrive|Adsk|Autodesk|NVIDIA|Broker' -or
        $_.DisplayName -match 'Superfetch|Connected User|Search|Autodesk|Broadcast'
    )
}
$services | Select-Object Name, DisplayName, Status, StartType | Format-Table -AutoSize

Write-Host "`n================ 3. RUNNING PROCESSES OVER 100MB ================" -ForegroundColor Cyan
Get-Process | Where-Object { $_.WorkingSet64 -gt 100MB } | Sort-Object WorkingSet64 -Descending | Select-Object Id, ProcessName, @{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize

Write-Host "`n================ 4. PAGEFILE (VIRTUAL MEMORY) ================" -ForegroundColor Cyan
Get-CimInstance Win32_PageFileUsage | Select-Object Name, AllocatedBaseSize, CurrentUsage, PeakUsage | Format-Table -AutoSize
