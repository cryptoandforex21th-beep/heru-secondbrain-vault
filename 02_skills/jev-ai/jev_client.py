"""
Jev AI / TypeSafe System One Client Helper
Provides ultra-fast (70-500ms), type-safe probabilistic decisions (Choice, Score, Noul).
"""

import os
import sys
import json
from typing import Optional, Dict, Any, List

try:
    from dotenv import load_dotenv
    # Load from Second Brain root or system dir if available
    load_dotenv(dotenv_path=r"d:\SecondBrain\00_system\.env")
    load_dotenv()
except ImportError:
    pass

try:
    from typesafe_sdk import TypeSafeClient, Choice, Score, Noul
    import jev
except ImportError as e:
    print(f"[Error] Required libraries not found: {e}")
    print("Run: pip install jev typesafe-sdk")
    sys.exit(1)


def get_client(api_key: Optional[str] = None) -> TypeSafeClient:
    key = api_key or os.environ.get("TYPESAFE_API_KEY") or os.environ.get("JEV_API_KEY")
    if not key:
        raise ValueError(
            "API Key missing. Set TYPESAFE_API_KEY or JEV_API_KEY in environment or d:\\SecondBrain\\00_system\\.env"
        )
    return TypeSafeClient(api_key=key)


def quick_noul(state: str, statement: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Evaluates a binary probability (truthfulness/confidence) on state.
    """
    with get_client(api_key) as client:
        res = client.system_one(
            state=state,
            questions={"result": Noul(instructions=statement)},
        )
        noul_res = res.nouls["result"]
        return {
            "statement": statement,
            "probability": noul_res.noul,
            "raw": noul_res.model_dump() if hasattr(noul_res, "model_dump") else str(noul_res)
        }


def quick_choice(state: str, instruction: str, options: List[str], api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Chooses the best option from a predefined list with confidence score.
    """
    criteria = {opt: None for opt in options}
    with get_client(api_key) as client:
        res = client.system_one(
            state=state,
            questions={"choice": Choice(instructions=instruction, criteria=criteria)},
        )
        choice_res = res.choices["choice"]
        return {
            "selected": choice_res.choice,
            "confidence": getattr(choice_res, "confidence", None),
            "distribution": getattr(choice_res, "distribution", None),
        }


def quick_score(state: str, instruction: str, levels: int = 5, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Scores state on an ordered scale (e.g., 1 to 5 or 1 to 10).
    """
    with get_client(api_key) as client:
        res = client.system_one(
            state=state,
            questions={"score": Score(instructions=instruction, levels=levels)},
        )
        score_res = res.scores["score"]
        return {
            "score": score_res.score,
            "confidence": getattr(score_res, "confidence", None),
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python jev_client.py [status|test|demo]")
        print("  status : Check if SDK & API Key are available")
        print("  test   : Test API connection with active credentials")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "status":
        key = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("JEV_API_KEY")
        print(f"Jev SDK Version      : {jev.__file__}")
        print(f"TypeSafe SDK Version : {TypeSafeClient.__module__}")
        if key:
            masked = key[:6] + "..." + key[-4:] if len(key) > 10 else "***"
            print(f"API Key              : Configured ({masked})")
        else:
            print("API Key              : NOT SET (Need TYPESAFE_API_KEY from defapi.org / jevai.net)")

    elif cmd == "test":
        try:
            print("[Jev AI] Connecting to TypeSafe System One API...")
            res = quick_noul(
                state="The user wants to export a schedule from Revit 2027 to Excel.",
                statement="Does this task involve Autodesk Revit?"
            )
            print("[Jev AI] Test successful!")
            print(json.dumps(res, indent=2))
        except Exception as e:
            print(f"[Jev AI] Connection test failed: {e}")


if __name__ == "__main__":
    main()
