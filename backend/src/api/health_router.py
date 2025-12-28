from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from ..core.qdrant import qdrant_service
from ..services.embedding_service import embedding_service
from ..core.logging import app_logger
import openai


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    dependencies: Dict[str, str]


health_router = APIRouter()


@health_router.get("/health", response_model=HealthResponse)
async def health():
    dependencies = {
        "qdrant": "unknown",
        "openai": "unknown"
    }

    # Check Qdrant connection
    try:
        # Try to get the collection to verify connection
        qdrant_service.client.get_collection(qdrant_service.collection_name)
        dependencies["qdrant"] = "healthy"
    except Exception as e:
        dependencies["qdrant"] = f"unhealthy: {str(e)}"
        app_logger.error(f"Qdrant health check failed: {str(e)}")

    # Check OpenAI connection
    try:
        # Make a simple request to verify API key and connectivity
        embedding_service.client.embeddings.create(
            input=["health check"],
            model=embedding_service.model
        )
        dependencies["openai"] = "healthy"
    except Exception as e:
        dependencies["openai"] = f"unhealthy: {str(e)}"
        app_logger.error(f"OpenAI health check failed: {str(e)}")

    # Determine overall status
    overall_status = "healthy" if all(status == "healthy" for status in dependencies.values()) else "degraded"

    response = HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        dependencies=dependencies
    )

    return response