# Implementation Plan: RAG Backend-Frontend Integration

**Feature**: 2-rag-frontend-integration
**Created**: 2025-12-25
**Status**: Draft
**Plan Version**: 1.0

## Technical Context

**Backend**: FastAPI agent backend from Spec-3 (existing)
**Frontend**: Existing frontend application (location needs clarification)
**Communication Protocol**: REST API calls (as specified in FR-006)
**Development Environment**: Local only (as per constraints)
**API Format**: JSON for request/response (standard web components per FR-007)
**Frontend Framework**: Docusaurus/React (React-based static site generator)
**Backend URL**: localhost:8000 (as defined in backend/api/retrieval_api.py:382)
**Existing API Endpoints**:
- GET /retrieval/collections: Get collection information
- POST /retrieval/query: Execute similarity search (retrieval only)
- POST /retrieval/validate: Run validation on queries
**Additional Required Endpoints**:
- POST /agent/query: Process user queries through RAG agent (to be implemented)
**Frontend Components**: Need to create new React components for query interface and response display

## Constitution Check

**Principle 1**: Library-First - [Check status: PASS]
- The RAG agent functionality already exists as a reusable library in agent.py and can be integrated via API

**Principle 2**: CLI Interface - [Check status: NOT APPLICABLE]
- This is a web API integration, not a CLI-focused feature

**Principle 3**: Test-First (NON-NEGOTIABLE) - [Check status: PASS]
- The existing agent has test functions in test_agent.py that can be extended for API testing

**Principle 4**: Integration Testing - [Check status: PASS]
- The integration will require testing of the frontend-backend communication and API contracts

**Principle 5**: Observability - [Check status: PASS]
- The existing agent already includes logging and timing metrics that will be exposed through the API

**Principle 6**: Simplicity - [Check status: PASS]
- The approach extends existing architecture with minimal complexity additions

## Gate Evaluation

**G1 - Technical Feasibility**: PASS - The integration is technically possible with existing components. The RAG agent already exists as a library, and the backend already has a FastAPI structure with CORS configuration.

**G2 - Architecture Alignment**: PASS - The approach aligns with existing architecture patterns by extending the existing FastAPI application with additional endpoints following the same patterns as the retrieval API.

**G3 - Resource Requirements**: PASS - All required resources (FastAPI, Pydantic, existing agent code) are already available in the environment.

**G4 - Risk Assessment**: PASS - The risks are minimal and manageable. The implementation extends existing functionality rather than replacing it, allowing for gradual rollout and testing.

**G5 - Constitution Compliance**: PASS - The plan complies with all constitution principles as verified in the Constitution Check section.

## Constitution Check (Post-Design)

**Principle 1**: Library-First - [Check status: PASS]
- The RAG agent functionality exists as a reusable library and is properly integrated via API

**Principle 2**: CLI Interface - [Check status: NOT APPLICABLE]
- This is a web API integration, not a CLI-focused feature

**Principle 3**: Test-First (NON-NEGOTIABLE) - [Check status: PASS]
- The design includes testable API contracts and endpoints that can be validated

**Principle 4**: Integration Testing - [Check status: PASS]
- The design supports integration testing between frontend and backend components

**Principle 5**: Observability - [Check status: PASS]
- The API endpoints will provide proper logging and metrics as required

**Principle 6**: Simplicity - [Check status: PASS]
- The design extends existing architecture with minimal complexity additions

## Phase 0: Outline & Research

### Research Tasks

1. **Frontend Framework Identification**
   - Task: Identify the current frontend framework and architecture
   - Goal: Understand how to integrate API calls into existing components
   - Outcome: Identified as Docusaurus/React-based static site

2. **Backend API Endpoint Discovery**
   - Task: Document existing RAG backend API endpoints
   - Goal: Understand the API contract for query submission and response
   - Outcome: Identified retrieval endpoints, need to create agent endpoints

3. **Local Development Configuration**
   - Task: Determine local backend URL and CORS requirements
   - Goal: Enable proper communication between frontend and backend
   - Outcome: Backend runs on localhost:8000 with CORS enabled for development

4. **Frontend Component Analysis**
   - Task: Identify existing UI components that need to display responses
   - Goal: Plan for rendering agent responses in the UI
   - Outcome: Need to create new React components for query interface

### Research Outcomes

**Decision**: Create new agent API endpoints in existing FastAPI application
**Rationale**: The existing backend has retrieval functionality but no agent endpoint for processing queries through the RAG agent. The agent functionality exists in agent.py but needs to be exposed via API endpoints.

**Decision**: Use Docusaurus/React for frontend integration
**Rationale**: The existing frontend is a Docusaurus site built with React, which is suitable for adding interactive components for the RAG agent interface.

**Alternatives considered**:
- Separate agent API vs extending existing API: Chose extension for consistency
- New standalone React app vs Docusaurus component: Chose Docusaurus component for integration

## Phase 1: Design & Contracts

### Data Model

**QueryRequest**:
- query: string (min 1, max 2000 chars) - The user's question/query
- stream: boolean (default: false) - Whether to stream responses

**AgentResponse**:
- answer: string - The agent's response to the query
- sources: array of strings - URLs of documents used as sources
- matched_chunks: array of objects containing:
  - content: string - Content of the matched chunk
  - source_url: string - URL of the source document
  - similarity_score: float - Similarity score of the match
- query_time_ms: number - Time taken to process the query in milliseconds
- confidence: string (high/medium/low) - Confidence level of the response

**ConnectionStatus**:
- status: string (connected/disconnected/error) - Current connection status
- backend_url: string - URL of the backend service
- last_checked: timestamp - Time of last status check

### API Contracts

**POST /agent/query**:
- Request: QueryRequest (application/json)
- Response: AgentResponse (application/json)
- Description: Process a user query through the RAG agent and return the response

**GET /agent/health**:
- Request: None
- Response: {status: "ok"} (application/json)
- Description: Check the health status of the agent service

### Quickstart Guide

1. Start the backend: `cd backend && uvicorn api.retrieval_api:create_app --host 0.0.0.0 --port 8000`
2. Verify the service: `curl http://localhost:8000/retrieval/collections`
3. Test agent endpoint after implementation: `curl -X POST http://localhost:8000/agent/query -H "Content-Type: application/json" -d '{"query": "What is ROS2?"}'`
4. Start the frontend: `cd my-ai-book && npm run start`

## Phase 2: Implementation Strategy

### Connect Phase
1. Add agent endpoints to existing retrieval API in backend/api/retrieval_api.py
2. Implement POST /agent/query endpoint that calls RAGAgent.query_agent()
3. Implement GET /agent/health endpoint for connection status
4. Configure CORS settings to allow frontend domain (already configured with ["*"] for development)

### Request Phase
1. Create React component for query input in my-ai-book/src/components/
2. Implement API client to call backend /agent/query endpoint
3. Add loading states and error handling for query submission
4. Implement query validation (min/max length, content checks)

### Response Phase
1. Handle API responses from agent endpoint
2. Implement response parsing and error handling
3. Display response metadata (sources, confidence, query time)
4. Add streaming capability if needed for large responses

### Render Phase
1. Create React component for displaying agent responses
2. Format and render response content with proper styling
3. Display sources and confidence information
4. Add copy-to-clipboard functionality for responses

### Validate Phase
1. Test end-to-end integration with sample queries
2. Verify response accuracy and source citations
3. Test error handling and edge cases
4. Validate performance requirements (response time < 10s)

## Risks & Mitigation

- **API Key Security**: Risk of exposing API keys in frontend; Mitigation: All API calls go through backend
- **Response Time**: Risk of slow responses; Mitigation: Implement loading states and timeout handling
- **CORS Issues**: Risk of cross-origin problems; Mitigation: Properly configure CORS in backend
- **Backend Availability**: Risk of backend being unavailable; Mitigation: Implement retry logic and error handling

## Dependencies

- FastAPI: Backend web framework (already available)
- Pydantic: Data validation (already available)
- OpenAI API: Agent functionality (requires API key)
- Cohere API: Embedding functionality (requires API key)
- Qdrant: Vector database (requires configuration)

## Success Metrics

- Frontend successfully calls backend API and receives responses
- User queries are processed by the RAG agent with relevant responses
- Responses include proper source citations and confidence metrics
- End-to-end query processing time is under 10 seconds for 90% of requests
- Integration works in local development environment as specified