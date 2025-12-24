import React, { useState, useRef, useEffect } from 'react';
import Layout from '@theme/Layout';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const chatContainerRef = useRef(null);

  // Persistent session id for this browser session
  const sessionIdRef = useRef(`web-${Date.now()}`);

  // ⚠️ NOTE: Your URL has a double /api/v1
  // Keep this ONLY if your backend truly exposes it this way
  const API_URL =
    'https://shajarain-rag-backend.hf.space/api/v1/api/v1/rag/query';

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage.text,
          session_id: sessionIdRef.current,
          context: '',
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed (${response.status})`);
      }

      const data = await response.json();

      const botText =
        data.answer ??
        data.result ??
        data.response ??
        data.message ??
        JSON.stringify(data);

      const botResponse = {
        id: Date.now() + 1,
        text: botText,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (err) {
      console.error(err);
      setError(err.message);

      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          text: `Error: ${err.message}`,
          sender: 'bot',
          timestamp: new Date(),
        },
      ]);
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

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Layout title="Chat" description="Chat with the Physical AI assistant">
      <main className="chat-page">
        <div className="chat-container">
          <div className="chat-header">
            <h1>Chat with AI</h1>
          </div>

          <div className="chat-messages" ref={chatContainerRef}>
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`message ${msg.sender}-message`}
              >
                <div className="message-text">{msg.text}</div>
                <div className="message-timestamp">
                  {msg.timestamp.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message bot-message">
                <div className="message-text">Thinking…</div>
              </div>
            )}
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="chat-input-area">
            <textarea
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              rows={3}
              className="chat-input"
            />
            <button
              onClick={handleSend}
              disabled={isLoading || !inputValue.trim()}
              className="send-button"
            >
              {isLoading ? 'Sending…' : 'Send'}
            </button>
          </div>
        </div>

        <style jsx>{`
          .chat-page {
            display: flex;
            justify-content: center;
            padding: 24px;
            background: var(--ifm-background-color);
          }

          .chat-container {
            width: 100%;
            max-width: 800px;
            height: calc(100vh - 160px);
            background: #fff;
            display: flex;
            flex-direction: column;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          }

          .chat-header {
            background: #007cba;
            color: #fff;
            padding: 16px;
            text-align: center;
          }

          .chat-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
          }

          .message {
            max-width: 75%;
            padding: 12px;
            border-radius: 14px;
            animation: fadeIn 0.2s ease;
          }

          .user-message {
            align-self: flex-end;
            background: #007cba;
            color: white;
          }

          .bot-message {
            align-self: flex-start;
            background: #e9ecef;
            color: black;
          }

          .message-timestamp {
            font-size: 0.7rem;
            margin-top: 4px;
            opacity: 0.6;
            text-align: right;
          }

          .chat-input-area {
            display: flex;
            padding: 12px;
            border-top: 1px solid #ddd;
          }

          .chat-input {
            flex: 1;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
            margin-right: 8px;
          }

          .send-button {
            padding: 10px 20px;
            background: #007cba;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
          }

          .send-button:disabled {
            background: #ccc;
          }

          .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            margin: 10px;
            border-radius: 4px;
          }

          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}</style>
      </main>
    </Layout>
  );
};

export default ChatPage;
