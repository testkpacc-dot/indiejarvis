// src/lib/api-client/adminClient.ts
import { createInstance, retryRequest } from './http';

const API_BASE = (import.meta.env.VITE_API_BASE as string) || '';
const inst = createInstance(API_BASE);

/**
 * triggerTrainer - call trainer/run or simulate if absent
 */
export async function triggerTrainer() {
  return retryRequest(async () => {
    const res = await inst.post('/trainer/run');
    return res.data;
  }, 1, 200);
}

export async function getTrainerStatus(jobId?: string) {
  return retryRequest(async () => {
    const url = jobId ? `/trainer/job/${jobId}` : '/trainer/status';
    const res = await inst.get(url);
    return res.data;
  }, 1, 200);
}
