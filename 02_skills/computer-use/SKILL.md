---
name: computer-use
description: >-
  Use this skill when the user asks Antigravity to control Windows desktop apps,
  click or type in a graphical interface, inspect the screen, operate a program,
  or complete a multi-step GUI workflow outside the built-in browser agent.
---

# Windows Computer Use 2.1 (Hyper-Speed Engine)

Control Windows desktop applications, click, drag, type, inspect UI elements, and automate multi-step GUI tasks with maximum speed via the standalone compiled micro-client [`bin/cu.exe`](./bin/cu.exe) and its persistent in-memory controller daemon.

---

## ⚡ CRITICAL ZERO-OVERHEAD RULES (MANDATORY)

To prevent latency, token waste, and tool churn, **strictly adhere to the following rules**:

1. **NEVER create scratch `.ps1` files, `.cs` files, or temporary scripts on disk.**
   - Do NOT use `write_to_file` to write ad-hoc automation or inspection scripts.
   - Do NOT write custom C# P/Invoke code or run `Add-Type`.
   - Everything (desktop switching, mouse events, absolute coordinates, DPI scaling, UIA caching, screen diffing) is already built into `bin/cu.exe`.

2. **NEVER spend turns overthinking low-level Win32 details.**
   - Window handles, focus management, STA message loops, and keyboard translation are handled automatically by the daemon.
   - Dispatch commands immediately via `run_command` in a single tool call.

3. **ALWAYS invoke `bin/cu.exe` directly via `run_command`.**
   ```powershell
   & "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" <action> [options]
   ```

4. **PREFER AGILE 1–2 ACTION MICRO-STEPS directly via CLI.**
   - Do NOT write giant multi-step JSON batch scripts to disk upfront; it creates high perceived latency and delays user feedback.
   - Execute 1–2 fast, atomic actions at a time directly on the CLI (`cu focus`, `cu type`, `cu key`, `cu click`), which execute in ~15 ms and provide immediate visual feedback on screen.
   - Reserve `cu batch` strictly for continuous high-speed drawing strokes or tightly coupled atomic gestures.

5. **KEEP HUD PERMANENTLY VISIBLE during execution.**
   - The Frosted White Dynamic Island HUD and Pure White Ambient Glows must remain active and visible continuously while performing actions.
   - Do not terminate or restart the session between short micro-steps; keep it resident so the user has visual confirmation and the instant ESC latch throughout the workflow.

6. **ALWAYS clean up (`cu session-stop`) when the task is done.**
   - As soon as your UI workflow finishes and you hand control back to the user, call `cu session-stop`.
   - This smoothly dismisses the HUD capsule and side glows so they don't linger on the screen after the task is over.

---

## 🚀 Instant Command Cheatsheet

### 1. Session Lifecycle
```powershell
# Start session (Headless - background, no windows or popups):
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" session-start -NoOverlay

# Start session (HUD - Apple Dynamic Island frosted white bar + ambient glows):
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" session-start

# Check session status (~15 ms):
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" session-status

# Stop session:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" session-stop
```

### 2. Window Discovery & Focus
```powershell
# List all open windows with handles, titles, bounds, and process names:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" windows

# Focus window by title or handle:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" focus -Title "Paint"
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" focus -Handle 461072
```

### 3. Mouse & Keyboard Actions
```powershell
# Click coordinate:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" click -X 500 -Y 300

# Drag / Draw stroke:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" drag -FromX 400 -FromY 300 -ToX 800 -ToY 500 -Steps 15

# Type text:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" type -Text "Hello world!"

# Press key or shortcut:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" hotkey -Keys "Ctrl,S"
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" key -Keys "Enter"
```

### 4. Screen Observation & Semantic UI Automation
```powershell
# Inspect window (RAM SHA-256 diff + pre-cached UIA tree):
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" observe -Handle 461072

# Find specific UI button or control:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" find-control -Handle 461072 -ControlName "Save" -ControlType Button

# Click UI control directly by semantic name:
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" invoke-control -Handle 461072 -ControlName "Save"
```

### 5. Multi-Step Batching (`cu batch`)
Execute complete pipelines in a single call without back-and-forth roundtrips:
```powershell
& "C:\Users\Heru Ardiansyah\.gemini\config\skills\computer-use\bin\cu.exe" batch -Batch '[{"action":"focus","title":"Paint"},{"action":"click","x":242,"y":78},{"action":"drag","fromX":500,"fromY":500,"toX":800,"toY":500},{"action":"hotkey","keys":["Ctrl","s"]}]'
```

---

## 🛡️ Emergency Stop (ESC)

- Global `ESC` is continuously monitored by the controller engine.
- Pressing `ESC` instantly aborts any running batch or movement, clears queues, and latches `stop.flag` (exit code 130).
- If code 130 is returned, **immediately halt and consult the user** before resuming with `cu resume -ConfirmResume`.
