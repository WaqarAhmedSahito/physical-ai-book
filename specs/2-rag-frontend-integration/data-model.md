# Data Model: RAG Agent Integration

## Core Entities

### QueryRequest
Represents a user query submitted to the RAG agent.

**Fields:**
- `query` (string, required): The user's question or query text
  - Min length: 1 character
  - Max length: 2000 characters
- `stream` (boolean, optional): Whether to stream responses
  - Default: false

**Validation rules:**
- Query must not be empty
- Query must not exceed 2000 characters

### AgentResponse
Represents the response from the RAG agent after processing a query.

**Fields:**
- `answer` (string, required): The agent's response to the query
- `sources` (array of strings, required): URLs of documents used as sources
- `matched_chunks` (array of MatchedChunk objects, required): Chunks of content that were matched during retrieval
- `query_time_ms` (number, required): Time taken to process the query in milliseconds
- `confidence` (string, required): Confidence level of the response
  - Values: "high", "medium", "low"

**Validation rules:**
- Answer must not be empty
- Sources array may be empty but must be present
- Matched chunks array may be empty but must be present
- Query time must be a positive number
- Confidence must be one of the allowed values

### MatchedChunk
Represents a chunk of content that was matched during the retrieval process.

**Fields:**
- `content` (string, required): Content of the matched chunk
- `source_url` (string, required): URL of the source document
- `similarity_score` (number, required): Similarity score of the match (0.0 to 1.0)

**Validation rules:**
- Content must not be empty
- Source URL must be a valid URL format
- Similarity score must be between 0.0 and 1.0

### ConnectionStatus
Represents the connection status between frontend and backend.

**Fields:**
- `status` (string, required): Current connection status
  - Values: "connected", "disconnected", "error"
- `backend_url` (string, required): URL of the backend service
- `last_checked` (string, required): ISO timestamp of last status check

## State Transitions

### Query Processing States
1. **Submitted**: Query has been received by the backend
2. **Retrieving**: Retrieval process is ongoing
3. **Processing**: Agent is generating response
4. **Completed**: Response is ready for frontend
5. **Error**: An error occurred during processing

## Relationships

- One `QueryRequest` generates one `AgentResponse`
- One `AgentResponse` contains multiple `MatchedChunk` objects
- Multiple queries may reference the same source documents in `sources`

## Constraints

- All string fields should be properly sanitized to prevent injection attacks
- Query processing should have a maximum timeout of 30 seconds
- Response caching may be implemented for identical queries
- Error responses should not expose sensitive system information