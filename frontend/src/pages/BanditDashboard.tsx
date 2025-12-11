import React, { useEffect, useState } from 'react';
import axios from 'axios';
import type { BanditArm } from '../types/api';

export default function BanditDashboard() {
  const [arms, setArms] = useState<BanditArm[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const base = import.meta.env.VITE_BANDIT_BASE;

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await axios.get(`${base}/arms`);
        // backend returns: { arms: [...] }
        setArms(res.data.arms || []);
      } catch (err: any) {
        console.error("Failed to fetch bandit arms", err);
        setError("Failed to load arms");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [base]);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Bandit Arms</h2>

      {loading && <div className="text-sm text-gray-500">Loading arms…</div>}
      {error && <div className="text-sm text-red-600">{error}</div>}

      {arms.map(a => (
        <div key={a.prompt_id} className="p-3 border rounded mb-2 bg-white">
          <div className="font-medium">{a.prompt_id}</div>
          <div className="text-sm text-gray-500">risk: {a.risk}</div>
          <div className="text-sm mt-1">
            α: {a.alpha} — β: {a.beta} — samples: {a.samples}
          </div>
        </div>
      ))}
    </div>
  );
}
