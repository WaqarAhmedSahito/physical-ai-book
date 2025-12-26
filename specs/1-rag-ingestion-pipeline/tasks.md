# Implementation Tasks: RAG Content Ingestion Pipeline

**Feature**: RAG Content Ingestion Pipeline
**Branch**: `1-rag-ingestion-pipeline`
**Created**: 2025-12-19
**Spec**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

## Phase 1: Setup
**Goal**: Initialize project structure and dependencies per implementation plan

**Independent Test**: Project structure exists and dependencies can be installed

- [x] T001 Create backend directory structure
- [x] T002 Initialize pyproject.toml with UV for dependency management
- [x] T003 Add required dependencies to pyproject.toml: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv
- [x] T004 Create .env file template with COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY variables
- [x] T005 Create main.py file with basic structure and imports

## Phase 2: Foundational Components
**Goal**: Implement core data structures and utility functions that all user stories depend on

**Independent Test**: Core entities can be created and manipulated without errors

- [x] T006 [P] Define TextChunk data class in main.py with all required fields and validation
- [x] T007 [P] Define Embedding data class in main.py with all required fields and validation
- [x] T008 [P] Define ProcessingResult data class in main.py with all required fields and validation
- [x] T009 [P] Implement utility function to calculate content hash for idempotency
- [x] T010 [P] Implement configuration loading from environment variables
- [x] T011 [P] Implement error handling and logging utilities

## Phase 3: User Story 1 - Extract Book Content from URLs (Priority: P1)
**Goal**: Extract content from deployed book URLs to process text for the RAG system

**Independent Test**: Can provide a GitHub Pages URL and verify that content is extracted successfully, delivering raw text for further processing

**Acceptance Scenarios**:
1. Given a valid GitHub Pages URL containing book content, when the extraction process runs, then all textual content from the book is retrieved without losing structural information
2. Given a GitHub Pages URL with multiple pages/chapters, when the extraction process runs, then content from all pages is retrieved with proper page/chapter identification

- [x] T012 [US1] Implement get_all_urls function to extract all URLs from https://physical-ai-book-topaz.vercel.app/ using sitemap.xml
- [x] T013 [US1] Implement extract_text_from_url function using requests and BeautifulSoup to get clean text content
- [x] T014 [US1] Implement URL validation and error handling for inaccessible pages
- [x] T015 [US1] Add metadata extraction (page numbers, section titles) from URL content
- [ ] T016 [US1] Test content extraction with sample URLs from the book site

## Phase 4: User Story 2 - Process and Chunk Text Content (Priority: P2)
**Goal**: Chunk the extracted text content with proper metadata so it can be embedded effectively

**Independent Test**: Can provide raw text content and verify that it's broken into chunks with proper page/section metadata retained

**Acceptance Scenarios**:
1. Given raw book content, when the chunking process runs, then text is divided into appropriately sized segments with page/section metadata preserved
2. Given content that spans multiple pages/sections, when the chunking process runs, then each chunk contains metadata indicating its original source location

- [x] T017 [US2] Implement chunk_text function to split content into 500-800 word segments with 100-word overlap
- [x] T018 [US2] Preserve metadata (source URL, page number, section title) in each chunk
- [x] T019 [US2] Implement word count calculation for each chunk
- [x] T020 [US2] Add validation to ensure chunks are not empty and meet minimum size requirements
- [ ] T021 [US2] Test chunking with various content sizes and structures

## Phase 5: User Story 3 - Generate Embeddings Using Cohere (Priority: P3)
**Goal**: Generate vector embeddings from text chunks using Cohere so semantic similarity can be computed later

**Independent Test**: Can provide text chunks and verify that Cohere generates appropriate vector representations

**Acceptance Scenarios**:
1. Given properly chunked text with metadata, when Cohere embedding generation runs, then vector representations are created that capture semantic meaning
2. Given multiple text chunks, when embedding process runs, then all vectors are generated consistently with the same dimensionality

- [x] T022 [US3] Implement generate_embedding function using Cohere API with embed-english-v3.0 model
- [x] T023 [US3] Add rate limiting to respect free-tier API limits (1000 calls/day)
- [x] T024 [US3] Implement retry mechanism for Cohere API calls with exponential backoff
- [x] T025 [US3] Add error handling for API failures and quota limits
- [x] T026 [US3] Validate that generated embeddings have correct dimensions (1024 for Cohere)
- [ ] T027 [US3] Test embedding generation with sample text chunks

