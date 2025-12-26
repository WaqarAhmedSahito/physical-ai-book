import React, { useState, useEffect } from 'react';
import { agentApi } from '../services/agent-api';
import './ChatPopup.css';

const ChatPopup = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [agentStatus, setAgentStatus] = useState('checking');

  useEffect(() => {
    // Check agent health on component mount
    checkAgentStatus();
  }, []);

  const checkAgentStatus = async () => {
    const health = await agentApi.healthCheck();
    setAgentStatus(health.status || 'unknown');
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { text: inputValue, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get response from agent
      const response = await agentApi.queryAgent(inputValue);

      const agentMessage = {
        text: response.answer,
        sender: 'agent',
        timestamp: new Date(),
        sources: response.sources,
        confidence: response.confidence
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      const errorMessage = {
        text: 'Sorry, I encountered an error processing your request.',
        sender: 'agent',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-popup">
      {/* Floating button */}
      <button
        className={`chat-button ${isOpen ? 'open' : ''} ${agentStatus === 'ok' ? 'online' : 'offline'}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="chat-icon">
          {agentStatus === 'ok' ? '🤖' : '⚠️'}
        </div>
        {isOpen ? 'Close' : 'AI Assistant'}
      </button>

      {/* Chat popup */}
      {isOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <h3>AI Assistant</h3>
            <div className={`status-indicator ${agentStatus}`}>
              {agentStatus === 'ok' ? 'Online' : agentStatus === 'warning' ? 'Limited' : 'Offline'}
            </div>
          </div>

          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your AI assistant. Ask me anything about this page or the content.</p>
                <p>Try asking: "What is this page about?" or "Summarize this content"</p>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`message ${message.sender}`}
                >
                  <div className="message-content">
                    <div className="message-text">{message.text}</div>
                    {message.sources && message.sources.length > 0 && (
                      <div className="message-sources">
                        <small>Sources: {message.sources.slice(0, 2).join(', ')}</small>
                      </div>
                    )}
                    {message.confidence && (
                      <div className="message-confidence">
                        <small>Confidence: {message.confidence}</small>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message agent">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="chat-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything..."
              disabled={isLoading}
              rows="2"
            />
            <button
              onClick={handleSend}
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatPopup;