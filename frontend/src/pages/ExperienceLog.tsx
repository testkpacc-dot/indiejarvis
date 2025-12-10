// src/pages/ExperienceLog.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import type { Experience } from '../types/api';
import SkeletonList from '../components/skeletons/SkeletonList';


export default function ExperienceLog() {
  const [exps, setExps] = useState<Experience[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const expBase =
    (import.meta.env.VITE_EXPERIENCE_BASE as string) ||
    (import.meta.env.VITE_API_BASE as string) ||
    '';

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        if (!expBase) {
          setError('Experience API base URL not configured (VITE_EXPERIENCE_BASE).');
          setExps([]);
          return;
        }
        const res = await axios.get(`${expBase}/experiences`);
        if (res.data?.ok) setExps(res.data.data);
        else setError('Unexpected response from experience store.');
      } catch (err: any) {
        console.error('Failed to fetch experiences', err);
        setError(err?.message || 'Network error');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [expBase]);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Experience Log</h2>

      {loading && <SkeletonList count={3} />}
      {error && <div className="text-sm text-red-600 mb-3">{error}</div>}

      <div className="space-y-3">
        {exps.length === 0 && !loading && !error && (
          <div className="text-sm text-gray-500">No experiences yet.</div>
        )}

        {exps.map((e) => (
          <div key={e.id} className="p-3 border border-gray-200 rounded-md bg-white">
            <div className="flex items-start justify-between">
              <div>
                <div className="text-sm text-gray-500">{new Date(e.timestamp).toLocaleString()}</div>
                <div className="mt-1 text-sm leading-relaxed whitespace-pre-wrap">{e.response?.text}</div>
                <div className="text-xs text-gray-500 mt-2">Prompt: {e.prompt_id}</div>
              </div>
              <div className="text-right text-sm">
                <div className="text-sm font-medium">{e.verifier_result?.reward === 1 ? '✅' : '❌'}</div>
                <div className="text-xs text-gray-600 mt-1">{(e.verifier_result?.tags || []).join(', ')}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
