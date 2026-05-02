import React, { useState, useRef, useEffect } from 'react';
import './chatbot.css';

export const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { 
      text: '¡Hola! Soy el asistente de Naycol. ¿En qué puedo ayudarte hoy?', 
      sender: 'bot',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMessage = { text: input, sender: 'user', time: currentTime };
    
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) throw new Error('Error en el servidor');

      const data = await response.json();
      setMessages((prev) => [...prev, { 
        text: data.response, 
        sender: 'bot',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { 
          text: 'Lo siento, no puedo conectarme con el servidor de Naycol en este momento.', 
          sender: 'bot',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      {!isOpen && (
        <button className="chatbot-button" onClick={() => setIsOpen(true)}>
          <i className="fa fa-comments"></i>
        </button>
      )}

      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="header-info">
              <div className="status-dot"></div>
              <h3>Asistente de Naycol</h3>
            </div>
            <button className="chatbot-close" onClick={() => setIsOpen(false)}>
              <i className="fa fa-times"></i>
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message-wrapper ${msg.sender}`}>
                <div className={`message ${msg.sender}`}>
                  {msg.text}
                </div>
                <div className="message-time">{msg.time}</div>
              </div>
            ))}
            {isLoading && (
              <div className="message-wrapper bot">
                <div className="message bot">Escribiendo...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chatbot-input-area" onSubmit={handleSend}>
            <input
              type="text"
              placeholder="Escribe un mensaje..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button type="submit" className="chatbot-send" disabled={isLoading || !input.trim()}>
              <i className="fa fa-paper-plane"></i>
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
