---
sdk: docker
app_port: 7860
---

# RAG Chatbot Backend

This directory contains the FastAPI backend for the RAG (Retrieval-Augmented Generation) Chatbot that integrates with the Docusaurus documentation site.

## Overview

The backend provides:
- Natural language Q&A over documentation content
- Source citation for all answers
- Text selection context awareness
- Content ingestion from MD/MDX files

## Architecture

- **FastAPI**: Web framework and API endpoints
- **Qdrant**: Vector database for semantic search
- **Neon Postgres**: Metadata storage
- **OpenAI**: Language model for response generation
- **LangChain**: Text processing and splitting

## Endpoints

### `GET /health`
Simple health check endpoint.

### `POST /chat`
Main RAG query endpoint.
- Request: `ChatRequest` (question and optional selected_context)
- Response: `ChatResponse` (answer and source_citations)

### `POST /ingest`
Content ingestion endpoint.
- Request: `IngestRequest` (source_path and optional force_reprocess)
- Response: `IngestResponse` (status, processed_files, and errors)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and connection strings
   ```

3. Run the server:
   ```bash
   uvicorn rag_backend.main:app --reload
   ```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL to your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for your Qdrant Cloud instance
- `NEON_DATABASE_URL`: Connection string for your Neon Postgres database
- `LOG_LEVEL`: Logging level (default: INFO)

## Development

Run tests:
```bash
pytest
```

## Deployment

For deployment instructions, see the deployment documentation in the main documentation.