# ⚡ Antigravity Computer Use 2.1 (Hyper-Speed Engine)

> Zero-latency, atomic Windows desktop automation skill designed for **Google Antigravity** and autonomous AI coding agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows 10/11](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6.svg)](https://microsoft.com/windows)
[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill%202.1-10B981.svg)](https://antigravity.google)

---

## 🌟 Overview

Most computer use implementations suffer from severe latency: an agent takes a screenshot, waits for vision model inference, sends a single click, waits for another turn, and repeats. Doing complex UI tasks takes dozens of turns and minutes of waiting.

**Antigravity Computer Use 2.1** eliminates this overhead through an in-memory resident controller and compiled micro-client (`cu.exe`):
1. **Atomic Batching (`cu batch`)**: Dispatches complete action pipelines (focus, clicks, typing, hotkeys, drags) in a single call. Entire multi-step flows execute in **<100 ms**.
2. **Apple Dynamic Island Frosted Glass HUD**: Top-centered floating capsule (`#F8FAFC`, dark `#0F172A` text, emerald glowing status indicator, instant `ESC` abort badge).
3. **Pure White Ambient Side Glow**: Frosted white edge illumination (`RGB 255, 255, 255` premultiplied ARGB) that informs the user the agent is active without obscuring content.
4. **Persistent `HWND_TOPMOST` Lock**: 200 ms re-pinning cycle ensuring the HUD and edge glows never flicker or get occluded by newly focused or maximized windows.
5. **Alt+Tab Safety Shield (Target Window Lock)**: Continuously tracks foreground window handles. If the user Alt-Tabs to Discord, Telegram, or a browser during execution, all mouse buttons release and execution latches off instantly.
6. **Semantic UIAutomation First**: Direct control of controls (`InvokePattern`, `ValuePattern`, `SelectionItemPattern`) with coordinate fallback.
7. **RAM SHA-256 Screen Diffing**: Avoids redundant frame processing when screen content has not changed.

---

## 📂 Project Structure

```text
computer-use/
├── SKILL.md                          # Antigravity skill declaration & system prompt
├── README.md                         # Documentation & benchmarks
├── bin/
│   └── cu.exe                        # Standalone compiled high-speed C# micro-client
├── scripts/
│   ├── cu.cs                         # Source code for cu.exe
│   ├── computer-use-controller.ps1   # Resident STA controller daemon (TCP IPC, Win32)
│   └── computer-use.ps1              # CLI wrapper fallback
└── references/
    └── command-reference.md          # Full action and flag reference
```

---

## 🚀 Quickstart

### 1. Installation into Antigravity
Clone or copy this directory into your global Antigravity configuration directory:
```powershell
# Copy to global skills directory:
Copy-Item -Recurse -Path .\computer-use -Destination "$env:USERPROFILE\.gemini\config\skills\computer-use"
```

Once installed, Antigravity automatically detects the skill and provides it to the agent.

### 2. Basic Commands
```powershell
# Start session with Frosted White HUD & White Side Glow:
cu session-start

# Check status (~15 ms):
cu session-status

# List open windows:
cu windows

# Focus a window:
cu focus -Title "Calculator"

# Click / Type / Hotkey:
cu click -X 500 -Y 300
cu type -Text "Hello world!"
cu hotkey -Keys "Ctrl,S"

# Stop session:
cu session-stop
```

### 3. Atomic Batching Example (`cu batch`)
Execute multi-step sequences in <100 ms:
```json
[
  {"action": "focus", "title": "Calculator"},
  {"action": "invoke-control", "automationId": "hexButton"},
  {"action": "invoke-control", "automationId": "bButton"},
  {"action": "invoke-control", "automationId": "eButton"},
  {"action": "invoke-control", "automationId": "eButton"},
  {"action": "invoke-control", "automationId": "fButton"}
]
```
```powershell
cu batch -BatchPath .\hex_batch.json
```

---

## 🎨 Visual HUD & Edge Lighting

- **Capsule Dimensions**: 430 × 40 px, 16 px border radius.
- **Glass Tint**: Frosted White gradient (`#FFFFFF` to `#F4F6F9`), subtle border (`#DAE0E9`).
- **Indicator**: Active emerald green pulse (`#10B981`) with soft diffused glow.
- **Side Glow**: 100 px wide alpha-blended pure white gradients pinned to primary display borders.
- **Safety Interruption**: Pressing `ESC` triggers emergency stop via Win32 `RegisterHotKey(0x41C7, VK_ESCAPE)`.

## 📄 License
MIT License. Created by Ilya (@akumulator18650) & Antigravity.

