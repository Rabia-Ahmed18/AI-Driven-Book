# AI-Powered Book Assistant (RAG Chatbot)

This project implements a Retrieval-Augmented Generation (RAG) system integrated into a digital book platform. The system allows users to ask questions about book content and receive accurate answers grounded in the source material.

## Architecture

The system consists of:
- **Backend**: FastAPI application handling API requests and RAG operations
- **Vector Database**: Qdrant Cloud for storing and querying text embeddings
- **Relational Database**: Neon Serverless Postgres for user data and session management
- **LLM Integration**: OpenAI SDK for response generation
- **Frontend**: React-based chatbot component for user interaction

## Features

- **Dual-Context Retrieval**: Supports both global book queries and selection-specific queries
- **Content Ingestion**: API for ingesting book content and generating embeddings
- **Citation System**: Responses include citations to specific sections of the book
- **Session Management**: Track conversation history with books
- **Text Selection**: Capture user-selected text for context-specific queries

## Setup

### Backend

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create a `.env` file with the following environment variables:
```env
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
QDRANT_URL=https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key
```

3. Run the backend:
```bash
cd backend
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t book-assistant-backend .
```

2. Run the container:
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-openai-api-key \
  -e QDRANT_URL=your-qdrant-url \
  -e QDRANT_API_KEY=your-qdrant-api-key \
  -e NEON_DATABASE_URL=your-neon-db-url \
  book-assistant-backend
```

### HuggingFace Spaces Deployment

To deploy on HuggingFace Spaces:

1. Create a Space with Docker type
2. Add your repository URL
3. Add the following environment variables in the Space settings:
   - `OPENAI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `NEON_DATABASE_URL`
4. The Space will automatically build and deploy using the Dockerfile and space.yml

### Frontend

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Create a `.env` file in the frontend directory:
```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

3. Run the frontend:
```bash
cd frontend
npm start
```

## API Endpoints

- `POST /api/v1/ingest`: Ingest a book into the system
- `POST /api/v1/chat`: Chat with the book assistant
- `GET /api/v1/books`: List all books
- `POST /api/v1/books`: Create a new book entry
- `GET /api/v1/books/{book_id}`: Get details about a specific book
- `POST /api/v1/sessions`: Create a new chat session
- `GET /api/v1/sessions/{session_id}/interactions`: Get session interactions

## Environment Variables

### Backend (.env)
```env
# Database Configuration
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require

# Vector Database Configuration
QDRANT_URL=https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=book_chunks

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4-turbo

# Application Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
SECRET_KEY=your-secret-key
```

### Frontend (.env)
```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_CHATBOT_ENABLED=true
```

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
│   └── utils/           # Helper functions
└── tests/               # Test files
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/      # React components
│   ├── hooks/           # Custom hooks
│   ├── services/        # API clients
│   └── types/           # TypeScript types
└── tests/               # Test files
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

## Railway Deployment

To deploy this application on Railway:

1. Create a new Railway project
2. Connect your GitHub repository or push directly using the Railway CLI
3. Set the following environment variables in Railway:
   - `OPENAI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `NEON_DATABASE_URL`
   - `SECRET_KEY`
4. The application will build using the Dockerfile in the root directory
5. Make sure to set the start command to match the Dockerfile CMD instruction if needed

### Troubleshooting Railway Deployment

If you encounter a build error like:
```
ERROR: failed to build: failed to solve: failed to calculate checksum of ref ...: "/backend/requirements.txt": not found
```

This issue has been fixed in the current Dockerfile by ensuring the entire project is copied to the build context before attempting to access the backend/requirements.txt file.