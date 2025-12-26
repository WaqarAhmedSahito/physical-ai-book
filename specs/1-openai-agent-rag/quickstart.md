# Quickstart Guide: OpenAI Agent with RAG Integration

**Feature**: OpenAI Agent with RAG Integration
**Version**: 1.0
**Date**: 2025-12-22

## Overview

This guide provides instructions for setting up and running the retrieval-enabled AI agent that uses OpenAI Agents SDK and FastAPI. The system accepts user queries via API, retrieves relevant content from Qdrant, and generates responses grounded in the retrieved content.

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Access to Qdrant instance with `rag_embedding` collection
- Existing Cohere embeddings in the Qdrant collection

## Installation

### 1. Clone or navigate to the project directory

```bash
cd your-project-directory
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi openai qdrant-client python-dotenv uvicorn pydantic
```

## Configuration

### 1. Create environment file

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here  # Optional, if authentication required
QDRANT_COLLECTION=rag_embedding
```

### 2. Verify Qdrant connection

Ensure that:
- Your Qdrant instance is accessible at the specified URL
- The `rag_embedding` collection exists and contains Cohere embeddings
- The collection has the expected schema with fields like `source_url`, `content`, etc.

## Running the Application

### 1. Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### 2. Verify the service is running

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-22T10:30:00Z",
  "dependencies": {
    "openai_api": "healthy",
    "qdrant": "healthy",
    "processing_capacity": "healthy"
  }
}
```

## Using the API

### Submit a query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is embodied AI?"
  }'
```

### Sample response

```json
{
  "response_id": "resp_abc123",
  "query": "What is embodied AI?",
  "response": "Embodied AI refers to artificial intelligence systems that interact with the physical world through sensors and actuators...",
  "sources": [
    {
      "chunk_id": "chunk_xyz789",
      "content_preview": "Embodied artificial intelligence (AI) refers to AI systems that...",
      "source_url": "https://physical-ai-book-topaz.vercel.app/module-1/chapter-1",
      "section_title": "Introduction to Embodied AI",
      "similarity_score": 0.87,
      "page_number": 15
    }
  ],
  "confidence": 0.85,
  "processing_time_ms": 2450,
  "metadata": {}
}
```

## Development

### Project Structure

```
project/
├── main.py                 # FastAPI application entry point
├── agent.py               # Agent logic and OpenAI integration
├── retrieval.py           # Qdrant retrieval functionality
├── models.py              # Data models
├── .env                   # Environment variables
└── requirements.txt       # Dependencies
```

### Adding a new feature

1. Update the data model if needed
2. Create or update API endpoints
3. Implement the business logic
4. Add tests
5. Update documentation

## Troubleshooting

### Common Issues

**Issue**: "OpenAI API key not found"
**Solution**: Verify that OPENAI_API_KEY is set in your environment variables

**Issue**: "Cannot connect to Qdrant"
**Solution**: Check that QDRANT_URL is correct and the service is accessible

**Issue**: "No relevant content found"
**Solution**: Verify that the `rag_embedding` collection has content and embeddings are properly indexed

### Performance

- Queries typically return responses in 2-5 seconds
- First query may be slower due to initialization
- Subsequent queries benefit from connection pooling

## Next Steps

1. Implement rate limiting for production use
2. Add request logging and monitoring
3. Set up automated tests
4. Deploy to production environment