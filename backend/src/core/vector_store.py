from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional
from .config import settings


class VectorStore:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False  # Using HTTP for simplicity
        )
        self.collection_name = settings.qdrant_collection_name
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Create the collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except Exception as e:
            # Create collection if it doesn't exist
            # Using 1536 dimensions for OpenAI's text-embedding-3-small model
            try:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
                )
            except Exception as create_error:
                # If collection already exists, that's fine
                if "already exists" not in str(create_error):
                    raise create_error
    
    def add_vectors(self, book_id: str, vectors: List[dict]):
        """Add vectors to the collection"""
        points = []
        for i, vector_data in enumerate(vectors):
            points.append(models.PointStruct(
                id=i,  # In a real implementation, you'd want proper UUIDs
                vector=vector_data['vector'],
                payload={
                    'book_id': book_id,
                    'content': vector_data['content'],
                    'metadata': vector_data.get('metadata', {})
                }
            ))
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search(self, query_vector: List[float], book_id: Optional[str] = None, limit: int = 10):
        """Search for similar vectors"""
        # Prepare filters if book_id is provided
        if book_id:
            filter_conditions = models.Filter(
                must=[
                    models.FieldCondition(
                        key="book_id",
                        match=models.MatchValue(value=book_id)
                    )
                ]
            )
        else:
            filter_conditions = None
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=filter_conditions,
            limit=limit
        )
        
        return results
    
    def delete_by_book_id(self, book_id: str):
        """Delete all vectors associated with a book"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="book_id",
                            match=models.MatchValue(value=book_id)
                        )
                    ]
                )
            )
        )


# Global instance
vector_store = VectorStore()