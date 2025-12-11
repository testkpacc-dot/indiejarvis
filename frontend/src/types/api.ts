// src/types/api.ts
export type ContextFeatures = Record<string, any>;

export type QueryRequest = {
  user_id: string;
  session_id: string;
  text: string;
  features?: ContextFeatures;
};

export type VerifierResult = {
  reward: 0 | 1;
  tags: string[];
  details: Record<string, any>;
};

export type OrchestratorResponse = {
  response_text: string;
  prompt_id: string;
  verifier_result: VerifierResult;
};

export type BanditArm = {
  prompt_id: string;
  alpha: number;
  beta: number;
  samples: number;
  risk?: 'low' | 'high';
};

export type Experience = {
  id: number;
  timestamp: string;
  context: Record<string, any>;
  prompt_id: string;
  response: { text: string; trace?: string };
  verifier_result: VerifierResult;
  feedback?: Record<string, any>;
};
