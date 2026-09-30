param([string]$targetScript)
$action = New-ScheduledTaskAction -Execute "C:\Python314\python.exe" -Argument $targetScript -WorkingDirectory "d:\SecondBrain\00_system"
Set-ScheduledTask -TaskName "AntigravityGUI" -Action $action
Start-ScheduledTask -TaskName "AntigravityGUI"
