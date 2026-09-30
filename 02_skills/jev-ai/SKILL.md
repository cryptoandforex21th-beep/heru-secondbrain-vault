---
name: jev-ai
description: >-
  Use this skill to leverage Jev AI (TypeSafe AI System One Model) for sub-second,
  type-safe probabilistic decisions (Choice, Score, Noul), fast task routing,
  and zero-hallucination workflow gating.
---

# Jev AI (TypeSafe System One Decision Model)

Jev is the flagship **System One Model** developed by TypeSafe AI (founded by a ChatGPT co-inventor). Unlike traditional LLMs (System Two) that produce conversational text token-by-token with latency of seconds, Jev gives up text generation to provide **machine-speed, type-safe probabilistic decisions** in **70–500 ms**.

---

## ⚡ Core Capabilities & Primitives

1. **`Choice`**: Categorical classification among pre-defined choices (e.g. routing support requests, intent detection, tool selection) with probability distributions.
2. **`Score`**: Evaluating intensity or quality on an ordered scale (e.g. risk level 1-5, priority scoring).
3. **`Noul`**: Binary truth probability judgment (0.0 to 1.0) with epistemically calibrated confidence.
4. **Zero Hallucinations**: Mathematically impossible to produce invalid schemas or imaginary text since outputs are strictly typed.
5. **High Speed & Low Cost**: 40–200× faster than frontier LLMs; output tokens are free, input tokens are fraction of standard LLM pricing.

---

## 🛠️ Installation & Setup

1. **Python SDKs**:
   Already installed in system:
   ```bash
   pip install jev typesafe-sdk
   ```

2. **API Key Setup**:
   Obtain an API key from [defapi.org](https://defapi.org/model/typesafe/jev-1.13) or [jevai.net](https://jevai.net/).
   Configure it via environment variable or in `d:\SecondBrain\00_system\.env`:
   ```bash
   TYPESAFE_API_KEY="your-api-key-here"
   ```

3. **Status Check**:
   ```powershell
   python d:\SecondBrain\02_skills\jev-ai\jev_client.py status
   ```

---

## 🚀 Usage in Antigravity Workflows

Use Jev AI when you need an immediate check or decision without waiting for full LLM token generation:

```python
from typesafe_sdk import TypeSafeClient, Choice, Score, Noul

with TypeSafeClient() as client:
    result = client.system_one(
        state="Revit model parameter 'Cost' needs updating from AHSP Makassar",
        questions={
            "category": Choice(instructions="What domain is this?", criteria={"BIM": None, "Finance": None, "Code": None}),
            "is_safe": Noul(instructions="Is this operation safe to execute non-interactively?"),
            "priority": Score(instructions="Rate task urgency 1-5", levels=5)
        }
    )
    print(result.choices["category"].choice) # 'BIM'
    print(result.nouls["is_safe"].noul)       # 0.98
    print(result.scores["priority"].score)   # 4
```
