# Deployment Guide: RAG Chatbot

## Backend Deployment (FastAPI)

### Option 1: Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following environment variables in the Render dashboard:
   - `OPENAI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `NEON_DATABASE_URL`
   - `LOG_LEVEL` (optional, default: INFO)

4. Set the build command:
   ```
   pip install -r requirements.txt
   ```

5. Set the start command:
   ```
   uvicorn rag_backend.main:app --host 0.0.0.0 --port $PORT
   ```

### Option 2: Deploy to Railway

1. Create a new project on Railway
2. Connect your GitHub repository
3. Set the required environment variables in the Railway dashboard
4. Railway will automatically detect it's a Python application
5. Deploy the application

### Environment Variables

You'll need to configure these environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL to your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for your Qdrant Cloud instance
- `NEON_DATABASE_URL`: Connection string for your Neon Postgres database
- `LOG_LEVEL`: (Optional) Logging level (default: INFO)

## Frontend Integration

### Updating the API URL

In the `RAGChatbot.tsx` component, update the API endpoint:

```typescript
// Before deploying, change the backend URL from localhost to your deployed backend
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'https://your-backend-url.onrender.com';
// Replace fetch calls:
const response = await fetch(`${BACKEND_URL}/chat`, {
  // ... rest of the code
});
```

### Environment Configuration

For Docusaurus, you can set environment variables using a `.env` file or set them directly in your hosting platform:

```env
# For development
REACT_APP_BACKEND_URL=http://localhost:8000

# For production
REACT_APP_BACKEND_URL=https://your-deployed-backend.onrender.com
```

## Docusaurus Integration

To integrate the component with your Docusaurus site:

1. If you're using a custom layout, import and add the component:
   ```jsx
   import RAGChatbot from '@site/src/components/RAGChatbot';
   
   // In your layout component
   <RAGChatbot />
   ```

2. You can also add it to specific pages by importing directly in the MDX files:
   ```mdx
   import RAGChatbot from '@site/src/components/RAGChatbot';
   
   <RAGChatbot />
   ```

## Proxy Setup (if needed)

If your Docusaurus site and backend are hosted on different domains, you might need to set up a proxy. You can add a proxy configuration to your Docusaurus setup if needed:

```js
// In docusaurus.config.js
module.exports = {
  // ... existing config
  themes: [
    // ... existing themes
  ],
  plugins: [
    [
      '@docusaurus/plugin-client-redirects',
      {
        fromExtensions: ['html'],
        redirects: [
          // Add proxy redirects if needed
        ],
      },
    ],
  ],
};
```

## Post-Deployment Steps

1. Test the `/health` endpoint to confirm the backend is running
2. Verify that the ingestion process works by uploading test content
3. Test both general questions and selected text queries
4. Confirm that source citations are being returned properly
5. Validate that the chatbot integrates properly with your Docusaurus site

## Troubleshooting

- If you get CORS errors, ensure the backend is configured to allow requests from your frontend domain
- If API calls fail, verify that all environment variables are properly set
- If the chatbot doesn't appear, check that the component is properly imported and rendered