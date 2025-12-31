# Quickstart Guide: RAG Chatbot Integration

## Overview
This guide provides a quick setup process to get the RAG Chatbot integration running with your Docusaurus book.

## Prerequisites
- Python 3.11+
- Node.js 16+ (for Docusaurus)
- Access to OpenAI API
- Qdrant Cloud account

## Setup Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 3. Configure Environment Variables
Edit the `.env` file with your credentials:
```env
OPENAI_API_KEY=your-openai-api-key
QDRANT_URL=your-qdrant-cluster-url
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=book_chunks
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4-turbo
SECRET_KEY=your-secret-key
```

### 4. Ingest Documentation Content
```bash
# Run the ingestion script to process your Docusaurus docs
python ingestion_script.py
```

### 5. Start the Backend Server
```bash
# From the backend directory
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Update the backend API URL in .env
REACT_APP_API_BASE_URL=http://localhost:8000
```

### 7. Integrate with Docusaurus
Add the ChatWidget component to your Docusaurus site by modifying `src/theme/Root.js`:

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

### 8. Start the Docusaurus Development Server
```bash
# From your Docusaurus project directory
npm start
```

## Testing the Integration
1. Visit your Docusaurus site
2. The chat widget should appear on all pages
3. Try asking questions about your documentation
4. Test the text selection feature by highlighting text and using the floating action button

## Deployment
### Backend
Deploy the FastAPI application to a platform like Render, Railway, or AWS. Ensure your environment variables are properly configured.

### Frontend
Deploy your Docusaurus site to Vercel, Netlify, or similar platform. Update the `REACT_APP_API_BASE_URL` environment variable to point to your deployed backend.

## Troubleshooting
- If the chat widget doesn't appear, check that it's properly integrated in your Docusaurus theme
- If queries return no results, verify that the ingestion script ran successfully and populated Qdrant
- For API errors, check that your environment variables are correctly set