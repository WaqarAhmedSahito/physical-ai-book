# Claude Agent Context: RAG Frontend Integration

## Project Overview
- Feature: 2-rag-frontend-integration
- Purpose: Integrate RAG backend with Docusaurus/React frontend
- Architecture: FastAPI backend with React frontend via REST API

## Backend Components
- Main API: backend/api/retrieval_api.py (FastAPI app with create_app())
- Agent logic: backend/agent.py (RAGAgent class)
- Current endpoints: /retrieval/* (collections, query, validate)
- New endpoints to add: /agent/* (query, health)

## API Specifications
- Agent query endpoint: POST /agent/query
- Request model: QueryRequest with 'query' (string) and optional 'stream' (boolean)
- Response model: AgentResponse with 'answer', 'sources', 'matched_chunks', 'query_time_ms', 'confidence'
- Health endpoint: GET /agent/health

## Frontend Components
- Framework: Docusaurus (React-based static site)
- Location: my-ai-book/ directory
- Components to create: Query input, response display, loading states
- API client: REST calls to backend endpoints

## Implementation Steps
1. Extend retrieval_api.py to add agent endpoints
2. Create React components for query interface
3. Implement API client for backend communication
4. Add response rendering with source citations
5. Test end-to-end integration

## Environment
- Backend: uvicorn api.retrieval_api:create_app --host 0.0.0.0 --port 8000
- Frontend: npm run start in my-ai-book directory
- CORS: Already configured with allow_origins=["*"] for development