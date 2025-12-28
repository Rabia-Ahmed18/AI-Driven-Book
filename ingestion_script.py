#!/usr/bin/env python3
"""
Ingestion script for the RAG Chatbot integration.
This script reads .md or .mdx files from the /docs directory,
chunks them using a recursive character splitter,
and upserts them into a Qdrant Cloud collection with OpenAI embeddings.
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.src.services.embedding_service import embedding_service
from backend.src.core.qdrant import qdrant_service
from backend.src.models.chunk import DocumentChunk
from backend.src.core.logging import app_logger

load_dotenv()

def read_docs_files(docs_path: str) -> List[Dict[str, Any]]:
    """
    Read all .md and .mdx files from the docs directory
    """
    files = []
    patterns = [os.path.join(docs_path, "**/*.md"), os.path.join(docs_path, "**/*.mdx")]

    for pattern in patterns:
        for file_path in glob.glob(pattern, recursive=True):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Create a relative URL from the file path
                relative_path = os.path.relpath(file_path, docs_path)
                url = f"/docs/{relative_path.replace(os.sep, '/')}"

                files.append({
                    "content": content,
                    "source_url": url,
                    "file_path": file_path
                })

    return files

def chunk_document(content: str, source_url: str, heading: str = "") -> List[DocumentChunk]:
    """
    Chunk the document content using RecursiveCharacterTextSplitter
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_text(content)

    document_chunks = []
    for i, chunk_text in enumerate(chunks):
        chunk = DocumentChunk(
            content=chunk_text,
            source_url=source_url,
            heading=heading,
            metadata={"chunk_index": i, "total_chunks": len(chunks)}
        )
        document_chunks.append(chunk)

    return document_chunks

def process_document(doc_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Process a single document: chunk it and generate embeddings
    """
    chunks = chunk_document(
        content=doc_data["content"],
        source_url=doc_data["source_url"],
        heading=Path(doc_data["file_path"]).stem  # Use filename as heading
    )

    processed_chunks = []
    for chunk in chunks:
        # Generate embedding for the chunk
        embedding = embedding_service.generate_embedding(chunk.content)
        chunk.embedding = embedding

        processed_chunks.append({
            "id": chunk.id,
            "vector": chunk.embedding,
            "payload": {
                "content": chunk.content,
                "source_url": chunk.source_url,
                "heading": chunk.heading,
                "metadata": chunk.metadata
            }
        })

    return processed_chunks

def main(docs_path: str = "./docs"):
    """
    Main ingestion function
    """
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"Docs directory not found: {docs_path}")

    app_logger.info(f"Starting ingestion from {docs_path}")

    # Read all docs files
    docs_files = read_docs_files(docs_path)
    app_logger.info(f"Found {len(docs_files)} files to process")

    all_chunks_for_upsert = []

    # Process each document
    for i, doc_data in enumerate(docs_files):
        app_logger.info(f"Processing file {i+1}/{len(docs_files)}: {doc_data['source_url']}")

        try:
            chunks_for_upsert = process_document(doc_data)
            all_chunks_for_upsert.extend(chunks_for_upsert)
        except Exception as e:
            app_logger.error(f"Error processing file {doc_data['source_url']}: {str(e)}")
            continue

    # Upsert all chunks to Qdrant
    if all_chunks_for_upsert:
        app_logger.info(f"Upserting {len(all_chunks_for_upsert)} chunks to Qdrant...")
        count = qdrant_service.upsert_vectors(all_chunks_for_upsert)
        app_logger.info(f"Successfully upserted {count} chunks to Qdrant")
    else:
        app_logger.warning("No chunks to upsert")

    app_logger.info("Ingestion completed")


if __name__ == "__main__":
    main()