// src/lib/api-client/experienceClient.ts
import { createInstance, retryRequest } from './http';
import type { Experience } from '../../types/api';

const EXP_BASE = (import.meta.env.VITE_EXPERIENCE_BASE as string) || (import.meta.env.VITE_API_BASE as string) || '';
const inst = createInstance(EXP_BASE);

export async function logExperience(payload: Partial<Experience>) {
  return retryRequest(async () => {
    const res = await inst.post('/log', payload);
    return res.data;
  });
}

export async function getExperiences(params?: { limit?: number; since?: string }) {
  return retryRequest(async () => {
    const q = params ? `?${new URLSearchParams(Object.entries(params).filter(([,v])=>v!=null).map(([k,v])=>[k,String(v)]))}` : '';
    const res = await inst.get(`/experiences${q}`);
    return res.data;
  });
}
