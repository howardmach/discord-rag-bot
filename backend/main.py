from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag.pipeline import rag_answer

app = FastAPI()

# -----------------------------
#  Request / Response Models
# -----------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

# -----------------------------
#  Chat Endpoint
# -----------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Pass the message into your RAG pipeline
    answer = rag_answer(req.message)
    return ChatResponse(answer=answer)

# -----------------------------
#  Feedback Endpoint
# -----------------------------
@app.post("/feedback")
def feedback(data: dict):
    # You can later store this in a DB or log file
    print("Received feedback:", data)
    return {"status": "ok"}