import { askAI } from './apiClient';

export async function getAIResponse(prompt) {
  return askAI(prompt);
} 