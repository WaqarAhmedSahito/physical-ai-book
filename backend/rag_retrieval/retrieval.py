"""
Core retrieval functions for the RAG retrieval validation system.

This module implements:
- Query embedding generation using Cohere
- Similarity search against Qdrant vector database
- Result ranking and metadata retrieval
"""
import os
import logging
from typing import List, Optional, Dict
from datetime import datetime
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

from .models import Query, RetrievalResult

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)


def load_config() -> Dict[str, str]:
    """
    Load configuration from environment variables.

    Returns:
        A dictionary with configuration values
    """
    return {
        "cohere_api_key": os.getenv("COHERE_API_KEY"),
        "qdrant_url": os.getenv("QDRANT_URL"),
        "qdrant_api_key": os.getenv("QDRANT_API_KEY"),
    }


def generate_query_embedding(query_text: str, model: str = "embed-english-v3.0") -> List[float]:
    """
    Generate embedding vector for query text using Cohere API.

    Args:
        query_text: The query text to generate embeddings for
        model: The embedding model to use (default: embed-english-v3.0)

    Returns:
        A list of floats representing the embedding vector (1024-dimensional)

    Raises:
        ValueError: If query text is empty or Cohere API key is not found
        Exception: If there's an error generating the embedding
    """
    if not query_text or not query_text.strip():
        raise ValueError("Query text must not be empty")

    config = load_config()
    api_key = config["cohere_api_key"]

    if not api_key:
        raise ValueError("Cohere API key not found in environment variables")

    try:
        co = cohere.Client(api_key)
        response = co.embed(
            texts=[query_text],
            model=model,
            input_type="search_query"  # Optimal for search queries in RAG applications
        )
        embedding = response.embeddings[0]  # Return the first (and only) embedding

        if len(embedding) != 1024:
            raise ValueError(f"Expected 1024-dimensional embedding, got {len(embedding)}")

        logger.debug(f"Generated {len(embedding)}-dimensional embedding for query: {query_text[:50]}...")
        return embedding

    except Exception as e:
        logger.error(f"Error generating embedding for query: {str(e)}")
        raise


def retrieve_similar_chunks(
    query_text: str,
    top_k: int = 5,
    threshold: float = 0.0,
    collection_name: str = "rag_embedding"
) -> List[RetrievalResult]:
    """
    Retrieve similar text chunks from Qdrant based on the query text.

    Args:
        query_text: The text query to search for similar content
        top_k: Number of results to return (default: 5)
        threshold: Minimum similarity score threshold (default: 0.0)
        collection_name: Name of the Qdrant collection to search (default: rag_embedding)

    Returns:
        A list of RetrievalResult objects containing the most similar chunks

    Raises:
        ValueError: If query text is empty or parameters are invalid
        Exception: If there's an error during retrieval
    """
    if not query_text or not query_text.strip():
        raise ValueError("Query text must not be empty")

    if top_k <= 0:
        raise ValueError(f"top_k must be positive, got {top_k}")

    if not (0 <= threshold <= 1):
        raise ValueError(f"threshold must be between 0 and 1, got {threshold}")

    try:
        # Generate embedding for the query
        logger.info(f"Generating embedding for query: {query_text[:100]}...")
        query_embedding = generate_query_embedding(query_text)

        # Initialize Qdrant client
        config = load_config()
        qdrant_url = config["qdrant_url"]
        qdrant_api_key = config["qdrant_api_key"]

        if not qdrant_url:
            raise ValueError("Qdrant URL not found in environment variables")

        # Initialize Qdrant client
        client_kwargs = {"url": qdrant_url}
        if qdrant_api_key:
            client_kwargs["api_key"] = qdrant_api_key
        
        client = QdrantClient(**client_kwargs)

        # Verify collection exists
        try:
            collection_info = client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' exists with {collection_info.points_count} points")
        except Exception:
            logger.error(f"Collection '{collection_name}' does not exist")
            raise ValueError(f"Collection '{collection_name}' does not exist in Qdrant")

        # Perform similarity search using query_points
        logger.info(f"Searching for top {top_k} similar chunks in '{collection_name}' collection")
        
        # For Qdrant client 1.16.2, query_points returns a QueryResponse object
        query_response = client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=top_k,
            score_threshold=threshold,
            with_payload=True
        )
        
        # Extract points from QueryResponse
        search_results = query_response.points
        
        logger.debug(f"Found {len(search_results)} search results")
        
        results = []
        for rank, hit in enumerate(search_results, start=1):
            payload = hit.payload
            
            # Extract metadata from payload
            chunk_id = payload.get("chunk_id", "")
            content = payload.get("content", "")
            
            # Use 'source_url' from payload (as seen in your test output)
            source_url = payload.get("source_url", "")
            
            section_title = payload.get("section_title", "")
            page_number = payload.get("page_number")
            similarity_score = float(hit.score)

            # Create RetrievalResult object
            result = RetrievalResult(
                chunk_id=chunk_id,
                content=content,
                source_url=source_url,
                section_title=section_title,
                page_number=page_number,
                similarity_score=similarity_score,
                rank=rank
            )

            results.append(result)
            logger.debug(f"Added result {rank}: score={similarity_score:.4f}, content preview: {content[:100]}...")

        logger.info(f"Retrieved {len(results)} similar chunks for query: {query_text[:50]}...")
        
        if not results:
            logger.warning(f"No results found for query: {query_text}")
        
        return results

    except Exception as e:
        logger.error(f"Error retrieving similar chunks: {str(e)}")
        raise

def create_query_with_embedding(query_text: str) -> Query:
    """
    Create a Query object with embedding generated from the text.

    Args:
        query_text: The text query to create

    Returns:
        A Query object with generated embedding and timestamp
    """
    embedding = generate_query_embedding(query_text)
    query = Query(
        text=query_text,
        embedding=embedding,
        created_at=datetime.now()
    )
    logger.debug(f"Created query object with embedding for: {query_text[:50]}...")
    return query