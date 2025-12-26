# Implementation Plan: RAG Content Ingestion Pipeline

**Branch**: `1-rag-ingestion-pipeline` | **Date**: 2025-12-19 | **Spec**: [link to spec](../spec.md)

**Input**: Feature specification from `/specs/1-rag-ingestion-pipeline/spec.md`

## Summary

Implementation of a RAG content ingestion pipeline that extracts content from GitHub Pages URLs, chunks and preprocesses text, generates Cohere embeddings, and stores vectors with metadata in Qdrant. The system will be implemented as a single-file Python application in `backend/main.py` with a linear pipeline flow: get_all_urls → extract_text_from_url → chunk_text → embedding → create_collection → save_chunk_to_qdrant.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv
**Storage**: Qdrant vector database (external service)
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server environment
**Project Type**: Backend processing pipeline
**Performance Goals**: Process 100 pages within 30 minutes while staying within free-tier usage limits
**Constraints**: <200MB memory usage during processing, free-tier compatible with Cohere and Qdrant
**Scale/Scope**: Single pipeline processing book content with idempotent operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution, the following checks pass:
- Single-file design approach aligns with the requirement for a simple, focused implementation
- Use of external services (Cohere, Qdrant) is within architectural guidelines
- Idempotency requirement is addressed in the implementation approach
- Free-tier compatibility is considered in the design

## Project Structure

### Documentation (this feature)
```text
specs/1-rag-ingestion-pipeline/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── pyproject.toml       # UV package configuration
├── main.py              # Single-file implementation of the entire pipeline
└── .env                 # Environment variables (not committed)
```

**Structure Decision**: Selected Option 2 (Web application with backend only) with a single-file approach in the backend directory. The backend will contain the entire pipeline implementation in main.py as specified in the requirements.

## Phase 0: Research & Analysis

### Research Tasks
1. **URL Extraction**: Research how to extract all URLs from https://physical-ai-book-topaz.vercel.app/

2. **Content Extraction**: Best practices for extracting text content from web pages using requests and BeautifulSoup
3. **Text Chunking**: Optimal strategies for chunking book content while preserving metadata
4. **Cohere Integration**: Free-tier usage limits and best practices for embedding generation
5. **Qdrant Integration**: Collection creation and vector storage patterns for RAG systems
6. **Idempotency**: Techniques to ensure pipeline can be run multiple times without duplicates

### Key Decisions
- **Dependency Management**: Using UV (pyproject.toml) as specified in requirements
- **Single-File Architecture**: Entire system in main.py to maintain simplicity
- **External Services**: Cohere for embeddings and Qdrant for vector storage as per constraints
- **Idempotency Approach**: Using URL + chunk hash as unique identifier to prevent duplicates

## Phase 1: Design & Contracts

### Data Model
- **TextChunk**: Contains content, source URL, page/section metadata, and unique identifier
- **Embedding**: Vector representation with associated TextChunk reference
- **ProcessingResult**: Status and metrics for pipeline execution

### API Contracts
The system will not expose external APIs but will use the following internal function contracts:
- `get_all_urls(base_url: str) -> List[str]`: Extract all book page URLs from the base URL
- `extract_text_from_url(url: str) -> str`: Extract clean text content from a single URL
- `chunk_text(content: str, metadata: dict) -> List[TextChunk]`: Split content into manageable chunks
- `generate_embedding(text: str) -> List[float]`: Create vector embedding from text
- `create_collection(collection_name: str) -> None`: Initialize Qdrant collection
- `save_chunk_to_qdrant(chunk: TextChunk, embedding: List[float]) -> None`: Store vector with metadata

### Quickstart Guide
```bash
# Setup
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Configuration
cp .env.example .env
# Add COHERE_API_KEY and QDRANT_URL to .env

# Run pipeline
python main.py
```

## Phase 2: Implementation Approach

### Pipeline Flow
1. `get_all_urls`: Discover all book page URLs from https://physical-ai-book-topaz.vercel.app/
2. `extract_text_from_url`: For each URL, extract clean text content
3. `chunk_text`: Split content into appropriately sized chunks with metadata
4. `embedding`: Generate Cohere embeddings for each chunk
5. `create_collection`: Initialize Qdrant collection named "rag_embedding"
6. `save_chunk_to_qdrant`: Store embeddings with metadata in Qdrant

### Validation Strategy
- Confirm all URLs from https://physical-ai-book-topaz.vercel.app/ are processed
- Verify embeddings are stored in Qdrant collection
- Check for idempotency by running pipeline multiple times
- Validate metadata preservation throughout the process

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| External Dependencies | Cohere and Qdrant are required by feature constraints | Feature specification mandates these specific services |

- **Sitemap Url**:https://physical-ai-book-topaz.vercel.app/sitemap.xml