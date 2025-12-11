// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';
import dayjs from 'dayjs';
import type { OrchestratorResponse, BanditArm, Experience } from '../types/api';

const exampleResponse: OrchestratorResponse = {
  response_text: "This is a mock LLM response.",
  prompt_id: "p_v1_1",
  verifier_result: { reward: 1, tags: ["ok"], details: { hallucination_score: 0.01 } },
};

const arms: BanditArm[] = [
  { prompt_id: "p_v1_1", alpha: 10, beta: 2, samples: 12, risk: 'low' },
  { prompt_id: "p_v1_2", alpha: 4, beta: 6, samples: 10, risk: 'low' },
];

const experiences: Experience[] = [
  {
    id: 1,
    timestamp: dayjs().subtract(1, 'hour').toISOString(),
    context: { user_id: "u1" },
    prompt_id: "p_v1_1",
    response: { text: "mock response" },
    verifier_result: { reward: 1, tags: ["ok"], details: {} },
  },
];

export const handlers = [
  // POST /query
  http.post(`${import.meta.env.VITE_API_BASE}/query`, async () => {
    return HttpResponse.json({ ok: true, data: exampleResponse });
  }),

  // GET /bandit/arms
  http.get(`${import.meta.env.VITE_BANDIT_BASE}/arms`, async () => {
    return HttpResponse.json({ ok: true, data: arms });
  }),

  // GET /prompts
  http.get(`${import.meta.env.VITE_PROMPT_BASE}/prompts`, async () => {
    return HttpResponse.json({
      ok: true,
      data: [{ prompt_id: "p_v1_1", version: 1, metadata: {} }],
    });
  }),

  // GET /experiences
  http.get(`${import.meta.env.VITE_EXPERIENCE_BASE}/experiences`, async () => {
    return HttpResponse.json({ ok: true, data: experiences });
  }),
];
