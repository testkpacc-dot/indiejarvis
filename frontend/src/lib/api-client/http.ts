// src/lib/api-client/http.ts
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

// read base from VITE_API_BASE; services may override with their own env var
const DEFAULT_BASE = (import.meta.env.VITE_API_BASE as string) || '';

export function createInstance(baseURL?: string): AxiosInstance {
  const inst = axios.create({
    baseURL: baseURL || DEFAULT_BASE,
    timeout: 20000,
    headers: { 'Content-Type': 'application/json' },
  });

  // Accept any internal config shape here to avoid axios internal-type mismatch.
  // We're only mutating headers, which is safe in browser environments.
  inst.interceptors.request.use((config: any) => {
    if (!config.headers) config.headers = {};
    try {
      // Prefer browser crypto if available
      (config.headers as any)['X-Request-ID'] = (crypto as any).randomUUID?.() ?? Math.random().toString(36).slice(2, 9);
    } catch {
      (config.headers as any)['X-Request-ID'] = Math.random().toString(36).slice(2, 9);
    }
    return config;
  });

  return inst;
}

export async function retryRequest<T>(fn: () => Promise<T>, retries = 2, delayMs = 300) {
  let lastErr: any;

  for (let i = 0; i <= retries; i++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (i < retries) {
        await new Promise((r) => setTimeout(r, delayMs * (i + 1)));
      }
    }
  }

  throw lastErr;
}

export { DEFAULT_BASE };
