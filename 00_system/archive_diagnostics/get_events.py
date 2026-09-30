import subprocess

# Get recent Windows Application Event Log entries 
ps_script = r"""
$events = Get-WinEvent -FilterHashtable @{
    LogName='Application'
    StartTime=(Get-Date '2026-09-25 22:00:00')
} -ErrorAction SilentlyContinue

foreach ($ev in $events) {
    $match = ($ev.ProviderName -in @('Application Error', 'Application Hang', '.NET Runtime', 'Windows Error Reporting'))
    if ($match) {
        Write-Host ("=" * 60)
        Write-Host "Time: $($ev.TimeCreated)"
        Write-Host "Provider: $($ev.ProviderName)"
        Write-Host "EventId: $($ev.Id)"
        $lines = ($ev.Message -split "`n")[0..20]
        foreach ($l in $lines) { Write-Host $l }
    }
}
"""

res = subprocess.run(
    ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
    capture_output=True, text=True, timeout=30
)
print("STDOUT:")
print(res.stdout[:6000])
print("STDERR:")
print(res.stderr[:500])
