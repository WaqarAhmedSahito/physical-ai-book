# Research: RAG Retrieval Pipeline Validation

## Overview

This research document addresses the technical unknowns and implementation decisions required for the RAG retrieval validation feature. It covers Qdrant similarity search best practices, Cohere embedding consistency, validation metrics, and metadata validation methods.

## Qdrant Similarity Search Best Practices

### Decision: Use cosine distance for semantic similarity
**Rationale**: Cosine distance is the standard for semantic similarity in vector search, especially when working with normalized embeddings like those from Cohere. It measures the angle between vectors, which correlates well with semantic similarity.

**Alternatives considered**:
- Euclidean distance: Less suitable for high-dimensional embeddings as it measures absolute distance rather than directional similarity
- Dot product: Can be affected by vector magnitude, making it less reliable for comparing similarity across different query types

### Decision: Use search parameters for optimal retrieval
**Rationale**: Qdrant offers several parameters to optimize search results:
- `limit`: Number of results to return (typically 5-10 for RAG applications)
- `score_threshold`: Minimum similarity score to filter results (0.3-0.7 range depending on requirements)
- `with_payload`: Include metadata with results for validation
- `with_vectors`: Include vectors if needed for additional processing

## Cohere Embedding Consistency

### Decision: Use same model and input type for consistency
**Rationale**: To ensure accurate similarity matching, the query embeddings must be generated using the same model and input type as the stored embeddings. The ingestion pipeline uses:
- Model: `embed-english-v3.0`
- Input type: `search_document` for stored content
- For queries: Use `search_query` input type for optimal retrieval performance

**Alternatives considered**:
- Different models: Would result in incompatible embeddings
- Different input types: Could reduce retrieval accuracy

### Decision: Preprocess queries similarly to stored content
**Rationale**: Query preprocessing should match the text processing used during ingestion to ensure consistency in embedding generation.

## Retrieval Validation Metrics

### Decision: Implement precision, recall, and MRR metrics
**Rationale**: These are standard metrics for evaluating retrieval system performance:
- **Precision@K**: Proportion of relevant results in top K retrieved items
- **Recall@K**: Proportion of all relevant items that appear in top K results
- **Mean Reciprocal Rank (MRR)**: Average of reciprocal ranks of first relevant result

**Alternatives considered**:
- F1-score: Combination of precision and recall but doesn't account for ranking
- NDCG (Normalized Discounted Cumulative Gain): More complex but accounts for graded relevance

### Decision: Create test dataset with known relevant pairs
**Rationale**: To validate retrieval quality, we need a dataset of queries with known relevant documents. This can be created by:
1. Using sample questions from the book content
2. Manually identifying relevant sections for each query
3. Measuring how well the system retrieves these sections

## Metadata Validation Methods

### Decision: Validate metadata integrity through cross-referencing
**Rationale**: To ensure that retrieved chunks have correct metadata, implement validation by:
- Checking that URL exists and is accessible
- Verifying that page number and section title match the source document
- Confirming that content appears in the correct location in the source

### Decision: Implement metadata consistency checks
**Rationale**: During retrieval, validate that:
- All expected metadata fields are present
- Metadata values are properly formatted
- URL format is valid and consistent with source domain

## Technical Unknowns Resolved

### FR-006: Specific accuracy metrics for retrieval validation
**Decision**: Implement the following metrics:
- Precision@5 and Precision@10
- Recall@5 and Recall@10
- Mean Reciprocal Rank (MRR)
- Semantic similarity score distribution analysis
- Hit rate (percentage of queries that return at least one result above threshold)

**Rationale**: These metrics provide a comprehensive view of retrieval quality across different aspects: relevance, completeness, and ranking quality.

## Implementation Approach

### Phase 1: Basic Retrieval
1. Implement query embedding generation using Cohere
2. Execute similarity search against Qdrant `rag_embedding` collection
3. Return top N results with metadata

### Phase 2: Validation Tools
1. Implement validation metrics calculation
2. Create test dataset with known relevant pairs
3. Build CLI tools for manual validation
4. Add performance and accuracy reporting

### Phase 3: Quality Assurance
1. Run validation on sample queries
2. Adjust parameters based on results
3. Document performance characteristics