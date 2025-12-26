---
id: 1
title: Create Initial Constitution
stage: constitution
date: 2025-12-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Y.T
command: /sp.constitution
labels: [constitution,setup,initial]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
/sp.constitution

Project: AI-Native Book with Embedded RAG Chatbot

Core principles:
- Spec-driven development using Spec-Kit Plus
- Technical accuracy and reproducibility
- Clear writing for developers and CS students
- AI-native architecture (agents, RAG, cloud-native)
- No hallucinations; source-grounded answers only

Key standards:
- Book framework: Docusaurus
- Deployment: GitHub Pages
- Code generated via Claude Code
- RAG stack:
  - OpenAI Agents / ChatKit SDKs
  - FastAPI backend
  - Neon Serverless Postgres (metadata, sessions)
  - Qdrant Cloud Free Tier (vector storage)
- Chatbot must:
  - Answer from full book content
  - Answer using only user-selected text
  - Cite source sections

Constraints:
- All claims must be verifiable
- Code must be runnable and documented
- No hard-coded secrets
- Environment variables required
- Type-safe where applicable

Deliverables:
1. Fully written AI-generated book (Docusaurus)
2. Deployed GitHub Pages site
3. Embedded RAG chatbot inside the book
4. Complete specs for book, backend, RAG, and APIs

Success criteria:
- Successful GitHub Pages deployment
- Accurate, source-grounded chatbot answers
- Selected-text Q&A works correctly
- Zero hallucinations
- Specs match implementation
```

## Response snapshot

Created initial constitution for the AI-Native Book with Embedded RAG Chatbot project, incorporating all specified principles, standards, constraints, and deliverables. The constitution includes six core principles covering spec-driven development, technical accuracy, clear writing, AI-native architecture, source-grounded answers, and verifiable claims. Additional sections detail technology stack constraints, development workflow, and governance procedures.

## Outcome

- ✅ Impact: Created foundational project constitution document that will guide all future development
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Proceed with creating spec documents for the book, backend, RAG, and APIs
- 🧠 Reflection: Constitution properly captures all specified requirements and constraints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Begin creating feature specifications based on the constitution