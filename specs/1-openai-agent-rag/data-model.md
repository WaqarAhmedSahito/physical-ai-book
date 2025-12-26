# Data Model: OpenAI Agent with RAG Integration

**Feature**: OpenAI Agent with RAG Integration
**Model Date**: 2025-12-22
**Status**: Draft

## Entity Definitions

### Query
**Description**: A user's text input requesting information or assistance

**Fields**:
- `query_text` (string, required): The raw text of the user's query
- `query_id` (string, required): Unique identifier for the query
- `timestamp` (datetime, required): When the query was submitted
- `user_id` (string, optional): Identifier for the user (if applicable)
- `metadata` (object, optional): Additional query metadata

**Validation Rules**:
- `query_text` must be non-empty
- `query_text` length < 2000 characters
- `query_id` must be unique
- `timestamp` must be current or past

**State Transitions**: N/A (immutable input)

### RetrievedChunk
**Description**: A text segment from the knowledge base that is relevant to the user's query

**Fields**:
- `chunk_id` (string, required): Unique identifier for the chunk
- `content` (string, required): The text content of the chunk
- `source_url` (string, required): URL where the content originated
- `section_title` (string, optional): Title of the section where content appears
- `page_number` (integer, optional): Page number in original document
- `similarity_score` (float, required): Cosine similarity score (0.0-1.0)
- `rank` (integer, required): Position in ranked results (1-indexed)
- `metadata` (object, optional): Additional chunk metadata

**Validation Rules**:
- `content` must be non-empty
- `similarity_score` must be between 0.0 and 1.0
- `rank` must be positive integer
- `source_url` must be valid URL format

**State Transitions**: N/A (immutable retrieved data)

### AgentResponse
**Description**: The AI-generated answer based on the retrieved content

**Fields**:
- `response_id` (string, required): Unique identifier for the response
- `query_id` (string, required): Reference to the original query
- `content` (string, required): The AI-generated response text
- `sources` (array, required): List of RetrievedChunk IDs used
- `confidence` (float, optional): Confidence score for the response (0.0-1.0)
- `processing_time_ms` (integer, required): Time taken to generate response
- `timestamp` (datetime, required): When the response was generated
- `metadata` (object, optional): Additional response metadata

**Validation Rules**:
- `content` must be non-empty
- `sources` array must not be empty
- `confidence` must be between 0.0 and 1.0 if provided
- `processing_time_ms` must be non-negative
- `query_id` must reference a valid Query

**State Transitions**: N/A (immutable output)

### AgentThread
**Description**: Conversation thread maintaining context for the agent

**Fields**:
- `thread_id` (string, required): Unique identifier for the thread
- `created_at` (datetime, required): When the thread was created
- `last_updated` (datetime, required): When the thread was last modified
- `messages` (array, required): List of messages in the thread
- `metadata` (object, optional): Additional thread metadata

**Validation Rules**:
- `thread_id` must be unique
- `messages` array must not be empty
- `last_updated` must be same or after `created_at`

**State Transitions**:
- `active`: Thread is currently receiving messages
- `archived`: Thread is read-only for historical purposes

## Relationships

### Query → AgentResponse
- One-to-one relationship
- AgentResponse references Query via `query_id`

### Query → RetrievedChunk
- One-to-many relationship (through agent processing)
- AgentResponse contains references to multiple RetrievedChunk items in `sources`

### AgentThread → Query/AgentResponse
- One-to-many relationship
- Both Query and AgentResponse can belong to a thread via thread context

## Constraints

### Business Rules
1. Each query must result in exactly one agent response
2. Agent responses must be grounded in at least one retrieved chunk
3. Retrieved chunks must have a minimum similarity score (e.g., 0.3)
4. Agent responses must include source references to retrieved content

### Performance Constraints
1. Query processing must complete within 10 seconds
2. System must handle up to 100 concurrent threads
3. Retrieval should return results within 2 seconds

### Data Integrity
1. All IDs must be globally unique
2. Timestamps must use ISO 8601 format
3. All required fields must be present in valid instances
4. Cross-references must point to existing entities