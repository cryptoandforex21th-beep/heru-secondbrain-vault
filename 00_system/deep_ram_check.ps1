# Deep RAM Investigation Script
$os = Get-CimInstance Win32_OperatingSystem
$perf = Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory

Write-Host "================ MEMORY BREAKDOWN ================" -ForegroundColor Cyan
Write-Host "Total Visible RAM       : $([math]::Round($os.TotalVisibleMemorySize / 1MB, 2)) GB"
Write-Host "Free Physical RAM       : $([math]::Round($os.FreePhysicalMemory / 1MB, 2)) GB"
Write-Host "Available Memory        : $([math]::Round($perf.AvailableMBytes / 1024, 2)) GB"
Write-Host "Cache (Standby/Cached)  : $([math]::Round($perf.CacheBytes / 1GB, 2)) GB"
Write-Host "Pool Paged Bytes        : $([math]::Round($perf.PoolPagedBytes / 1MB, 2)) MB"
Write-Host "Pool Non-Paged Bytes    : $([math]::Round($perf.PoolNonpagedBytes / 1MB, 2)) MB"
Write-Host "System Driver Resident  : $([math]::Round($perf.SystemDriverTotalBytes / 1MB, 2)) MB"
Write-Host "Committed Bytes         : $([math]::Round($perf.CommittedBytes / 1GB, 2)) GB / $([math]::Round($perf.CommitLimit / 1GB, 2)) GB"

Write-Host "`n================ CHECK HARDWARE RESERVED ================" -ForegroundColor Cyan
$comp = Get-CimInstance Win32_ComputerSystem
$installed = Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum
$physTotal = [math]::Round($installed.Sum / 1GB, 2)
$visibleTotal = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$reserved = [math]::Round($physTotal - $visibleTotal, 2)
Write-Host "Physical RAM Installed  : $physTotal GB"
Write-Host "Windows Usable RAM      : $visibleTotal GB"
Write-Host "Hardware Reserved       : $reserved GB"

Write-Host "`n================ CHECK KILLER / ACER NETWORK LEAKS ================" -ForegroundColor Cyan
Get-Process | Where-Object { $_.ProcessName -match "killer|acer|care|nitro|nv|killercontrol" } | Select-Object Id, ProcessName, @{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize
