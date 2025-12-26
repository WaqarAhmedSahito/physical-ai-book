"""
Pydantic models for the RAG Agent API.

This module defines the data models used for request and response validation
in the RAG Agent API endpoints.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class MatchedChunk(BaseModel):
    """Represents a chunk of content that was matched during the retrieval process."""
    content: str = Field(..., min_length=1, description="Content of the matched chunk")
    source_url: str = Field(..., description="URL of the source document")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score of the match (0.0 to 1.0)")


class QueryRequest(BaseModel):
    """Represents a user query submitted to the RAG agent."""
    query: str = Field(..., min_length=1, max_length=2000, description="The user's question or query text")
    stream: bool = Field(False, description="Whether to stream responses")


class AgentResponse(BaseModel):
    """Represents the response from the RAG agent after processing a query."""
    answer: str = Field(..., min_length=1, description="The agent's response to the query")
    sources: List[str] = Field(..., description="URLs of documents used as sources")
    matched_chunks: List[MatchedChunk] = Field(..., description="Chunks of content that were matched during retrieval")
    query_time_ms: float = Field(..., gt=0, description="Time taken to process the query in milliseconds")
    confidence: str = Field(..., pattern=r"^(high|medium|low)$", description="Confidence level of the response")


class ConnectionStatus(BaseModel):
    """Represents the connection status between frontend and backend."""
    status: str = Field(..., pattern=r"^(connected|disconnected|error)$", description="Current connection status")
    backend_url: str = Field(..., description="URL of the backend service")
    last_checked: str = Field(..., description="ISO timestamp of last status check")