from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..models.chunk import DocumentChunk
from ..core.logging import app_logger


class ChunkingService:
    """
    Service for chunking documents using RecursiveCharacterTextSplitter
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
    
    def chunk_text(self, text: str, source_url: str, heading: str = "") -> List[DocumentChunk]:
        """
        Chunk the provided text using RecursiveCharacterTextSplitter
        """
        try:
            chunks = self.text_splitter.split_text(text)
            document_chunks = []
            
            for i, chunk_text in enumerate(chunks):
                chunk = DocumentChunk(
                    content=chunk_text,
                    source_url=source_url,
                    heading=heading,
                    metadata={
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "chunk_size": len(chunk_text)
                    }
                )
                document_chunks.append(chunk)
            
            app_logger.info(f"Successfully chunked text into {len(document_chunks)} chunks")
            return document_chunks
        except Exception as e:
            app_logger.error(f"Error chunking text: {str(e)}")
            raise
    
    def chunk_document(self, document: dict) -> List[DocumentChunk]:
        """
        Chunk a parsed document
        """
        content = document.get("content", "")
        source_url = document.get("file_path", "")  # Using file path as source URL for now
        heading = document.get("title", "")
        
        return self.chunk_text(content, source_url, heading)


# Global instance
chunking_service = ChunkingService()