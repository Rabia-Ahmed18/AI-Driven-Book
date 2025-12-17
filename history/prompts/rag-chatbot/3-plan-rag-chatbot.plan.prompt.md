---
id: 3
title: Plan RAG Chatbot Implementation
stage: plan
date: 2025-01-14
surface: agent
model: gpt-4o
feature: rag-chatbot
branch: main
user: user
command: /sp.plan
labels: [plan,rag,chatbot,fastapi,qdrant,neon]
links:
  spec: /specs/006-rag-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/007-rag-chatbot-full-implementation/plan.md
 - specs/007-rag-chatbot-full-implementation/research.md
 - specs/007-rag-chatbot-full-implementation/data-model.md
 - specs/007-rag-chatbot-full-implementation/quickstart.md
 - specs/007-rag-chatbot-full-implementation/contracts/openapi.yaml
 - QWEN.md
tests:
 - null
---

## Prompt

```
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/bash/setup-plan.sh --json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/bash/update-agent-context.sh qwen`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.plan A. Backend Development (FastAPI, Qdrant, Neon Postgres, OpenAI)The backend implementation will be completed in 5 sequential sprints:SprintTask TitleDetailed Steps & Code FocusDependencies/ToolsB1Project Setup & Environment1. Generate requirements.txt and .env.example. 2. Implement the main.py file with basic FastAPI structure and CORS middleware. 3. Add the /health endpoint.FastAPI, Uvicorn, Python-dotenvB2Data Service Clients1. Implement qdrant_client.py with an async client connection, create_collection, and search function. 2. Implement postgres_client.py with an async connection pool to Neon Postgres and a save_metadata function. 3. Define the Postgres table schema for document metadata (e.g., chunk_id, filename, source_text).qdrant-client, asyncpgB3Ingestion Pipeline1. Implement a standalone ingestion script (or /ingest endpoint). 2. Create a function to load and chunk Markdown/MDX files using a recursive text splitter. 3. Write a function to generate embeddings (text-embedding-3-small or similar) for each chunk. 4. Batch upload chunk vectors to Qdrant. 5. Save chunk metadata (ID, source file, etc.) to Neon Postgres.OpenAI SDK, Text Splitters, Qdrant ClientB4Core RAG Logic (/chat)1. Implement the rag_pipeline.py logic. 2. Define the decision tree: Check for selected_context.  3. Contextual Flow: If selected_context is present, bypass Qdrant and feed the selected text directly as the primary context to the LLM. 4. General Flow: If no context, use Qdrant to retrieve $k=5$ chunks based on the user question. 5. Generation: Use the OpenAI Agents/ChatKit SDK to construct a system prompt instructing the model to answer only based on the provided context.OpenAI Agents/ChatKit SDK, qdrant_client.pyB5Finalizing Backend Endpoints1. Complete the /chat endpoint in main.py, calling the RAG pipeline. 2. Ensure the response includes the source_citations (e.g., chunk IDs or document titles). 3. Add robust error handling and logging to all critical functions.FastAPI, main.pyB. Frontend Development (Docusaurus, React, TypeScript)The frontend implementation will focus on user experience and integration into the existing Docusaurus theme.SprintTask TitleDetailed Steps & Code FocusDependencies/ToolsF1Component Scaffold & Styling1. Create a new React component, RAGChatbot.js (or .tsx), using the Docusaurus swizzle feature if necessary, and embed it as a fixed sidebar or footer button. 2. Design a basic chat interface (input box, history window, submit button). 3. Implement state management for chat history and loading status.React, Docusaurus Theme/LayoutF2Text Selection Listener1. Implement a useEffect hook to attach a global selectionchange event listener to the document. 2. Use window.getSelection().toString() to capture highlighted text. 3. Create a state variable to store the selectedText. 4. Implement a dynamic "Ask about selection" button that only appears when text is selected.React Hooks, JavaScript Selection APIF3API Connection & Handling1. Implement an async function to make POST requests to the FastAPI /chat endpoint. 2. The function must conditionally send the selected_context or null based on the current component state. 3. Handle loading states and display the response/citations from the backend.Fetch API / AxiosF4Deployment Preparation1. Update the Docusaurus theme/layout to persistently render the RAGChatbot component. 2. Update docusaurus.config.js with any necessary component imports or routes. 3. Document the steps for proxying/deploying the FastAPI backend (e.g., using a platform like Render or Railway) and updating the frontend API URL to the deployed backend URL.Docusaurus Config, Final Documentation

## Response snapshot

Successfully executed the implementation planning workflow for the RAG Chatbot project. Created the following artifacts:

1. Implementation plan (plan.md) with technical context, constitution check, and project structure
2. Research document (research.md) resolving all technology decisions and alternatives
3. Data model (data-model.md) defining backend and frontend data structures
4. API contracts (contracts/openapi.yaml) specifying all endpoints and schemas
5. Quickstart guide (quickstart.md) for new developers
6. Updated Qwen agent context (QWEN.md) with new technology stack information

The plan covers both backend (FastAPI, Qdrant, Neon Postgres) and frontend (React, Docusaurus) components as specified in the user requirements, following all constitution principles.

## Outcome

- ✅ Impact: Complete implementation plan for RAG chatbot with all required artifacts
- 🧪 Tests: N/A (planning phase)
- 📁 Files: Created 6 new files across the planning directory
- 🔁 Next prompts: Ready for task generation (/sp.tasks) to begin implementation
- 🧠 Reflection: Plan satisfies all constitution requirements and user specifications

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): Standard plan generation
- Next experiment (smallest change to try): Begin implementation with generated tasks