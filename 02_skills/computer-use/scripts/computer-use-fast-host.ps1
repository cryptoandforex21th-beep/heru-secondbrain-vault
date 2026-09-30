[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$StateDirectory,
    [Parameter(Mandatory = $true)][string]$PipeName,
    [ValidateRange(1, 120)][int]$IdleTimeoutMinutes = 10
)

$ErrorActionPreference = 'Stop'
[IO.Directory]::CreateDirectory($StateDirectory) | Out-Null
$stopFile = Join-Path $StateDirectory 'stop.flag'
$exitFile = Join-Path $StateDirectory 'exit.flag'
$heartbeatFile = Join-Path $StateDirectory 'heartbeat.txt'
$readyFile = Join-Path $StateDirectory 'fast-host.ready'
$pidFile = Join-Path $StateDirectory 'fast-host.pid'

Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;

namespace AntigravityComputerUseFast
{
    public static class Native
    {
        [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X; public int Y; }
        [StructLayout(LayoutKind.Sequential)] public struct INPUT { public uint type; public INPUTUNION u; }
        [StructLayout(LayoutKind.Explicit)] public struct INPUTUNION { [FieldOffset(0)] public KEYBDINPUT ki; }
        [StructLayout(LayoutKind.Sequential)] public struct KEYBDINPUT { public ushort wVk; public ushort wScan; public uint dwFlags; public uint time; public UIntPtr dwExtraInfo; }

        [DllImport("user32.dll")] static extern IntPtr OpenDesktop(string name, uint flags, bool inherit, uint access);
        [DllImport("user32.dll")] static extern bool SetThreadDesktop(IntPtr desktop);
        [DllImport("user32.dll")] static extern bool CloseDesktop(IntPtr desktop);
        [DllImport("user32.dll")] static extern bool SetCursorPos(int x, int y);
        [DllImport("user32.dll")] static extern bool GetCursorPos(out POINT point);
        [DllImport("user32.dll")] static extern void mouse_event(uint flags, uint dx, uint dy, uint data, UIntPtr extraInfo);
        [DllImport("user32.dll")] static extern void keybd_event(byte key, byte scan, uint flags, UIntPtr extraInfo);
        [DllImport("user32.dll")] static extern uint SendInput(uint count, INPUT[] input, int size);

        static void OnDesktop(Action action)
        {
            Exception failure = null;
            Thread thread = new Thread(() => {
                IntPtr desktop = OpenDesktop("default", 0, false, 0x01FF);
                try {
                    if (desktop != IntPtr.Zero) SetThreadDesktop(desktop);
                    action();
                } catch (Exception ex) { failure = ex; }
                finally { if (desktop != IntPtr.Zero) CloseDesktop(desktop); }
            });
            thread.SetApartmentState(ApartmentState.STA);
            thread.Start();
            thread.Join();
            if (failure != null) throw failure;
        }

        public static bool Move(int x, int y) { bool ok = false; OnDesktop(() => ok = SetCursorPos(x, y)); return ok; }
        public static POINT Cursor() { POINT point = new POINT(); OnDesktop(() => GetCursorPos(out point)); return point; }
        public static void Click(int x, int y, string button, int count)
        {
            OnDesktop(() => {
                if (!SetCursorPos(x, y)) throw new InvalidOperationException("SetCursorPos failed.");
                uint down = button == "right" ? 0x0008u : button == "middle" ? 0x0020u : 0x0002u;
                uint up = button == "right" ? 0x0010u : button == "middle" ? 0x0040u : 0x0004u;
                for (int i = 0; i < count; i++) { mouse_event(down, 0, 0, 0, UIntPtr.Zero); mouse_event(up, 0, 0, 0, UIntPtr.Zero); if (count > 1) Thread.Sleep(80); }
            });
        }
        public static void Scroll(int delta) { OnDesktop(() => mouse_event(0x0800, 0, 0, unchecked((uint)(delta * 120)), UIntPtr.Zero)); }
        public static void Keys(byte[] keys)
        {
            OnDesktop(() => {
                foreach (byte key in keys) keybd_event(key, 0, 0, UIntPtr.Zero);
                for (int i = keys.Length - 1; i >= 0; i--) keybd_event(keys[i], 0, 0x0002, UIntPtr.Zero);
            });
        }
        public static void TypeText(string text, string stopPath)
        {
            OnDesktop(() => {
                foreach (char character in text) {
                    if (File.Exists(stopPath)) throw new InvalidOperationException("user_aborted: ESC was pressed.");
                    INPUT down = new INPUT { type = 1, u = new INPUTUNION { ki = new KEYBDINPUT { wScan = character, dwFlags = 0x0004 } } };
                    INPUT up = down; up.u.ki.dwFlags = 0x0006;
                    if (SendInput(2, new INPUT[] { down, up }, Marshal.SizeOf(typeof(INPUT))) != 2) throw new InvalidOperationException("SendInput failed while typing.");
                }
            });
        }
    }
}
'@

