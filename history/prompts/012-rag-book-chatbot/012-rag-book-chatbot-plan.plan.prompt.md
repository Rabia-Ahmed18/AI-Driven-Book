---
id: 12
title: RAG Book Chatbot Plan
stage: plan
date: 2025-12-24
surface: agent
model: Qwen
feature: rag-book-chatbot
branch: 012-rag-book-chatbot
user: User
command: /sp.plan
labels: ["plan", "rag", "chatbot", "book", "architecture"]
links:
  spec: ../specs/012-rag-book-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - ../specs/012-rag-book-chatbot/plan.md
 - ../specs/012-rag-book-chatbot/research.md
 - ../specs/012-rag-book-chatbot/data-model.md
 - ../specs/012-rag-book-chatbot/quickstart.md
 - ../specs/012-rag-book-chatbot/contracts/openapi.yaml
tests:
 - null
---

## Prompt

```text
/sp.plan Project Title: Integrated RAG Chatbot for Digital Book Platform

Instructions: Generate a phased development plan for building a RAG chatbot using FastAPI, Neon Postgres, Qdrant Cloud, and OpenAI ChatKit. The plan must cover the full lifecycle from data ingestion to frontend embedding.

Phase 1: Infrastructure Setup

Provision Neon Serverless Postgres (schema for users, conversations, and feedback).

Configure Qdrant Cloud collection with appropriate vector dimensions (e.g., 1536 for OpenAI text-embedding-3-small).

Phase 2: Ingestion Pipeline

Create a script to parse the book (PDF/Markdown) into semantic chunks.

Implement metadata tagging (chapter, page number) for each chunk.

Upsert vectors into Qdrant.

Phase 3: Backend API Development

Develop FastAPI endpoints: /chat (general RAG) and /chat/selection (context-constrained RAG).

Implement a "Hybrid Retrieval" logic: Use Qdrant for book-wide queries and a direct string-injection for "selected text" queries.

Integrate OpenAI ChatKit to manage conversation state and system personas.

Phase 4: Frontend Integration

Build a React/Vue floating chat widget for the bottom-right corner.

Implement the "Selection Listener" logic: detect highlighted text in the book UI and pass it to the chatbot context.

Phase 5: Evaluation & Deployment

Set up basic RAG evaluation (relevancy checks).

Deploy FastAPI to a cloud provider (e.g., Vercel or Railway) and connect to the production Neon/Qdrant instances.

Output Format: Provide the plan as a checklist with technical milestones for each phase.

Understanding the RAG Flow
To help you visualize how these technologies interact within your project, here is the architectural flow:

Technical Highlights of your Stack
Neon Postgres: Will store your "Conversation Memory," allowing the bot to remember what the user asked three questions ago.

Qdrant: Acts as the "Digital Library Card Catalog," finding the exact page of your book relevant to a query in milliseconds.

FastAPI: Serves as the "Traffic Controller," routing user clicks and text highlights to the correct AI logic.
```

## Response snapshot

# Implementation Plan: AI-Powered Book Assistant (RAG Chatbot)

**Branch**: `012-rag-book-chatbot` | **Date**: 2025-12-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/012-rag-book-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Retrieval-Augmented Generation (RAG) system integrated into a digital book platform. The system will provide dual-context retrieval allowing both global book queries and selection-specific queries. The backend will use FastAPI to handle API requests, with Qdrant Cloud as the vector database for storing and querying text embeddings, and Neon Serverless Postgres for user data and session management. The system will integrate with OpenAI SDK for response generation, with a React-based frontend component for user interaction.

## Technical Context

**Language/Version**: Python 3.11, TypeScript for frontend components
**Primary Dependencies**: FastAPI, Qdrant, Neon Postgres, OpenAI SDK, React
**Storage**: Qdrant Cloud (vector database) for embeddings, Neon Serverless Postgres (relational database) for user/session data
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application with Docusaurus integration
**Project Type**: Web (backend + frontend components)
**Performance Goals**: Responses within 5 seconds (as per spec), handle 1000+ concurrent users
**Constraints**: <200ms p95 for internal API calls, resource usage optimized for free tier limitations
**Scale/Scope**: Support multiple books, 10k+ users, 1M+ text chunks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. RAG-First Architecture**: PASS - All functionality will be built around RAG foundation with responses grounded in book content
**II. Full-Stack Modularity**: PASS - Clear separation between FastAPI backend, Qdrant vector store, Neon Postgres, and React frontend
**III. Test-First**: PASS - All components will follow TDD methodology with unit, integration, and E2E tests
**IV. Content Context Integrity**: PASS - Strict separation maintained between book-wide Q&A and selected text contextual Q&A
**V. Source Transparency**: PASS - All responses will include citations to original content with source locations
**VI. Deployment-First Design**: PASS - Code will be production-ready with environment variable configuration

## Project Structure

### Documentation (this feature)

```text
specs/012-rag-book-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── book.py          # Book entity and schema
│   │   ├── chat_session.py  # Chat session entity and schema
│   │   ├── interaction.py   # Interaction entity and schema
│   │   └── user.py          # User entity and schema
│   ├── services/
│   │   ├── ingestion_service.py     # Ingestion logic
│   │   ├── rag_service.py           # RAG operations
│   │   ├── chat_service.py          # Chat session management
│   │   └── database_service.py      # Database operations
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   │   ├── ingest.py        # Ingestion endpoints
│   │   │   │   ├── chat.py          # Chat endpoints
│   │   │   │   └── books.py         # Book management endpoints
│   │   │   └── api.py               # API router
│   │   └── main.py                  # FastAPI application
│   ├── core/
│   │   ├── config.py        # Configuration and settings
│   │   ├── database.py      # Database connection and setup
│   │   └── vector_store.py  # Vector store connection and setup
│   └── utils/
│       ├── text_splitter.py # Text chunking utilities
│       └── validators.py    # Input validation utilities
└── tests/
    ├── unit/
    │   ├── models/
    │   ├── services/
    │   └── api/
    ├── integration/
    │   ├── api/
    │   └── database/
    └── contract/
        └── openapi.json     # API contract

frontend/
├── src/
│   ├── components/
│   │   ├── RagChatbot.tsx     # Main chatbot component
│   │   ├── ChatWindow.tsx     # Chat interface
│   │   ├── TextSelectionHandler.tsx  # Text selection logic
│   │   └── FloatingButton.tsx # Floating chat button
│   ├── hooks/
│   │   ├── useChat.ts         # Chat state management
│   │   └── useTextSelection.ts # Text selection hook
│   ├── services/
│   │   └── apiClient.ts       # API communication layer
│   └── types/
│       └── index.ts           # Type definitions
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
        └── chatbot.e2e.ts

docs/
└── chatbot-integration.md    # Documentation for integrating chatbot into Docusaurus
```

**Structure Decision**: Web application structure with separate backend and frontend directories to maintain clear separation of concerns. The backend uses FastAPI with a modular structure following the principles in the constitution. The frontend is a React application that can be integrated into the Docusaurus documentation site.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|

## Outcome

- ✅ Impact: Created comprehensive implementation plan for the RAG chatbot feature with detailed architecture, data models, and project structure
- 🧪 Tests: N/A (Planning phase)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts/openapi.yaml
- 🔁 Next prompts: Ready for task breakdown with /sp.tasks
- 🧠 Reflection: The plan follows the constitution principles and provides a clear roadmap for implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation of the ingestion service