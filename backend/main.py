# RAG-Based AI Book Chatbot - Backend

from fastapi import FastAPI
from .config import settings
from .routers import chat

app = FastAPI(
    title="RAG-Based AI Book Chatbot API",
    description="API for interacting with the RAG-based AI book chatbot",
    version="1.0.0"
)

# Include routers
app.include_router(chat.app, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG-Based AI Book Chatbot API"}