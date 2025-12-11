// src/pages/QueryConsole.tsx
import { useState } from 'react';
import api from '../lib/api';
import type { OrchestratorResponse } from '../types/api';
import { useToast } from '../hooks/useToast';
import { experienceClient } from '../lib/api-client';
import SkeletonResponse from '../components/skeletons/SkeletonResponse';
import { Send, Sparkles, Zap, Tag, Award, Loader2, RefreshCw, Copy, Check } from 'lucide-react';

const EXAMPLES = [
  "Summarize the last conversation in 2 lines.",
  "Is the claim 'X caused Y' supported?",
  "Generate a short email about meeting reschedule."
];

export default function QueryConsole() {
  const [text, setText] = useState('');
  const [resp, setResp] = useState<OrchestratorResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const toast = useToast();

  async function onSend() {
    if (!text.trim() || loading) return;
    setLoading(true);
    setResp(null);

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

  const copyResponse = () => {
    if (resp?.response_text) {
      navigator.clipboard.writeText(resp.response_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="w-full space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-gradient-to-br from-teal-500 to-blue-600 rounded-xl shadow-lg">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-slate-900 to-blue-900 bg-clip-text text-transparent">
              Query Console
            </h2>
          </div>
          <p className="text-slate-600 ml-14">
            Send queries and inspect AI responses with verifier insights
          </p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-sm border border-slate-200">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-medium text-slate-700">Live</span>
        </div>
      </div>

      {/* Input Section */}
      <div className="relative">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full min-h-[160px] p-5 pr-14 text-base border-2 border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-teal-100 focus:border-teal-400 transition-all duration-200 resize-none bg-white shadow-sm"
          placeholder="✨ Type your query here or select an example below..."
          aria-label="User query"
        />
        <div className="absolute bottom-4 right-4 flex items-center gap-2 text-sm text-slate-400">
          <Zap className="w-4 h-4" />
          <span>{text.length} chars</span>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-3">
        <button
          onClick={onSend}
          disabled={loading || !text.trim()}
          className="group flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-teal-600 to-blue-600 text-white rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 font-medium"
          aria-label="Send query"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Sending...
            </>
          ) : (
            <>
              <Send className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              Send Query
            </>
          )}
        </button>

        <button
          onClick={() => { setText(''); setResp(null); }}
          className="flex items-center gap-2 px-5 py-3 border-2 border-slate-200 rounded-xl text-slate-700 hover:bg-slate-50 hover:border-slate-300 transition-all duration-200 font-medium"
          aria-label="Clear"
        >
          <RefreshCw className="w-4 h-4" />
          Clear
        </button>
      </div>

      {/* Examples */}
      <div>
        <p className="text-sm font-medium text-slate-600 mb-3">Quick Examples:</p>
        <div className="flex flex-wrap gap-2">
          {EXAMPLES.map((e, idx) => (
            <button
              key={idx}
              onClick={() => setText(e)}
              className="px-4 py-2 bg-gradient-to-r from-slate-100 to-slate-50 text-sm rounded-lg hover:from-teal-50 hover:to-blue-50 hover:shadow-md transition-all duration-200 border border-slate-200 text-slate-700 hover:text-teal-700 font-medium"
              title={e}
            >
              {e.split(' ').slice(0, 4).join(' ')}...
            </button>
          ))}
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="p-6 border-2 border-slate-200 rounded-xl bg-gradient-to-br from-slate-50 to-white animate-in fade-in duration-300">
          <SkeletonResponse />
          <div className="flex items-center gap-3 text-teal-600 mt-4">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span className="font-medium">Processing your query...</span>
          </div>
        </div>
      )}

      {/* Response Section */}
      {!loading && resp && (
        <div className="space-y-4 animate-in fade-in duration-500">
          {/* Response Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg shadow-md">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900">AI Response</h3>
                <p className="text-sm text-slate-500">Generated successfully</p>
              </div>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-200">
              <Tag className="w-4 h-4 text-purple-600" />
              <span className="text-sm font-semibold text-purple-900">{resp.prompt_id}</span>
            </div>
          </div>

          {/* Response Content */}
          <div className="relative group">
            <div className="bg-gradient-to-br from-slate-50 to-white p-6 rounded-xl border-2 border-slate-200 shadow-sm">
              <pre className="whitespace-pre-wrap text-slate-700 leading-relaxed font-sans">
                {resp.response_text}
              </pre>
            </div>
            <button
              onClick={copyResponse}
              className="absolute top-4 right-4 p-2 bg-white rounded-lg shadow-md opacity-0 group-hover:opacity-100 transition-opacity border border-slate-200 hover:bg-slate-50"
              title="Copy response"
            >
              {copied ? (
                <Check className="w-4 h-4 text-green-600" />
              ) : (
                <Copy className="w-4 h-4 text-slate-600" />
              )}
            </button>
          </div>

          {/* Metadata */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
              <Tag className="w-5 h-5 text-blue-600 flex-shrink-0" />
              <div className="min-w-0">
                <p className="text-xs font-medium text-blue-900 mb-1">Verifier Tags</p>
                <div className="flex flex-wrap gap-1">
                  {(resp.verifier_result?.tags || []).map((tag: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-white text-xs font-medium text-blue-700 rounded border border-blue-200"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-amber-50 to-orange-50 rounded-lg border border-amber-200">
              <Award className="w-5 h-5 text-amber-600 flex-shrink-0" />
              <div>
                <p className="text-xs font-medium text-amber-900 mb-1">Quality Reward</p>
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-bold text-amber-700">
                    {resp.verifier_result?.reward !== undefined 
                      ? (resp.verifier_result.reward * 100).toFixed(0)
                      : 'N/A'
                    }
                  </span>
                  {resp.verifier_result?.reward !== undefined && (
                    <span className="text-sm text-amber-600">/ 100</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}