import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="AI Social Manager Backend", version="0.1.0")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

class GenerateRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=500)
    platform: str = Field(min_length=2, max_length=40)
    content_type: str = Field(min_length=2, max_length=60)
    tone: str = Field(min_length=2, max_length=60)

@app.get("/health")
def health():
    return {"status": "ok", "ai_configured": bool(OPENAI_API_KEY)}

@app.post("/generate")
def generate(req: GenerateRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="Backend-এ OPENAI_API_KEY সেট করা হয়নি")
    prompt = (
        "তুমি একজন বাংলা social media content strategist। বাস্তবসম্মত, মৌলিক ও প্ল্যাটফর্ম-উপযোগী কনটেন্ট লেখো। "
        "অযাচাইকৃত তথ্য বা নিশ্চিত viral হওয়ার দাবি করবে না।\n"
        f"Platform: {req.platform}\nContent type: {req.content_type}\nTone: {req.tone}\nTopic: {req.topic}\n"
        "বাংলায় উত্তর দাও। ক্যাপশন হলে প্রাসঙ্গিক হ্যাশট্যাগ দাও; ভিডিও স্ক্রিপ্ট হলে hook, scene/মূল বক্তব্য এবং CTA দাও; আইডিয়া হলে নম্বরযুক্ত ধারণা দাও।"
    )
    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
            json={"model": OPENAI_MODEL, "input": prompt, "store": False},
            timeout=60,
        )
        if response.status_code >= 400:
            try: detail = response.json().get("error", {}).get("message", "AI provider request failed")
            except Exception: detail = "AI provider request failed"
            raise HTTPException(status_code=502, detail=detail)
        data = response.json()
        pieces = []
        for item in data.get("output", []):
            if item.get("type") == "message":
                for part in item.get("content", []):
                    if part.get("type") == "output_text": pieces.append(part.get("text", ""))
        text = "\n".join(pieces).strip()
        if not text: raise HTTPException(status_code=502, detail="AI provider returned no text")
        return {"text": text}
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"AI provider connection error: {exc}")
