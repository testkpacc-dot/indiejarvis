// src/pages/PromptViewer.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import SkeletonList from '../components/skeletons/SkeletonList';


type PromptItem = {
  prompt_id: string;
  version?: number;
  metadata?: Record<string, any>;
};

export default function PromptViewer() {
  const [prompts, setPrompts] = useState<PromptItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const promptBase =
    (import.meta.env.VITE_PROMPT_BASE as string) ||
    (import.meta.env.VITE_API_BASE as string) ||
    '';

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        if (!promptBase) {
          setError('Prompt API base URL not configured (VITE_PROMPT_BASE).');
          setPrompts([]);
          return;
        }
        const res = await axios.get(`${promptBase}/prompts`);
        if (res.data?.ok) setPrompts(res.data.data);
        else setError('Unexpected response from prompt registry.');
      } catch (err: any) {
        console.error('Failed to fetch prompts', err);
        setError(err?.message || 'Network error');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [promptBase]);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Prompt Registry</h2>

      {loading && <SkeletonList count={3} />}
      {error && <div className="text-sm text-red-600 mb-3">{error}</div>}

      <div className="grid grid-cols-1 gap-3">
        {prompts.length === 0 && !loading && !error && (
          <div className="text-sm text-gray-500">No prompts available.</div>
        )}

        {prompts.map((p) => (
          <div key={p.prompt_id} className="p-3 border border-gray-200 rounded-md bg-white">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-800">{p.prompt_id}</div>
                <div className="text-sm text-gray-500">v{p.version ?? 'N/A'}</div>
              </div>
              <div className="text-sm text-gray-600">
                <button
                  className="px-3 py-1 border border-gray-200 rounded text-sm hover:bg-gray-50"
                  onClick={() => navigator.clipboard?.writeText(p.prompt_id)}
                  title="Copy prompt id"
                >
                  Copy ID
                </button>
              </div>
            </div>

            {p.metadata && (
              <div className="mt-3 text-sm text-gray-700">
                <pre className="whitespace-pre-wrap text-xs">{JSON.stringify(p.metadata, null, 2)}</pre>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
