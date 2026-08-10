from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from contextlib import asynccontextmanager

from router_agent import route
from vector_store import load_collection

# --- In-memory session store ---
# key = conversation_id, value = that conversation's message history
sessions: Dict[str, List[dict]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ChromaDB collection once when the server starts, not per-request
    load_collection()
    yield


app = FastAPI(lifespan=lifespan)


# --- Request/response models ---
class ChatRequest(BaseModel):
    conversation_id: str
    message: str


class ChatResponse(BaseModel):
    conversation_id: str
    response: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conv_id = request.conversation_id

    # Get or create this conversation's history
    if conv_id not in sessions:
        sessions[conv_id] = []

    history = sessions[conv_id]

    # Run the full router pipeline (memory, retrieval, tool use) with this conversation's history
    reply = route(request.message, history=history)

    # Update this conversation's history with the new turn
    history.append({"role": "user", "content": request.message})
    history.append({"role": "assistant", "content": reply})

    return {"conversation_id": conv_id, "response": reply}


# --- Optional: view a conversation's history (useful for debugging) ---
@app.get("/chat/{conversation_id}/history")
def get_history(conversation_id: str):
    return {"conversation_id": conversation_id, "history": sessions.get(conversation_id, [])}