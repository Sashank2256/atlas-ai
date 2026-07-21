from fastapi import FastAPI
from pydantic import BaseModel

from app.ai import chat_with_ai

app = FastAPI(title="Atlas AI", version="1.0.0")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "running", "message": "Welcome to Atlas AI 🚀"}


@app.post("/chat")
def chat(request: ChatRequest):
    answer = chat_with_ai(request.message)

    return {"response": answer}
