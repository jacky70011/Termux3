from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()
generator = pipeline("text2text-generation", model="google/flan-t5-small")  # ← Bas yeh line chhoti model ke liye

approved_api_keys = {
    "jacky_786_secret": "Jacky (Admin)",
    "user1_786_key": "User 1",
    "user2_trial_key": "Trial User"
}

class AskRequest(BaseModel):
    prompt: str
    api_key: str

@app.post("/ask")
async def ask(request: AskRequest):
    if request.api_key not in approved_api_keys:
        raise HTTPException(status_code=401, detail="Unauthorized: API Key not approved")

    username = approved_api_keys[request.api_key]
    response = generator(request.prompt, max_length=100)[0]["generated_text"]
    return {
        "user": username,
        "response": response
    }
