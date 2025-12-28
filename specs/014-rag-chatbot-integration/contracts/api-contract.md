# API Contract: RAG Chatbot Integration

## Overview
This document defines the API contracts for the RAG Chatbot integration, including endpoints, request/response schemas, and error handling.

## Base URL
`https://api.example.com/v1`

## Common Headers
- `Content-Type: application/json`
- `Authorization: Bearer {api_key}` (for protected endpoints)

## Endpoints

### POST /chat
Initiates a conversation or continues an existing one with a general question about the book content.

#### Request
```json
{
  "question": "string (required)",
  "session_id": "string (optional)",
  "selected_text": "string (optional)"
}
```

#### Response (Success 200)
```json
{
  "response_id": "string",
  "session_id": "string",
  "answer": "string",
  "sources": [
    {
      "url": "string",
      "heading": "string",
      "content": "string"
    }
  ],
  "timestamp": "ISO 8601 datetime"
}
```

#### Response (Error 400)
```json
{
  "error": "string",
  "message": "string"
}
```

#### Response (Error 429 - Rate Limited)
```json
{
  "error": "rate_limited",
  "message": "Rate limit exceeded. Please try again later."
}
```

### POST /query
Accepts a user question and returns a RAG-based answer (alternative to /chat).

#### Request
```json
{
  "question": "string (required)",
  "session_id": "string (optional)"
}
```

#### Response (Success 200)
```json
{
  "response_id": "string",
  "session_id": "string",
  "answer": "string",
  "sources": [
    {
      "url": "string",
      "heading": "string",
      "content": "string"
    }
  ],
  "timestamp": "ISO 8601 datetime"
}
```

### POST /query-selection
Accepts both a question AND a selected_text string to perform focused grounding.

#### Request
```json
{
  "question": "string (required)",
  "selected_text": "string (required)",
  "session_id": "string (optional)"
}
```

#### Response (Success 200)
```json
{
  "response_id": "string",
  "session_id": "string",
  "answer": "string",
  "sources": [
    {
      "url": "string",
      "heading": "string",
      "content": "string"
    }
  ],
  "timestamp": "ISO 8601 datetime"
}
```

### POST /ingest
Ingests documentation from Docusaurus /docs folder or sitemap.xml into the system.

#### Request
```json
{
  "source_type": "string (docs_directory|sitemap_xml)",
  "source_path": "string (required if source_type is docs_directory)",
  "sitemap_url": "string (required if source_type is sitemap_xml)"
}
```

#### Response (Success 200)
```json
{
  "status": "success",
  "chunks_processed": "integer",
  "timestamp": "ISO 8601 datetime"
}
```

### GET /health
Checks the health of the API and its dependencies.

#### Response (Success 200)
```json
{
  "status": "healthy",
  "timestamp": "ISO 8601 datetime",
  "dependencies": {
    "qdrant": "healthy",
    "openai": "healthy"
  }
}
```

## Error Codes
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid API key
- `429 Rate Limited`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Dependency unavailable