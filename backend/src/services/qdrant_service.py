from typing import List, Dict, Any
from ..core.qdrant import qdrant_service
from ..core.logging import app_logger


class QdrantDocumentService:
    """
    Service for document-specific operations in Qdrant
    """
    
    def __init__(self):
        self.qdrant_client = qdrant_service
    
    def upsert_document_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Upsert document chunks to Qdrant
        chunks format: [
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
        try:
            count = qdrant_service.upsert_vectors(chunks)
            app_logger.info(f"Successfully upserted {count} document chunks to Qdrant")
            return count
        except Exception as e:
            app_logger.error(f"Error upserting document chunks to Qdrant: {str(e)}")
            raise
    
    def search_documents(self, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for document chunks in Qdrant
        """
        try:
            results = qdrant_service.search_vectors(query_vector, limit)
            app_logger.info(f"Found {len(results)} results from Qdrant search")
            return results
        except Exception as e:
            app_logger.error(f"Error searching documents in Qdrant: {str(e)}")
            raise
    
    def delete_document_chunks(self, document_id: str) -> bool:
        """
        Delete all chunks associated with a specific document
        """
        # This would require implementation based on how documents are identified
        # For now, this is a placeholder
        app_logger.warning("Delete document chunks functionality not fully implemented")
        return True


# Global instance
qdrant_document_service = QdrantDocumentService()