# RAG Agent

This module implements a Retrieval-Augmented Generation (RAG) agent that combines OpenAI's GPT models with your custom knowledge base. The agent retrieves relevant documents from your vector database before generating responses to ensure answers are grounded in your specific content.

## Features

- **RAG Integration**: Retrieves relevant documents before generating responses
- **OpenAI Integration**: Uses OpenAI's GPT models for response generation
- **Synchronous Support**: Handles synchronous queries (simplified implementation)
- **Confidence Scoring**: Provides confidence levels based on similarity scores
- **Source Citations**: Cites sources used in generating responses

## Prerequisites

Before running the agent, ensure you have:

1. **Python Environment**: Python 3.8+ with required packages installed
2. **Environment Variables**: Set up your `.env` file with:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `COHERE_API_KEY`: Your Cohere API key (for embeddings)
   - `QDRANT_URL`: Your Qdrant vector database URL
   - `QDRANT_API_KEY`: Your Qdrant API key (if using cloud)
3. **Vector Database**: A populated Qdrant collection with your documents
4. **Ingested Content**: Run the main.py script to populate your vector database first

## Installation

1. Install required dependencies:
   ```bash
   pip install openai cohere qdrant-client python-dotenv beautifulsoup4
   ```

2. Make sure your `.env` file contains all required API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## How to Run the Agent

### Method 1: Run the agent directly with example queries
```bash
cd backend
python agent.py
```

This will run the agent with example queries and show the results.

### Method 2: Use the agent in your own code
```python
from agent import RAGAgent

# Initialize the agent
agent = RAGAgent()

# Query the agent
response = agent.query_agent("Your question here")

# The response includes:
# - answer: The generated response
# - sources: List of sources used
# - matched_chunks: Retrieved chunks with similarity scores
# - query_time_ms: Time taken to process the query
# - confidence: Confidence level (high/medium/low)
```

### Method 3: Use the convenience function
```python
from agent import query_agent

# Query directly
response = query_agent("What is ROS2?")
print(f"Answer: {response['answer']}")
print(f"Sources: {response['sources']}")
```

## Architecture

- `RAGAgent`: Main class that manages OpenAI client and RAG functionality
- `retrieve_information`: Function that queries the vector database using rag_retrieval
- `query_agent`: Main method that orchestrates retrieval and generation
- `query_agent`: Convenience function for direct usage

## Configuration

The agent requires:
- Environment variables loaded via `.env` file
- Access to the RAG retrieval system via `rag_retrieval.retrieval.retrieve_similar_chunks`
- OpenAI API access for response generation

## Example Queries

The main function includes example queries for testing:
- "What is ROS2?"
- "Explain humanoid design principles"
- "How does VLA work?"
- "What are simulation techniques?"
- "Explain AI control systems"

## Troubleshooting

### Common Issues:

1. **Missing API Keys**: Make sure all required environment variables are set in your `.env` file
2. **Vector Database Not Populated**: Run `python main.py` first to populate your Qdrant collection
3. **Connection Issues**: Verify your Qdrant URL and API key are correct
4. **OpenAI API Error**: Check your OpenAI API key and ensure you have sufficient credits

### Debugging:

- Check the logs for detailed error messages
- Verify that your Qdrant collection exists and has data
- Ensure your `.env` file is in the correct directory and loaded properly

## Dependencies

- OpenAI Python library
- Cohere Python library
- Qdrant Python client
- python-dotenv for environment variable management
- beautifulsoup4 for content extraction (if needed)

