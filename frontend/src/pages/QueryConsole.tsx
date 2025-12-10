// src/pages/QueryConsole.tsx
import { useState } from 'react';
import api from '../lib/api';
import type { OrchestratorResponse } from '../types/api';
import { useToast } from '../hooks/useToast';
import { experienceClient } from '../lib/api-client';
import SkeletonResponse from '../components/skeletons/SkeletonResponse';

const EXAMPLES = [
  "Summarize the last conversation in 2 lines.",
  "Is the claim 'X caused Y' supported?",
  "Generate a short email about meeting reschedule."
];

export default function QueryConsole() {
  const [text, setText] = useState('');
  const [resp, setResp] = useState<OrchestratorResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const toast = useToast();

  async function onSend() {
    if (!text.trim() || loading) return;
    setLoading(true);
    setResp(null); // reset UI when sending a new request

    try {
      const { data } = await api.post('/query', {
        user_id: 'u1',
        session_id: 's1',
        text,
      });

      if (data?.ok) {
        const payload = data.data as OrchestratorResponse;
        setResp(payload);
        toast.success('Response received', 'LLM');

        // Log experience (non-blocking)
        try {
          await experienceClient.logExperience({
            timestamp: new Date().toISOString(),
            context: { user_id: 'u1' },
            prompt_id: payload.prompt_id,
            response: { text: payload.response_text },
            verifier_result: payload.verifier_result,
          } as any);
        } catch (logErr) {
          console.warn('Experience logging failed', logErr);
          toast.warn('Experience logging failed');
        }
      } else {
        toast.error('LLM returned an unexpected response', 'LLM');
        console.error('Unexpected API response', data);
      }
    } catch (err: any) {
      console.error(err);
      toast.error('Request failed — check console', 'Network');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-xl font-semibold">Query Console</h2>
          <p className="text-sm text-gray-500">Send a query and inspect the chosen prompt and verifier tags.</p>
        </div>
        <div className="text-sm text-gray-500">Mock Mode</div>
      </div>

      <div className="mt-4">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full min-h-[140px] p-4 border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-200 focus:border-teal-500 transition"
          placeholder="Type a user query or pick an example below..."
          aria-label="User query"
        />

        <div className="flex items-center gap-3 mt-3">
          <button
            onClick={onSend}
            disabled={loading || !text.trim()}
            className="px-4 py-2 bg-teal-600 text-white rounded-md shadow-sm hover:shadow transition disabled:opacity-60 disabled:cursor-not-allowed"
            aria-label="Send query"
          >
            {loading ? 'Sending…' : 'Send'}
          </button>

          <button
            onClick={() => { setText(''); setResp(null); }}
            className="px-3 py-2 border border-gray-200 rounded-md text-sm hover:bg-gray-50 transition"
            aria-label="Clear"
          >
            Clear
          </button>

          <div className="ml-auto flex gap-2">
            {EXAMPLES.map((e) => (
              <button
                key={e}
                onClick={() => setText(e)}
                className="px-3 py-1 bg-gray-100 text-sm rounded hover:bg-gray-200 transition"
                title={e}
              >
                {e.split(' ').slice(0, 5).join(' ')}…
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Skeleton loader */}
      {loading && <SkeletonResponse />}

      {/* Actual response */}
      {!loading && resp && (
        <div className="mt-6 border-t pt-4">
          <div className="flex items-center justify-between">
            <h3 className="font-medium">Response</h3>
            <div className="text-sm text-gray-500">
              Prompt: <span className="font-medium">{resp.prompt_id}</span>
            </div>
          </div>

          <div className="mt-3 bg-gray-50 p-4 rounded border border-gray-100">
            <pre className="whitespace-pre-wrap text-sm leading-relaxed">{resp.response_text}</pre>
          </div>

          <div className="flex items-center gap-3 mt-3 text-sm text-gray-600">
            <div>Tags: <span className="text-gray-800">{(resp.verifier_result?.tags || []).join(', ')}</span></div>
            <div className="text-gray-400">|</div>
            <div>Reward: <strong>{resp.verifier_result?.reward}</strong></div>
          </div>
        </div>
      )}
    </div>
  );
}
