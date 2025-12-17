---
id: 2
title: Generate RAG Backend Tasks
stage: tasks
date: 2025-01-14
surface: agent
model: gpt-4o
feature: rag-backend
branch: main
user: user
command: /sp.tasks
labels: [tasks,rag,backend,fastapi]
links:
  spec: /specs/006-rag-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/006-rag-backend/tasks.md
 - specs/006-rag-backend/spec.md
 - specs/006-rag-backend/plan.md
tests:
 - null
---

## Prompt

```
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: Component: FastAPI RAG Backend MicroserviceGoal: Define the complete structure, endpoints, and initial implementation details for the core RAG microservice using FastAPI. This service will handle all book content query logic.Dependencies: Must utilize OpenAI Agents/ChatKit SDK, Qdrant Cloud Client, and Asyncpg or similar library for Neon Serverless Postgres interaction.1. Project Structure and InitializationThe AI must generate the following files and directory structure:/rag_backend/main.py: The core FastAPI application.requirements.txt: List all Python dependencies (fastapi, uvicorn, openai, qdrant-client, asyncpg, pydantic, python-dotenv, etc.)..env.example: A template for environment variables (API keys, connection strings).rag_core/qdrant_client.py: Module for Qdrant connection and retrieval logic.postgres_client.py: Module for Neon Postgres connection and metadata storage.rag_pipeline.py: Module containing the main RAG orchestration logic using OpenAI/ChatKit.2. Required Endpoints in main.pyEndpointMethodPurposeInput (Body)Output (JSON)/chatPOSTPrimary RAG Query endpoint.ChatRequestChatResponse/ingestPOSTIngestion trigger for book content.IngestRequestIngestResponse/healthGETSimple health check.None{"status": "ok"}3. Data Models (Pydantic)The AI must define the following Pydantic models for request/response bodies:ChatRequest:question: str (The user's question).selected_context: Optional[str] (The highlighted text from the Docusaurus page. Default: None).ChatResponse:answer: str (The final LLM-generated answer).source_citations: List[str] (List of document/chunk IDs or titles retrieved from Qdrant/Postgres).4. Logic Flow for /chat Endpoint (Core Logic)The /chat function in main.py must implement this high-level logic:Check selected_context:If selected_context is provided: The RAG pipeline must treat the selected_context as the primary, pre-retrieved context. The question should be answered strictly based on this text, with minimal reliance on Qdrant, if possible. (This satisfies Requirement 2).If selected_context is NOT provided (general Q&A): The pipeline proceeds to Step 2.Vector Retrieval: Use the question to query the Qdrant database to retrieve top-k (e.g., $k=5$) relevant text chunks from the book content.Context Construction: Combine the question and the retrieved chunks (and/or selected_context) into a single, cohesive prompt.LLM Generation: Send the context to the OpenAI Agents/ChatKit for generation. The LLM's instruction must be to answer based only on the provided context.Response: Return the generated answer and the list of source citations from the retrieved chunks/context.5. Backend Configuration StandardsImplement CORS middleware in FastAPI to allow requests from the Docusaurus frontend (running on GitHub Pages).Use uvicorn for running the service.

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Response snapshot

Successfully generated tasks.md for the RAG Backend Microservice feature. The tasks.md file includes:

- Phase 1: Setup tasks (project initialization)
- Phase 2: Foundational tasks (blocking prerequisites for all user stories)
- Phase 3: User Story 1 tasks (Basic RAG Queries - P1 priority)
- Phase 4: User Story 2 tasks (Content Ingestion - P2 priority) 
- Phase 5: User Story 3 tasks (Health Monitoring - P3 priority)
- Phase 6: Polish & cross-cutting concerns

All tasks follow the required checklist format with proper IDs, story labels, and file paths. The tasks align with the requirements specified in the user input, including all endpoints, data models, and implementation details for the FastAPI RAG backend.

## Outcome

- ✅ Impact: Created comprehensive task breakdown for RAG backend implementation
- 🧪 Tests: Included test tasks for all user stories as best practice
- 📁 Files: Created specs/006-rag-backend/tasks.md with 43 executable tasks
- 🔁 Next prompts: Implementation can proceed following task breakdown
- 🧠 Reflection: Tasks organized by user story priority with clear dependencies

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): Standard task generation
- Next experiment (smallest change to try): Begin implementation with Phase 1 tasks