from fastapi import FastAPI
from pydantic import BaseModel
from src.model import ask_crypto_bot

app = FastAPI(title="Crypto Chat Agent")

class ChatRequest(BaseModel):
    question: str

@app.post("/crypto-chat")
async def crypto_chat(request: ChatRequest):
    response = ask_crypto_bot(request.question)
    return response
