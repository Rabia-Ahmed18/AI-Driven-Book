---
id: 1
title: Update RAG Chatbot Constitution
stage: constitution
date: 2025-01-14
surface: agent
model: gpt-4o
feature: rag-chatbot
branch: main
user: user
command: /sp.constitution
labels: [constitution,rag,chatbot,docusaurus]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

```
$ARGUMENTS
```

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

## Response snapshot

I have successfully created and updated the project constitution for the Integrated Book-Content RAG Chatbot project. The constitution now includes:

- Six core principles covering RAG-first architecture, modularity, test-first approach, content context integrity, source transparency, and deployment-first design
- Detailed technology stack requirements for backend, frontend, and infrastructure components
- Feature implementation standards for Q&A capabilities, selected text contextual queries, content ingestion, and quality assurance
- Governance guidelines for contributions and code reviews

The constitution is saved at `.specify/memory/constitution.md` with version 1.0.0, and includes a Sync Impact Report at the top of the file noting that templates may require updates.

## Outcome

- ✅ Impact: Created complete project constitution aligning with RAG chatbot requirements
- 🧪 Tests: N/A (documentation update)
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive principles
- 🔁 Next prompts: Feature implementation can now follow constitution guidelines
- 🧠 Reflection: The constitution captures all specified technology stack and feature requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): Standard constitution generation
- Next experiment (smallest change to try): Begin feature specification based on constitution