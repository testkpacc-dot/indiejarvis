// src/pages/AdminPanel.tsx
import { useState } from 'react';
import axios from 'axios';
import SkeletonBlock from '../components/skeletons/SkeletonBlock';


type JobStatus = 'idle' | 'running' | 'done' | 'failed';

export default function AdminPanel() {
  const [job, setJob] = useState<JobStatus>('idle');
  const [log, setLog] = useState<string>('');
  const apiBase =
    (import.meta.env.VITE_API_BASE as string) ||
    '';

  async function runTrainer() {
    setJob('running');
    setLog('Starting trainer job (mock)…');
    try {
      // Try /trainer/run if available, else simulate
      if (apiBase) {
        const res = await axios.post(`${apiBase}/trainer/run`);
        if (res.data?.ok) {
          setLog((prev) => prev + '\nTrainer triggered: ' + JSON.stringify(res.data.data));
        } else {
          setLog((prev) => prev + '\nTrainer returned unexpected response.');
        }
      } else {
        // simulation
        await new Promise((r) => setTimeout(r, 1500));
        setLog((prev) => prev + '\nTrainer simulated run complete.');
      }
      // simulate result
      setJob('done');
    } catch (err: any) {
      console.error(err);
      setLog((prev) => prev + '\nError: ' + (err?.message || 'unknown'));
      setJob('failed');
    }
  }

  async function startCanary() {
    setLog((prev) => prev + '\nStarting canary rollout (mock)…');
    // simulate canary: check some metrics
    await new Promise((r) => setTimeout(r, 1000));
    setLog((prev) => prev + '\nCanary completed: no regressions.');
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Admin — Trainer & Canary</h2>
      <div className="grid grid-cols-1 gap-3">
        <div className="p-3 border border-gray-200 rounded-md bg-white">
          <div className="flex items-center gap-3">
            <button
              className="px-4 py-2 bg-teal-600 text-white rounded-md"
              onClick={runTrainer}
              disabled={job === 'running'}
            >
              {job === 'running' && <SkeletonBlock className="h-4 w-32 mt-2" />}
            </button>

            <button
              className="px-3 py-2 border border-gray-200 rounded-md"
              onClick={startCanary}
            >
              Start Canary (simulate)
            </button>
          </div>

          <div className="mt-4">
            <div className="text-sm text-gray-500">Job status: <strong>{job}</strong></div>
            <pre className="mt-2 text-sm bg-gray-50 p-3 rounded border border-gray-100 whitespace-pre-wrap">{log || 'No logs yet.'}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}
