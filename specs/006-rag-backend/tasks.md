---

description: "Task list for RAG Backend Microservice implementation"
---

# Tasks: RAG Backend Microservice

**Input**: Design documents from `/specs/006-rag-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: The feature specification does not explicitly request test tasks, but we will include them for best practice.

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

- [ ] T001 [P] Create project directory structure: rag_backend/, rag_backend/rag_core/, rag_backend/tests/
- [ ] T002 [P] Create requirements.txt with FastAPI, uvicorn, OpenAI, qdrant-client, asyncpg, pydantic, python-dotenv
- [ ] T003 Create .env.example with API key and connection string placeholders
- [ ] T004 Create rag_backend/__init__.py and rag_backend/rag_core/__init__.py files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create base Pydantic models: ChatRequest, ChatResponse, IngestRequest, IngestResponse in rag_backend/models.py
- [ ] T006 Create Qdrant client module: rag_backend/rag_core/qdrant_client.py with connection and retrieval logic
- [ ] T007 Create Neon Postgres client module: rag_backend/rag_core/postgres_client.py with connection and metadata storage
- [ ] T008 Setup environment configuration management in rag_backend/config.py
- [ ] T009 Create RAG orchestration pipeline: rag_backend/rag_core/rag_pipeline.py with main logic
- [ ] T010 Setup FastAPI application structure in rag_backend/main.py
- [ ] T011 Configure CORS middleware in main.py to allow requests from Docusaurus frontend
- [ ] T012 Set up error handling and logging infrastructure in rag_backend/utils/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic RAG Queries (Priority: P1) 🎯 MVP

**Goal**: Implement core functionality for users to ask questions about book content and receive answers with source citations

**Independent Test**: The system can receive a question, retrieve relevant chunks from the database, generate a response using the LLM, and return the answer with source citations.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for /chat endpoint in rag_backend/tests/contract/test_chat_endpoint.py
- [ ] T014 [P] [US1] Unit test for RAG pipeline in rag_backend/tests/unit/test_rag_pipeline.py
- [ ] T015 [P] [US1] Integration test for /chat endpoint in rag_backend/tests/integration/test_chat_integration.py

### Implementation for User Story 1

- [ ] T016 [US1] Implement /chat endpoint in rag_backend/main.py that accepts ChatRequest
- [ ] T017 [US1] Enhance rag_pipeline.py to handle selected_context parameter for contextual queries
- [ ] T018 [US1] Implement vector retrieval logic in qdrant_client.py to fetch relevant chunks
- [ ] T019 [US1] Implement source citation generation in rag_pipeline.py
- [ ] T020 [US1] Ensure context-aware querying when selected_context is provided (Requirement FR-003)
- [ ] T021 [US1] Return ChatResponse with answer and source citations from /chat endpoint

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Content Ingestion (Priority: P2)

**Goal**: Implement functionality to trigger the ingestion of new book content into the RAG system

**Independent Test**: The system can accept an ingestion request via the /ingest endpoint and successfully process book content into vector embeddings stored in Qdrant.

### Tests for User Story 2

- [ ] T022 [P] [US2] Contract test for /ingest endpoint in rag_backend/tests/contract/test_ingest_endpoint.py
- [ ] T023 [P] [US2] Unit test for ingestion logic in rag_backend/tests/unit/test_ingestion.py
- [ ] T024 [P] [US2] Integration test for /ingest endpoint in rag_backend/tests/integration/test_ingest_integration.py

### Implementation for User Story 2

- [ ] T025 [US2] Create ingestion-specific data models in rag_backend/models.py if needed
- [ ] T026 [US2] Implement /ingest endpoint in rag_backend/main.py that accepts IngestRequest
- [ ] T027 [US2] Implement content processing and embedding logic in rag_backend/rag_core/rag_pipeline.py
- [ ] T028 [US2] Implement vector storage in Qdrant via qdrant_client.py (Requirement FR-004)
- [ ] T029 [US2] Implement metadata storage in Neon Postgres via postgres_client.py (Requirement FR-005)
- [ ] T030 [US2] Return IngestResponse confirming successful content ingestion from /ingest endpoint

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Health Monitoring (Priority: P3)

**Goal**: Implement health monitoring functionality for operations engineers to monitor service availability

**Independent Test**: The system can respond to health check requests via the /health endpoint.

### Tests for User Story 3

- [ ] T031 [P] [US3] Unit test for health check endpoint in rag_backend/tests/unit/test_health.py
- [ ] T032 [P] [US3] Contract test for /health endpoint in rag_backend/tests/contract/test_health_endpoint.py

### Implementation for User Story 3

- [ ] T033 [US3] Implement /health endpoint in rag_backend/main.py
- [ ] T034 [US3] Return status response from /health endpoint with "ok" status (Requirement FR-006)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T035 [P] Add comprehensive logging throughout all modules for observability
- [ ] T036 Add request validation and error responses following FastAPI best practices
- [ ] T037 Add performance monitoring and timeout mechanisms
- [ ] T038 [P] Add unit tests for all core modules
- [ ] T039 Add documentation for all endpoints and public functions
- [ ] T040 Test complete service integration with all endpoints
- [ ] T041 Update .env.example with all required environment variables
- [ ] T042 Add Dockerfile for containerized deployment
- [ ] T043 Add README.md with setup and usage instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for /chat endpoint in rag_backend/tests/contract/test_chat_endpoint.py"
Task: "Unit test for RAG pipeline in rag_backend/tests/unit/test_rag_pipeline.py"
Task: "Integration test for /chat endpoint in rag_backend/tests/integration/test_chat_integration.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Implement /chat endpoint in rag_backend/main.py"
Task: "Enhance rag_pipeline.py to handle selected_context parameter"
Task: "Implement vector retrieval logic in qdrant_client.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All functional requirements from spec are addressed (FR-001 through FR-006)