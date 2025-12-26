from fastapi import APIRouter
from .routes import chat, ingest, books


api_router = APIRouter()

# Include all API routes
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(ingest.router, tags=["ingestion"])
api_router.include_router(books.router, tags=["books"])