# Research Findings: RAG-Based AI Book Chatbot

**Feature**: 008-rag-chatbot-full-implementation
**Created**: 2025-12-21
**Status**: Complete

## Authentication Model

### Decision: Session-based authentication with UUID tokens
- Users can be anonymous or authenticated
- Sessions stored in Neon Postgres with UUID tokens
- No need for complex user management for initial implementation

### Rationale:
- Simpler implementation for anonymous chatbot usage
- Sessions can be tied to users if authentication is added later
- Consistent with temporary chat session patterns

### Alternatives Considered:
- JWT tokens: More complex, requires token management
- OAuth integration: Overkill for initial implementation
- Cookie-based: Not ideal for API-first approach

## Rate Limiting Constraints

### Decision: Implement client-side and server-side rate limiting based on free tier limits
- OpenAI: 3,000,000 tokens per day per organization
- Qdrant Cloud Free Tier: Limited to 10,000 vectors
- Neon Serverless: Connection limits based on plan

### Rationale:
- Need to be mindful of costs and availability
- Server-side protection prevents abuse
- Client-side hints improve user experience

### Alternatives Considered:
- No rate limiting: Risk of exceeding free tier limits
- Aggressive rate limiting: May impact user experience

## Text Selection Implementation

### Decision: JavaScript event listener with window.getSelection()
- Capture selected text when user initiates chat
- Send selected text as optional parameter to backend
- Integrate with Docusaurus theme components

### Rationale:
- Native browser API, widely supported
- Simple to implement and maintain
- Works well with existing Docusaurus architecture

### Alternatives Considered:
- Custom selection component: More complex, reinventing the wheel
- React-specific libraries: May conflict with Docusaurus

## Qdrant Integration

### Decision: Collection per book with metadata for filtering
- Create separate Qdrant collections for each book
- Store source file and section metadata with each vector
- Use payload filtering for targeted searches

### Rationale:
- Allows for efficient querying of specific books
- Metadata enables rich source attribution
- Scalable approach for multiple books

### Alternatives Considered:
- Single collection for all books: Complex filtering, potential performance issues
- Separate instances: More complex management

## OpenAI SDK Usage

### Decision: Use OpenAI Python SDK with async calls
- Use text-embedding-3-small for embeddings
- Use gpt-4o for chat completions
- Implement proper error handling and timeouts

### Rationale:
- Official SDK provides best practices and updates
- Async calls improve performance
- Proper error handling ensures robustness

### Alternatives Considered:
- Raw HTTP requests: More complex, no built-in error handling
- Other LLM providers: Would require different integration patterns