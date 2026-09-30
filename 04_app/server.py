import os
import glob
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load env variables if available
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SYSTEM_DIR = BASE_DIR / "00_system"
KNOWLEDGE_DIR = BASE_DIR / "01_knowledge"
PROFILE_PATH = SYSTEM_DIR / "PROFILE.md"

app = FastAPI(title="SecondBrain Antigravity Portal", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_system_profile() -> str:
    """Membaca PROFILE.md dan aturan sistem."""
    if PROFILE_PATH.exists():
        return PROFILE_PATH.read_text(encoding="utf-8")
    return "Bertindaklah sebagai asisten pribadi SecondBrain yang to the point dan terstruktur."

def get_knowledge_summary() -> str:
    """Merangkum daftar catatan yang ada di SecondBrain."""
    files = list(KNOWLEDGE_DIR.glob("**/*.md"))
    if not files:
        return "Belum ada catatan."
    summary = "Daftar catatan dalam SecondBrain saat ini:\n"
    for f in files[:20]:  # limit agar ringkas
        rel = f.relative_to(KNOWLEDGE_DIR)
        summary += f"- {rel}\n"
    return summary

class ChatRequest(BaseModel):
    message: str
    admin_model: str = "gemini"  # "gemini", "claude", "gpt"
    include_knowledge: bool = True

class SaveNoteRequest(BaseModel):
    title: str
    content: str
    folder: str = "inbox"  # inbox, projects, areas, resources

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = BASE_DIR / "04_app" / "static" / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>SecondBrain Server Running</h1>")

@app.get("/api/profile")
async def get_profile():
    return {"profile": load_system_profile()}

@app.get("/api/notes")
async def list_notes():
    result = []
    for p in KNOWLEDGE_DIR.glob("**/*.md"):
        rel = str(p.relative_to(KNOWLEDGE_DIR)).replace("\\", "/")
        result.append({
            "path": rel,
            "filename": p.name,
            "size": p.stat().st_size,
            "folder": p.parent.name
        })
    return {"notes": result}

@app.get("/api/note")
async def read_note(path: str):
    target = KNOWLEDGE_DIR / path
    if not target.resolve().is_relative_to(KNOWLEDGE_DIR.resolve()) or not target.exists():
        raise HTTPException(status_code=404, detail="File tidak ditemukan")
    return {"path": path, "content": target.read_text(encoding="utf-8")}

@app.post("/api/save_note")
async def save_note(req: SaveNoteRequest):
    folder_path = KNOWLEDGE_DIR / req.folder
    folder_path.mkdir(parents=True, exist_ok=True)
    clean_title = "".join(c for c in req.title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    if not clean_title:
        clean_title = "note"
    file_path = folder_path / f"{clean_title}.md"
    
    file_path.write_text(req.content, encoding="utf-8")
    return {"status": "success", "file": str(file_path.relative_to(BASE_DIR)).replace("\\", "/")}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    user_msg = req.message
    admin = req.admin_model.lower()
    
    system_prompt = load_system_profile()
    if req.include_knowledge:
        system_prompt += "\n\n" + get_knowledge_summary()

    # 1. Jalur Default: GEMINI (via google-genai / Antigravity)
    if admin == "gemini":
        gemini_key = os.getenv("GEMINI_API_KEY")
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=gemini_key) if gemini_key else genai.Client()
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_msg,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                )
            )
            return {"admin": "Gemini 2.5 Flash (Google AI)", "reply": response.text}
        except Exception as e:
            # Fallback jika API key belum diset
            return {
                "admin": "Gemini (Mode Info)",
                "reply": f"⚠️ Terjadi kendala memanggil Gemini API: {str(e)}\n\n💡 Catatan: Pastikan Anda telah memasukkan `GEMINI_API_KEY` di file `.env` di folder SecondBrain Anda. Dapatkan gratis di: https://aistudio.google.com/app/api-keys"
            }

    # 2. Jalur Alternatif: CLAUDE
    elif admin == "claude":
        claude_key = os.getenv("ANTHROPIC_API_KEY")
        if not claude_key:
            return {
                "admin": "Claude (Status)",
                "reply": "💡 Kunci API Claude (`ANTHROPIC_API_KEY`) belum diatur di file `.env`.\n\nJika ingin memakai Claude lewat web claude.ai secara gratis tanpa API key, cukup buka menu Claude Projects dan lampirkan `00_system/PROFILE.md`!"
            }
        try:
            import httpx
            headers = {
                "x-api-key": claude_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 2048,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_msg}]
            }
            async with httpx.AsyncClient() as http_client:
                r = await http_client.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers, timeout=60.0)
                data = r.json()
                reply_text = data["content"][0]["text"]
                return {"admin": "Claude 3.5 Sonnet", "reply": reply_text}
        except Exception as e:
            return {"admin": "Claude (Error)", "reply": f"Gagal menghubungi Claude: {str(e)}"}

    # 3. Jalur Alternatif: GPT
    elif admin == "gpt":
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return {
                "admin": "GPT (Status)",
                "reply": "💡 Kunci API OpenAI (`OPENAI_API_KEY`) belum diatur di file `.env`.\n\nJika ingin memakai ChatGPT secara gratis tanpa API key, Anda cukup memasukkan isi `00_system/PROFILE.md` ke Custom Instructions di web chatgpt.com!"
            }
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ]
            )
            return {"admin": "GPT-4o", "reply": completion.choices[0].message.content}
        except Exception as e:
            return {"admin": "GPT (Error)", "reply": f"Gagal menghubungi GPT: {str(e)}"}

    return {"admin": "Unknown", "reply": "Model admin tidak dikenali."}
