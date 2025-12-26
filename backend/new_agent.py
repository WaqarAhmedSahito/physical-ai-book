import os
import json
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv
import openai
from openai import OpenAI
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retrieve_information(query: str) -> Dict:
    """
    Retrieve information from the knowledge base based on a query
    """
    # Import from the rag_retrieval package
    from rag_retrieval.retrieval import retrieve_similar_chunks

    try:
        # Call the existing retrieve_similar_chunks function from the rag_retrieval package
        results = retrieve_similar_chunks(query_text=query, top_k=5, threshold=0.3)

        # Format the results for the assistant
        formatted_results = []
        for result in results:
            formatted_results.append({
                'content': result.content,
                'url': result.source_url,
                'position': result.rank,
                'similarity_score': result.similarity_score
            })

        return {
            'query': query,
            'retrieved_chunks': formatted_results,
            'total_results': len(formatted_results)
        }
    except Exception as e:
        logger.error(f"Error in retrieve_information: {e}")
        return {
            'query': query,
            'retrieved_chunks': [],
            'total_results': 0,
            'error': str(e)
        }

class RAGAgent:
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=api_key)
        logger.info("RAG Agent initialized with OpenAI client")

    def query_agent(self, query_text: str) -> Dict:
        """
        Process a query through the RAG agent and return structured response
        """
        start_time = time.time()

        logger.info(f"Processing query through RAG agent: '{query_text[:50]}...'")

        try:
            # First, retrieve relevant information
            retrieved_info = retrieve_information(query_text)

            if retrieved_info.get('error'):
                logger.warning(f"Retrieval error: {retrieved_info['error']}")

            # Format the retrieved information for the assistant
            context_info = ""
            sources = set()
            matched_chunks = []

            for chunk in retrieved_info.get('retrieved_chunks', []):
                context_info += f"Source: {chunk['url']}\nContent: {chunk['content']}\n\n"
                sources.add(chunk['url'])
                matched_chunks.append(chunk)

            # Create the prompt for OpenAI with the retrieved context
            if context_info.strip():
                system_prompt = f"""You are a helpful assistant that answers questions based on retrieved documents.
                Use the following retrieved information to answer the question. If the information doesn't contain the answer,
                clearly state that you don't have enough information. Always cite your sources and provide relevant information
                that was used to generate the answer.

                Retrieved Information:
                {context_info}"""
            else:
                system_prompt = "You are a helpful assistant. Answer the question to the best of your ability."

            # Make the API call to OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or gpt-4 if available
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query_text}
                ],
                temperature=0.3
            )

            # Extract the assistant's response
            assistant_response = response.choices[0].message.content

            # Calculate query time (including retrieval time)
            query_time_ms = (time.time() - start_time) * 1000

            # Format the response
            formatted_response = {
                "answer": assistant_response,
                "sources": list(sources),
                "matched_chunks": matched_chunks,
                "query_time_ms": query_time_ms,
                "confidence": self._calculate_confidence(matched_chunks)
            }

            logger.info(f"Query processed in {query_time_ms:.2f}ms")
            return formatted_response

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": "Sorry, I encountered an error processing your request.",
                "sources": [],
                "matched_chunks": [],
                "error": str(e),
                "query_time_ms": (time.time() - start_time) * 1000
            }

    def _calculate_confidence(self, matched_chunks: List[Dict]) -> str:
        """
        Calculate confidence level based on similarity scores and number of matches
        """
        if not matched_chunks:
            return "low"

        avg_score = sum(chunk.get('similarity_score', 0.0) for chunk in matched_chunks) / len(matched_chunks)

        if avg_score >= 0.7:
            return "high"
        elif avg_score >= 0.4:
            return "medium"
        else:
            return "low"

def query_agent(query_text: str) -> Dict:
    """
    Convenience function to query the RAG agent
    """
    agent = RAGAgent()
    return agent.query_agent(query_text)

def main():
    """
    Main function to demonstrate the RAG agent functionality
    """
    logger.info("Initializing RAG Agent...")

    try:
        # Initialize the agent
        agent = RAGAgent()

        # Example queries to test the system
        test_queries = [
            "What is ROS2?",
            "Explain humanoid design principles",
            "How does VLA work?",
            "What are simulation techniques?",
            "Explain AI control systems"
        ]

        print("RAG Agent - Testing Queries")
        print("=" * 50)

        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}: {query}")
            print("-" * 30)

            # Process query through agent
            response = agent.query_agent(query)

            # Print formatted results
            print(f"Answer: {response['answer']}")

            if response.get('sources'):
                print(f"Sources: {len(response['sources'])} documents")
                for source in response['sources'][:3]:  # Show first 3 sources
                    print(f"  - {source}")

            if response.get('matched_chunks'):
                print(f"Matched chunks: {len(response['matched_chunks'])}")
                for j, chunk in enumerate(response['matched_chunks'][:2], 1):  # Show first 2 chunks
                    content_preview = chunk['content'][:100] + "..." if len(chunk['content']) > 100 else chunk['content']
                    print(f"  Chunk {j}: {content_preview}")
                    print(f"    Source: {chunk['url']}")
                    print(f"    Score: {chunk['similarity_score']:.3f}")

            print(f"Query time: {response['query_time_ms']:.2f}ms")
            print(f"Confidence: {response.get('confidence', 'unknown')}")

            if i < len(test_queries):  # Don't sleep after the last query
                time.sleep(1)  # Small delay between queries
    except ValueError as e:
        print(f"Error initializing agent: {e}")
        print("Make sure you have set the OPENAI_API_KEY in your environment variables.")

if __name__ == "__main__":
    main()