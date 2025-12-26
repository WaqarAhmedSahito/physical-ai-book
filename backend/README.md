# RAG Content Pipeline

This pipeline includes functionality for both content ingestion and retrieval validation:
- **Ingestion**: Extracts content from book URLs, chunks the text, generates embeddings using Cohere, and stores the vectors with metadata in Qdrant
- **Retrieval**: Executes similarity searches against the vector database and validates retrieval quality

The ingestion pipeline follows the flow: `get_all_urls → extract_text_from_url → chunk_text → embedding → create_collection → save_chunk_to_qdrant`.

The retrieval validation system enables similarity search against stored vectors and provides metrics for evaluating retrieval quality.

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd physical-ai-book/backend
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
   ```

3. **Configure environment variables**
   ```bash
   cp .env .env.local
   ```

   Edit `.env.local` and add your API keys:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## Usage

Run the pipeline with default settings:
```bash
python main.py
```

### Command Line Options

- `--target-url`: Target URL to extract content from (default: `https://physical-ai-book-topaz.vercel.app/`)
- `--collection-name`: Qdrant collection name (default: `rag_embedding`)
- `--log-level`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) (default: `INFO`)
- `--dry-run`: Run the pipeline without saving to Qdrant
- `--min-chunk-size`: Minimum words per chunk (default: 500)
- `--max-chunk-size`: Maximum words per chunk (default: 800)
- `--chunk-overlap`: Overlap in words between chunks (default: 100)
- `--max-api-calls-per-minute`: Maximum Cohere API calls per minute (default: 100)

### Examples

Run with custom settings:
```bash
python main.py --target-url "https://example-book.com" --min-chunk-size 300 --max-chunk-size 600
```

Perform a dry run (processes content but doesn't save to Qdrant):
```bash
python main.py --dry-run --log-level DEBUG
```

## Architecture

The pipeline consists of the following components:

1. **URL Extraction**: Extracts all URLs from the target site using sitemap.xml
2. **Content Extraction**: Extracts clean text content from each URL
3. **Text Chunking**: Splits content into configurable segments with metadata preservation
4. **Embedding Generation**: Creates vector embeddings using Cohere API
5. **Storage**: Saves embeddings and metadata to Qdrant vector database
6. **Idempotency**: Ensures the pipeline can be safely rerun without creating duplicates

## Configuration

The pipeline supports the following configuration options:

- **Chunking parameters**: Control how text is split into segments
- **Rate limiting**: Configure API call limits to respect free-tier quotas
- **Logging**: Adjust verbosity for monitoring and debugging
- **Dry run**: Test the pipeline without making changes to the database

## Idempotency

The pipeline is designed to be idempotent, meaning it can be safely run multiple times without creating duplicate entries. This is achieved by:

1. Using a combination of source URL and content hash as the unique identifier
2. Checking if a chunk already exists in Qdrant before saving
3. Skipping chunks that already exist

## Error Handling

The pipeline includes comprehensive error handling:

- Network timeouts and retries for content extraction
- Exponential backoff for API calls
- Graceful degradation when individual chunks fail
- Detailed logging for troubleshooting

## Retrieval and Validation

The retrieval system enables similarity search against the stored vectors and provides validation metrics:

### CLI Usage

Execute similarity searches from the command line:

```bash
# Retrieve top 5 similar chunks
python -m cli.retrieval_cli --query "What is embodied AI?" --top-k 5

# Retrieve with validation metrics
python -m cli.retrieval_cli --query "Explain robot navigation" --top-k 10 --validate

# Export results to JSON
python -m cli.retrieval_cli --query "How does SLAM work?" --top-k 5 --output results.json
```

### API Usage

Start the API server:

```bash
uvicorn api.retrieval_api:app --host 0.0.0.0 --port 8000
```

Then use the API endpoints:

```bash
# Execute similarity search
curl -X POST "http://localhost:8000/retrieval/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main concept of embodied AI?",
    "top_k": 5,
    "threshold": 0.5,
    "validate": true
  }'
```

### Programmatic Usage

Use the retrieval functions directly in Python:

```python
from rag_retrieval import retrieve_similar_chunks, calculate_validation_metrics

# Execute retrieval
results = retrieve_similar_chunks("What is embodied AI?", top_k=5)

# Calculate validation metrics
metrics = calculate_validation_metrics(
    query_id="test_query",
    results=results,
    relevant_chunk_ids=["expected_chunk_id_1", "expected_chunk_id_2"]
)
```

## Monitoring

The pipeline tracks and reports the following metrics:

- Number of URLs processed
- Number of text chunks created
- Number of embeddings generated
- Processing errors encountered
- Pipeline execution time