# Quickstart: RAG Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+ (for Docusaurus frontend)
- Access to OpenAI API
- Qdrant Cloud account (free tier)
- Neon Serverless Postgres account (free tier)

## Setup Backend

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up the backend environment**
   ```bash
   cd rag_backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and connection strings
   ```

4. **Run the backend service**
   ```bash
   uvicorn main:app --reload
   ```

The backend will be available at `http://localhost:8000`

## Setup Frontend

1. **Install frontend dependencies**
   ```bash
   cd <project-root>
   npm install
   ```

2. **Configure Docusaurus to use the RAG component**
   Update `docusaurus.config.js` to include the RAG chatbot component.

3. **Start the development server**
   ```bash
   npm run start
   ```

The frontend will be available at `http://localhost:3000`

## Ingest Content

1. **Prepare your content**
   Ensure your book content is in the `docs/` directory in MDX/Markdown format.

2. **Run the ingestion process**
   ```bash
   # Either call the API endpoint
   curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d '{"source_path": "docs/"}'
   
   # Or run the standalone script
   python ingestion/ingestion_script.py
   ```

## Test the API

1. **Check health**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Ask a question**
   ```bash
   curl -X POST http://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{"question": "What is the main concept of this book?"}'
   ```

3. **Ask with selected context**
   ```bash
   curl -X POST http://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{"question": "Can you elaborate on this?", "selected_context": "RAG combines retrieval and generation..."}'
   ```

## Deploy

### Backend Deployment
Deploy the FastAPI backend to a cloud platform like Render, Railway, or AWS. Ensure environment variables are configured with production API keys.

### Frontend Deployment
The Docusaurus frontend can be built and deployed to GitHub Pages:
```bash
npm run build
# Deploy the build/ directory to GitHub Pages
```

## Troubleshooting

### Common Issues

1. **Environment Variables Not Set**
   - Verify all required environment variables are set in your `.env` file
   - Check that you're using the correct API keys and connection strings

2. **Database Connection Issues**
   - Verify your Neon Postgres connection string is correct
   - Check that your database is accessible from your current network

3. **Vector Database Connection Issues**
   - Verify your Qdrant Cloud configuration is correct
   - Ensure the collection exists and has the right schema

### API Error Responses

- **400 Bad Request**: Check the request body format against the API specification
- **500 Internal Server Error**: Check backend logs for detailed error information
- **Timeout Errors**: The RAG process might be taking too long; check the content indexing

## Next Steps

1. Customize the chatbot UI to match your documentation theme
2. Fine-tune the RAG pipeline for your specific content
3. Add additional features like chat history or user preferences
4. Set up monitoring and analytics for the RAG system