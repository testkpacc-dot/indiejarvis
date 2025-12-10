// src/lib/api-client/banditClient.ts
import { createInstance, retryRequest } from './http';

const BANDIT_BASE = (import.meta.env.VITE_BANDIT_BASE as string) || (import.meta.env.VITE_API_BASE as string) || '';
const inst = createInstance(BANDIT_BASE);

export async function getArms() {
  return retryRequest(async () => {
    const res = await inst.get('/arms');
    return res.data;
  });
}

export async function choose(promptContext: Record<string, any>) {
  return retryRequest(async () => {
    const res = await inst.post('/choose', promptContext);
    return res.data;
  });
}

export async function reward(promptId: string, rewardValue = 1, metadata: Record<string, any> = {}) {
  return retryRequest(async () => {
    const res = await inst.post('/reward', { prompt_id: promptId, reward: rewardValue, metadata });
    return res.data;
  });
}
