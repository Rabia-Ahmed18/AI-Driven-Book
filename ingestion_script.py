"""
Data Ingestion Pipeline for RAG-Based AI Book Chatbot

This script processes book content, chunks it, generates embeddings,
and stores them in the vector database with appropriate metadata.
"""
import os
import sys
import logging
from typing import List, Dict, Any
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.embedding_service import EmbeddingService
from backend.vector_store import VectorStore
from backend.database import SessionLocal
from backend.models.document_chunk import DocumentChunk
from backend.models.book_metadata import BookMetadata
import uuid


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IngestionPipeline:
    def __init__(self, book_id: str, source_path: str, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.book_id = book_id
        self.source_path = Path(source_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.db = SessionLocal()
        
        # Initialize text splitter with RecursiveCharacterTextSplitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )
    
    def load_documents(self) -> List[Dict[str, Any]]:
        """Load documents from the source path"""
        documents = []
        
        # Walk through all markdown files in the source directory
        for file_path in self.source_path.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Create document entry
                    documents.append({
                        "content": content,
                        "source_file": str(file_path.relative_to(self.source_path)),
                        "source_section": ""  # Will extract section headers if needed
                    })
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
        
        return documents
    
    def split_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Split documents into chunks"""
        chunks = []
        
        for doc in documents:
            content = doc["content"]
            source_file = doc["source_file"]
            
            # Split the content
            split_texts = self.text_splitter.split_text(content)
            
            for i, chunk_text in enumerate(split_texts):
                chunk = {
                    "content": chunk_text,
                    "source_file": source_file,
                    "source_section": doc.get("source_section", ""),
                    "chunk_index": i
                }
                chunks.append(chunk)
        
        return chunks
    
    def process_and_store(self) -> int:
        """Process documents and store in vector database"""
        try:
            # Load documents
            logger.info(f"Loading documents from {self.source_path}")
            documents = self.load_documents()
            
            if not documents:
                logger.warning("No documents found to process")
                return 0
            
            # Split documents into chunks
            logger.info(f"Splitting {len(documents)} documents into chunks")
            chunks = self.split_documents(documents)
            
            if not chunks:
                logger.warning("No chunks created from documents")
                return 0
            
            # Process each chunk
            processed_count = 0
            vectors_data = []
            
            for i, chunk in enumerate(chunks):
                # Generate embedding for the chunk
                embedding = self.embedding_service.generate_embedding(chunk["content"])
                
                if embedding is None:
                    logger.error(f"Failed to generate embedding for chunk {i}")
                    continue
                
                # Create a unique ID for the vector
                vector_id = str(uuid.uuid4())
                
                # Prepare payload for vector store
                payload = {
                    "book_id": self.book_id,
                    "source_file": chunk["source_file"],
                    "source_section": chunk["source_section"],
                    "chunk_index": chunk["chunk_index"],
                    "content_preview": chunk["content"][:100]  # Store a preview of the content
                }
                
                # Store in vector database
                success = self.vector_store.store_embedding(vector_id, embedding, payload)
                
                if success:
                    # Also store in the SQL database for metadata
                    db_chunk = DocumentChunk(
                        book_id=self.book_id,
                        content=chunk["content"],
                        source_file=chunk["source_file"],
                        source_section=chunk["source_section"],
                        chunk_index=chunk["chunk_index"],
                        embedding_vector_id=vector_id
                    )
                    
                    self.db.add(db_chunk)
                    
                    processed_count += 1
                    logger.info(f"Processed chunk {i+1}/{len(chunks)}")
                else:
                    logger.error(f"Failed to store embedding for chunk {i}")
            
            # Commit to database
            self.db.commit()
            
            logger.info(f"Successfully processed and stored {processed_count} chunks")
            return processed_count
            
        except Exception as e:
            logger.error(f"Error in ingestion pipeline: {e}")
            self.db.rollback()
            raise e
        finally:
            self.db.close()


def main():
    # Example usage
    if len(sys.argv) < 3:
        print("Usage: python ingestion_script.py <book_id> <source_path> [chunk_size] [chunk_overlap]")
        sys.exit(1)
    
    book_id = sys.argv[1]
    source_path = sys.argv[2]
    chunk_size = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    chunk_overlap = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    
    logger.info(f"Starting ingestion for book {book_id} from {source_path}")
    
    pipeline = IngestionPipeline(
        book_id=book_id,
        source_path=source_path,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    processed_count = pipeline.process_and_store()
    
    logger.info(f"Ingestion completed. Processed {processed_count} chunks.")


if __name__ == "__main__":
    main()