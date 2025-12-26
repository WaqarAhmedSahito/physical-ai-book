# Quickstart: RAG Content Ingestion Pipeline

## Overview
This guide provides step-by-step instructions to set up and run the RAG content ingestion pipeline that extracts content from book URLs, generates embeddings using Cohere, and stores them in Qdrant.

## Prerequisites
- Python 3.11 or higher
- UV package manager
- Access to Cohere API (free tier sufficient)
- Access to Qdrant vector database (cloud or local instance)

## Setup Instructions

### 1. Clone and Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
```

### 4. Configure Environment Variables
Create a `.env` file in the backend directory:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here  # if using cloud
```

## Running the Pipeline

### 1. Execute the Pipeline
```bash
python main.py
```

### 2. Monitor the Process
The pipeline will:
1. Extract all URLs from https://physical-ai-book-topaz.vercel.app/
2. Process each URL to extract text content
3. Chunk the text while preserving metadata
4. Generate embeddings using Cohere
5. Create the "rag_embedding" collection in Qdrant
6. Store all embeddings with metadata

## Expected Output
Upon successful completion, you should see:
- Processed URL count
- Number of text chunks created
- Number of embeddings generated
- Confirmation that data is stored in Qdrant

## Validation
To verify the pipeline worked correctly:
1. Check that all URLs from the source were processed
2. Verify that the "rag_embedding" collection exists in Qdrant
3. Confirm that embeddings are queryable in Qdrant

## Troubleshooting
- If you encounter API rate limits, add delays between requests
- If URLs fail to load, check network connectivity and URL validity
- If embeddings fail, verify your Cohere API key and quota
- If Qdrant storage fails, check your connection and credentials