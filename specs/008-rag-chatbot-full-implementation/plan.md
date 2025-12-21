# Implementation Plan: RAG-Based AI Book Chatbot

**Feature**: 008-rag-chatbot-full-implementation
**Created**: 2025-12-21
**Status**: Draft
**Branch**: 008-rag-chatbot-full-implementation

## Technical Context

- **Backend Framework**: FastAPI (Python)
- **Database**: Neon Serverless Postgres for session data and book metadata
- **Vector Store**: Qdrant Cloud for document embeddings
- **LLM Integration**: OpenAI SDK for embeddings and chat completions
- **Frontend Integration**: Docusaurus with text selection capabilities
- **API Contract**: REST endpoints with JSON payloads
- **Authentication**: Session-based with UUID tokens, anonymous sessions supported
- **Rate Limiting**: Based on OpenAI and Qdrant Cloud free tier limits
- **Deployment**: Cloud services for backend, GitHub Pages for frontend

## Constitution Check

Based on the project constitution, this implementation must:

- [ ] Follow RAG-First Architecture principles (responses grounded in book content)
- [ ] Maintain Full-Stack Modularity (separate backend, vector DB, metadata store, frontend)
- [ ] Implement Test-First methodology (TDD with Red-Green-Refactor cycle)
- [ ] Ensure Content Context Integrity (separation between book-wide and selected text Q&A)
- [ ] Provide Source Transparency (responses with citations to original content)
- [ ] Follow Deployment-First Design (production-ready from inception)

## Gates

- [ ] Architecture aligns with constitution principles
- [ ] Dependencies compatible with deployment constraints
- [ ] Security model addresses user data protection
- [ ] Performance targets achievable within free tier limitations

## Phase 0: Research & Unknown Resolution

### Research Tasks

1. **Authentication Model**: Research session management best practices for FastAPI with Neon Postgres
2. **Rate Limiting Constraints**: Investigate OpenAI and Qdrant Cloud free tier limitations
3. **Text Selection Implementation**: Find best practices for capturing selected text in Docusaurus/React
4. **Qdrant Integration**: Research optimal vector storage patterns for book content
5. **OpenAI SDK Usage**: Best practices for embedding generation and chat completion

## Phase 1: Design & Contracts

### 1.1 Data Model Design

#### Session Entity
- `session_id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key, optional for anonymous users)
- `created_at`: Timestamp
- `updated_at`: Timestamp
- `metadata`: JSONB (additional session data)

#### Book Metadata Entity
- `book_id`: UUID (Primary Key)
- `title`: String
- `author`: String
- `version`: String
- `created_at`: Timestamp
- `source_path`: String (path to source files)

#### Document Chunk Entity
- `chunk_id`: UUID (Primary Key)
- `book_id`: UUID (Foreign Key)
- `content`: Text
- `source_file`: String
- `source_section`: String
- `chunk_index`: Integer
- `embedding_vector_id`: String (Qdrant ID)
- `created_at`: Timestamp

#### Chat Message Entity
- `message_id`: UUID (Primary Key)
- `session_id`: UUID (Foreign Key)
- `role`: Enum ('user', 'assistant')
- `content`: Text
- `created_at`: Timestamp
- `sources`: JSONB (references to document chunks)

### 1.2 API Contracts

#### POST /chat
- **Purpose**: Process user queries and return AI-generated responses
- **Request Body**:
  ```json
  {
    "query": "string",
    "session_id": "string (optional)",
    "selected_text": "string (optional)",
    "book_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "response": "string",
    "session_id": "string",
    "sources": [
      {
        "chunk_id": "string",
        "content": "string",
        "source_file": "string",
        "relevance_score": "number"
      }
    ]
  }
  ```
- **Error Responses**:
  - 400: Invalid request parameters
  - 429: Rate limit exceeded
  - 500: Internal server error

#### POST /ingest
- **Purpose**: Process book content and store embeddings
- **Request Body**:
  ```json
  {
    "book_id": "string",
    "source_path": "string",
    "chunk_size": "number (default 1000)"
  }
  ```
- **Response**:
  ```json
  {
    "status": "completed",
    "chunks_processed": "number",
    "book_id": "string"
  }
  ```
- **Error Responses**:
  - 400: Invalid request parameters
  - 500: Ingestion failed

### 1.3 Quickstart Guide

#### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API key
- Qdrant Cloud account
- Neon Postgres account

#### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Install Python dependencies**
   ```bash
   pip install fastapi uvicorn python-dotenv openai qdrant-client psycopg2-binary python-multipart
   ```

3. **Install Node.js dependencies** (for frontend)
   ```bash
   npm install
   ```

4. **Set up environment variables**
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_key
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   DATABASE_URL=your_neon_postgres_connection_string
   ```

5. **Run the application**
   ```bash
   # Backend
   uvicorn main:app --reload

   # Frontend (in separate terminal)
   npm run start
   ```

## Phase 2: Implementation Steps

### Step 1: Environment & Database Setup
- [ ] Configure Neon Postgres connection
- [ ] Set up Qdrant Cloud collection for document embeddings
- [ ] Create database models using SQLAlchemy
- [ ] Implement connection pooling and error handling

### Step 2: Data Ingestion Pipeline
- [ ] Create ingestion script to process book content
- [ ] Implement Recursive Character Text Splitting
- [ ] Generate embeddings using OpenAI's text-embedding-3-small
- [ ] Upsert embeddings to Qdrant with metadata
- [ ] Create mapping between chunks and source locations

### Step 3: FastAPI Backend Development
- [ ] Create API endpoints for chat functionality
- [ ] Implement Path A: Standard RAG (vector search in Qdrant)
- [ ] Implement Path B: Targeted RAG (context from selected text)
- [ ] Add proper error handling and validation
- [ ] Implement session management with Neon Postgres

### Step 4: Integration with OpenAI SDK
- [ ] Implement embedding generation for queries
- [ ] Create chat completion requests with proper context
- [ ] Handle streaming responses for better UX
- [ ] Add source attribution to responses

### Step 5: Frontend Integration
- [ ] Implement text selection detection in Docusaurus
- [ ] Create event listener for selected text
- [ ] Send selected text to backend as optional parameter
- [ ] Update UI to show source citations
- [ ] Add loading indicators and error states

### Step 6: Testing & Quality Assurance
- [ ] Write unit tests for core functions
- [ ] Create integration tests for API endpoints
- [ ] Implement E2E tests for complete Q&A flows
- [ ] Add response validation to ensure source grounding
- [ ] Test both RAG paths (standard and targeted)

## Phase 3: Deployment Preparation

### Backend Deployment
- [ ] Containerize application with Docker
- [ ] Set up CI/CD pipeline
- [ ] Configure environment variables for production
- [ ] Implement health checks and monitoring

### Frontend Deployment
- [ ] Build static assets for GitHub Pages
- [ ] Configure Docusaurus for production
- [ ] Set up CDN for static assets
- [ ] Implement error logging and analytics

## Risks & Mitigation

1. **Rate Limiting**: Implement retry mechanisms and caching
2. **Vector Store Costs**: Optimize chunking strategy to reduce API calls
3. **Response Latency**: Implement streaming responses and caching
4. **Data Privacy**: Ensure user queries are not stored unnecessarily
5. **Source Attribution**: Implement robust tracking from chunks to responses