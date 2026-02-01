from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag.pipeline import rag_answer

app = FastAPI()

# Request model
class ChatRequest(BaseModel):
    message: str

# Response model
class ChatResponse(BaseModel):
    answer: str

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer = rag_answer(req.message)
    return ChatResponse(answer=answer)