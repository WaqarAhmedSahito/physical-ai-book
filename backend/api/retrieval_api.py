"""
API endpoints for the RAG retrieval validation system and agent functionality.

This module implements the REST API endpoints as specified in the contract:
- POST /retrieval/query: Execute similarity search
- POST /retrieval/validate: Run validation on queries
- GET /retrieval/collections: Get collection information
- POST /agent/query: Process user queries through RAG agent
- GET /agent/health: Check agent service health
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from pydantic import BaseModel, Field
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:
    # If FastAPI is not available, provide a message
    print("FastAPI and related packages are required for the API endpoints.")
    print("Install with: pip install fastapi uvicorn python-multipart")
    raise


from rag_retrieval import retrieve_similar_chunks, calculate_validation_metrics, batch_validate_results

# Import the new models for agent functionality
from .models import QueryRequest as AgentQueryRequest, AgentResponse, MatchedChunk

# Import the RAG Agent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent import RAGAgent

def query_agent(query_text: str):
    """
    Convenience function to query the RAG agent with error handling for missing API keys
    """
    try:
        agent = RAGAgent()
        return agent.query_agent(query_text)
    except ValueError as e:
        # Handle API key errors by returning a mock response
        if "API_KEY" in str(e).upper():
            return {
                "answer": "This is a mock response for testing. The actual agent requires API keys to function.",
                "sources": ["https://example.com/mock-source"],
                "matched_chunks": [
                    {
                        "content": "This is mock content for testing purposes",
                        "source_url": "https://example.com/mock-source",
                        "similarity_score": 0.8
                    }
                ],
                "query_time_ms": 100.0,
                "confidence": "medium",
                "error": str(e)
            }
        else:
            raise e


# Pydantic models for retrieval request/response validation
class RetrievalQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="The text query to search for similar content")
    top_k: int = Field(5, ge=1, le=20, description="Number of results to return (default: 5, max: 20)")
    threshold: float = Field(0.0, ge=0.0, le=1.0, description="Minimum similarity score threshold (default: 0.0)")
    collection_name: str = Field("rag_embedding", description="Qdrant collection to search (default: 'rag_embedding')")
    validate: bool = Field(False, description="Whether to calculate validation metrics (default: false)")


class RetrievalResult(BaseModel):
    chunk_id: str
    content: str
    source_url: str
    section_title: Optional[str] = None
    page_number: Optional[int] = None
    similarity_score: float
    rank: int


class SearchMetadata(BaseModel):
    total_results: int
    search_time_ms: int
    query_embedding_dimension: int = 1024


class ValidationMetrics(BaseModel):
    precision_at_k: Dict[int, float]
    recall_at_k: Dict[int, float]
    mrr: float
    hit_rate: float
    avg_similarity_score: float
    total_results: int
    relevant_results: int
    calculated_at: str


class QueryResponse(BaseModel):
    query_id: str
    query_text: str
    results: List[RetrievalResult]
    search_metadata: SearchMetadata
    validation_metrics: Optional[ValidationMetrics] = None


class ValidationQuery(BaseModel):
    query: str
    expected_chunks: List[str]


class ValidateRequest(BaseModel):
    queries: List[ValidationQuery]
    top_k: int = Field(10, ge=1, le=20, description="Number of results to consider for validation (default: 10)")


class ValidationResultItem(BaseModel):
    query_id: str
    query_text: str
    retrieved_chunks: List[str]
    relevant_retrieved: int
    total_expected: int
    metrics: ValidationMetrics


class ValidateResponse(BaseModel):
    validation_id: str
    total_queries: int
    results: List[ValidationResultItem]
    aggregate_metrics: Dict[str, float]
    completed_at: str


class CollectionInfo(BaseModel):
    name: str
    vector_size: int
    distance: str
    point_count: int
    created_at: str


class CollectionsResponse(BaseModel):
    collections: List[CollectionInfo]


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="RAG Retrieval Validation API",
        description="API for executing similarity searches and validating RAG retrieval quality",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, configure specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/retrieval/query", response_model=QueryResponse)
    async def retrieval_query(request: RetrievalQueryRequest):
        """Execute a similarity search against the vector database with the provided query."""
        try:
            import time
            start_time = time.time()

            # Execute the retrieval
            results = retrieve_similar_chunks(
                query_text=request.query,
                top_k=request.top_k,
                threshold=request.threshold,
                collection_name=request.collection_name
            )

            # Calculate search time
            search_time_ms = int((time.time() - start_time) * 1000)

            # Prepare the response results
            response_results = []
            for result in results:
                response_results.append(RetrievalResult(
                    chunk_id=result.chunk_id,
                    content=result.content,
                    source_url=result.source_url,
                    section_title=result.section_title,
                    page_number=result.page_number,
                    similarity_score=result.similarity_score,
                    rank=result.rank
                ))

            # Prepare search metadata
            search_metadata = SearchMetadata(
                total_results=len(response_results),
                search_time_ms=search_time_ms,
                query_embedding_dimension=1024
            )

            # Prepare base response
            response = QueryResponse(
                query_id=f"query_{int(datetime.now().timestamp())}",
                query_text=request.query,
                results=response_results,
                search_metadata=search_metadata
            )

            # Add validation metrics if requested
            if request.validate:
                # For validation, we need expected relevant chunks - in a real scenario,
                # these would come from a test dataset or be provided by the user
                expected_chunks = []  # In real usage, you might have expected chunks for validation
                validation_metrics = calculate_validation_metrics(
                    query_id=response.query_id,
                    results=results,
                    relevant_chunk_ids=expected_chunks,
                    k_values=[5, 10]
                )

                response.validation_metrics = ValidationMetrics(
                    precision_at_k=validation_metrics.precision_at_k,
                    recall_at_k=validation_metrics.recall_at_k,
                    mrr=validation_metrics.mrr,
                    hit_rate=validation_metrics.hit_rate,
                    avg_similarity_score=validation_metrics.avg_similarity_score,
                    total_results=validation_metrics.total_results,
                    relevant_results=validation_metrics.relevant_results,
                    calculated_at=validation_metrics.calculated_at.isoformat()
                )

            return response

        except ValueError as e:
            logger.error(f"Invalid request parameters: {str(e)}")
            raise HTTPException(status_code=400, detail={
                "error": {
                    "code": "INVALID_PARAMETERS",
                    "message": str(e),
                    "details": {"request": request.dict()}
                }
            })
        except Exception as e:
            logger.error(f"Error during retrieval: {str(e)}")
            raise HTTPException(status_code=500, detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal error occurred during retrieval"
                }
            })


    @app.post("/retrieval/validate", response_model=ValidateResponse)
    async def retrieval_validate(request: ValidateRequest):
        """Run validation on a set of queries to evaluate retrieval quality."""
        try:
            import time
            start_time = time.time()
            validation_id = f"validation_{int(datetime.now().timestamp())}"

            results = []
            total_precision_5 = 0
            total_recall_5 = 0
            total_mrr = 0
            queries_with_hits = 0

            for query_item in request.queries:
                # Execute retrieval for this query
                retrieval_results = retrieve_similar_chunks(
                    query_text=query_item.query,
                    top_k=request.top_k,
                    threshold=0.0,  # No threshold for validation to get full results
                    collection_name="rag_embedding"
                )

                # Calculate validation metrics
                validation_metrics = calculate_validation_metrics(
                    query_id=f"query_{len(results)}",
                    results=retrieval_results,
                    relevant_chunk_ids=query_item.expected_chunks,
                    k_values=[5, 10]
                )

                # Prepare the result item
                result_item = ValidationResultItem(
                    query_id=f"query_{len(results)}",
                    query_text=query_item.query,
                    retrieved_chunks=[r.chunk_id for r in retrieval_results],
                    relevant_retrieved=validation_metrics.relevant_results,
                    total_expected=len(query_item.expected_chunks),
                    metrics=ValidationMetrics(
                        precision_at_k=validation_metrics.precision_at_k,
                        recall_at_k=validation_metrics.recall_at_k,
                        mrr=validation_metrics.mrr,
                        hit_rate=validation_metrics.hit_rate,
                        avg_similarity_score=validation_metrics.avg_similarity_score,
                        total_results=validation_metrics.total_results,
                        relevant_results=validation_metrics.relevant_results,
                        calculated_at=validation_metrics.calculated_at.isoformat()
                    )
                )

                results.append(result_item)

                # Accumulate metrics for aggregate calculation
                if 5 in validation_metrics.precision_at_k:
                    total_precision_5 += validation_metrics.precision_at_k[5]
                if 5 in validation_metrics.recall_at_k:
                    total_recall_5 += validation_metrics.recall_at_k[5]
                total_mrr += validation_metrics.mrr
                if validation_metrics.hit_rate > 0:
                    queries_with_hits += 1

            # Calculate aggregate metrics
            num_queries = len(request.queries)
            aggregate_metrics = {
                "avg_precision_at_5": total_precision_5 / num_queries if num_queries > 0 else 0,
                "avg_recall_at_5": total_recall_5 / num_queries if num_queries > 0 else 0,
                "overall_mrr": total_mrr / num_queries if num_queries > 0 else 0,
                "hit_rate": queries_with_hits / num_queries if num_queries > 0 else 0
            }

            response = ValidateResponse(
                validation_id=validation_id,
                total_queries=num_queries,
                results=results,
                aggregate_metrics=aggregate_metrics,
                completed_at=datetime.now().isoformat()
            )

            return response

        except ValueError as e:
            logger.error(f"Invalid validation request: {str(e)}")
            raise HTTPException(status_code=400, detail={
                "error": {
                    "code": "INVALID_PARAMETERS",
                    "message": str(e)
                }
            })
        except Exception as e:
            logger.error(f"Error during validation: {str(e)}")
            raise HTTPException(status_code=500, detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal error occurred during validation"
                }
            })


    @app.get("/retrieval/collections", response_model=CollectionsResponse)
    async def get_collections():
        """Get information about available collections for retrieval."""
        try:
            from qdrant_client import QdrantClient
            from dotenv import load_dotenv
            import os

            load_dotenv()

            qdrant_url = os.getenv("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY")

            if not qdrant_url:
                raise HTTPException(status_code=500, detail={
                    "error": {
                        "code": "CONFIG_ERROR",
                        "message": "Qdrant URL not configured"
                    }
                })

            # Initialize Qdrant client
            if qdrant_api_key:
                client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            else:
                client = QdrantClient(url=qdrant_url)

            # Get list of collections
            collections_response = client.get_collections()
            collections = []

            for collection in collections_response.collections:
                # Get collection details
                collection_info = client.get_collection(collection.name)

                collection_model = CollectionInfo(
                    name=collection.name,
                    vector_size=collection_info.config.params.vectors.size,
                    distance=collection_info.config.params.vectors.distance.name,
                    point_count=collection_info.points_count,
                    created_at=datetime.now().isoformat()  # Simplified - in real scenario, would get actual creation time
                )

                collections.append(collection_model)

            return CollectionsResponse(collections=collections)

        except Exception as e:
            logger.error(f"Error getting collections: {str(e)}")
            raise HTTPException(status_code=500, detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An error occurred while retrieving collections"
                }
            })

    @app.post("/agent/query", response_model=AgentResponse)
    async def agent_query(request: AgentQueryRequest):
        """Process a user query through the RAG agent and return the response."""
        try:
            import time
            start_time = time.time()

            # Process the query through the RAG agent
            response = query_agent(request.query)

            # Calculate total processing time (including the time spent in query_agent)
            total_time_ms = (time.time() - start_time) * 1000

            # Create the AgentResponse object
            agent_response = AgentResponse(
                answer=response["answer"],
                sources=response["sources"],
                matched_chunks=[
                    MatchedChunk(
                        content=chunk["content"],
                        source_url=chunk["source_url"],
                        similarity_score=chunk["similarity_score"]
                    ) for chunk in response["matched_chunks"]
                ],
                query_time_ms=response.get("query_time_ms", total_time_ms),
                confidence=response.get("confidence", "unknown")
            )

            return agent_response

        except ValueError as e:
            logger.error(f"Invalid request parameters: {str(e)}")
            raise HTTPException(status_code=400, detail={
                "error": {
                    "code": "INVALID_PARAMETERS",
                    "message": str(e),
                    "details": {"request": request.dict()}
                }
            })
        except Exception as e:
            logger.error(f"Error during agent query processing: {str(e)}")
            # If it's an API key error, provide a more specific response
            error_msg = str(e)
            if "API_KEY" in error_msg.upper() or "KEY" in error_msg.upper():
                # Return a mock response for testing purposes when API keys are missing
                mock_response = AgentResponse(
                    answer="This is a mock response for testing. The actual agent requires API keys to function.",
                    sources=["https://example.com/mock-source"],
                    matched_chunks=[
                        MatchedChunk(
                            content="This is mock content for testing purposes",
                            source_url="https://example.com/mock-source",
                            similarity_score=0.8
                        )
                    ],
                    query_time_ms=100.0,
                    confidence="medium"
                )
                return mock_response
            else:
                raise HTTPException(status_code=500, detail={
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": "An internal error occurred during agent query processing"
                    }
                })

    @app.get("/agent/health")
    async def agent_health():
        """Check the health status of the agent service."""
        try:
            # Try to initialize the agent to verify it's working
            agent = RAGAgent()
            return {"status": "ok", "message": "Agent service is healthy"}
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Health check failed: {error_msg}")
            # Check if it's an API key error and return a different status
            if "API_KEY" in error_msg.upper() or "KEY" in error_msg.upper():
                return {"status": "warning", "message": f"Agent service is available but requires API keys: {str(e)}"}
            else:
                raise HTTPException(status_code=500, detail={
                    "error": {
                        "code": "HEALTH_CHECK_FAILED",
                        "message": "Agent service is not healthy"
                    }
                })

    return app


# For direct execution
if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)