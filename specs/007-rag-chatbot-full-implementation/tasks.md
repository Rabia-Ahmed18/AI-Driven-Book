---

description: "Task list for RAG Chatbot Backend & Frontend Implementation"
---

# Tasks: RAG Chatbot Backend & Frontend Implementation

**Input**: Design documents from `/specs/007-rag-chatbot-full-implementation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Using the structure from plan.md: `rag_backend/` directory with subdirectories for core modules

<!--
  ============================================================================
  Actual tasks generated based on user stories from spec.md and requirements from plan.md
  ============================================================================ 
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create project directory structure: rag_backend/, rag_backend/rag_core/, rag_backend/tests/
- [X] T002 [P] Create requirements.txt with FastAPI, uvicorn, OpenAI, qdrant-client, asyncpg, pydantic, python-dotenv
- [X] T003 Create .env.example with API key and connection string placeholders
- [X] T004 Create rag_backend/__init__.py and rag_backend/rag_core/__init__.py files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create base Pydantic models: ChatRequest, ChatResponse, IngestRequest, IngestResponse in rag_backend/models.py
- [X] T006 Create Qdrant client module: rag_backend/rag_core/qdrant_client.py with connection and retrieval logic
- [X] T007 Create Neon Postgres client module: rag_backend/rag_core/postgres_client.py with connection and metadata storage
- [X] T008 Setup environment configuration management in rag_backend/config.py
- [X] T009 Create RAG orchestration pipeline: rag_backend/rag_core/rag_pipeline.py with main logic
- [X] T010 Setup FastAPI application structure in rag_backend/main.py
- [X] T011 Configure CORS middleware in main.py to allow requests from Docusaurus frontend
- [X] T012 Set up error handling and logging infrastructure in rag_backend/utils/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: Backend Development (Sequential Sprints)

### Sprint B1: Project Setup & Environment

**Goal**: Establish basic backend project structure and core endpoints

- [X] T013 Generate requirements.txt with FastAPI, uvicorn, python-dotenv dependencies
- [X] T014 Implement the main.py file with basic FastAPI structure and CORS middleware
- [X] T015 Add the /health endpoint to main.py

### Sprint B2: Data Service Clients

**Goal**: Implement data clients for Qdrant and Neon Postgres

- [X] T016 Implement qdrant_client.py with an async client connection, create_collection, and search function
- [X] T017 Implement postgres_client.py with an async connection pool to Neon Postgres and a save_metadata function
- [X] T018 Define the Postgres table schema for document metadata (e.g., chunk_id, filename, source_text)

### Sprint B3: Ingestion Pipeline

**Goal**: Create functionality to ingest and process book content into vector database

- [X] T019 Implement a standalone ingestion script (or /ingest endpoint)
- [X] T020 Create a function to load and chunk Markdown/MDX files using a recursive text splitter
- [X] T021 Write a function to generate embeddings (text-embedding-3-small or similar) for each chunk
- [X] T022 Batch upload chunk vectors to Qdrant
- [X] T023 Save chunk metadata (ID, source file, etc.) to Neon Postgres

### Sprint B4: Core RAG Logic (/chat)

**Goal**: Implement the core RAG pipeline logic

- [X] T024 Implement the rag_pipeline.py logic
- [X] T025 Define the decision tree: Check for selected_context
- [X] T026 Implement Contextual Flow: If selected_context is present, bypass Qdrant and feed the selected text directly as the primary context to the LLM
- [X] T027 Implement General Flow: If no context, use Qdrant to retrieve k=5 chunks based on the user question
- [X] T028 Use the OpenAI Agents/ChatKit SDK to construct a system prompt instructing the model to answer only based on the provided context

### Sprint B5: Finalizing Backend Endpoints

**Goal**: Complete the backend API endpoints with error handling

- [X] T029 Complete the /chat endpoint in main.py, calling the RAG pipeline
- [X] T030 Ensure the response includes the source_citations (e.g., chunk IDs or document titles)
- [X] T031 Add robust error handling and logging to all critical functions

---

## Phase 4: Frontend Development (Sequential Sprints)

### Sprint F1: Component Scaffold & Styling

**Goal**: Create the basic React component structure for the chatbot

- [X] T032 Create a new React component, RAGChatbot.tsx, using the Docusaurus swizzle feature if necessary, and embed it as a fixed sidebar or footer button
- [X] T033 Design a basic chat interface (input box, history window, submit button)
- [X] T034 Implement state management for chat history and loading status

### Sprint F2: Text Selection Listener

**Goal**: Implement functionality to capture selected text on the page

- [X] T035 Implement a useEffect hook to attach a global selectionchange event listener to the document
- [X] T036 Use window.getSelection().toString() to capture highlighted text
- [X] T037 Create a state variable to store the selectedText
- [X] T038 Implement a dynamic "Ask about selection" button that only appears when text is selected

### Sprint F3: API Connection & Handling

**Goal**: Connect the frontend to backend API endpoints

- [X] T039 Implement an async function to make POST requests to the FastAPI /chat endpoint
- [X] T040 The function must conditionally send the selected_context or null based on the current component state
- [X] T041 Handle loading states and display the response/citations from the backend

### Sprint F4: Deployment Preparation

**Goal**: Prepare the frontend for integration with the existing Docusaurus theme

- [X] T042 Update the Docusaurus theme/layout to persistently render the RAGChatbot component
- [X] T043 Update docusaurus.config.js with any necessary component imports or routes
- [X] T044 Document the steps for proxying/deploying the FastAPI backend (e.g., using a platform like Render or Railway) and updating the frontend API URL to the deployed backend URL

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T045 [P] Add comprehensive logging throughout all modules for observability
- [X] T046 Add request validation and error responses following FastAPI best practices
- [X] T047 Add performance monitoring and timeout mechanisms
- [X] T048 [P] Add unit tests for all core modules
- [X] T049 Add documentation for all endpoints and public functions
- [X] T050 Test complete service integration with all endpoints
- [X] T051 Update .env.example with all required environment variables
- [X] T052 Add Dockerfile for containerized deployment
- [X] T053 Add README.md with setup and usage instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **Backend Sprints (Phase 3)**: Depends on Foundational phase completion
- **Frontend Sprints (Phase 4)**: Depends on Backend completion
- **Polish (Final Phase)**: Depends on all desired features being complete

### Sprint Dependencies

- **Sprint B1**: Can start after Foundational (Phase 2)
- **Sprint B2**: Depends on Sprint B1 completion
- **Sprint B3**: Depends on Sprint B2 completion
- **Sprint B4**: Depends on Sprint B3 completion
- **Sprint B5**: Depends on Sprint B4 completion
- **Sprint F1**: Depends on Backend completion
- **Sprint F2**: Depends on Sprint F1 completion
- **Sprint F3**: Depends on Sprint F2 completion
- **Sprint F4**: Depends on Sprint F3 completion

### Within Each Sprint

- Models before services
- Services before endpoints
- Core implementation before integration
- Sprint complete before moving to next sprint

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Tasks within the same sprint may run in parallel if they modify different files

---

## Implementation Strategy

### Sequential Delivery

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all sprints)
3. Complete Phase 3: Backend Sprints (B1 → B2 → B3 → B4 → B5)
4. Complete Phase 4: Frontend Sprints (F1 → F2 → F3 → F4)
5. Complete Phase 5: Polish & Cross-Cutting Concerns

### Sprint-by-Sprint Development

With each sprint:

1. Complete all tasks for the sprint
2. Test the sprint functionality independently
3. Validate against requirements before moving to next sprint
4. Each sprint adds value without breaking previous functionality

---

## Notes

- [P] tasks = different files, no dependencies
- Each sprint should be independently completable and testable
- Commit after each sprint or logical group
- Stop at any sprint checkpoint to validate functionality independently
- All functional requirements from spec are addressed (FR-001 through FR-006)