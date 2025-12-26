# Quickstart Guide: RAG Agent Frontend Integration

## Prerequisites

- Python 3.8+ with pip
- Node.js 18+ with npm
- Backend dependencies installed (`cd backend && pip install -r requirements.txt`)
- Frontend dependencies installed (`cd my-ai-book && npm install`)
- API keys configured in backend/.env file:
  - OPENROUTER_API_KEY (or OPENAI_API_KEY)
  - QDRANT_URL
  - QDRANT_API_KEY (if using secured Qdrant instance)
  - COHERE_API_KEY

## Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or if using uv: uv pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create or update `backend/.env` with your API keys:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here (if applicable)
   COHERE_API_KEY=your_cohere_api_key_here
   ```

4. **Start the backend server:**
   ```bash
   uvicorn api.retrieval_api:create_app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Verify the backend is running:**
   ```bash
   curl http://localhost:8000/retrieval/collections
   ```

## Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd my-ai-book
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm run start
   ```

4. **Access the frontend:**
   Open your browser to `http://localhost:3000`

## Testing the Integration

1. **Test the agent endpoint directly (backend):**
   ```bash
   curl -X POST http://localhost:8000/agent/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is ROS2?"}'
   ```

2. **Verify the response includes:**
   - `answer`: The agent's response
   - `sources`: Array of source documents used
   - `matched_chunks`: Array of relevant content chunks
   - `query_time_ms`: Processing time
   - `confidence`: Confidence level

## Integration Points

### Backend API Endpoints
- `POST /agent/query`: Process user queries through RAG agent
- `GET /agent/health`: Check agent service health
- `POST /retrieval/query`: Execute similarity search (existing)
- `GET /retrieval/collections`: Get collection information (existing)

### Frontend Components
The integration will add:
- Query input component for user questions
- Response display component for agent answers
- Loading and error states
- Source citation display

## Troubleshooting

### Common Issues

**Backend not starting:**
- Check that all required environment variables are set
- Verify that required Python packages are installed
- Ensure port 8000 is not in use

**CORS errors:**
- Backend already configured with `allow_origins=["*"]` for development
- For production, configure specific origins in `backend/api/retrieval_api.py`

**API key errors:**
- Verify API keys are correctly set in `.env` file
- Check that the API provider (OpenRouter/OpenAI) is accessible

**No results from queries:**
- Ensure the vector database has been populated with content
- Verify that the Qdrant connection is working
- Check that the retrieval pipeline has been run successfully

### Verification Steps

1. **Check backend health:**
   ```bash
   curl http://localhost:8000/agent/health
   ```

2. **Check retrieval functionality:**
   ```bash
   curl -X POST http://localhost:8000/retrieval/query \
     -H "Content-Type: application/json" \
     -d '{"query": "test query", "top_k": 5}'
   ```

3. **Test full agent functionality:**
   ```bash
   curl -X POST http://localhost:8000/agent/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is this book about?"}'
   ```