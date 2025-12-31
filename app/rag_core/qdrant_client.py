import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from typing import List, Dict, Any, Optional
import logging
from contextlib import asynccontextmanager


class QdrantClientWrapper:
    def __init__(self, url: str = None, api_key: str = None, host: str = "localhost", port: int = 6333):
        self.url = url
        self.api_key = api_key
        self.host = host
        self.port = port
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_chunks")
        
        if url and api_key:
            # Use cloud instance
            self.client = QdrantClient(
                url=url,
                api_key=api_key,
            )
        else:
            # Use local instance
            self.client = QdrantClient(
                host=host,
                port=port,
            )
        
        self.logger = logging.getLogger(__name__)

    async def create_collection(self):
        """Create the collection if it doesn't exist"""
        try:
            # Check if collection exists
            collections = await self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                # Create collection with vector configuration
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)  # Assuming OpenAI embeddings
                )
                self.logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                self.logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            self.logger.error(f"Error creating Qdrant collection: {e}")
            raise

    async def close(self):
        """Close the Qdrant client connection"""
        if hasattr(self.client, '_grpc_channel') and self.client._grpc_channel:
            await self.client._grpc_channel.close()
        elif hasattr(self.client, 'close'):
            self.client.close()

    # Add other Qdrant methods as needed by the main.py file
    async def upsert_vectors(self, vectors_with_payload):
        """Upsert vectors with payload to the collection"""
        try:
            # Implementation would go here
            pass
        except Exception as e:
            self.logger.error(f"Error upserting vectors: {e}")
            raise

    async def search_vectors(self, query_vector, limit=5):
        """Search for similar vectors in the collection"""
        try:
            # Implementation would go here
            pass
        except Exception as e:
            self.logger.error(f"Error searching vectors: {e}")
            raise