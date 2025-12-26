"""
Data models for the RAG retrieval validation system.

This module defines the core data entities used in the retrieval process:
- Query: Represents a text query that will be used for similarity search
- RetrievalResult: Represents a single result from the similarity search
- ValidationResult: Captures the validation assessment of a retrieval result
- ValidationMetrics: Aggregates metrics for evaluating retrieval performance
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
import uuid


@dataclass
class Query:
    """
    Represents a text query that will be used for similarity search against the vector database.

    Fields:
    - id: Unique identifier for the query
    - text: The actual query text
    - embedding: Vector representation of the query text (1024-dimensional for Cohere)
    - created_at: Timestamp when the query was created
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    text: str = ""
    embedding: Optional[List[float]] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the query after initialization."""
        if not self.text or not self.text.strip():
            raise ValueError("Query text must not be empty")

        if self.embedding is not None:
            if len(self.embedding) != 1024:
                raise ValueError(f"Embedding must have exactly 1024 dimensions, got {len(self.embedding)}")

        if not isinstance(self.created_at, datetime):
            raise ValueError("created_at must be a valid datetime object")


@dataclass
class RetrievalResult:
    """
    Represents a single result from the similarity search, containing the matched text chunk and its metadata.

    Fields:
    - chunk_id: Unique identifier of the matched text chunk
    - content: The text content of the chunk
    - source_url: The URL where the content originated
    - section_title: Title of the section where the content appears
    - page_number: Page number in the original document
    - similarity_score: Cosine similarity score between query and result
    - rank: Position in the ranked results (1-indexed)
    """
    chunk_id: str
    content: str
    source_url: str
    section_title: Optional[str] = None
    page_number: Optional[int] = None
    similarity_score: float = 0.0
    rank: int = 1

    def __post_init__(self):
        """Validate the retrieval result after initialization."""
        if not self.content or not self.content.strip():
            raise ValueError("Content must not be empty")

        if not self.source_url:
            raise ValueError("Source URL must not be empty")

        if not (0 <= self.similarity_score <= 1):
            raise ValueError(f"Similarity score must be between 0 and 1, got {self.similarity_score}")

        if self.rank <= 0:
            raise ValueError(f"Rank must be a positive integer, got {self.rank}")


@dataclass
class ValidationResult:
    """
    Captures the validation assessment of a retrieval result against expected criteria.

    Fields:
    - result_id: Reference to the RetrievalResult being validated
    - is_relevant: Whether the result is relevant to the query
    - relevance_score: Subjective relevance score (0-1)
    - validation_criteria: List of criteria used for validation
    - notes: Additional notes about the validation
    - validated_at: Timestamp when validation was performed
    """
    result_id: str
    is_relevant: bool
    relevance_score: float = 1.0
    validation_criteria: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    validated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the validation result after initialization."""
        if not self.result_id:
            raise ValueError("Result ID must not be empty")

        if not (0 <= self.relevance_score <= 1):
            raise ValueError(f"Relevance score must be between 0 and 1, got {self.relevance_score}")

        if not isinstance(self.validated_at, datetime):
            raise ValueError("validated_at must be a valid datetime object")


@dataclass
class ValidationMetrics:
    """
    Aggregates metrics for evaluating the overall performance of the retrieval system.

    Fields:
    - query_id: Reference to the query being evaluated
    - precision_at_k: Precision at different k values (e.g., {5: 0.8, 10: 0.7})
    - recall_at_k: Recall at different k values
    - mrr: Mean Reciprocal Rank
    - hit_rate: Proportion of queries with at least one relevant result
    - avg_similarity_score: Average similarity score of top results
    - total_results: Total number of results evaluated
    - relevant_results: Number of relevant results
    - calculated_at: Timestamp when metrics were calculated
    """
    query_id: str
    precision_at_k: Dict[int, float] = field(default_factory=dict)
    recall_at_k: Dict[int, float] = field(default_factory=dict)
    mrr: float = 0.0
    hit_rate: float = 0.0
    avg_similarity_score: float = 0.0
    total_results: int = 0
    relevant_results: int = 0
    calculated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the validation metrics after initialization."""
        if not self.query_id:
            raise ValueError("Query ID must not be empty")

        # Validate all score values are between 0 and 1
        for score in self.precision_at_k.values():
            if not (0 <= score <= 1):
                raise ValueError(f"Precision score must be between 0 and 1, got {score}")

        for score in self.recall_at_k.values():
            if not (0 <= score <= 1):
                raise ValueError(f"Recall score must be between 0 and 1, got {score}")

        if not (0 <= self.mrr <= 1):
            raise ValueError(f"MRR must be between 0 and 1, got {self.mrr}")

        if not (0 <= self.hit_rate <= 1):
            raise ValueError(f"Hit rate must be between 0 and 1, got {self.hit_rate}")

        if not (0 <= self.avg_similarity_score <= 1):
            raise ValueError(f"Average similarity score must be between 0 and 1, got {self.avg_similarity_score}")

        if self.total_results < 0:
            raise ValueError(f"Total results must be non-negative, got {self.total_results}")

        if self.relevant_results < 0:
            raise ValueError(f"Relevant results must be non-negative, got {self.relevant_results}")

        if self.relevant_results > self.total_results:
            raise ValueError(f"Relevant results ({self.relevant_results}) cannot exceed total results ({self.total_results})")

        if not isinstance(self.calculated_at, datetime):
            raise ValueError("calculated_at must be a valid datetime object")