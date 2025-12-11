// src/lib/api-client/promptClient.ts
import { createInstance, retryRequest } from './http';

const PROMPT_BASE = (import.meta.env.VITE_PROMPT_BASE as string) || (import.meta.env.VITE_API_BASE as string) || '';

const inst = createInstance(PROMPT_BASE);

/**
 * getPrompts - list prompts
 */
export async function getPrompts() {
  return retryRequest(async () => {
    const res = await inst.get('/prompts');
    return res.data;
  });
}

/**
 * getPrompt - fetch single prompt by id
 */
export async function getPrompt(promptId: string) {
  return retryRequest(async () => {
    const res = await inst.get(`/prompt/${encodeURIComponent(promptId)}`);
    return res.data;
  });
}
