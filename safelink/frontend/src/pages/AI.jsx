import React, { useState } from 'react';
import { getAIResponse } from '../services/aiClient';

export default function AI() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');

  const handleAsk = async () => {
    const res = await getAIResponse(input);
    setResponse(res.response || JSON.stringify(res));
  };

  return (
    <div>
      <h2>AI Chatbot</h2>
      <input value={input} onChange={e => setInput(e.target.value)} placeholder="Ask something..." />
      <button onClick={handleAsk}>Ask</button>
      <div><strong>Response:</strong> {response}</div>
    </div>
  );
} 