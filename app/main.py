from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from app.models import ChatRequest, ChatResponse, IngestRequest, IngestResponse
from app.config import settings
from app.rag_core.qdrant_client import QdrantClientWrapper
from app.rag_core.postgres_client import PostgresClient
from app.rag_core.rag_pipeline import RAGPipeline
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

# Global variables to hold our clients and pipeline
qdrant_client = None
postgres_client = None
rag_pipeline = None
openai_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events to initialize and cleanup resources
    """
    global qdrant_client, postgres_client, rag_pipeline, openai_client

    try:
        # Initialize OpenAI client
        openai_client = AsyncOpenAI(api_key=os.getenv("GEMINI_API_KEY"))

        # Initialize Qdrant client
        qdrant_client = QdrantClientWrapper(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            host=settings.qdrant_host,
            port=settings.qdrant_port
        )

        # Initialize Postgres client
        postgres_client = PostgresClient(settings.neon_database_url)

        # Connect to databases
        await postgres_client.connect()

        # Create Qdrant collection if needed
        await qdrant_client.create_collection()

        # Initialize RAG pipeline
        rag_pipeline = RAGPipeline(
            openai_client=openai_client,
            qdrant_client=qdrant_client,
            postgres_client=postgres_client,
            config=settings
        )

        logger.info("Application startup complete")

        # Run the application
        yield

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        # Cleanup resources on shutdown
        if qdrant_client:
            await qdrant_client.close()
        if postgres_client:
            await postgres_client.close()
        logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot Backend API",
    description="API for the RAG Chatbot that enables users to ask questions about book content with source citations",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow requests from Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """
    Primary RAG Query endpoint
    """
    try:
        # Process the query through the RAG pipeline
        result = await rag_pipeline.process_query(
            question=chat_request.question,
            selected_context=chat_request.selected_context
        )

        return ChatResponse(
            answer=result["answer"],
            source_citations=result["source_citations"]
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(ingest_request: IngestRequest):
    """
    Ingestion trigger for book content
    """
    try:
        from .ingestion.ingestion_script import process_content
        # Process the content
        result = await process_content(ingest_request.source_path, ingest_request.force_reprocess)

        return IngestResponse(
            status=result["status"],
            processed_files=[file['file'] for file in result.get('processed_files', [])],
            errors=[error.get('message', 'Unknown error') for error in result.get('errors', [])]
        )
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)