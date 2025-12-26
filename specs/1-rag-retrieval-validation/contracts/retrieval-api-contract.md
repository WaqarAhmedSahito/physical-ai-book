# RAG Retrieval API Contract

## Overview

This document defines the API contract for the RAG retrieval validation system. The API enables similarity search against the Qdrant vector database and provides validation metrics for retrieved results.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints require a valid API key sent in the Authorization header:

```
Authorization: Bearer {API_KEY}
```

## Endpoints

### POST /retrieval/query

Execute a similarity search against the vector database with the provided query.

#### Request

```json
{
  "query": "What is the main concept of embodied AI?",
  "top_k": 5,
  "threshold": 0.3,
  "collection_name": "rag_embedding",
  "validate": false
}
```

**Request Parameters:**
- `query` (string, required): The text query to search for similar content
- `top_k` (integer, optional): Number of results to return (default: 5, max: 20)
- `threshold` (number, optional): Minimum similarity score threshold (default: 0.0, range: 0.0-1.0)
- `collection_name` (string, optional): Qdrant collection to search (default: "rag_embedding")
- `validate` (boolean, optional): Whether to calculate validation metrics (default: false)

#### Response

**Success Response (200 OK):**
```json
{
  "query_id": "query_12345",
  "query_text": "What is the main concept of embodied AI?",
  "results": [
    {
      "chunk_id": "chunk_abc123",
      "content": "Embodied AI refers to artificial intelligence systems that interact with the physical world through sensors and actuators...",
      "source_url": "https://physical-ai-book-topaz.vercel.app/chapter-1",
      "section_title": "Introduction to Embodied AI",
      "page_number": 15,
      "similarity_score": 0.85,
      "rank": 1
    },
    {
      "chunk_id": "chunk_def456",
      "content": "The core principle of embodied AI is that intelligence emerges from the interaction between an agent and its environment...",
      "source_url": "https://physical-ai-book-topaz.vercel.app/chapter-2",
      "section_title": "Embodied Cognition",
      "page_number": 28,
      "similarity_score": 0.78,
      "rank": 2
    }
  ],
  "search_metadata": {
    "total_results": 2,
    "search_time_ms": 120,
    "query_embedding_dimension": 1024
  }
}
```

**Validation Response (when validate=true):**
```json
{
  "query_id": "query_12345",
  "query_text": "What is the main concept of embodied AI?",
  "results": [/* same as above */],
  "validation_metrics": {
    "precision_at_k": {
      "5": 0.8,
      "10": 0.75
    },
    "recall_at_k": {
      "5": 0.6,
      "10": 0.7
    },
    "mrr": 0.72,
    "hit_rate": 1.0,
    "avg_similarity_score": 0.78,
    "total_results": 2,
    "relevant_results": 2,
    "calculated_at": "2025-12-20T10:30:00Z"
  },
  "search_metadata": { /* same as above */ }
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Query text is required and must be between 1 and 2000 characters",
    "details": {
      "field": "query",
      "value": ""
    }
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or missing API key"
  }
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An internal error occurred during retrieval"
  }
}
```

### POST /retrieval/validate

Run validation on a set of queries to evaluate retrieval quality.

#### Request

```json
{
  "queries": [
    {
      "query": "What is the main concept of embodied AI?",
      "expected_chunks": ["chunk_abc123", "chunk_xyz789"]
    },
    {
      "query": "Explain robot navigation algorithms",
      "expected_chunks": ["chunk_def456"]
    }
  ],
  "top_k": 10
}
```

**Request Parameters:**
- `queries` (array, required): Array of query objects with expected results for validation
- `top_k` (integer, optional): Number of results to consider for validation (default: 10)

#### Response

**Success Response (200 OK):**
```json
{
  "validation_id": "validation_67890",
  "total_queries": 2,
  "results": [
    {
      "query_id": "query_12345",
      "query_text": "What is the main concept of embodied AI?",
      "retrieved_chunks": ["chunk_abc123", "chunk_def456", "chunk_xyz789"],
      "relevant_retrieved": 2,
      "total_expected": 2,
      "metrics": {
        "precision_at_k": {
          "5": 0.8,
          "10": 0.75
        },
        "recall_at_k": {
          "5": 0.6,
          "10": 1.0
        },
        "mrr": 0.72,
        "hit_rate": 1.0
      }
    }
  ],
  "aggregate_metrics": {
    "avg_precision_at_5": 0.8,
    "avg_recall_at_5": 0.6,
    "overall_mrr": 0.72,
    "hit_rate": 1.0
  },
  "completed_at": "2025-12-20T10:30:00Z"
}
```

### GET /retrieval/collections

Get information about available collections for retrieval.

#### Response

**Success Response (200 OK):**
```json
{
  "collections": [
    {
      "name": "rag_embedding",
      "vector_size": 1024,
      "distance": "Cosine",
      "point_count": 1500,
      "created_at": "2025-12-15T09:00:00Z"
    }
  ]
}
```

## Data Models

### Query
```json
{
  "query": "string",
  "top_k": "integer",
  "threshold": "number",
  "collection_name": "string",
  "validate": "boolean"
}
```

### RetrievalResult
```json
{
  "chunk_id": "string",
  "content": "string",
  "source_url": "string",
  "section_title": "string | null",
  "page_number": "integer | null",
  "similarity_score": "number",
  "rank": "integer"
}
```

### ValidationMetrics
```json
{
  "precision_at_k": "object",
  "recall_at_k": "object",
  "mrr": "number",
  "hit_rate": "number",
  "avg_similarity_score": "number",
  "total_results": "integer",
  "relevant_results": "integer",
  "calculated_at": "string"
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_QUERY | 400 | Query text is invalid or missing |
| INVALID_PARAMETERS | 400 | Request parameters are invalid |
| UNAUTHORIZED | 401 | Invalid or missing API key |
| COLLECTION_NOT_FOUND | 404 | Specified collection does not exist |
| EMBEDDING_ERROR | 500 | Error occurred during embedding generation |
| DATABASE_ERROR | 500 | Error occurred during database query |
| INTERNAL_ERROR | 500 | General internal server error |

## Rate Limits

- Queries per minute: 100 per API key
- Concurrent requests: 10 per API key

## Examples

### cURL Example
```bash
curl -X POST http://localhost:8000/api/v1/retrieval/query \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main concept of embodied AI?",
    "top_k": 5,
    "threshold": 0.5,
    "validate": true
  }'
```

### Python Example
```python
import requests

headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "query": "What is the main concept of embodied AI?",
    "top_k": 5,
    "threshold": 0.5,
    "validate": True
}

response = requests.post(
    "http://localhost:8000/api/v1/retrieval/query",
    headers=headers,
    json=data
)

if response.status_code == 200:
    result = response.json()
    print(f"Found {len(result['results'])} results")
else:
    print(f"Error: {response.status_code} - {response.text}")
```