import asyncio
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag_backend.rag_core.qdrant_client import QdrantClientWrapper
from rag_backend.rag_core.postgres_client import PostgresClient
from rag_backend.config import settings
from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)

class IngestionPipeline:
    def __init__(self, qdrant_client: QdrantClientWrapper, postgres_client: PostgresClient, config):
        self.qdrant_client = qdrant_client
        self.postgres_client = postgres_client
        self.config = config
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
        )

    async def load_and_chunk_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load a single file and split it into chunks
        """
        try:
            # Read file content based on extension
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Split content into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Create chunk entries with metadata
            chunk_entries = []
            for i, chunk in enumerate(chunks):
                chunk_id = f"{Path(file_path).stem}_{i}_{hashlib.md5(chunk.encode()).hexdigest()[:8]}"
                chunk_entries.append({
                    'id': chunk_id,
                    'content': chunk,
                    'source_file': str(file_path),
                    'metadata': {
                        'source_file': str(file_path),
                        'chunk_index': i
                    }
                })
                
            logger.info(f"Chunked {file_path} into {len(chunks)} pieces")
            return chunk_entries
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return []

    async def generate_embeddings(self, text_chunks: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text chunks using OpenAI
        """
        try:
            response = await self.openai_client.embeddings.create(
                input=text_chunks,
                model=self.config.embedding_model
            )
            
            embeddings = [item.embedding for item in response.data]
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    async def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single file: chunk, embed, and store
        """
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Load and chunk the file
            chunk_entries = await self.load_and_chunk_file(file_path)
            if not chunk_entries:
                return {'file': file_path, 'status': 'failed', 'message': 'No chunks created'}
            
            # Extract content for embedding
            texts = [chunk['content'] for chunk in chunk_entries]
            
            # Generate embeddings
            embeddings = await self.generate_embeddings(texts)
            
            # Prepare points for Qdrant
            qdrant_points = []
            postgres_records = []
            
            for chunk_entry, embedding in zip(chunk_entries, embeddings):
                # Prepare Qdrant point
                qdrant_points.append({
                    'id': chunk_entry['id'],
                    'vector': embedding,
                    'payload': {
                        'content': chunk_entry['content'],
                        'source_file': chunk_entry['metadata']['source_file'],
                        'chunk_index': chunk_entry['metadata']['chunk_index']
                    }
                })
                
                # Prepare Postgres record
                postgres_records.append({
                    'chunk_id': chunk_entry['id'],
                    'source_file': chunk_entry['metadata']['source_file'],
                    'source_section': f"chunk_{chunk_entry['metadata']['chunk_index']}",
                    'content_text': chunk_entry['content'][:500],  # Store first 500 chars as preview
                    'embedding_id': chunk_entry['id']
                })
            
            # Upload vectors to Qdrant
            await self.qdrant_client.batch_upload(qdrant_points)
            
            # Save metadata to Postgres
            for record in postgres_records:
                await self.postgres_client.save_metadata(
                    chunk_id=record['chunk_id'],
                    source_file=record['source_file'],
                    source_section=record['source_section'],
                    content_text=record['content_text'],
                    embedding_id=record['embedding_id']
                )
            
            logger.info(f"Successfully processed {file_path}: {len(chunk_entries)} chunks")
            return {'file': file_path, 'status': 'success', 'chunks_created': len(chunk_entries)}
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return {'file': file_path, 'status': 'failed', 'message': str(e)}

    async def process_directory(self, directory_path: str, force_reprocess: bool = False) -> Dict[str, Any]:
        """
        Process all markdown/MDX files in a directory
        """
        results = {
            'processed_files': [],
            'errors': [],
            'total_chunks': 0
        }
        
        # Find all markdown and MDX files
        file_extensions = ['.md', '.mdx']
        files_to_process = []
        
        for ext in file_extensions:
            files_to_process.extend(Path(directory_path).rglob(f"*{ext}"))
        
        logger.info(f"Found {len(files_to_process)} files to process")
        
        # Process each file
        for file_path in files_to_process:
            result = await self.process_file(str(file_path))
            if result['status'] == 'success':
                results['processed_files'].append(result)
                results['total_chunks'] += result.get('chunks_created', 0)
            else:
                results['errors'].append(result)
        
        # Determine overall status
        if results['errors'] and results['processed_files']:
            results['status'] = 'partial_success'
        elif results['errors']:
            results['status'] = 'error'
        else:
            results['status'] = 'success'
        
        return results


# Add the missing initialization of clients and the process_content function
import asyncio
import os
from pathlib import Path
from typing import Dict, Any
from rag_backend.config import settings
from rag_backend.rag_core.qdrant_client import QdrantClientWrapper
from rag_backend.rag_core.postgres_client import PostgresClient
from openai import AsyncOpenAI


async def process_content(source_path: str, force_reprocess: bool = False) -> Dict[str, Any]:
    """
    Main function to process content from a source path
    """
    # Initialize clients - this is a simplified approach
    # In a real application, you might want to pass these as dependencies
    openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    qdrant_client = QdrantClientWrapper(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        host=settings.qdrant_host,
        port=settings.qdrant_port
    )
    postgres_client = PostgresClient(settings.neon_database_url)

    # Connect to databases
    await postgres_client.connect()

    # Initialize ingestion pipeline
    ingestion_pipeline = IngestionPipeline(
        qdrant_client=qdrant_client,
        postgres_client=postgres_client,
        config=settings
    )

    # Determine if it's a file or directory
    path_obj = Path(source_path)

    try:
        if path_obj.is_file():
            # Process a single file
            result = await ingestion_pipeline.process_file(source_path)
            results = {
                'status': 'success' if result['status'] == 'success' else 'error',
                'processed_files': [result] if result['status'] == 'success' else [],
                'errors': [] if result['status'] == 'success' else [result]
            }
        elif path_obj.is_dir():
            # Process all markdown/MDX files in a directory
            results = await ingestion_pipeline.process_directory(source_path, force_reprocess)
        else:
            # Path doesn't exist
            results = {
                'status': 'error',
                'processed_files': [],
                'errors': [{'file': source_path, 'status': 'failed', 'message': 'Path does not exist'}]
            }

        return results

    finally:
        # Cleanup resources
        await qdrant_client.close()
        await postgres_client.close()