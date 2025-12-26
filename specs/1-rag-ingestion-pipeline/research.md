# Research: RAG Content Ingestion Pipeline

## Overview
This document captures research findings for implementing the RAG content ingestion pipeline, addressing the technical requirements and constraints specified in the feature specification.

## Decision: URL Extraction Method
**Rationale**: To extract all URLs from https://physical-ai-book-topaz.vercel.app/, we'll use requests to get the main page and BeautifulSoup to parse HTML and extract all relative links.

**Alternatives considered**:
- Web scraping with Selenium: More complex and slower, unnecessary for static content
- Direct sitemap parsing: May not capture all pages if sitemap is incomplete

## Decision: Content Extraction Library
**Rationale**: Using BeautifulSoup4 with requests is the most reliable approach for extracting clean text from web pages. It handles malformed HTML gracefully and provides precise control over content selection.

**Alternatives considered**:
- Scrapy: More complex framework than needed for this single-task pipeline
- Newspaper3k: Focused on news articles, may not work optimally for book content
- Raw requests + regex: Unreliable for HTML parsing

## Decision: Text Chunking Strategy
**Rationale**: Using a sliding window approach with overlap to maintain context while ensuring chunks are small enough for Cohere's token limits (max 512 tokens). Target chunk size: ~500-800 words with 100-word overlap.

**Alternatives considered**:
- Sentence-based chunking: May result in chunks that are too small or too large
- Fixed character length: May split sentences inappropriately
- Semantic chunking: More complex and unnecessary for book content

## Decision: Cohere Integration
**Rationale**: Using Cohere's embed-english-v3.0 model with "search_document" input type for optimal performance with RAG applications. Free tier allows 1000 API calls/day which should be sufficient for book processing.

**Alternatives considered**:
- OpenAI embeddings: Would violate constraint of using Cohere
- Local embedding models: Would violate constraint of using Cohere
- Other embedding services: Would violate constraint of using Cohere

## Decision: Qdrant Collection Design
**Rationale**: Creating a collection named "rag_embedding" with appropriate vector dimensions (expected 1024 for Cohere embeddings) and metadata schema to store URL, page number, and section information.

**Alternatives considered**:
- Different vector databases: Would violate constraint of using Qdrant
- Different collection naming: Current name clearly indicates purpose

## Decision: Idempotency Implementation
**Rationale**: Using a combination of source URL and chunk content hash as the point ID in Qdrant to ensure that identical content is not stored multiple times when the pipeline is run repeatedly.

**Alternatives considered**:
- Timestamp-based IDs: Would create duplicates on re-run
- Sequential IDs: Would create duplicates on re-run
- Content-only hash: Might have collisions across different documents

## Technical Constraints & Considerations

### Memory Management
- Process one URL at a time to avoid memory issues with large books
- Clear variables after processing each chunk
- Use generators where possible for large datasets

### Error Handling
- Graceful handling of network timeouts during URL fetching
- Retry mechanism for Cohere API calls
- Continue processing other URLs if one fails

### Free-Tier Compatibility
- Implement rate limiting to respect API limits
- Batch operations where possible to minimize API calls
- Monitor usage to stay within free-tier limits

## Validation Approach
- Compare URL count before and after pipeline execution
- Verify Qdrant collection contains expected number of vectors
- Test idempotency by running pipeline multiple times and confirming no duplicate entries
- Validate that metadata is preserved throughout the process