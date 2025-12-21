# Data Model: RAG-Based AI Book Chatbot

**Feature**: 008-rag-chatbot-full-implementation
**Created**: 2025-12-21
**Status**: Complete

## Entity: Session

### Description
Represents a user's chat session with the AI book assistant.

### Fields
- `session_id`: UUID (Primary Key)
  - Unique identifier for the session
  - Generated server-side when session starts
- `user_id`: UUID (Optional, Foreign Key to Users table)
  - Links to authenticated user if available
  - NULL for anonymous sessions
- `created_at`: DateTime (UTC)
  - Timestamp when session was created
  - Used for session cleanup
- `updated_at`: DateTime (UTC)
  - Timestamp of last activity in session
  - Used for session timeout management
- `metadata`: JSONB
  - Additional session data (book_id, preferences, etc.)
  - Flexible storage for future requirements

### Relationships
- One-to-Many with ChatMessage (via session_id foreign key)
- Optional One-to-One with User (via user_id foreign key)

### Validation Rules
- `session_id` must be unique
- `created_at` must be in the past
- `updated_at` must be >= `created_at`

## Entity: BookMetadata

### Description
Stores information about the books in the system that can be queried by the chatbot.

### Fields
- `book_id`: UUID (Primary Key)
  - Unique identifier for the book
  - Used to separate content in Qdrant collections
- `title`: String (255 characters max)
  - Title of the book
  - Required field
- `author`: String (255 characters max)
  - Author of the book
  - Required field
- `version`: String (50 characters max)
  - Version identifier for the book
  - Used to track updates to book content
- `created_at`: DateTime (UTC)
  - Timestamp when book was first ingested
- `updated_at`: DateTime (UTC)
  - Timestamp when book was last updated
- `source_path`: String (500 characters max)
  - Path to the source files for the book
  - Used for reprocessing if needed

### Relationships
- One-to-Many with DocumentChunk (via book_id foreign key)
- One-to-Many with ChatMessage (via book_id in metadata)

### Validation Rules
- `title` and `author` are required
- `book_id` must be unique
- `version` must follow semantic versioning format (optional)

## Entity: DocumentChunk

### Description
Represents segments of book content that have been processed and stored with embeddings in the knowledge base.

### Fields
- `chunk_id`: UUID (Primary Key)
  - Unique identifier for the document chunk
  - Used for source attribution in responses
- `book_id`: UUID (Foreign Key)
  - Links to the book this chunk belongs to
  - Used for filtering in Qdrant
- `content`: Text
  - The actual content of the chunk
  - Used for context in RAG responses
- `source_file`: String (500 characters max)
  - Path to the original source file
  - Used for source attribution
- `source_section`: String (255 characters max)
  - Section heading or identifier in the source
  - Used for precise source attribution
- `chunk_index`: Integer
  - Sequential index of the chunk within the source
  - Helps maintain content order if needed
- `embedding_vector_id`: String
  - ID of the corresponding vector in Qdrant
  - Used for retrieval during RAG process
- `created_at`: DateTime (UTC)
  - Timestamp when the chunk was created
- `checksum`: String (64 characters)
  - SHA-256 hash of the content
  - Used to detect changes during reprocessing

### Relationships
- Many-to-One with BookMetadata (via book_id foreign key)

### Validation Rules
- `content` is required and non-empty
- `source_file` is required
- `chunk_index` must be non-negative
- `embedding_vector_id` must be unique across all chunks

### State Transitions
- NEW → PROCESSED: When chunk is successfully embedded and stored in Qdrant
- PROCESSED → UPDATED: When source content changes and chunk is reprocessed

## Entity: ChatMessage

### Description
Individual message in the conversation, including user query and AI response.

### Fields
- `message_id`: UUID (Primary Key)
  - Unique identifier for the message
- `session_id`: UUID (Foreign Key)
  - Links to the session this message belongs to
- `role`: Enum ('user', 'assistant')
  - Specifies if the message is from user or AI
- `content`: Text
  - The actual content of the message
- `created_at`: DateTime (UTC)
  - Timestamp when the message was created
- `sources`: JSONB
  - References to document chunks used in the response
  - Format: [{"chunk_id": "...", "content": "...", "relevance_score": 0.85}]
- `selected_text`: Text (Optional)
  - Text that was selected by the user when this message was created
  - NULL if standard RAG flow was used
- `response_time_ms`: Integer
  - Time in milliseconds it took to generate the response
  - Used for performance monitoring

### Relationships
- Many-to-One with Session (via session_id foreign key)

### Validation Rules
- `role` must be either 'user' or 'assistant'
- `content` is required
- `session_id` must reference an existing session
- `response_time_ms` must be non-negative if provided

### State Transitions
- PENDING → COMPLETED: When AI response is generated successfully
- PENDING → ERROR: When there's an error generating the response