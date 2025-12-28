import os
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
from ..core.logging import app_logger

load_dotenv()

class QdrantService:
    def __init__(self):
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_url or not qdrant_api_key:
            # Use local Qdrant instance for development if cloud credentials not provided
            app_logger.warning("QDRANT_URL or QDRANT_API_KEY not set, using in-memory instance")
            self.client = QdrantClient(":memory:")  # Use in-memory storage for development
            self.is_local = True
        else:
            # Only create remote client if both URL and API key are provided
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                prefer_grpc=True
            )
            self.is_local = False

        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_chunks")
        self.vector_size = 1536  # For OpenAI's text-embedding-3-small
        self.distance = Distance.COSINE
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists.")
        except Exception as e:
            # For in-memory instance, create the collection
            try:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=self.distance
                    )
                )
                print(f"Created collection '{self.collection_name}'.")
            except Exception as create_error:
                # If collection already exists (common with in-memory client), that's fine
                if "already exists" in str(create_error).lower():
                    print(f"Collection '{self.collection_name}' already exists.")
                else:
                    app_logger.error(f"Error creating collection: {str(create_error)}")
                    raise create_error

    def upsert_vectors(self, vectors_data: List[dict]):
        """
        Upsert vectors to the collection
        vectors_data format: [
            {
                "id": str,
                "vector": List[float],
                "payload": {
                    "content": str,
                    "source_url": str,
                    "heading": str,
                    "metadata": dict
                }
            }
        ]
        """
        points = []
        for data in vectors_data:
            points.append(models.PointStruct(
                id=data["id"],
                vector=data["vector"],
                payload=data["payload"]
            ))

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        return len(points)

    def search_vectors(self, query_vector: List[float], limit: int = 10) -> List[dict]:
        """
        Search for similar vectors in the collection
        """
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )

        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            })

        return results

    def delete_collection(self):
        """Delete the entire collection (use with caution!)"""
        self.client.delete_collection(self.collection_name)

# Global instance
qdrant_service = QdrantService()