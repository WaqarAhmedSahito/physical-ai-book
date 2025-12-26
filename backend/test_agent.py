import asyncio
import sys
import os

# Add the backend directory to the path so we can import the agent
sys.path.insert(0, os.path.dirname(__file__))

def test_agent():
    '''
    Test the RAG agent functionality
    '''
    from agent import RAGAgent

    print('Testing RAG Agent...')
    print('=' * 50)

    try:
        # Initialize the agent
        agent = RAGAgent()
        print('✓ Agent initialized successfully')

        # Test query
        test_query = 'What is embodied AI?'
        print(f'\nQuery: {test_query}')

        # Process query
        response = agent.query_agent(test_query)

        print(f'Answer: {response["answer"]}')
        print(f'Sources: {len(response["sources"])}')
        print(f'Matched chunks: {len(response["matched_chunks"])}')
        print(f'Query time: {response["query_time_ms"]}ms')
        print(f'Confidence: {response["confidence"]}')

        print('\n✓ Agent test completed successfully')

    except Exception as e:
        print(f'✗ Error during agent test: {e}')
        import traceback
        traceback.print_exc()

def test_sync_agent():
    '''
    Test the synchronous agent functionality
    '''
    from agent import query_agent

    print('\nTesting Synchronous Agent...')
    print('=' * 50)

    try:
        # Test query
        test_query = 'What is machine learning?'
        print(f'Query: {test_query}')

        # Process query synchronously using the convenience function
        response = query_agent(test_query)

        print(f'Answer: {response["answer"]}')
        print(f'Sources: {len(response["sources"])}')
        print(f'Matched chunks: {len(response["matched_chunks"])}')
        print(f'Query time: {response["query_time_ms"]}ms')
        print(f'Confidence: {response["confidence"]}')

        print('\n✓ Synchronous agent test completed successfully')

    except Exception as e:
        print(f'✗ Error during synchronous agent test: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_agent()
    test_sync_agent()
