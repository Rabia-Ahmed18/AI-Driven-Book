from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from uuid import UUID
import logging
from .config import settings


class VectorStore:
    def __init__(self):
        # Initialize Qdrant client
        if settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                prefer_grpc=True
            )
        else:
            # For local or cloud without auth
            self.client = QdrantClient(url=settings.QDRANT_URL)
        
        self.collection_name = "document_chunks"
        self._create_collection_if_not_exists()
    
    def _create_collection_if_not_exists(self):
        """Create the collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logging.info(f"Collection '{self.collection_name}' already exists")
        except:
            # Create collection with appropriate vector size for OpenAI embeddings
            # text-embedding-3-small produces 1536-dimensional vectors
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
            logging.info(f"Created collection '{self.collection_name}'")
    
    def store_embedding(self, vector_id: str, vector: List[float], payload: Dict[str, Any]) -> bool:
        """Store a single embedding in the vector store"""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=vector_id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )
            return True
        except Exception as e:
            logging.error(f"Error storing embedding: {e}")
            return False
    
    def batch_store_embeddings(self, vectors_data: List[Dict[str, Any]]) -> bool:
        """Store multiple embeddings in the vector store"""
        try:
            points = [
                models.PointStruct(
                    id=data["id"],
                    vector=data["vector"],
                    payload=data["payload"]
                )
                for data in vectors_data
            ]
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            logging.error(f"Error storing batch embeddings: {e}")
            return False
    
    def search_similar(self, query_vector: List[float], book_id: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors in the store"""
        try:
            # Prepare filters if book_id is specified
            filters = None
            if book_id:
                filters = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="book_id",
                            match=models.MatchValue(value=book_id)
                        )
                    ]
                )
            
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=filters,
                limit=limit
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                })
            
            return formatted_results
        except Exception as e:
            logging.error(f"Error searching for similar vectors: {e}")
            return []
    
    def delete_by_book_id(self, book_id: str) -> bool:
        """Delete all vectors associated with a specific book"""
        try:
            # Find all points with the specified book_id
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="book_id",
                            match=models.MatchValue(value=book_id)
                        )
                    ]
                ),
                limit=10000  # Adjust based on expected max chunks per book
            )
            
            # Extract IDs to delete
            ids_to_delete = [point.id for point, _ in search_result]
            
            if ids_to_delete:
                # Delete the points
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(points=ids_to_delete)
                )
            
            return True
        except Exception as e:
            logging.error(f"Error deleting vectors by book_id: {e}")
            return False