## Phase 6: User Story 4 - Store Vectors in Qdrant Database (Priority: P4)
**Goal**: Store embeddings and metadata in Qdrant so they can be efficiently queried later

**Independent Test**: Can verify that embeddings and metadata are stored in Qdrant and can be retrieved

**Acceptance Scenarios**:
1. Given embeddings with metadata, when storage process runs, then vectors are stored in Qdrant with associated metadata preserved
2. Given stored vectors in Qdrant, when retrieval query runs, then stored embeddings and metadata can be accessed successfully

- [x] T028 [US4] Implement create_collection function to initialize "rag_embedding" collection in Qdrant
- [x] T029 [US4] Implement save_chunk_to_qdrant function to store embeddings with metadata
- [x] T030 [US4] Configure Qdrant collection with 1024-dimensional vectors and cosine distance
- [x] T031 [US4] Map TextChunk and Embedding fields to Qdrant payload schema
- [x] T032 [US4] Add error handling for Qdrant connection and storage failures
- [ ] T033 [US4] Test storage and retrieval of sample embeddings

## Phase 7: User Story 5 - Ensure Pipeline Idempotency (Priority: P5)
**Goal**: Make the ingestion pipeline idempotent so it can be safely rerun without creating duplicate entries

**Independent Test**: Can run the pipeline multiple times and verify no duplicates are created

**Acceptance Scenarios**:
1. Given a completed ingestion run, when the same pipeline runs again with identical inputs, then no duplicate entries are created in the vector database

- [x] T034 [US5] Implement idempotency check using URL and content hash as unique identifier
- [x] T035 [US5] Modify save_chunk_to_qdrant to use hash-based IDs to prevent duplicates
- [x] T036 [US5] Add duplicate detection and skip logic in the pipeline
- [ ] T037 [US5] Test idempotency by running pipeline multiple times and confirming no duplicates
- [ ] T038 [US5] Add pipeline execution tracking with ProcessingResult

## Phase 8: Complete Pipeline Integration
**Goal**: Integrate all components into a cohesive pipeline that executes the complete flow

**Independent Test**: The complete pipeline runs from URL extraction to Qdrant storage successfully

- [x] T039 [P] Implement main pipeline function that orchestrates the complete flow: get_all_urls → extract_text_from_url → chunk_text → embedding → create_collection → save_chunk_to_qdrant
- [x] T040 [P] Add progress tracking and metrics collection during pipeline execution
- [x] T041 [P] Implement command-line interface for pipeline execution
- [ ] T042 [P] Add validation to confirm all URLs from https://physical-ai-book-topaz.vercel.app/ are processed
- [x] T043 [P] Add comprehensive error handling and graceful degradation
- [x] T044 [P] Implement memory management to handle large books without exceeding limits

## Phase 9: Polish & Cross-Cutting Concerns
**Goal**: Add final touches, documentation, and validation to ensure production readiness

**Independent Test**: Pipeline runs completely and meets all success criteria from specification

- [x] T045 Add comprehensive logging throughout the pipeline
- [x] T046 Add configuration options for chunk size, overlap, and API rate limits
- [x] T047 Create README.md with usage instructions and examples
- [x] T048 Add validation script to confirm all URLs were embedded and stored in Qdrant
- [x] T049 Implement monitoring of free-tier usage to prevent overages
- [x] T050 Run complete pipeline and verify all success criteria are met

## Dependencies

**User Story Completion Order**:
1. US1 (Extract Book Content) → Must be completed first as it provides input for all other stories
2. US2 (Process and Chunk Text) → Depends on US1, processes extracted content
3. US3 (Generate Embeddings) → Depends on US2, generates embeddings from chunks
4. US4 (Store Vectors) → Depends on US3, stores generated embeddings
5. US5 (Idempotency) → Can be implemented in parallel with US4, but needed for final pipeline

## Parallel Execution Examples

**Per User Story**:
- US1: Can parallelize URL extraction and content extraction for different URLs
- US2: Can parallelize chunking of different content pieces
- US3: Can parallelize embedding generation for different chunks (with rate limiting)
- US4: Can parallelize storage of different embeddings
- US5: Idempotency logic applies across all operations

## Implementation Strategy

**MVP Scope**: Focus on User Story 1 (content extraction) as the minimum viable product that demonstrates the core functionality.

**Incremental Delivery**:
1. Phase 1-2: Setup and foundational components
2. Phase 3: Content extraction (MVP)
3. Phase 4: Text chunking
4. Phase 5: Embedding generation
5. Phase 6: Storage in Qdrant
6. Phase 7: Idempotency
7. Phase 8-9: Integration and polish