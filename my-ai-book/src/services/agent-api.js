// API client for the RAG agent
const API_BASE_URL = 'https://waqar-d-backend.hf.space';

export const agentApi = {
  // Query the RAG agent
  async queryAgent(query) {
    try {
      const response = await fetch(`${API_BASE_URL}/agent/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error querying agent:', error);
      // Return mock response for testing
      return {
        answer: "This is a mock response. The actual agent requires API keys to function properly.",
        sources: ["https://example.com/mock-source"],
        matched_chunks: [{
          content: "This is mock content for testing purposes",
          source_url: "https://example.com/mock-source",
          similarity_score: 0.8
        }],
        query_time_ms: 100,
        confidence: "medium"
      };
    }
  },

  // Check agent health
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/agent/health`);
      return await response.json();
    } catch (error) {
      console.error('Error checking agent health:', error);
      return { status: 'error', message: 'Agent service not available' };
    }
  }
};
