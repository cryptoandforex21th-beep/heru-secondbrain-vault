"""
Fast Dispatcher & System 1 Decision Engine via Gemini Flash (100% Free Tier)
Sub-second classification, routing, and verification with resilient model failover.
"""

import os
import sys
import json
import time
from typing import Dict, Any, List, Optional

CANDIDATE_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-3.6-flash"
]

def load_key():
    env_file = r"d:\SecondBrain\00_system\.env"
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["GEMINI_API_KEY"] = val
                    return val
    return os.environ.get("GEMINI_API_KEY")

def get_client():
    key = load_key()
    if not key:
        return None
    from google import genai
    return genai.Client(api_key=key)

def generate_with_failover(prompt: str, json_mode: bool = True) -> str:
    client = get_client()
    if not client:
        raise ValueError("GEMINI_API_KEY is not set.")

    cfg = {"temperature": 0.0}
    if json_mode:
        cfg["response_mime_type"] = "application/json"

    last_error = None
    for model_name in CANDIDATE_MODELS:
        for attempt in range(2):
            try:
                res = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=cfg
                )
                return res.text
            except Exception as e:
                last_error = e
                time.sleep(0.4)
    raise RuntimeError(f"All fallback models failed. Last error: {last_error}")

def quick_choice(state: str, question: str, options: List[str]) -> Dict[str, Any]:
    """
    Sub-second categorical selection (System 1) using Gemini Flash.
    """
    prompt = f"""You are a high-speed System 1 decision engine.
State: {state}
Question: {question}
Allowed Options: {json.dumps(options)}

Return strictly a JSON object with:
"selected": (one of the allowed options),
"confidence": (float between 0.0 and 1.0)
"""
    raw = generate_with_failover(prompt, json_mode=True)
    return json.loads(raw)

def quick_noul(state: str, statement: str) -> Dict[str, Any]:
    """
    Probabilistic truth / safety verification (0.0 to 1.0).
    """
    prompt = f"""State: {state}
Statement: {statement}

Evaluate the mathematical truth/probability that this statement holds.
Return strictly a JSON object:
"probability": (float between 0.0 and 1.0),
"reason": (very short 1 sentence reason)
"""
    raw = generate_with_failover(prompt, json_mode=True)
    return json.loads(raw)

def quick_score(state: str, criterion: str, max_score: int = 5) -> Dict[str, Any]:
    """
    1-5 or 1-10 priority/urgency scoring.
    """
    prompt = f"""State: {state}
Criterion: {criterion} (Scale 1 to {max_score})

Return strictly a JSON object:
"score": (integer 1 to {max_score}),
"confidence": (float 0.0 to 1.0)
"""
    raw = generate_with_failover(prompt, json_mode=True)
    return json.loads(raw)

if __name__ == "__main__":
    key = load_key()
    if not key:
        print("STATUS: GEMINI_API_KEY is NOT configured.")
        sys.exit(1)
        
    print(f"STATUS: GEMINI_API_KEY configured ({key[:8]}...{key[-4:]})")
    print("Testing resilient System 1 Dispatcher...")
    try:
        t0 = time.time()
        c = quick_choice(
            state="Heru minta kirim pesan WhatsApp ke glo mbg",
            question="Alur otomasi yang sesuai?",
            options=["WHATSAPP_AUTOMATION", "REVIT_BIM", "BROWSER_TAB", "NOTES"]
        )
        t1 = time.time()
        print(f"Choice ({t1-t0:.2f}s):", json.dumps(c, indent=2))
        
        n = quick_noul(
            state="Perintah: python d:\\SecondBrain\\00_system\\app_launcher.py rhino",
            statement="Apakah perintah ini aman dieksekusi?"
        )
        t2 = time.time()
        print(f"Noul   ({t2-t1:.2f}s):", json.dumps(n, indent=2))
        
        s = quick_score(
            state="Revit mengalami crash VendorCode 22 saat pyRevit dibuka",
            criterion="Tingkat keparahan isu teknis"
        )
        t3 = time.time()
        print(f"Score  ({t3-t2:.2f}s):", json.dumps(s, indent=2))
        print("All tests PASSED successfully!")
    except Exception as e:
        print("Error:", e)
