from fastapi import FastAPI
from backend.src.api.v1.api import api_router
from backend.src.core.config import settings


def create_app():
    app = FastAPI(
        title="AI-Powered Book Assistant API",
        description="API for the RAG-based book assistant system that allows users to ask questions about book content",
        version="1.0.0"
    )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )