"""
Validation functions for the RAG retrieval validation system.

This module implements:
- Precision@K calculation
- Recall@K calculation
- Mean Reciprocal Rank (MRR) calculation
- Hit rate calculation
- Aggregate validation metrics
"""
from typing import List, Dict, Tuple
from datetime import datetime
import logging

from .models import RetrievalResult, ValidationMetrics, ValidationResult

# Set up logging
logger = logging.getLogger(__name__)


def calculate_precision_at_k(results: List[RetrievalResult], relevant_chunk_ids: List[str], k: int) -> float:
    """
    Calculate precision at k (P@k) for the retrieval results.

    Precision@k = (number of relevant items in top k results) / k

    Args:
        results: List of retrieval results ordered by relevance
        relevant_chunk_ids: List of chunk IDs that are relevant to the query
        k: Number of top results to consider

    Returns:
        Precision at k value (0-1)
    """
    if not results or k <= 0:
        return 0.0

    # Get the top k results
    top_k_results = results[:k] if len(results) >= k else results

    # Count how many of the top k results are relevant
    relevant_count = 0
    for result in top_k_results:
        if result.chunk_id in relevant_chunk_ids:
            relevant_count += 1

    precision_at_k = relevant_count / k
    logger.debug(f"Precision@{k}: {precision_at_k} ({relevant_count}/{k})")
    return precision_at_k


def calculate_recall_at_k(results: List[RetrievalResult], relevant_chunk_ids: List[str], k: int) -> float:
    """
    Calculate recall at k (R@k) for the retrieval results.

    Recall@k = (number of relevant items in top k results) / (total number of relevant items)

    Args:
        results: List of retrieval results ordered by relevance
        relevant_chunk_ids: List of chunk IDs that are relevant to the query
        k: Number of top results to consider

    Returns:
        Recall at k value (0-1)
    """
    if not relevant_chunk_ids or not results or k <= 0:
        return 0.0

    # Get the top k results
    top_k_results = results[:k] if len(results) >= k else results

    # Count how many of the top k results are relevant
    relevant_in_top_k = 0
    for result in top_k_results:
        if result.chunk_id in relevant_chunk_ids:
            relevant_in_top_k += 1

    recall_at_k = relevant_in_top_k / len(relevant_chunk_ids)
    logger.debug(f"Recall@{k}: {recall_at_k} ({relevant_in_top_k}/{len(relevant_chunk_ids)})")
    return recall_at_k


def calculate_mrr(results: List[RetrievalResult], relevant_chunk_ids: List[str]) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR) for the retrieval results.

    MRR = average of (1 / rank of first relevant result for each query)

    Args:
        results: List of retrieval results ordered by relevance
        relevant_chunk_ids: List of chunk IDs that are relevant to the query

    Returns:
        Mean Reciprocal Rank value (0-1)
    """
    if not results or not relevant_chunk_ids:
        return 0.0

    # Find the rank of the first relevant result
    for rank, result in enumerate(results, start=1):
        if result.chunk_id in relevant_chunk_ids:
            reciprocal_rank = 1.0 / rank
            logger.debug(f"MRR: 1/{rank} = {reciprocal_rank}")
            return reciprocal_rank

    # If no relevant results found, MRR is 0
    logger.debug("MRR: 0 (no relevant results found)")
    return 0.0


def calculate_hit_rate(results: List[RetrievalResult], relevant_chunk_ids: List[str], threshold: float = 0.0) -> float:
    """
    Calculate hit rate - proportion of queries with at least one relevant result above threshold.

    Args:
        results: List of retrieval results ordered by relevance
        relevant_chunk_ids: List of chunk IDs that are relevant to the query
        threshold: Minimum similarity score threshold for relevance

    Returns:
        Hit rate value (0-1)
    """
    if not results or not relevant_chunk_ids:
        return 0.0

    # Check if any of the results are both relevant and above threshold
    for result in results:
        if result.chunk_id in relevant_chunk_ids and result.similarity_score >= threshold:
            logger.debug(f"Hit rate: 1 (found relevant result with score {result.similarity_score})")
            return 1.0

    logger.debug("Hit rate: 0 (no relevant results above threshold)")
    return 0.0


def calculate_average_similarity_score(results: List[RetrievalResult]) -> float:
    """
    Calculate the average similarity score of the results.

    Args:
        results: List of retrieval results

    Returns:
        Average similarity score
    """
    if not results:
        return 0.0

    total_score = sum(result.similarity_score for result in results)
    avg_score = total_score / len(results)
    logger.debug(f"Average similarity score: {avg_score}")
    return avg_score


def calculate_validation_metrics(
    query_id: str,
    results: List[RetrievalResult],
    relevant_chunk_ids: List[str],
    k_values: List[int] = None,
    threshold: float = 0.0
) -> ValidationMetrics:
    """
    Calculate comprehensive validation metrics for retrieval results.

    Args:
        query_id: ID of the query being evaluated
        results: List of retrieval results ordered by relevance
        relevant_chunk_ids: List of chunk IDs that are relevant to the query
        k_values: List of k values to calculate precision/recall for (default: [1, 3, 5, 10])
        threshold: Minimum similarity score threshold for relevance

    Returns:
        ValidationMetrics object with all calculated metrics
    """
    if k_values is None:
        k_values = [1, 3, 5, 10]

    # Calculate precision at different k values
    precision_at_k = {}
    for k in k_values:
        precision_at_k[k] = calculate_precision_at_k(results, relevant_chunk_ids, k)

    # Calculate recall at different k values
    recall_at_k = {}
    for k in k_values:
        recall_at_k[k] = calculate_recall_at_k(results, relevant_chunk_ids, k)

    # Calculate MRR
    mrr = calculate_mrr(results, relevant_chunk_ids)

    # Calculate hit rate
    hit_rate = calculate_hit_rate(results, relevant_chunk_ids, threshold)

    # Calculate average similarity score
    avg_similarity_score = calculate_average_similarity_score(results)

    # Count total and relevant results
    total_results = len(results)
    relevant_results = sum(1 for result in results if result.chunk_id in relevant_chunk_ids)

    # Create ValidationMetrics object
    metrics = ValidationMetrics(
        query_id=query_id,
        precision_at_k=precision_at_k,
        recall_at_k=recall_at_k,
        mrr=mrr,
        hit_rate=hit_rate,
        avg_similarity_score=avg_similarity_score,
        total_results=total_results,
        relevant_results=relevant_results,
        calculated_at=datetime.now()
    )

    logger.info(f"Calculated validation metrics for query {query_id}")
    logger.debug(f"Metrics - P@5: {precision_at_k.get(5, 0)}, R@5: {recall_at_k.get(5, 0)}, MRR: {mrr}, Hit Rate: {hit_rate}")

    return metrics


def validate_single_result(result: RetrievalResult, expected_chunk_id: str, threshold: float = 0.7) -> ValidationResult:
    """
    Validate a single retrieval result against an expected result.

    Args:
        result: The retrieval result to validate
        expected_chunk_id: The expected relevant chunk ID
        threshold: Minimum similarity score to consider relevant

    Returns:
        ValidationResult object with validation assessment
    """
    is_relevant = result.chunk_id == expected_chunk_id
    relevance_score = result.similarity_score if is_relevant else 0.0

    # Adjust relevance score based on similarity if it's the expected chunk
    if is_relevant and result.similarity_score < threshold:
        relevance_score = result.similarity_score  # Lower the score if below threshold
    elif is_relevant:
        relevance_score = min(1.0, result.similarity_score)  # Cap at 1.0 if above threshold

    validation_result = ValidationResult(
        result_id=result.chunk_id,
        is_relevant=is_relevant,
        relevance_score=relevance_score,
        validation_criteria=[f"Expected chunk ID: {expected_chunk_id}", f"Threshold: {threshold}"],
        notes=f"Result similarity: {result.similarity_score}"
    )

    logger.debug(f"Validated result {result.chunk_id}: relevant={is_relevant}, score={relevance_score}")
    return validation_result


def batch_validate_results(
    results: List[RetrievalResult],
    expected_chunk_ids: List[str],
    threshold: float = 0.7
) -> List[ValidationResult]:
    """
    Validate a batch of retrieval results against expected results.

    Args:
        results: List of retrieval results to validate
        expected_chunk_ids: List of expected relevant chunk IDs
        threshold: Minimum similarity score to consider relevant

    Returns:
        List of ValidationResult objects
    """
    validation_results = []

    for result in results:
        # Check if this result matches any expected chunk
        is_relevant = result.chunk_id in expected_chunk_ids
        relevance_score = 0.0

        if is_relevant:
            # If it's relevant, use the similarity score but adjust based on threshold
            relevance_score = min(1.0, max(0.0, result.similarity_score))
            if result.similarity_score < threshold:
                # Lower the relevance score if below threshold
                relevance_score = result.similarity_score * 0.5  # Penalize low-confidence relevant results

        validation_result = ValidationResult(
            result_id=result.chunk_id,
            is_relevant=is_relevant,
            relevance_score=relevance_score,
            validation_criteria=[f"Expected chunk IDs: {expected_chunk_ids}", f"Threshold: {threshold}"],
            notes=f"Result similarity: {result.similarity_score}, matched expected: {is_relevant}"
        )

        validation_results.append(validation_result)

    logger.info(f"Batch validated {len(validation_results)} results, {sum(1 for vr in validation_results if vr.is_relevant)} relevant")
    return validation_results