from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
from ..services.document_parser import document_parser
from ..services.chunking_service import chunking_service
from ..services.embedding_service import embedding_service
from ..services.qdrant_service import qdrant_document_service
from ..core.logging import app_logger
import os

ingest_router = APIRouter()


class IngestRequest(BaseModel):
    source_type: str  # "docs_directory" or "sitemap_xml"
    source_path: Optional[str] = None  # required if source_type is docs_directory
    sitemap_url: Optional[str] = None  # required if source_type is sitemap_xml


class IngestResponse(BaseModel):
    status: str
    chunks_processed: int
    timestamp: str


@ingest_router.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(request: IngestRequest):
    try:
        if request.source_type == "docs_directory":
            if not request.source_path:
                raise HTTPException(status_code=400, detail="source_path is required for docs_directory source_type")

            # Validate that the path exists
            if not os.path.exists(request.source_path):
                raise HTTPException(status_code=400, detail=f"Path does not exist: {request.source_path}")

            # Parse documents from the directory
            documents = document_parser.get_all_documents(request.source_path)
            app_logger.info(f"Parsed {len(documents)} documents from {request.source_path}")

            total_chunks = 0
            all_chunks_for_upsert = []

            # Process each document
            for doc in documents:
                # Chunk the document
                chunks = chunking_service.chunk_document(doc)

                # Generate embeddings for each chunk
                for chunk in chunks:
                    embedding = embedding_service.generate_embedding(chunk.content)
                    chunk.embedding = embedding

                    # Prepare for upsert to Qdrant
                    chunk_data = {
                        "id": chunk.id,
                        "vector": chunk.embedding,
                        "payload": {
                            "content": chunk.content,
                            "source_url": chunk.source_url,
                            "heading": chunk.heading,
                            "metadata": chunk.metadata
                        }
                    }
                    all_chunks_for_upsert.append(chunk_data)

                total_chunks += len(chunks)

            # Upsert all chunks to Qdrant
            if all_chunks_for_upsert:
                count = qdrant_document_service.upsert_document_chunks(all_chunks_for_upsert)
                app_logger.info(f"Successfully upserted {count} chunks to Qdrant")

            response = IngestResponse(
                status="success",
                chunks_processed=total_chunks,
                timestamp="2025-12-28T10:00:00Z"  # In a real implementation, use actual timestamp
            )

            app_logger.info(f"Ingestion completed: {total_chunks} chunks processed")
            return response

        elif request.source_type == "sitemap_xml":
            if not request.sitemap_url:
                raise HTTPException(status_code=400, detail="sitemap_url is required for sitemap_xml source_type")

            # Implementation for sitemap XML ingestion would go here
            # This would involve fetching the sitemap, parsing it, fetching the pages,
            # extracting content, and then chunking and embedding as above
            raise HTTPException(status_code=501, detail="Sitemap XML ingestion not yet implemented")

        else:
            raise HTTPException(status_code=400, detail=f"Invalid source_type: {request.source_type}")

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        app_logger.error(f"Error in ingestion endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during ingestion")