function Send-Response { param($Writer, [hashtable]$Data) $Writer.WriteLine(($Data | ConvertTo-Json -Compress -Depth 5)); $Writer.Flush() }
function Assert-Allowed { if (Test-Path -LiteralPath $stopFile) { throw 'user_aborted: ESC was pressed. Computer control is latched off.' } }
function Resolve-Key { param([string]$Name)
    $value = $Name.Trim().ToUpperInvariant(); $map = @{ CTRL=0x11; CONTROL=0x11; SHIFT=0x10; ALT=0x12; WIN=0x5B; ENTER=0x0D; TAB=0x09; ESC=0x1B; ESCAPE=0x1B; SPACE=0x20; BACKSPACE=0x08; DELETE=0x2E; HOME=0x24; END=0x23; LEFT=0x25; UP=0x26; RIGHT=0x27; DOWN=0x28 }
    if ($map.ContainsKey($value)) { return [byte]$map[$value] }
    if ($value.Length -eq 1 -and $value -match '[A-Z0-9]') { return [byte][char]$value }
    throw "Unsupported fast-host key '$Name'."
}

try {
    [IO.File]::WriteAllText($pidFile, [Diagnostics.Process]::GetCurrentProcess().Id.ToString())
    [IO.File]::WriteAllText($readyFile, [DateTime]::UtcNow.ToString('O'))
    $running = $true
    while ($running) {
        $server = New-Object IO.Pipes.NamedPipeServerStream($PipeName, [IO.Pipes.PipeDirection]::InOut, 1, [IO.Pipes.PipeTransmissionMode]::Byte, [IO.Pipes.PipeOptions]::Asynchronous)
        try {
            $wait = $server.BeginWaitForConnection($null, $null)
            while (-not $wait.AsyncWaitHandle.WaitOne(250)) {
                if (Test-Path -LiteralPath $exitFile) { $running = $false; break }
                if ((Test-Path -LiteralPath $heartbeatFile) -and ([DateTime]::UtcNow - [IO.File]::GetLastWriteTimeUtc($heartbeatFile)).TotalMinutes -gt $IdleTimeoutMinutes) { $running = $false; break }
            }
            if (-not $running) { continue }
            $server.EndWaitForConnection($wait)
            $reader = New-Object IO.StreamReader($server)
            $writer = New-Object IO.StreamWriter($server); $writer.AutoFlush = $true
            $request = $reader.ReadLine() | ConvertFrom-Json
            try {
                if ($request.action -eq 'shutdown') { Send-Response $writer @{ ok=$true; action='shutdown' }; $running = $false; continue }
                Assert-Allowed
                switch ($request.action) {
                    'move' { $ok = [AntigravityComputerUseFast.Native]::Move([int]$request.x, [int]$request.y); Send-Response $writer @{ ok=$ok; action='move'; x=[int]$request.x; y=[int]$request.y } }
                    'click' { [AntigravityComputerUseFast.Native]::Click([int]$request.x,[int]$request.y,[string]$request.button,1); Send-Response $writer @{ ok=$true; action='click' } }
                    'double-click' { [AntigravityComputerUseFast.Native]::Click([int]$request.x,[int]$request.y,[string]$request.button,2); Send-Response $writer @{ ok=$true; action='double-click' } }
                    'scroll' { [AntigravityComputerUseFast.Native]::Scroll([int]$request.delta); Send-Response $writer @{ ok=$true; action='scroll'; delta=[int]$request.delta } }
                    'type' { [AntigravityComputerUseFast.Native]::TypeText([string]$request.text,$stopFile); Send-Response $writer @{ ok=$true; action='type'; characters=([string]$request.text).Length } }
                    'key' { $keys=@($request.keys | ForEach-Object { Resolve-Key $_ }); [AntigravityComputerUseFast.Native]::Keys([byte[]]$keys); Send-Response $writer @{ ok=$true; action='key'; keys=$request.keys } }
                    'hotkey' { $keys=@($request.keys | ForEach-Object { Resolve-Key $_ }); [AntigravityComputerUseFast.Native]::Keys([byte[]]$keys); Send-Response $writer @{ ok=$true; action='hotkey'; keys=$request.keys } }
                    'wait' { $remaining=[int]$request.delayMs; while($remaining -gt 0){ Assert-Allowed; $slice=[Math]::Min(50,$remaining); Start-Sleep -Milliseconds $slice; $remaining-=$slice }; Send-Response $writer @{ ok=$true; action='wait' } }
                    default { throw "Unsupported fast-host action '$($request.action)'." }
                }
            } catch { Send-Response $writer @{ ok=$false; action=$request.action; error=$_.Exception.Message } }
        } finally { $server.Dispose() }
    }
}
finally {
    Remove-Item -LiteralPath $readyFile -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
}
