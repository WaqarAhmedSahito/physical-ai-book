# Quickstart: RAG Retrieval Pipeline Validation

## Overview

This guide provides instructions for setting up and using the RAG retrieval validation system. The system allows you to execute similarity searches against the Qdrant vector database and validate the quality of retrieved results.

## Prerequisites

- Python 3.11+
- pip package manager
- Access to Cohere API (API key)
- Access to Qdrant vector database (URL and API key if secured)

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd physical-ai-book
```

### 2. Set up Python Virtual Environment
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If no requirements.txt exists, install the required packages:
```bash
pip install cohere qdrant-client python-dotenv requests beautifulsoup4
```

### 4. Configure Environment Variables
Create a `.env` file in the backend directory with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here  # Optional if Qdrant is not secured
```

## Running Retrieval Validation

### 1. Basic Retrieval
To execute a simple retrieval query:

```bash
python -m cli.retrieval_cli --query "your query text here"
```

### 2. Validation with Metrics
To run validation with metrics calculation:

```bash
python -m cli.retrieval_cli --validate --query "your query text here" --top-k 10
```

### 3. Batch Validation
To run validation on multiple queries:

```bash
python -m cli.retrieval_cli --batch-validate --queries-file path/to/queries.json
```

## CLI Usage Examples

### Simple Query
```bash
# Retrieve top 5 most similar chunks
python -m cli.retrieval_cli --query "What is the main concept of embodied AI?" --top-k 5
```

### Detailed Validation
```bash
# Retrieve with validation metrics
python -m cli.retrieval_cli --query "Explain robot navigation algorithms" --top-k 10 --validate
```

### Export Results
```bash
# Export results to JSON file
python -m cli.retrieval_cli --query "How does SLAM work?" --top-k 5 --output results.json
```

### Advanced Options
```bash
# With custom similarity threshold
python -m cli.retrieval_cli --query "What are the ethical considerations in AI?" --top-k 20 --threshold 0.5 --validate
```

## Programmatic Usage

### Basic Retrieval
```python
from rag_retrieval.retrieval import retrieve_similar_chunks

query = "What is the main concept of embodied AI?"
results = retrieve_similar_chunks(query, top_k=5)

for result in results:
    print(f"Score: {result.similarity_score}")
    print(f"Content: {result.content[:200]}...")
    print(f"Source: {result.source_url}")
    print("---")
```

### Validation
```python
from rag_retrieval.validation import calculate_validation_metrics

query = "Explain robot navigation algorithms"
results = retrieve_similar_chunks(query, top_k=10)

# Calculate validation metrics
metrics = calculate_validation_metrics(query, results)
print(f"Precision@10: {metrics.precision_at_k[10]}")
print(f"MRR: {metrics.mrr}")
print(f"Hit Rate: {metrics.hit_rate}")
```

## Configuration Options

### CLI Arguments
- `--query`: Text query for similarity search (required)
- `--top-k`: Number of results to return (default: 5)
- `--threshold`: Minimum similarity score threshold (default: 0.0)
- `--validate`: Calculate validation metrics (optional)
- `--output`: Output file path for results (optional)
- `--collection`: Qdrant collection name (default: rag_embedding)

### Environment Variables
- `COHERE_API_KEY`: API key for Cohere embedding service
- `QDRANT_URL`: URL for Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if secured)

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure API keys are correctly set in environment variables
   - Verify API keys have appropriate permissions

2. **Connection Errors**
   - Check Qdrant URL is accessible
   - Verify network connectivity to Qdrant instance

3. **Empty Results**
   - Confirm the `rag_embedding` collection has data
   - Verify the ingestion pipeline completed successfully

### Verification Steps
1. Test Cohere API connectivity:
   ```bash
   python -c "import cohere; co = cohere.Client('YOUR_KEY'); print(co.embed(texts=['test'], model='embed-english-v3.0'))"
   ```

2. Test Qdrant connectivity:
   ```bash
   python -c "from qdrant_client import QdrantClient; client = QdrantClient(url='YOUR_URL'); print(client.get_collections())"
   ```

3. Verify collection exists:
   ```bash
   python -c "from qdrant_client import QdrantClient; client = QdrantClient(url='YOUR_URL'); print(client.get_collection('rag_embedding'))"
   ```