'use client';

import React, { useState } from 'react';
import { FastForward, CheckCircle, AlertTriangle, ArrowRight, Calendar, Info } from 'lucide-react';

export default function PushForwardManager() {
  const [loanId, setLoanId] = useState('1');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePushForward = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!loanId) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`http://localhost:8000/api/loans/${loanId}/push-forward`, {
        method: 'POST',
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Push forward failed.');
      }
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Error executing push forward.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="bg-slate-900/80 border border-slate-800 p-6 sm:p-8 rounded-2xl">
        <div className="flex items-center gap-3 pb-6 border-b border-slate-800 mb-6">
          <div className="p-3 bg-amber-500/10 text-amber-400 rounded-xl border border-amber-500/20">
            <FastForward className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Push Forward Loan Engine</h3>
            <p className="text-xs text-slate-400">Carry remaining principal to the next monthly period</p>
          </div>
        </div>

        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80 mb-6 text-xs text-slate-400 space-y-2">
          <div className="font-semibold text-amber-400 flex items-center gap-1.5">
            <Info className="w-4 h-4" /> Rule for Push Forward:
          </div>
          <p className="leading-relaxed">
            The current monthly interest MUST be fully paid before pushing a loan forward. 
            Once executed, the current period status will change to <code className="text-amber-300 font-mono">CARRIED_FORWARD</code> and a new 30-day period will be generated.
          </p>
        </div>

        {error && (
          <div className="mb-6 bg-rose-500/10 border border-rose-500/20 text-rose-300 p-4 rounded-xl text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="mb-6 bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 p-5 rounded-xl text-xs space-y-3">
            <div className="flex items-center gap-2 font-bold text-emerald-400">
              <CheckCircle className="w-5 h-5" />
              <span>{result.message}</span>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl font-mono text-[11px] space-y-1 text-slate-300 border border-slate-800">
              <div>Principal Carried: KES {result.principal_carried?.toLocaleString()}</div>
              <div>New Monthly Interest Due: KES {result.new_interest_due?.toLocaleString()}</div>
              <div>Next Due Date: {result.next_due_date}</div>
            </div>
          </div>
        )}

        <form onSubmit={handlePushForward} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-2">Loan ID *</label>
            <input
              type="number"
              required
              placeholder="e.g. 1"
              value={loanId}
              onChange={(e) => setLoanId(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-3 text-xs outline-none focus:border-amber-500 font-mono"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-amber-600 hover:bg-amber-500 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-amber-600/20 flex items-center justify-center gap-2 text-xs disabled:opacity-50"
          >
            <FastForward className="w-4 h-4" />
            <span>{loading ? 'Processing Push Forward...' : 'Execute Loan Push Forward'}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
