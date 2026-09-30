# Safe RAM Cleaner - Working Set Trimmer
$code = @'
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

public class MemoryCleaner {
    [DllImport("psapi.dll")]
    public static extern int EmptyWorkingSet(IntPtr hwProc);

    public static void CleanAll() {
        Process[] processes = Process.GetProcesses();
        foreach (Process p in processes) {
            try {
                EmptyWorkingSet(p.Handle);
            } catch {
                // Ignore system or protected processes
            }
        }
    }
}
'@

Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue

$before = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory
[MemoryCleaner]::CleanAll()
[System.GC]::Collect()
Start-Sleep -Seconds 1
$after = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory

$freedMB = [math]::Round(($after - $before) / 1024, 1)
$totalFreeGB = [math]::Round($after / 1024 / 1024, 2)
Write-Host "RAM yang berhasil dibebaskan : $freedMB MB" -ForegroundColor Green
Write-Host "Total RAM Bebas Sekarang     : $totalFreeGB GB" -ForegroundColor Cyan
