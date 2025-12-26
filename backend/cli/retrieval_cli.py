#!/usr/bin/env python3
"""
CLI interface for the RAG retrieval validation system.

This module provides command-line tools to:
- Execute similarity searches against Qdrant
- Validate retrieval quality with metrics
- Export results to various formats
"""
import argparse
import json
import sys
import logging
from typing import List, Dict, Any

from rag_retrieval import retrieve_similar_chunks, calculate_validation_metrics, batch_validate_results


def setup_logging(verbosity: int):
    """Set up logging based on verbosity level."""
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def retrieve_and_print(query: str, top_k: int, threshold: float, validate: bool, expected_chunks: List[str] = None):
    """Execute retrieval and print results."""
    try:
        print(f"Query: {query}")
        print(f"Retrieving top {top_k} chunks with threshold {threshold}...")

        results = retrieve_similar_chunks(
            query_text=query,
            top_k=top_k,
            threshold=threshold
        )

        print(f"\nFound {len(results)} similar chunks:\n")

        for result in results:
            print(f"Rank {result.rank}: (Score: {result.similarity_score:.3f})")
            print(f"  Source: {result.source_url}")
            if result.section_title:
                print(f"  Section: {result.section_title}")
            if result.page_number is not None:
                print(f"  Page: {result.page_number}")
            print(f"  Content preview: {result.content[:200]}...")
            print()

        if validate and expected_chunks:
            print("Validating results...")
            validation_results = batch_validate_results(results, expected_chunks)
            relevant_count = sum(1 for vr in validation_results if vr.is_relevant)
            print(f"Relevant results: {relevant_count}/{len(validation_results)}")

            # Calculate and display metrics
            metrics = calculate_validation_metrics(
                query_id="cli_query",
                results=results,
                relevant_chunk_ids=expected_chunks if expected_chunks else []
            )

            print(f"\nValidation Metrics:")
            print(f"  Precision@5: {metrics.precision_at_k.get(5, 0):.3f}")
            print(f"  Recall@5: {metrics.recall_at_k.get(5, 0):.3f}")
            print(f"  MRR: {metrics.mrr:.3f}")
            print(f"  Hit Rate: {metrics.hit_rate:.3f}")
            print(f"  Avg Similarity: {metrics.avg_similarity_score:.3f}")

        return results

    except Exception as e:
        print(f"Error during retrieval: {str(e)}", file=sys.stderr)
        return None


def export_results(results: List, output_file: str, format: str = "json"):
    """Export results to a file in specified format."""
    if not results:
        print("No results to export", file=sys.stderr)
        return

    try:
        if format.lower() == "json":
            # Convert results to JSON-serializable format
            serializable_results = []
            for result in results:
                serializable_results.append({
                    "chunk_id": result.chunk_id,
                    "content": result.content,
                    "source_url": result.source_url,
                    "section_title": result.section_title,
                    "page_number": result.page_number,
                    "similarity_score": result.similarity_score,
                    "rank": result.rank
                })

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "results": serializable_results,
                    "count": len(serializable_results)
                }, f, indent=2, ensure_ascii=False)

            print(f"Results exported to {output_file}")

        else:
            print(f"Unsupported format: {format}", file=sys.stderr)

    except Exception as e:
        print(f"Error exporting results: {str(e)}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for RAG retrieval validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "What is embodied AI?" --top-k 5
  %(prog)s --query "Explain robot navigation" --top-k 10 --threshold 0.5 --validate
  %(prog)s --query "How does SLAM work?" --top-k 5 --output results.json
        """
    )

    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Text query for similarity search"
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of results to return (default: 5)"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.0,
        help="Minimum similarity score threshold (default: 0.0)"
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Calculate validation metrics"
    )

    parser.add_argument(
        "--expected-chunks",
        type=str,
        nargs="*",
        help="Expected relevant chunk IDs for validation"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file path for results"
    )

    parser.add_argument(
        "--format",
        type=str,
        default="json",
        choices=["json"],
        help="Output format (default: json)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (use -v, -vv, or -vvv for more detail)"
    )

    args = parser.parse_args()

    # Set up logging
    setup_logging(args.verbose)

    # Execute retrieval
    results = retrieve_and_print(
        query=args.query,
        top_k=args.top_k,
        threshold=args.threshold,
        validate=args.validate,
        expected_chunks=args.expected_chunks
    )

    # Export results if output file specified
    if args.output and results:
        export_results(results, args.output, args.format)


if __name__ == "__main__":
    main()