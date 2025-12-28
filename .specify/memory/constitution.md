<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0 (minor update with principle expansion)
Added sections: Enhanced RAG-First Architecture, Docusaurus Integration, Rate Limiting
Removed sections: None
Modified principles: 
  - Full-Stack Modularity: Updated to include Docusaurus frontend
  - Content Context Integrity: Enhanced with selection-aware context requirements
  - Infrastructure Constraints: Updated for Qdrant Cloud and Docusaurus
Templates requiring updates: ✅ updated - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Integrated Book-Content RAG Chatbot Constitution

## Core Principles

### I. RAG-First Architecture
All chatbot functionality must be built around a Retrieval-Augmented Generation foundation. Every response must be grounded in content from the book's documents. No standalone generative responses without source verification. This ensures factual accuracy and maintainability of the knowledge base. The system must crawl the Docusaurus /docs folder or parse the generated sitemap.xml, with text chunked and stored in Qdrant Cloud with metadata including the source URL/heading.

### II. Full-Stack Modularity
Backend (FastAPI), Vector Database (Qdrant Cloud), and Frontend (Docusaurus/React) must operate as clearly separated modules. Each module must be independently testable, configurable, and deployable. Clear API contracts between layers with defined error handling protocols. The system must support both global context (similarity search across entire Qdrant collection) and selection-aware context (accepting highlighted text as prioritized context window).

### III. Test-First (NON-NEGOTIABLE)
All components must follow TDD methodology: Tests written → Requirements validated → Tests fail → Then implement. Red-Green-Refactor cycle strictly enforced. Unit tests for all core functions, integration tests for API endpoints, E2E tests for complete Q&A flows.

### IV. Content Context Integrity
The system must maintain strict separation between book-wide Q&A and selected text contextual Q&A. Selected text context must be transmitted unmodified to the RAG pipeline, with clear provenance tracking from selection to response generation. When a user highlights text in the book, the chatbot must accept this selected string as a prioritized context window to answer specific questions about that passage.

### V. Source Transparency
Every response must include direct citations to original content with precise source locations (filename, section heading, or chunk ID). Responses without verifiable sources are invalid. Users must be able to trace any generated content back to the original book material.

### VI. Deployment-First Design
Code must be production-ready from inception. Configuration via environment variables only. Deployment targets Vercel for frontend, cloud services for backend. All dependencies must be compatible with deployment constraints. API keys for OpenAI and Qdrant must be handled via environment variables with no hardcoding allowed.

## Technology Stack Requirements

### Backend Components
- FastAPI (Python) must serve as the REST API layer with typed endpoints
- Vector storage handled exclusively through Qdrant Cloud Free Tier
- OpenAI Agents/ChatKit SDKs for orchestrating the RAG pipeline
- Rate limiting implementation to protect Free Tier usage

### Frontend Integration
- Docusaurus (React) components must integrate seamlessly within documentation site
- Text selection detection and capture functionality required
- Floating chat widget implementation with "Ask AI" tooltip for selected text
- Real-time chat interface with loading indicators and error states
- Responsive design that works well on documentation pages

### Infrastructure Constraints
- All API keys and credentials stored in environment variables (never hard-coded)
- Error handling for service unavailability, rate limiting, and timeout conditions
- Logging and monitoring capabilities built into all components
- Resource usage optimized for Qdrant Cloud Free Tier limitations
- Docusaurus-specific integration for injecting chat components via src/theme/Root.js or custom Navbar item

## Feature Implementation Standards

### Book-Wide Q&A Capability
- Ingestion pipeline must process all Markdown/MDX files from Docusaurus docs directory
- Text splitting with recursive character text splitter for optimal context chunks
- Embedding model (text-embedding-3-small) must be used for vector generation
- Search functionality must return relevant results from entire book corpus

### Selected Text Contextual Q&A
- Frontend must detect user text selections with precision
- Context preservation must maintain original formatting and meaning
- Endpoint must accept optional selected_context parameter
- Responses must be strictly scoped to provided context with clear attribution

### Content Ingestion Strategy
- Standalone ingestion script (ingestion_script.py) or dedicated FastAPI endpoint
- Parsing must handle Docusaurus-specific MDX features correctly
- Chunking strategy must optimize for both precision and recall
- Metadata tracking must map chunks back to source locations with URL/heading information

### Quality Assurance Measures
- Comprehensive error handling for API failures, database issues, and LLM limitations
- Response validation to ensure all answers ground in source material
- Timeout and retry mechanisms for external service calls
- Graceful degradation when context is insufficient for answering

## Governance
All contributions must verify compliance with these principles. Major architectural changes require team consensus. Code reviews must validate adherence to modularity, source transparency, and deployment readiness. Breaking changes to core APIs require migration plans. New features must enhance rather than compromise the core RAG functionality.

Version: 1.1.0 | Ratified: 2025-01-14 | Last Amended: 2025-12-28