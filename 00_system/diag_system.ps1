# System Diagnostic Script for Heru's Laptop
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "`n=================== 1. HARDWARE & CPU ===================" -ForegroundColor Cyan
$cpu = Get-CimInstance Win32_Processor
Write-Host "CPU Model          : $($cpu.Name)"
Write-Host "Cores / Threads    : $($cpu.NumberOfCores) Cores / $($cpu.NumberOfLogicalProcessors) Threads"
Write-Host "Max Clock Speed    : $($cpu.MaxClockSpeed) MHz"
Write-Host "Current Clock Speed: $($cpu.CurrentClockSpeed) MHz"

Write-Host "`n=================== 2. MEMORY (RAM) ===================" -ForegroundColor Cyan
$os = Get-CimInstance Win32_OperatingSystem
$totalRam = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeRam = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$usedRam = [math]::Round($totalRam - $freeRam, 2)
$ramPct = [math]::Round(($usedRam / $totalRam) * 100, 1)
Write-Host "Total RAM          : $totalRam GB"
Write-Host "Used RAM           : $usedRam GB ($ramPct %)"
Write-Host "Free RAM           : $freeRam GB"

Write-Host "`n=================== 3. DISK & STORAGE ===================" -ForegroundColor Cyan
Get-PSDrive -PSProvider FileSystem | ForEach-Object {
    $used = [math]::Round($_.Used / 1GB, 1)
    $free = [math]::Round($_.Free / 1GB, 1)
    $total = $used + $free
    $pct = if ($total -gt 0) { [math]::Round(($used / $total) * 100, 1) } else { 0 }
    Write-Host "Drive $($_.Name):  Used: $used GB / $total GB ($pct %) | Free: $free GB"
}

Write-Host "`n=================== 4. GPU / GRAPHICS ===================" -ForegroundColor Cyan
Get-CimInstance Win32_VideoController | ForEach-Object {
    Write-Host "GPU Name           : $($_.Name)"
    Write-Host "Driver Version     : $($_.DriverVersion)"
    Write-Host "Status             : $($_.Status)"
}

Write-Host "`n=================== 5. POWER PLAN & BATTERY ===================" -ForegroundColor Cyan
powercfg /getactivescheme
$battery = Get-CimInstance Win32_Battery
if ($battery) {
    Write-Host "Battery Status     : $($battery.BatteryStatus) (Estimated: $($battery.EstimatedChargeRemaining)%)"
} else {
    Write-Host "Battery            : Desktop / Plugged in directly"
}

Write-Host "`n=================== 6. TOP 8 MEMORY HOGS (RAM) ===================" -ForegroundColor Cyan
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 8 Id, ProcessName, @{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize

Write-Host "`n=================== 7. TOP 8 CPU HOGS ===================" -ForegroundColor Cyan
Get-Process | Sort-Object CPU -Descending | Select-Object -First 8 Id, ProcessName, @{N='CPU_Sec';E={[math]::Round($_.CPU,1)}}, @{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize
