---
id: 12
title: RAG Book Chatbot Tasks
stage: tasks
date: 2025-12-24
surface: agent
model: Qwen
feature: rag-book-chatbot
branch: 012-rag-book-chatbot
user: User
command: /sp.tasks
labels: ["tasks", "rag", "chatbot", "book", "implementation"]
links:
  spec: ../specs/012-rag-book-chatbot/spec.md
  plan: ../specs/012-rag-book-chatbot/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - ../specs/012-rag-book-chatbot/tasks.md
tests:
 - null
---

## Prompt

```text
Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.

Context for task generation: Task Title: Develop and Embed Integrated RAG Chatbot in Published Book Task Description: Build a fully functional Retrieval-Augmented Generation (RAG) chatbot and embed it seamlessly within a published digital book (e.g., an interactive web-based or e-book format where the chatbot UI appears alongside or overlaid on the book content). Key Requirements: - The chatbot must use Retrieval-Augmented Generation to accurately answer user questions based on the book's content. - Utilize OpenAI's Agents SDK and ChatKit SDK for building the agent workflow, handling conversations, tool calls, streaming responses, and providing a customizable, embeddable chat UI (including features like chain-of-thought visualization, file attachments if needed, and interactive widgets). - Backend: Implement using FastAPI to serve the chatbot API endpoints, manage sessions, and integrate with OpenAI services. - Vector Database: Use Qdrant Cloud (Free Tier) for storing and retrieving embedded chunks of the book's content efficiently. - Metadata Storage: Use Neon Serverless Postgres database to store any necessary metadata, thread history, user sessions, or additional structured data (e.g., chunk references, user preferences). - Core Features: - Answer general questions about the entire book's content using RAG retrieval from the indexed book text. - Support contextual queries based ONLY on user-selected text: The chatbot must detect or receive highlighted/selected passages from the book UI and restrict retrieval/responses strictly to that selected text (implement via client-side passage of selected text as context or a dedicated tool/query mode). - Embedding: Chunk the full book text appropriately, generate embeddings (using OpenAI embeddings API), and upload to Qdrant. - UI Embedding: Use ChatKit's embeddable components (e.g., ChatKitPanel or widgets) to integrate the chat interface directly into the book's viewer/page (ensure it feels native, with options for positioning, theming to match the book design, and mobile responsiveness). - Security & Best Practices: Handle authentication if needed, rate limiting, error handling, and ensure responses are grounded in retrieved content to minimize hallucinations. - Testing: Thoroughly test with sample questions on full book context vs. selected text only, verify retrieval accuracy, and ensure smooth streaming/responsiveness. Deliverables: - Complete source code repository (backend FastAPI app, frontend embedding code if separate, ingestion script for book content). - Deployment instructions (e.g., for Vercel/Netlify for frontend, Render/Fly.io for FastAPI, with env vars for API keys, Neon/Qdrant connections). - Indexed book content in Qdrant (provide setup script). - Working demo of the embedded chatbot in a sample book page/viewer. - Documentation: README with architecture overview, setup steps, and how the selected-text feature works. Constraints: - Stick to free tiers where possible (Qdrant Cloud Free, Neon Serverless free limits). - Use latest stable OpenAI SDKs (Agents SDK for workflow/tools, ChatKit for UI embedding). Provide step-by-step plan, estimated timeline, and any questions/clarifications needed before starting implementation.
```

## Response snapshot

# Tasks: AI-Powered Book Assistant (RAG Chatbot)

**Feature**: AI-Powered Book Assistant (RAG Chatbot)  
**Branch**: `012-rag-book-chatbot`  
**Generated**: 2025-12-24  
**Based on**: `/specs/012-rag-book-chatbot/spec.md`, `/specs/012-rag-book-chatbot/plan.md`

## Implementation Strategy

**MVP Scope**: User Story 1 (Ask Questions About a Book) with basic ingestion capability to have content to query.

**Approach**: Implement features incrementally following the user story priorities (P1, P2, P3) with each story being independently testable.

**Parallel Execution Opportunities**: Backend and frontend components can be developed in parallel after foundational setup is complete.

## Dependencies

- **User Story 2** (Ingest New Books) must be implemented before **User Story 1** can be fully tested with real content
- **User Story 3** (View Chat History) depends on the chat functionality from **User Story 1**

## Phase 1: Setup Tasks

**Goal**: Initialize project structure and configure development environment

- [ ] T001 Create backend directory structure per plan
- [ ] T002 Create frontend directory structure per plan
- [ ] T003 [P] Set up Python virtual environment for backend
- [ ] T004 [P] Initialize Node.js project for frontend
- [ ] T005 [P] Install backend dependencies (FastAPI, Qdrant, Neon Postgres, OpenAI SDK)
- [ ] T006 [P] Install frontend dependencies (React, TypeScript)
- [ ] T007 Create initial configuration files and environment variable templates
- [ ] T008 Set up basic project configuration for both backend and frontend

## Phase 2: Foundational Tasks

**Goal**: Implement core infrastructure needed for all user stories

- [ ] T009 [P] Create database models for Book entity in backend/src/models/book.py
- [ ] T010 [P] Create database models for User entity in backend/src/models/user.py
- [ ] T011 [P] Create database models for ChatSession entity in backend/src/models/chat_session.py
- [ ] T012 [P] Create database models for Interaction entity in backend/src/models/interaction.py
- [ ] T013 [P] Set up database connection and configuration in backend/src/core/database.py
- [ ] T014 [P] Set up vector store connection and configuration in backend/src/core/vector_store.py
- [ ] T015 [P] Create database service for CRUD operations in backend/src/services/database_service.py
- [ ] T016 Create Pydantic schemas for API validation
- [ ] T017 [P] Set up API configuration and middleware in backend/src/core/config.py
- [ ] T018 [P] Implement text splitting utilities in backend/src/utils/text_splitter.py
- [ ] T019 [P] Implement input validation utilities in backend/src/utils/validators.py
- [ ] T020 [P] Set up basic API structure with FastAPI in backend/src/api/main.py

## Phase 3: User Story 1 - Ask Questions About a Book (P1)

**Goal**: Enable users to ask questions about a specific book with dual-context retrieval

**Independent Test Criteria**: User can input a question about a book and receive relevant answers with citations to specific sections of the book

- [ ] T021 [P] [US1] Create RAG service for dual-context retrieval in backend/src/services/rag_service.py
- [ ] T022 [P] [US1] Implement global context query logic in RAG service
- [ ] T023 [P] [US1] Implement selection context query logic in RAG service
- [ ] T024 [P] [US1] Create chat service for session management in backend/src/services/chat_service.py
- [ ] T025 [P] [US1] Implement chat endpoint in backend/src/api/v1/routes/chat.py
- [ ] T026 [P] [US1] Add chat endpoint to API router in backend/src/api/v1/api.py
- [ ] T027 [P] [US1] Implement citation generation logic in RAG service
- [ ] T028 [P] [US1] Create frontend chat window component in frontend/src/components/ChatWindow.tsx
- [ ] T029 [P] [US1] Create main RAG chatbot component in frontend/src/components/RagChatbot.tsx
- [ ] T030 [P] [US1] Implement API client for chat functionality in frontend/src/services/apiClient.ts
- [ ] T031 [P] [US1] Create chat state management hook in frontend/src/hooks/useChat.ts
- [ ] T032 [P] [US1] Implement text selection handler in frontend/src/components/TextSelectionHandler.tsx
- [ ] T033 [P] [US1] Create text selection hook in frontend/src/hooks/useTextSelection.ts
- [ ] T034 [US1] Integrate text selection functionality with chat component
- [ ] T035 [US1] Test dual-context retrieval with global queries
- [ ] T036 [US1] Test dual-context retrieval with selection queries
- [ ] T037 [US1] Test citation functionality in responses

## Phase 4: User Story 2 - Ingest New Books into the System (P2)

**Goal**: Enable content administrators to add new books to the system for querying

**Independent Test Criteria**: An administrator can upload or provide book text, which then becomes available for querying through the system

- [ ] T038 [P] [US2] Create ingestion service in backend/src/services/ingestion_service.py
- [ ] T039 [P] [US2] Implement text chunking logic in ingestion service
- [ ] T040 [P] [US2] Implement embedding generation and storage in ingestion service
- [ ] T041 [P] [US2] Create ingestion endpoint in backend/src/api/v1/routes/ingest.py
- [ ] T042 [P] [US2] Add ingestion endpoint to API router in backend/src/api/v1/api.py
- [ ] T043 [P] [US2] Implement book management endpoint in backend/src/api/v1/routes/books.py
- [ ] T044 [P] [US2] Add book management to API router in backend/src/api/v1/api.py
- [ ] T045 [US2] Test book ingestion with sample content
- [ ] T046 [US2] Test book retrieval and listing functionality
- [ ] T047 [US2] Verify ingested content is available for querying in User Story 1

## Phase 5: User Story 3 - View Chat History (P3)

**Goal**: Enable users to review their previous conversations with the book assistant

**Independent Test Criteria**: A user can access their chat history with a specific book and see previous questions and the system's responses

- [ ] T048 [P] [US3] Enhance ChatSession model with history-related functionality
- [ ] T049 [P] [US3] Enhance Interaction model with history-related functionality
- [ ] T050 [P] [US3] Implement session management functionality in chat service
- [ ] T051 [P] [US3] Create session endpoint in backend/src/api/v1/routes/books.py
- [ ] T052 [P] [US3] Implement interaction history endpoint in backend/src/api/v1/routes/books.py
- [ ] T053 [P] [US3] Add session management to API router in backend/src/api/v1/api.py
- [ ] T054 [P] [US3] Create chat history display component in frontend/src/components/ChatWindow.tsx
- [ ] T055 [US3] Test session creation and management
- [ ] T056 [US3] Test retrieval of chat history for a session
- [ ] T057 [US3] Test UI display of chat history

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Complete the implementation with proper error handling, security, and deployment readiness

- [ ] T058 [P] Implement comprehensive error handling across all services
- [ ] T059 [P] Add logging and monitoring capabilities
- [ ] T060 [P] Implement rate limiting for API endpoints
- [ ] T061 [P] Add input validation and sanitization
- [ ] T062 [P] Implement authentication for admin functions
- [ ] T063 [P] Add API documentation with OpenAPI/Swagger
- [ ] T064 [P] Create deployment configuration files
- [ ] T065 [P] Write comprehensive tests (unit, integration, e2e)
- [ ] T066 [P] Add proper error states and loading indicators to frontend
- [ ] T067 [P] Optimize frontend performance and responsiveness
- [ ] T068 [P] Create documentation for integrating with Docusaurus
- [ ] T069 [P] Set up environment-specific configurations
- [ ] T070 Final integration testing and bug fixes

## Parallel Execution Examples

**Parallel Tasks Within User Stories**:
- Backend API development [US1]: T021-T027 can run parallel to Frontend component development [US1]: T028-T033
- Ingestion service [US2]: T038-T042 can run parallel to Book management [US2]: T043-T044
- Frontend components [US3]: T054 can run parallel to Backend services [US3]: T048-T053

**Parallel Tasks Across User Stories** (after foundational tasks complete):
- User Story 2 (Ingestion) development can run parallel to User Story 3 (History) development
- Both can run parallel to continued User Story 1 (Chat) refinements

## Outcome

- ✅ Impact: Created comprehensive task breakdown for the RAG chatbot feature with 70 specific, actionable tasks organized by user story
- 🧪 Tests: N/A (Task breakdown phase)
- 📁 Files: Created tasks.md with detailed task breakdown following checklist format
- 🔁 Next prompts: Ready for implementation of individual tasks
- 🧠 Reflection: Tasks are well-organized by user stories with clear dependencies and parallel execution opportunities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin with foundational setup tasks (T001-T008)