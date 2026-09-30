# Command Reference (Computer Use 2.1)

Use the high-speed native micro-client `cu.exe` located at `C:\Users\icomp\.gemini\config\skills\computer-use\bin\cu.exe`:

```powershell
# Shorthand usage:
cu <action> [options]

# Or full binary path:
& "C:\Users\icomp\.gemini\config\skills\computer-use\bin\cu.exe" <action> [options]
```

Legacy PowerShell fallback is also supported:
```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\icomp\.gemini\config\skills\computer-use\scripts\computer-use.ps1" -Action <action> [parameters]
```

## Control Session and Emergency Stop

Start a session before the first UI-changing action. By default, an Apple Dynamic Island-style frosted white HUD appears at the top center with ambient side glows, and global `ESC` becomes the instant emergency stop key.

```powershell
# Standard session with frosted white Dynamic Island HUD and side glow
cu session-start

# Headless session without popping up any visual windows or overlays (ideal for testing)
cu session-start -NoOverlay

# Check session status (~15 ms)
cu session-status

# Stop session cleanly
cu session-stop
```

### Emergency Stop (ESC)
Pressing `ESC` triggers an immediate in-memory stop, dismisses visual HUD overlays, and latches `stop.flag`. Any subsequent mutating action immediately returns `user_aborted` with exit code 130 in <2 ms.
Do not resume automatically. Only after explicit user approval:

```powershell
cu resume -ConfirmResume
```

The daemon automatically terminates after 10 minutes of idle time.

## Sub-Millisecond IPC Engine & Action Batches

The controller daemon runs a persistent local TCP server on `127.0.0.1:<port>`. In-session requests complete in **~2 ms**.

### Batch Actions (Pipeline)
Combine multiple actions into a single in-memory atomic sequence:
```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action batch -Batch '[{"action":"focus","title":"Fusion 360"},{"action":"find-control","controlName":"Extrude"},{"action":"cursor"}]'
```
If any step in the batch fails or if `ESC` is pressed, the batch halts immediately and returns what was executed up to the failure point.

## Observe & Semantic UI Automation

```powershell
# Virtual desktop bounds, monitor count, and DPI awareness
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action screen-info

# Full virtual desktop screenshot
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action screenshot

# Capture specific window
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action screenshot-window -Title "Notepad"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action screenshot-window -Handle 123456

# Visible top-level windows, titles, process names, handles, and bounds
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action windows

# Rapid cursor and foreground-window queries (~2 ms)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action cursor
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action foreground
```

### Observe with SHA-256 Frame Diff & UIA Cache
`observe` captures a screenshot of the window, hashes it with SHA-256, and inspects Windows UI Automation controls. If the window frame has not changed, it skips traversing the UIA tree and returns cached controls instantly:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action observe -Handle 123456
# Pass -Refresh to bypass cache and force full UI tree rescan:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action observe -Handle 123456 -Refresh
```

### Semantic Control Queries
```powershell
# List controls
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action controls -Handle 123456 -Limit 200

# Find specific controls by Name, AutomationId, or ControlType
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action find-control -Handle 123456 -ControlName "Save" -ControlType Button
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action find-control -Handle 123456 -AutomationId "saveButton" -Exact
```

### Semantic Actions
```powershell
# Invoke a button or actionable element via InvokePattern (fallback: bounding center click)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action invoke-control -Handle 123456 -ControlName "Save" -ControlType Button -Exact

# Set text input directly via ValuePattern (fallback: click + select all + typing)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action set-control-value -Handle 123456 -AutomationId "SearchBox" -Value "Extrude"

# Focus or select control
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action focus-control -Handle 123456 -ControlName "Search"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action select-control -Handle 123456 -ControlName "Option 1"
```

## Act (Coordinates & Input)

For 3D graphics viewports (Autodesk Fusion 360, Blender), games, or custom canvas areas where UI Automation does not expose internal geometry:

```powershell
# Focus window
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action focus -Title "Autodesk Fusion"

# Mouse actions
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action move -X 800 -Y 450
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action click -X 800 -Y 450 -Button left
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action double-click -X 800 -Y 450 -Button left
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action scroll -Delta -3

# Keyboard & Shortcuts
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action type -Text "Привет, Windows"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action key -Keys ENTER
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action hotkey -Keys CTRL,L
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ComputerUse -Action wait -DelayMs 500
```
