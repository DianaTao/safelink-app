const API_BASE = import.meta.env.VITE_API_URL;

export async function askAI(question) {
  const res = await fetch(`${API_BASE}/api/ai/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: question })
  });
  return res.json();
} 