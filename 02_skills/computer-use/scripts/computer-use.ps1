[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('session-start', 'session-status', 'session-stop', 'abort', 'resume', 'screen-info', 'screenshot', 'screenshot-window', 'observe', 'windows', 'foreground', 'cursor', 'controls', 'find-control', 'invoke-control', 'set-control-value', 'focus-control', 'select-control', 'focus', 'move', 'click', 'double-click', 'scroll', 'type', 'key', 'hotkey', 'wait', 'batch')]
    [string]$Action,

    [int]$X = 0,
    [int]$Y = 0,
    [ValidateSet('left', 'right', 'middle')]
    [string]$Button = 'left',
    [int]$Delta = 0,
    [string]$Text = '',
    [string[]]$Keys = @(),
    [string]$Title = '',
    [long]$Handle = 0,
    [string]$ControlName = '',
    [string]$AutomationId = '',
    [string]$ControlType = '',
    [string]$Value = '',
    [switch]$Exact,
    [switch]$Refresh,
    [switch]$NoOverlay,
    [switch]$ConfirmResume,
    [ValidateRange(1, 500)][int]$Limit = 120,
    [string]$Path = '',
    [string]$Batch = '',
    [string]$BatchPath = '',
    [ValidateRange(0, 30000)]
    [int]$DelayMs = 150
)

$ErrorActionPreference = 'Stop'

$script:ControlStateDirectory = Join-Path $env:LOCALAPPDATA 'AntigravityComputerUse'
$script:ControllerPath = Join-Path $PSScriptRoot 'computer-use-controller.ps1'
$script:StopFile = Join-Path $script:ControlStateDirectory 'stop.flag'
$script:ExitFile = Join-Path $script:ControlStateDirectory 'exit.flag'
$script:HeartbeatFile = Join-Path $script:ControlStateDirectory 'heartbeat.txt'
$script:CaptureFile = Join-Path $script:ControlStateDirectory 'capture.flag'
$script:ReadyFile = Join-Path $script:ControlStateDirectory 'ready.flag'
$script:PidFile = Join-Path $script:ControlStateDirectory 'controller.pid'
$script:PortFile = Join-Path $script:ControlStateDirectory 'controller.port'

function Get-ControllerProcess {
    if (-not (Test-Path -LiteralPath $script:PidFile)) { return $null }
    $controllerPid = 0
    if (-not [int]::TryParse(([IO.File]::ReadAllText($script:PidFile)).Trim(), [ref]$controllerPid)) { return $null }
    return Get-Process -Id $controllerPid -ErrorAction SilentlyContinue
}

function Get-ControllerPort {
    if (-not (Test-Path -LiteralPath $script:PortFile)) { return 0 }
    $port = 0
    if ([int]::TryParse(([IO.File]::ReadAllText($script:PortFile)).Trim(), [ref]$port)) {
        return $port
    }
    return 0
}

function Send-EngineCommand {
    param([hashtable]$Payload)

    $port = Get-ControllerPort
    if ($port -le 0) { return $null }

    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $iar = $client.BeginConnect('127.0.0.1', $port, $null, $null)
        $success = $iar.AsyncWaitHandle.WaitOne(800)
        if (-not $success) {
            $client.Close()
            return $null
        }
        $client.EndConnect($iar)

        $json = $Payload | ConvertTo-Json -Depth 10 -Compress
        $stream = $client.GetStream()
        $stream.ReadTimeout = 15000
        $stream.WriteTimeout = 5000

        $reader = New-Object System.IO.StreamReader($stream, [Text.Encoding]::UTF8)
        $writer = New-Object System.IO.StreamWriter($stream, [Text.Encoding]::UTF8)
        $writer.AutoFlush = $true

        $writer.WriteLine($json)
        $response = $reader.ReadLine()
        $client.Close()

        return $response
    }
    catch {
        return $null
    }
}

function Start-ControlSession {
    param([switch]$ResetStop, [switch]$Headless)
    [IO.Directory]::CreateDirectory($script:ControlStateDirectory) | Out-Null
    if ($ResetStop) {
        if (Test-Path -LiteralPath $script:StopFile) { [IO.File]::Delete($script:StopFile) }
        if (Test-Path -LiteralPath $script:StopFile) { throw 'Failed to clear the latched stop state.' }
    } elseif (Test-Path -LiteralPath $script:StopFile) {
        throw 'user_aborted: Computer control remains stopped. Only an explicit user-approved resume may clear it.'
    }
    Remove-Item -LiteralPath $script:ExitFile -Force -ErrorAction SilentlyContinue

    $process = Get-ControllerProcess
    $port = Get-ControllerPort
    if (-not $process -or $port -le 0) {
        Remove-Item -LiteralPath $script:ReadyFile -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $script:PidFile -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $script:PortFile -Force -ErrorAction SilentlyContinue

        $arguments = @(
            '-STA', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
            ('"{0}"' -f $script:ControllerPath), '-StateDirectory',
            ('"{0}"' -f $script:ControlStateDirectory)
        )
        if ($Headless) {
            $arguments += '-NoOverlay'
        }

        $process = Start-Process -FilePath 'powershell.exe' -ArgumentList $arguments -WindowStyle Hidden -PassThru
        $deadline = [DateTime]::UtcNow.AddSeconds(8)
        while ((-not (Test-Path -LiteralPath $script:ReadyFile) -or -not (Test-Path -LiteralPath $script:PortFile)) -and [DateTime]::UtcNow -lt $deadline) {
            if ($process.HasExited) {
                $crashFile = Join-Path $script:ControlStateDirectory 'crash.log'
                $crashMsg = if (Test-Path $crashFile) { Get-Content $crashFile -Raw } else { '' }
                throw "Status controller exited with code $($process.ExitCode). $crashMsg"
            }
            Start-Sleep -Milliseconds 100
        }
        if (-not (Test-Path -LiteralPath $script:PortFile)) {
            throw 'Status controller did not become ready.'
        }
    }
    return Get-ControllerProcess
}

# Build payload for TCP engine
$payload = [ordered]@{
    action = $Action
}

if ($X -ne 0) { $payload.x = $X }
if ($Y -ne 0) { $payload.y = $Y }
if ($Button) { $payload.button = $Button }
if ($Delta -ne 0) { $payload.delta = $Delta }
if ($Text) { $payload.text = $Text }
if ($Keys.Count -gt 0) { $payload.keys = $Keys }
if ($Title) { $payload.title = $Title }
if ($Handle -ne 0) { $payload.handle = $Handle }
if ($ControlName) { $payload.controlName = $ControlName }
if ($AutomationId) { $payload.automationId = $AutomationId }
if ($ControlType) { $payload.controlType = $ControlType }
if ($Value) { $payload.value = $Value }
if ($Exact) { $payload.exact = $true }
if ($Refresh) { $payload.refresh = $true }
if ($Limit -ne 120) { $payload.limit = $Limit }
if ($Path) { $payload.path = $Path }
if ($DelayMs -ne 150) { $payload.delayMs = $DelayMs }

if ($Action -eq 'batch') {
    $rawBatch = $Batch
    if ([string]::IsNullOrWhiteSpace($rawBatch) -and -not [string]::IsNullOrWhiteSpace($BatchPath) -and (Test-Path -LiteralPath $BatchPath)) {
        $rawBatch = [IO.File]::ReadAllText($BatchPath)
    }
    if (-not [string]::IsNullOrWhiteSpace($rawBatch)) {
        try {
            $parsedSteps = $rawBatch | ConvertFrom-Json
            $payload.steps = $parsedSteps
        }
        catch {
            Write-Output (@{ ok = $false; action = 'batch'; error = "Invalid JSON in batch: $($_.Exception.Message)" } | ConvertTo-Json -Compress)
            exit 1
        }
    }
}

try {
    # If starting session
    if ($Action -eq 'session-start') {
        if ((Test-Path -LiteralPath $script:StopFile) -and -not $ConfirmResume) {
            throw 'user_aborted: ESC stop is latched. Start again only after the user explicitly asks to resume, then pass ConfirmResume.'
        }
        [void](Start-ControlSession -ResetStop -Headless:$NoOverlay)
        $resp = Send-EngineCommand @{ action = 'session-status' }
        if ($resp) {
            Write-Output $resp
            exit 0
        }
    }

    # If controller is needed for mutating actions, ensure it is running
    $mutatingActions = @('invoke-control', 'set-control-value', 'focus-control', 'select-control', 'focus', 'move', 'click', 'double-click', 'scroll', 'type', 'key', 'hotkey', 'wait', 'batch')
    if ($Action -in $mutatingActions) {
        if (Test-Path -LiteralPath $script:StopFile) {
            throw 'user_aborted: ESC was pressed. Computer control is latched off until explicit resume.'
        }
        if (-not (Get-ControllerProcess) -or (Get-ControllerPort) -le 0) {
            [void](Start-ControlSession -Headless:$NoOverlay)
        }
    }

    # Try sending command to TCP Engine
    $rawResponse = Send-EngineCommand $payload
    if ($rawResponse) {
        Write-Output $rawResponse
        $obj = $null
        try { $obj = $rawResponse | ConvertFrom-Json } catch { }
        if ($obj -and $obj.error -and $obj.error.ToString().StartsWith('user_aborted:')) {
            exit 130
        }
        if ($obj -and ($obj.ok -eq $false)) {
            exit 1
        }
        exit 0
    }

    # Fallback to local execution if engine is unreachable
    # (e.g. session-status or screen-info without daemon)
    if ($Action -eq 'session-status') {
        $proc = Get-ControllerProcess
        $res = [ordered]@{
            ok = $true
            action = $Action
            session = [ordered]@{
                active = [bool]$proc
                stopped = Test-Path -LiteralPath $script:StopFile
                controllerPid = if ($proc) { $proc.Id } else { $null }
                indicator = if ($proc) { 'visible' } else { 'hidden' }
            }
        }
        Write-Output ($res | ConvertTo-Json -Compress)
        exit 0
    }
    elseif ($Action -eq 'abort') {
        [IO.Directory]::CreateDirectory($script:ControlStateDirectory) | Out-Null
        [IO.File]::WriteAllText($script:StopFile, [DateTime]::UtcNow.ToString('O'))
        $res = [ordered]@{ ok = $true; action = $Action; stopped = $true }
        Write-Output ($res | ConvertTo-Json -Compress)
        exit 0
    }
    elseif ($Action -eq 'resume') {
        if (-not $ConfirmResume) { throw 'Resume requires ConfirmResume.' }
        Remove-Item -LiteralPath $script:StopFile -Force -ErrorAction SilentlyContinue
        $res = [ordered]@{ ok = $true; action = $Action; stopped = $false }
        Write-Output ($res | ConvertTo-Json -Compress)
        exit 0
    }
    elseif ($Action -eq 'session-stop') {
        $proc = Get-ControllerProcess
        if ($proc) {
            [IO.File]::WriteAllText($script:ExitFile, [DateTime]::UtcNow.ToString('O'))
            Start-Sleep -Milliseconds 400
        }
        $res = [ordered]@{ ok = $true; action = $Action; session = @{ active = $false } }
        Write-Output ($res | ConvertTo-Json -Compress)
        exit 0
    }
    else {
        # If engine was expected but not running, start it and retry once
        [void](Start-ControlSession -Headless:$NoOverlay)
        $rawResponse = Send-EngineCommand $payload
        if ($rawResponse) {
            Write-Output $rawResponse
            exit 0
        }
        throw "Failed to communicate with control engine on port $(Get-ControllerPort)."
    }
}
catch {
    $errObj = [ordered]@{
        ok = $false
        action = $Action
        error = $_.Exception.Message
    }
    Write-Output ($errObj | ConvertTo-Json -Compress)
    if ($_.Exception.Message.StartsWith('user_aborted:')) { exit 130 }
    exit 1
}
