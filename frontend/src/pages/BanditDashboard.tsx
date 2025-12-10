// src/pages/BanditDashboard.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import type { BanditArm } from '../types/api';
import SkeletonList from '../components/skeletons/SkeletonList';


export default function BanditDashboard() {
  const [arms, setArms] = useState<BanditArm[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // safe base: use VITE_BANDIT_BASE, fallback to VITE_API_BASE, else empty
  const banditBase =
    (import.meta.env.VITE_BANDIT_BASE as string) ||
    (import.meta.env.VITE_API_BASE as string) ||
    '';

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        if (!banditBase) {
          setError('Bandit API base URL not configured (VITE_BANDIT_BASE).');
          setArms([]);
          return;
        }
        const res = await axios.get(`${banditBase}/arms`);
        if (res.data?.ok) setArms(res.data.data);
        else setError('Unexpected response from bandit service.');
      } catch (err: any) {
        console.error('Failed to fetch bandit arms', err);
        setError(err?.message || 'Network error');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [banditBase]);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Bandit Arms</h2>

      {loading && <SkeletonList count={3} />}
      {error && <div className="text-sm text-red-600 mb-3">{error}</div>}

      <div className="grid grid-cols-1 gap-3">
        {arms.length === 0 && !loading && !error && (
          <div className="text-sm text-gray-500">No arms found.</div>
        )}

        {arms.map((a) => (
          <div
            key={a.prompt_id}
            className="p-3 border border-gray-200 rounded-md flex items-center justify-between bg-white"
          >
            <div>
              <div className="font-medium text-gray-800">{a.prompt_id}</div>
              <div className="text-sm text-gray-500">risk: {a.risk || 'low'}</div>
            </div>

            <div className="text-sm text-gray-700 text-right">
              <div>
                α: <span className="font-semibold">{a.alpha}</span>
              </div>
              <div>
                β: <span className="font-semibold">{a.beta}</span>
              </div>
              <div>
                samples: <span className="font-semibold">{a.samples}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
