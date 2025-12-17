import asyncio
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import logging

logger = logging.getLogger(__name__)

class QdrantClientWrapper:
    def __init__(self, url: str = None, api_key: str = None, host: str = "localhost", port: int = 6333):
        """
        Initialize Qdrant client wrapper
        """
        self.url = url
        self.api_key = api_key
        self.host = host
        self.port = port
        
        if url:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            self.client = QdrantClient(host=host, port=port)
            
        self.collection_name = "book_content"

    async def create_collection(self, vector_size: int = 1536):
        """
        Create a collection for storing document embeddings if it doesn't exist
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)
            
            if not collection_exists:
                # Create collection with specified vector size
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
                )
                logger.info(f"Created collection '{self.collection_name}' with vector size {vector_size}")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

    async def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the collection
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'id': result.id,
                    'payload': result.payload,
                    'score': result.score
                })
                
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {e}")
            raise

    async def batch_upload(self, points: List[Dict[str, Any]]):
        """
        Upload multiple vectors to the collection
        """
        try:
            # Prepare points for Qdrant
            qdrant_points = []
            for point in points:
                qdrant_points.append(
                    models.PointStruct(
                        id=point['id'],
                        vector=point['vector'],
                        payload=point['payload']
                    )
                )
            
            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=qdrant_points
            )
            
            logger.info(f"Successfully uploaded {len(points)} points to Qdrant")
        except Exception as e:
            logger.error(f"Error uploading to Qdrant: {e}")
            raise

    async def close(self):
        """
        Close the client connection if needed
        """
        # QdrantClient doesn't require explicit closing in most cases
        pass