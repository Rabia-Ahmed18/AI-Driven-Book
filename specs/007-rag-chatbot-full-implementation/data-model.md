# Data Model: RAG Chatbot

## Backend Data Models

### ChatRequest
Represents a user query with optional selected context.

```python
class ChatRequest(BaseModel):
    question: str
    selected_context: Optional[str] = None
```

**Fields**:
- `question`: The user's question (required, string)
- `selected_context`: The highlighted text from the Docusaurus page (optional string, default: None)

**Validation rules**:
- question must be between 1 and 1000 characters
- question cannot be empty or whitespace only

### ChatResponse
Contains the LLM-generated answer and source citations.

```python
class ChatResponse(BaseModel):
    answer: str
    source_citations: List[str]
```

**Fields**:
- `answer`: The final LLM-generated answer (required, string)
- `source_citations`: List of document/chunk IDs or titles retrieved from Qdrant/Postgres (required, list of strings)

**Validation rules**:
- answer must not exceed 2000 characters
- source_citations must be a list of valid identifiers

### IngestRequest
Defines parameters for content ingestion.

```python
class IngestRequest(BaseModel):
    source_path: str
    force_reprocess: Optional[bool] = False
```

**Fields**:
- `source_path`: Path to the content to be ingested (required, string)
- `force_reprocess`: Whether to reprocess content even if already indexed (optional boolean, default: false)

**Validation rules**:
- source_path must be a valid file or directory path
- source_path must not be empty

### IngestResponse
Confirms successful content ingestion.

```python
class IngestResponse(BaseModel):
    status: str
    processed_files: List[str]
    errors: Optional[List[str]] = []
```

**Fields**:
- `status`: Status of the ingestion operation (required, string)
- `processed_files`: List of files that were successfully processed (required, list of strings)
- `errors`: List of any errors that occurred during processing (optional list of strings)

**Validation rules**:
- status must be "success" or "partial_success" or "error"
- processed_files list cannot be empty on successful operation

## Database Models

### VectorMetadata
Stores content-to-source mappings for citation tracking.

```sql
CREATE TABLE vector_metadata (
    chunk_id VARCHAR(255) PRIMARY KEY,
    source_file VARCHAR(500) NOT NULL,
    source_section VARCHAR(500),
    content_text TEXT,
    embedding_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields**:
- `chunk_id`: Unique identifier for the text chunk (primary key)
- `source_file`: Path to the original source file (required)
- `source_section`: Section heading or identifier within the file (optional)
- `content_text`: The actual text content of the chunk (required)
- `embedding_id`: Reference to the vector embedding in Qdrant (required)
- `created_at`: Timestamp when record was created (auto-generated)
- `updated_at`: Timestamp when record was last updated (auto-generated)

**Constraints**:
- chunk_id must be unique
- source_file cannot be empty
- embedding_id must exist in Qdrant

## Frontend Data Models

### ChatMessage
Represents a single message in the chat interface.

```typescript
interface ChatMessage {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    citations?: string[];
}
```

**Fields**:
- `id`: Unique identifier for the message
- `role`: Whether the message is from 'user' or 'assistant'
- `content`: The text content of the message
- `timestamp`: When the message was created
- `citations`: Optional list of source citations for assistant responses

### ChatState
Represents the current state of the chat session.

```typescript
interface ChatState {
    messages: ChatMessage[];
    isLoading: boolean;
    error?: string;
    selectedText: string | null;
}
```

**Fields**:
- `messages`: List of chat messages in chronological order
- `isLoading`: Whether the system is currently processing a request
- `error`: Optional error message if something went wrong
- `selectedText`: Currently selected text from the document (or null if nothing selected)

## Relationships

### Backend Relationships
- ChatRequest and ChatResponse are used in the /chat endpoint request/response cycle
- IngestRequest and IngestResponse are used in the /ingest endpoint request/response cycle
- VectorMetadata records are created during ingestion and referenced during chat operations

### Frontend Relationships
- ChatState contains multiple ChatMessage instances
- ChatMessage can reference VectorMetadata via citations

## State Transitions

### ChatState Transitions
1. Initial: `isLoading: false`, `messages: []`, `selectedText: null`
2. After text selection: `selectedText` updated to selected content
3. On question submission: `isLoading: true`, new user message added
4. On response: `isLoading: false`, assistant message added with citations
5. On error: `error` field populated, `isLoading: false`