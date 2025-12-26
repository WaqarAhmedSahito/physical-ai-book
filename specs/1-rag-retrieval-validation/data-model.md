# Data Model: RAG Retrieval Pipeline Validation

## Overview

This document defines the data entities used in the RAG retrieval validation system. The entities represent the core concepts of the retrieval process: queries, results, and validation metrics.

## Core Entities

### Query
Represents a text query that will be used for similarity search against the vector database.

**Fields**:
- `id: str` - Unique identifier for the query
- `text: str` - The actual query text
- `embedding: List[float]` - Vector representation of the query text (1024-dimensional for Cohere)
- `created_at: datetime` - Timestamp when the query was created

**Relationships**:
- One-to-many with RetrievalResult (a query produces multiple results)

**Validation rules**:
- Text must not be empty
- Embedding must have exactly 1024 dimensions (for Cohere compatibility)
- Created_at must be a valid timestamp

### RetrievalResult
Represents a single result from the similarity search, containing the matched text chunk and its metadata.

**Fields**:
- `chunk_id: str` - Unique identifier of the matched text chunk
- `content: str` - The text content of the chunk
- `source_url: str` - The URL where the content originated
- `section_title: Optional[str]` - Title of the section where the content appears
- `page_number: Optional[int]` - Page number in the original document
- `similarity_score: float` - Cosine similarity score between query and result
- `rank: int` - Position in the ranked results (1-indexed)

**Relationships**:
- Many-to-one with Query (multiple results for one query)
- One-to-one with ValidationResult (each result can be validated)

**Validation rules**:
- Similarity_score must be between 0 and 1
- Rank must be a positive integer
- Content must not be empty

### ValidationResult
Captures the validation assessment of a retrieval result against expected criteria.

**Fields**:
- `result_id: str` - Reference to the RetrievalResult being validated
- `is_relevant: bool` - Whether the result is relevant to the query
- `relevance_score: float` - Subjective relevance score (0-1)
- `validation_criteria: List[str]` - List of criteria used for validation
- `notes: Optional[str]` - Additional notes about the validation
- `validated_at: datetime` - Timestamp when validation was performed

**Relationships**:
- One-to-one with RetrievalResult (one validation per result)
- Many-to-one with ValidationMetrics (multiple validations contribute to metrics)

**Validation rules**:
- Relevance_score must be between 0 and 1
- Validated_at must be a valid timestamp

### ValidationMetrics
Aggregates metrics for evaluating the overall performance of the retrieval system.

**Fields**:
- `query_id: str` - Reference to the query being evaluated
- `precision_at_k: Dict[int, float]` - Precision at different k values (e.g., {5: 0.8, 10: 0.7})
- `recall_at_k: Dict[int, float]` - Recall at different k values
- `mrr: float` - Mean Reciprocal Rank
- `hit_rate: float` - Proportion of queries with at least one relevant result
- `avg_similarity_score: float` - Average similarity score of top results
- `total_results: int` - Total number of results evaluated
- `relevant_results: int` - Number of relevant results
- `calculated_at: datetime` - Timestamp when metrics were calculated

**Relationships**:
- One-to-many with ValidationResult (metrics aggregate multiple validations)
- Many-to-one with Query (metrics for a specific query)

**Validation rules**:
- All score values must be between 0 and 1
- Calculated_at must be a valid timestamp
- Total_results must be greater than or equal to relevant_results

## State Transitions

### Query States
- `created` → Query object is initialized with text
- `embedded` → Embedding has been generated for the query
- `searched` → Similarity search has been executed against Qdrant
- `validated` → Results have been validated and metrics calculated

### RetrievalResult States
- `retrieved` → Result has been retrieved from Qdrant
- `validated` → Result has been assessed for relevance

## API Contract Considerations

### Input Validation
- Query text length should be within reasonable limits (e.g., 1-2000 characters)
- Special characters should be handled appropriately
- Empty queries should be rejected

### Output Structure
- Results should be ordered by similarity score (descending)
- Metadata should be consistently formatted
- Error responses should include meaningful error messages

## Data Flow

1. **Query Creation**: User provides text query → Query object created with state `created`
2. **Embedding Generation**: Query text → Cohere API → Query state becomes `embedded`
3. **Similarity Search**: Query embedding → Qdrant search → RetrievalResult objects created with state `retrieved`
4. **Validation**: RetrievalResults → Validation process → ValidationResult objects created, ValidationMetrics calculated
5. **Reporting**: ValidationMetrics → Output to user with state `validated`