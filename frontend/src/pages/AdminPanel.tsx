// src/pages/AdminPanel.tsx
import { useState } from 'react';
import axios from 'axios';
import SkeletonBlock from '../components/skeletons/SkeletonBlock';
import { Settings, Play, Rocket, CheckCircle, XCircle, Loader2, Terminal } from 'lucide-react';

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

  const getStatusConfig = () => {
    switch (job) {
      case 'running':
        return {
          icon: Loader2,
          text: 'Running',
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          iconClass: 'animate-spin'
        };
      case 'done':
        return {
          icon: CheckCircle,
          text: 'Success',
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          iconClass: ''
        };
      case 'failed':
        return {
          icon: XCircle,
          text: 'Failed',
          color: 'text-red-600',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          iconClass: ''
        };
      default:
        return {
          icon: Terminal,
          text: 'Idle',
          color: 'text-slate-600',
          bgColor: 'bg-slate-50',
          borderColor: 'border-slate-200',
          iconClass: ''
        };
    }
  };

  const statusConfig = getStatusConfig();
  const StatusIcon = statusConfig.icon;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-gradient-to-br from-rose-500 to-pink-600 rounded-xl shadow-lg">
            <Settings className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Admin Panel</h2>
        </div>
        <p className="text-slate-600 ml-14">Manage trainer jobs and canary deployments</p>
      </div>

      {/* Action Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Trainer Card */}
        <div className="bg-gradient-to-br from-teal-50 to-blue-50 rounded-xl border-2 border-teal-200 p-6 hover:shadow-lg transition-all duration-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gradient-to-br from-teal-500 to-blue-600 rounded-lg shadow-md">
              <Play className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">Run Trainer</h3>
              <p className="text-xs text-slate-600">Execute training pipeline</p>
            </div>
          </div>
          <button
            className="w-full group flex items-center justify-center gap-2 px-5 py-3 bg-gradient-to-r from-teal-600 to-blue-600 text-white rounded-lg shadow-md hover:shadow-lg hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 font-medium"
            onClick={runTrainer}
            disabled={job === 'running'}
          >
            {job === 'running' ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Training in progress...
              </>
            ) : (
              <>
                <Play className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                Start Training
              </>
            )}
          </button>
        </div>

        {/* Canary Card */}
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border-2 border-purple-200 p-6 hover:shadow-lg transition-all duration-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-600 rounded-lg shadow-md">
              <Rocket className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">Canary Deploy</h3>
              <p className="text-xs text-slate-600">Test new configurations</p>
            </div>
          </div>
          <button
            className="w-full group flex items-center justify-center gap-2 px-5 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg shadow-md hover:shadow-lg hover:scale-105 transition-all duration-200 font-medium"
            onClick={startCanary}
          >
            <Rocket className="w-5 h-5 group-hover:-translate-y-1 transition-transform" />
            Launch Canary
          </button>
        </div>
      </div>

      {/* Status and Logs */}
      <div className="bg-white rounded-xl border-2 border-slate-200 shadow-sm overflow-hidden">
        {/* Status Bar */}
        <div className={`flex items-center gap-3 px-6 py-4 ${statusConfig.bgColor} border-b-2 ${statusConfig.borderColor}`}>
          <StatusIcon className={`w-5 h-5 ${statusConfig.color} ${statusConfig.iconClass}`} />
          <div>
            <p className="text-xs font-medium text-slate-600">Job Status</p>
            <p className={`font-bold ${statusConfig.color}`}>{statusConfig.text}</p>
          </div>
        </div>

        {/* Logs */}
        <div className="p-6">
          <div className="flex items-center gap-2 mb-3">
            <Terminal className="w-4 h-4 text-slate-500" />
            <h4 className="font-semibold text-slate-900">Execution Logs</h4>
          </div>
          <div className="bg-slate-900 rounded-lg p-4 shadow-inner">
            <pre className="text-sm text-green-400 font-mono whitespace-pre-wrap leading-relaxed">
              {log || '> Awaiting job execution...'}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}