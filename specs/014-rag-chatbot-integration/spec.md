# Feature Specification: RAG Chatbot Integration

**Feature Branch**: `014-rag-chatbot-integration`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "Goal: Implement a production-ready RAG Chatbot integration for the Docusaurus book using FastAPI, Qdrant Cloud, and OpenAI. Requirements for Execution: Backend (FastAPI & Qdrant): Vector Ingestion Script: Create a Python utility to read the .md or .mdx files from the /docs directory, chunk them using a recursive character splitter, and upsert them into a Qdrant Cloud collection with OpenAI embeddings. API Endpoints: * POST /query: Accepts a user question and returns a RAG-based answer. POST /query-selection: Accepts both a question AND a selected_text string to perform focused grounding. Environment Setup: Provide a .env.example file for OPENAI_API_KEY, QDRANT_URL, and QDRANT_API_KEY. Frontend (Docusaurus/React Integration): Chat Component: Create a React component (ChatWidget.js) using the ChatKit SDK or a custom Tailwind-styled UI. State Management: The widget must handle "Selected Text" mode. If a user highlights text, the widget should display "Answering based on selection..." Global Injection: Provide the code to modify docusaurus.config.js or src/theme/Root.js to ensure the chatbot is persistent across all pages. The "Selection-Only" Logic: Implement a JavaScript listener that captures window.getSelection().toString(). Provide a "Floating Action Button" that appears near the cursor when text is selected, allowing the user to send that text directly to the chatbot context. Output Format: Provide the directory structure for a /chatbot-backend folder. Provide the updated Docusaurus component code. Provide a README detailing how to link the Vercel-deployed frontend to the FastAPI backend. Context for your Setup To make this work seamlessly on Vercel, remember: The Backend: Since you are using FastAPI, you should host it on a service like Render or Railway (which support persistent Python processes better than Vercel's serverless functions for long LLM streaming). The Connection: Your Docusaurus site on Vercel will need the URL of your FastAPI backend added as an environment variable (CHAT_API_URL)."

## Clarifications

### Session 2025-12-28

- Q: For the RAG Chatbot integration, how should user authentication be handled? → A: Authentication only required for certain actions (like saving conversations)
- Q: What are the specific performance requirements for the chatbot response time? → A: Response time under 2 seconds for all requests
- Q: How should the system handle external service failures (like OpenAI or Qdrant being unavailable)? → A: System should gracefully degrade by providing general help when external services are unavailable
- Q: How long should user conversation data be retained? → A: Retain conversations for 30 days, then automatically delete
- Q: What accessibility standards should the chatbot interface follow? → A: Basic accessibility with keyboard navigation only

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Global Book Q&A (Priority: P1)

As a reader of the Docusaurus book, I want to ask questions about the content so that I can quickly find relevant information without manually searching through pages.

**Why this priority**: This is the core functionality that provides value to all users - being able to ask questions and get answers based on the book content.

**Independent Test**: Can be fully tested by asking questions about the book content and verifying that the responses are accurate and properly cited.

**Acceptance Scenarios**:

1. **Given** I am viewing any page in the Docusaurus book, **When** I type a question in the chat widget and submit it, **Then** I receive a relevant answer based on the book content with proper citations.
2. **Given** I have asked a question, **When** the system cannot find relevant information in the book, **Then** I receive a response indicating that the information is not available in the book.

---

### User Story 2 - Selection-Based Q&A (Priority: P2)

As a reader of the Docusaurus book, I want to select specific text and ask questions about it so that I can get more detailed explanations about particular concepts.

**Why this priority**: This provides enhanced functionality that allows users to get more focused answers based on specific content they're reading.

**Independent Test**: Can be fully tested by selecting text in the book, asking a question about it, and verifying that the response is contextually relevant to the selected text.

**Acceptance Scenarios**:

1. **Given** I have selected text in the book, **When** I click the floating action button that appears near my cursor, **Then** the chat widget opens in "selection mode" with the selected text as context.
2. **Given** I am in selection mode, **When** I ask a question, **Then** the response is focused on the selected text and displays "Answering based on selection..." indicator.

---

### User Story 3 - Content Ingestion (Priority: P3)

As a book maintainer, I want to automatically ingest new or updated content from the Docusaurus docs so that the chatbot always has access to the most current information.

**Why this priority**: This ensures the chatbot remains useful as the book content evolves over time.

**Independent Test**: Can be fully tested by running the ingestion script and verifying that new/updated content is properly chunked and stored in Qdrant Cloud.

**Acceptance Scenarios**:

1. **Given** new or updated .md or .mdx files exist in the /docs directory, **When** I run the ingestion script, **Then** the content is properly chunked and stored in Qdrant Cloud with OpenAI embeddings.
2. **Given** the ingestion script has run successfully, **When** I query about the new content, **Then** the chatbot can respond with information from that content.

---

### Edge Cases

- What happens when the Qdrant Cloud service is temporarily unavailable?
- How does the system handle very long text selections?
- What if the OpenAI API is rate-limited or unavailable?
- How does the system handle documents with special formatting or code blocks?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement RAG-first architecture with all responses grounded in book content
- **FR-002**: System MUST support both global book queries and selection-specific queries with proper context separation
- **FR-003**: Users MUST be able to highlight text in the documentation and trigger contextual Q&A via floating action button
- **FR-004**: System MUST crawl Docusaurus /docs folder to read .md or .mdx files for content ingestion
- **FR-005**: System MUST chunk text using recursive character splitter and store in Qdrant Cloud with OpenAI embeddings
- **FR-006**: System MUST provide direct citations to original content with precise source locations
- **FR-007**: System MUST handle API keys via environment variables only (no hardcoding)
- **FR-008**: System MUST implement rate limiting to protect Free Tier usage
- **FR-009**: Frontend MUST integrate a floating chat widget into the Docusaurus layout
- **FR-010**: System MUST maintain full-stack modularity with clear API contracts between components
- **FR-011**: Backend MUST provide POST /query endpoint that accepts user questions and returns RAG-based answers
- **FR-012**: Backend MUST provide POST /query-selection endpoint that accepts both question and selected_text for focused grounding
- **FR-013**: System MUST implement JavaScript listener to capture window.getSelection().toString() when text is selected
- **FR-014**: Frontend MUST display "Answering based on selection..." indicator when in selection mode
- **FR-015**: System MUST provide ingestion script to process .md/.mdx files and upsert to Qdrant Cloud
- **FR-016**: System MUST implement authentication only for certain actions (like saving conversations)
- **FR-017**: System MUST respond to all requests within 2 seconds
- **FR-018**: System MUST gracefully degrade by providing general help when external services (OpenAI/Qdrant) are unavailable
- **FR-019**: System MUST retain user conversations for 30 days, then automatically delete
- **FR-020**: System MUST provide basic accessibility with keyboard navigation

### Key Entities

- **Document Chunk**: Represents a segment of content from the book with associated metadata (source URL, heading, embedding vector)
- **Chat Session**: Represents a conversation between user and the chatbot with history of messages
- **Query Request**: Represents a user's question with optional selected text context

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can ask questions about book content and receive accurate answers within 2 seconds
- **SC-002**: At least 90% of user questions receive relevant responses based on the book content
- **SC-003**: Users can select text and ask questions about it with 95% accuracy in contextual responses
- **SC-004**: The system can handle 1000+ document chunks in the Qdrant Cloud collection
- **SC-005**: Content ingestion completes successfully for all .md/.mdx files in the /docs directory
- **SC-006**: System maintains 95% availability even when external services experience intermittent issues