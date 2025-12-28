from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .api.chat_router import chat_router
from .api.query_router import query_router
from .api.ingest_router import ingest_router
from .api.health_router import health_router
from .api.auth_router import auth_router
from .middleware.rate_limit import rate_limit_middleware
from .core.config import settings

load_dotenv()

app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG Chatbot integration with Docusaurus",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers to the browser
    expose_headers=["Access-Control-Allow-Origin"]
)

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(query_router, prefix="/api/v1", tags=["query"])
app.include_router(ingest_router, prefix="/api/v1", tags=["ingest"])
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot API is running!"}

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        import sys
        print("uvicorn is not installed. Please install it with: pip install uvicorn[standard]")
        sys.exit(1)