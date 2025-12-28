# Data Model: RAG Chatbot Integration

## Overview
This document defines the data models for the RAG Chatbot integration, including entities, their attributes, relationships, and validation rules.

## Entity: Document Chunk
**Description**: Represents a segment of content from the book with associated metadata
**Attributes**:
- id: string (primary key, UUID)
- content: string (the actual text content of the chunk)
- source_url: string (URL of the original document)
- heading: string (heading/section title where the chunk appears)
- embedding: float[] (vector embedding of the content, 1536 dimensions for OpenAI text-embedding-3-small)
- metadata: object (additional metadata like file path, document title, etc.)
- created_at: datetime (timestamp when chunk was created)
- updated_at: datetime (timestamp when chunk was last updated)

**Validation Rules**:
- content must not be empty
- source_url must be a valid URL
- embedding must have exactly 1536 dimensions
- created_at must be before updated_at (if present)

## Entity: Chat Session
**Description**: Represents a conversation between user and the chatbot with history of messages
**Attributes**:
- id: string (primary key, UUID)
- session_id: string (unique identifier for the session)
- user_id: string (optional, for identifying users)
- created_at: datetime (timestamp when session was created)
- updated_at: datetime (timestamp when session was last updated)
- is_active: boolean (whether the session is currently active)

**Validation Rules**:
- session_id must be unique
- created_at must be before updated_at (if present)

## Entity: Chat Message
**Description**: Represents a single message in a chat session
**Attributes**:
- id: string (primary key, UUID)
- session_id: string (foreign key to Chat Session)
- role: string (either "user" or "assistant")
- content: string (the actual message content)
- timestamp: datetime (when the message was created)
- context_used: string (optional, the selected text context if applicable)
- sources: array of objects (citations to source documents)

**Validation Rules**:
- role must be either "user" or "assistant"
- content must not be empty
- session_id must reference an existing Chat Session
- sources must be valid document references

## Entity: Query Request
**Description**: Represents a user's question with optional selected text context
**Attributes**:
- id: string (primary key, UUID)
- question: string (the user's question)
- selected_text: string (optional, text selected by user)
- session_id: string (optional, session identifier)
- timestamp: datetime (when the query was made)
- response_id: string (optional, reference to the response)

**Validation Rules**:
- question must not be empty
- selected_text, if provided, must not be empty
- session_id, if provided, must reference an existing Chat Session

## Entity: Query Response
**Description**: Represents the system's response to a user's query
**Attributes**:
- id: string (primary key, UUID)
- query_id: string (foreign key to Query Request)
- content: string (the response content)
- sources: array of objects (citations to source documents)
- timestamp: datetime (when the response was generated)
- tokens_used: integer (number of tokens used in the response)

**Validation Rules**:
- content must not be empty
- query_id must reference an existing Query Request
- tokens_used must be non-negative
- sources must be valid document references

## Relationships
- Chat Session (1) → (Many) Chat Message
- Query Request (1) → (1) Query Response
- Document Chunk (Many) → (Many) Query Response (through citations)