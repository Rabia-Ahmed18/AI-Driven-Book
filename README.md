# AI-Powered Book Assistant (RAG Chatbot)

This project implements a Retrieval-Augmented Generation (RAG) system integrated into a digital book platform. The system allows users to ask questions about book content and receive accurate answers grounded in the source material.

## Architecture

The system consists of:
- **Backend**: FastAPI application handling API requests and RAG operations
- **Vector Database**: Qdrant Cloud for storing and querying text embeddings
- **LLM Integration**: OpenAI SDK for response generation
- **Frontend**: Docusaurus/React-based chatbot component for user interaction
- **Content Source**: Docusaurus /docs folder or sitemap.xml for document ingestion

## Features

- **RAG-First Architecture**: All responses are grounded in source documentation content
- **Dual-Context Retrieval**: Supports both global book queries and selection-specific queries with proper context separation
- **Content Ingestion Pipeline**: Crawls Docusaurus /docs folder or parses sitemap.xml, chunks text, and stores in Qdrant with metadata
- **Citation System**: Responses include direct citations to original content with precise source locations
- **Text Selection Tool**: "Ask AI" tooltip appears when user highlights text, triggering chatbot with selection pre-loaded
- **Floating Chat Widget**: React-based chat component integrated into Docusaurus layout
- **Rate Limiting**: Implements rate limiting to protect Free Tier usage

## Setup

### Backend

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create a `.env` file with the following environment variables:
```env
OPENAI_API_KEY=your-openai-api-key
QDRANT_URL=https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=book_chunks
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4-turbo
SECRET_KEY=your-secret-key
DEBUG=false
```

3. Run the backend:
```bash
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Create a `.env` file in the frontend directory:
```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_CHATBOT_ENABLED=true
```

3. Run the frontend:
```bash
cd frontend
npm start
```

## API Endpoints

- `POST /api/v1/ingest`: Ingest documentation from Docusaurus /docs folder or sitemap.xml into the system
- `POST /api/v1/chat`: Chat with the book assistant (supports global and selection-specific contexts)
- `POST /api/v1/query`: Accepts a user question and returns a RAG-based answer
- `POST /api/v1/query-selection`: Accepts both a question AND a selected_text string to perform focused grounding
- `GET /api/v1/health`: Health check for the API and its dependencies

## Environment Variables

### Backend (.env)
```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4-turbo

# Qdrant Configuration
QDRANT_URL=https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=book_chunks

# Application Configuration
SECRET_KEY=your-secret-key
DEBUG=false
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
ALLOWED_ORIGINS=["*"]  # Should be configured properly for production
```

### Frontend (.env)
```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_CHATBOT_ENABLED=true
```

## Deployment

### Backend Deployment

The backend can be deployed on platforms like Render, Railway, or AWS. Ensure your environment variables are properly configured.

### Frontend Integration with Docusaurus

To integrate the chatbot with your Docusaurus site:

1. Add the ChatWidget component to your Docusaurus site by modifying `src/theme/Root.js`:

```javascript
import React from 'react';
import ChatWidget from './ChatWidget'; // Adjust path as needed

export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
```

### Vercel Deployment

To deploy your Docusaurus site to Vercel:

1. Push your Docusaurus site to a Git repository
2. Connect the repository to Vercel
3. Add the following environment variable in Vercel settings:
   - `REACT_APP_API_BASE_URL`: URL of your deployed backend API
4. Vercel will automatically build and deploy your site

## Development

The project follows a modular structure with clear separation between backend and frontend components. Each component is independently testable and deployable.

### Backend Structure
```
backend/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── api/             # API endpoints
│   ├── core/            # Core utilities
│   ├── middleware/      # Middleware components
│   └── utils/           # Helper functions
├── tests/               # Test files
├── requirements.txt     # Python dependencies
└── pyproject.toml       # Build and linting configuration
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/      # React components
│   ├── hooks/           # Custom hooks
│   ├── services/        # API clients
│   └── types/           # TypeScript types
├── tests/               # Test files
└── package.json         # Node.js dependencies
```

## Testing

Run backend tests:
```bash
cd backend
python -m pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Content Ingestion

To ingest your documentation content:

1. Place your .md or .mdx files in the `/docs` directory
2. Run the ingestion script:
```bash
python ingestion_script.py
```

This will parse the documents, chunk them using a recursive character splitter, generate OpenAI embeddings, and store them in Qdrant Cloud with metadata.