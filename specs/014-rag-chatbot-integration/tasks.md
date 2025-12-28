---

description: "Task list for RAG Chatbot Integration feature implementation"
---

# Tasks: RAG Chatbot Integration

**Input**: Design documents from `/specs/014-rag-chatbot-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend/ and frontend/ directories per implementation plan
- [X] T002 Initialize Python project with FastAPI, Qdrant, OpenAI dependencies in backend/requirements.txt
- [X] T003 [P] Initialize TypeScript/React project with Docusaurus dependencies in frontend/package.json
- [X] T004 [P] Configure linting and formatting tools for both backend and frontend
- [X] T005 Setup environment configuration management with .env.example file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Setup Qdrant Cloud connection and collection initialization in backend/src/core/qdrant.py
- [X] T007 [P] Implement Qdrant vector storage models for document chunks in backend/src/models/chunk.py
- [X] T008 [P] Setup API routing and middleware structure in backend/src/main.py
- [X] T009 Create base data models that all stories depend on (Document, Chunk, ChatSession) in backend/src/models/
- [X] T010 Configure error handling and logging infrastructure in backend/src/core/
- [X] T011 Setup environment configuration management with pydantic settings in backend/src/core/config.py
- [X] T012 Implement rate limiting middleware to protect Free Tier usage in backend/src/middleware/rate_limit.py
- [X] T013 Create base services for OpenAI integration and embedding generation in backend/src/services/embedding_service.py
- [X] T014 [P] Create base RAG service in backend/src/services/rag_service.py
- [X] T015 Setup ingestion script structure in ingestion_script.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Global Book Q&A (Priority: P1) 🎯 MVP

**Goal**: Enable users to ask questions about book content and receive relevant answers with proper citations

**Independent Test**: Can be fully tested by asking questions about the book content and verifying that the responses are accurate and properly cited.

### Implementation for User Story 1

- [X] T016 [P] [US1] Create Chat Session model in backend/src/models/chat_session.py
- [X] T017 [P] [US1] Create Chat Message model in backend/src/models/chat_message.py
- [X] T018 [P] [US1] Create Query Request model in backend/src/models/query_request.py
- [X] T019 [P] [US1] Create Query Response model in backend/src/models/query_response.py
- [X] T020 [US1] Implement Chat Session service in backend/src/services/chat_session_service.py
- [X] T021 [US1] Implement RAG query service in backend/src/services/rag_service.py (enhance existing)
- [X] T022 [US1] Implement POST /query endpoint in backend/src/api/query_router.py
- [X] T023 [US1] Implement POST /chat endpoint in backend/src/api/chat_router.py
- [X] T024 [US1] Add validation and error handling for global Q&A
- [X] T025 [US1] Add logging for user story 1 operations
- [X] T026 [US1] Create basic ChatWidget component in frontend/src/components/ChatWidget.js
- [X] T027 [US1] Create API service for chat interactions in frontend/src/services/chat_api.js
- [X] T028 [US1] Implement basic UI for chat widget in frontend/src/components/ChatWidget.js
- [X] T029 [US1] Add loading states and error handling to ChatWidget
- [X] T030 [US1] Connect ChatWidget to backend API endpoints

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Selection-Based Q&A (Priority: P2)

**Goal**: Enable users to select specific text and ask questions about it to get more focused answers

**Independent Test**: Can be fully tested by selecting text in the book, asking a question about it, and verifying that the response is contextually relevant to the selected text.

### Implementation for User Story 2

- [X] T031 [P] [US2] Create text selection hook in frontend/src/hooks/useTextSelection.js
- [X] T032 [US2] Implement floating action button in frontend/src/components/SelectionButton.js
- [X] T033 [US2] Enhance ChatWidget to handle selection mode in frontend/src/components/ChatWidget.js
- [X] T034 [US2] Update POST /query endpoint to accept selected_text parameter
- [X] T035 [US2] Implement POST /query-selection endpoint in backend/src/api/query_router.py
- [X] T036 [US2] Update RAG service to handle selected text context in backend/src/services/rag_service.py
- [X] T037 [US2] Add "Answering based on selection..." indicator to ChatWidget
- [X] T038 [US2] Add validation and error handling for selection-based Q&A
- [X] T039 [US2] Add logging for user story 2 operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Content Ingestion (Priority: P3)

**Goal**: Automatically ingest new or updated content from the Docusaurus docs so the chatbot has access to current information

**Independent Test**: Can be fully tested by running the ingestion script and verifying that new/updated content is properly chunked and stored in Qdrant Cloud.

### Implementation for User Story 3

- [X] T040 [P] [US3] Create document parsing service in backend/src/services/document_parser.py
- [X] T041 [US3] Implement text chunking service using RecursiveCharacterTextSplitter in backend/src/services/chunking_service.py
- [X] T042 [US3] Enhance ingestion script to process .md/.mdx files from docs directory
- [X] T043 [US3] Implement upsert logic for Qdrant Cloud in backend/src/services/qdrant_service.py
- [X] T044 [US3] Add embedding generation to ingestion pipeline in backend/src/services/embedding_service.py
- [X] T045 [US3] Implement POST /ingest endpoint in backend/src/api/ingest_router.py
- [X] T046 [US3] Add metadata extraction for source URL and heading in backend/src/services/document_parser.py
- [X] T047 [US3] Add validation and error handling for content ingestion
- [X] T048 [US3] Add logging for user story 3 operations
- [X] T049 [US3] Add progress tracking to ingestion script

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T050 [P] Add authentication for saving conversations in backend/src/api/auth_router.py
- [X] T051 [P] Add data retention policy for conversations (30 days) in backend/src/services/chat_session_service.py
- [X] T052 Add basic accessibility with keyboard navigation to ChatWidget
- [X] T053 Add graceful degradation when external services unavailable in backend/src/services/rag_service.py
- [X] T054 [P] Add health check endpoint in backend/src/api/health_router.py
- [X] T055 Add CORS configuration for Vercel frontend in backend/src/main.py
- [X] T056 [P] Add source attribution to responses in backend/src/services/rag_service.py
- [X] T057 Update README with deployment instructions
- [X] T058 Add prompt engineering for OpenAI Agent in backend/src/core/prompts.py
- [X] T059 [P] Add unit tests for backend services in backend/tests/
- [X] T060 [P] Add integration tests for API endpoints in backend/tests/
- [X] T061 Add e2e tests for frontend components in frontend/tests/
- [X] T062 Run quickstart.md validation

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
T016 [P] [US1] Create Chat Session model in backend/src/models/chat_session.py
T017 [P] [US1] Create Chat Message model in backend/src/models/chat_message.py
T018 [P] [US1] Create Query Request model in backend/src/models/query_request.py
T019 [P] [US1] Create Query Response model in backend/src/models/query_response.py
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
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence