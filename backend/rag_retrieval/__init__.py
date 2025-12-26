"""
RAG Retrieval Validation Module

This package provides functionality for:
- Executing similarity searches against Qdrant vector database
- Validating retrieval quality and accuracy
- Calculating performance metrics for RAG systems
"""
from .models import Query, RetrievalResult, ValidationResult, ValidationMetrics
from .retrieval import generate_query_embedding, retrieve_similar_chunks, create_query_with_embedding
from .validation import (
    calculate_precision_at_k,
    calculate_recall_at_k,
    calculate_mrr,
    calculate_hit_rate,
    calculate_validation_metrics,
    validate_single_result,
    batch_validate_results
)

__all__ = [
    "Query",
    "RetrievalResult",
    "ValidationResult",
    "ValidationMetrics",
    "generate_query_embedding",
    "retrieve_similar_chunks",
    "create_query_with_embedding",
    "calculate_precision_at_k",
    "calculate_recall_at_k",
    "calculate_mrr",
    "calculate_hit_rate",
    "calculate_validation_metrics",
    "validate_single_result",
    "batch_validate_results"
]