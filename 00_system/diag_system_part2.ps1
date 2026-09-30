# System Diagnostic Part 2
Write-Host "`n=================== 8. GPU ASSIGNMENT (EDGE / CHROME) ===================" -ForegroundColor Cyan
$props = Get-ItemProperty -Path 'HKCU:\Software\Microsoft\DirectX\UserGpuPreferences' -ErrorAction SilentlyContinue
if ($props) {
    $props.PSObject.Properties | Where-Object { $_.Name -notmatch '^PS' } | ForEach-Object {
        Write-Host "$($_.Name) => $($_.Value)"
    }
} else {
    Write-Host "No custom GPU preferences found (Default: Auto/Integrated)."
}

Write-Host "`n=================== 9. EDGE HARDWARE ACCELERATION ===================" -ForegroundColor Cyan
$edgeReg = Get-ItemProperty -Path 'HKCU:\Software\Policies\Microsoft\Edge' -ErrorAction SilentlyContinue
Write-Host "HardwareAccelerationModeEnabled: $($edgeReg.HardwareAccelerationModeEnabled)"

Write-Host "`n=================== 10. SYSTEM THERMAL / POWER THROTTLING ===================" -ForegroundColor Cyan
$power = Get-CimInstance Win32_Battery
Write-Host "Battery Status Code: $($power.BatteryStatus)"
Write-Host "Estimated Charge   : $($power.EstimatedChargeRemaining)%"

Write-Host "`n=================== 11. EDGE PROCESS TREE (WHAT TABS?) ===================" -ForegroundColor Cyan
Get-Process msedge -ErrorAction SilentlyContinue | Measure-Object -Property WorkingSet64 -Sum | ForEach-Object {
    $totalEdgeMB = [math]::Round($_.Sum / 1MB, 1)
    Write-Host "Total MS Edge RAM (All Tabs/Workers): $totalEdgeMB MB ($($_.Count) processes)"
}
