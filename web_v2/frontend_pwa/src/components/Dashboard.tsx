'use client';

import React, { useEffect, useState } from 'react';
import { Users, CreditCard, Wallet, TrendingUp, RefreshCw, AlertCircle, CheckCircle2 } from 'lucide-react';

interface DashboardSummary {
  total_borrowers: number;
  active_loans: number;
  total_lent: number;
  total_repaid: number;
  currency: string;
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isUsingFallback, setIsUsingFallback] = useState<boolean>(false);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/dashboard');
      if (!response.ok) {
        throw new Error(`Server status ${response.status}`);
      }
      const result: DashboardSummary = await response.json();
      setData(result);
      setIsUsingFallback(false);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to FastAPI backend at http://localhost:8000');
      setIsUsingFallback(true);
      // Fallback demo data
      setData({
        total_borrowers: 34,
        active_loans: 18,
        total_lent: 520000,
        total_repaid: 285000,
        currency: 'KES',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES',
      maximumFractionDigits: 0,
    }).format(val);
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/80 border border-slate-800 p-6 rounded-3xl backdrop-blur-xl shadow-2xl">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-black text-white tracking-tight">Executive Dashboard</h2>
            {!loading && !isUsingFallback && (
              <span className="flex items-center gap-1 text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-0.5 rounded-full font-medium">
                <CheckCircle2 className="w-3.5 h-3.5" /> Live Database Sync
              </span>
            )}
          </div>
          <p className="text-slate-400 text-sm mt-1">
            Real-time portfolio metrics from <code className="text-sky-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800 font-mono">mikopohub.db</code>
          </p>
        </div>
        <button
          onClick={fetchDashboardData}
          disabled={loading}
          className="flex items-center gap-2 bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-500 hover:to-blue-500 text-white px-5 py-2.5 rounded-2xl font-semibold transition-all shadow-lg shadow-sky-600/25 active:scale-95 text-sm disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Data</span>
        </button>
      </div>

      {/* Backend Offline Banner */}
      {isUsingFallback && (
        <div className="bg-amber-500/10 border border-amber-500/30 text-amber-300 p-4 rounded-2xl flex items-start sm:items-center gap-3 text-sm shadow-lg">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5 sm:mt-0 text-amber-400" />
          <div className="flex-1">
            <span className="font-bold">FastAPI Connection Notice: </span>
            {error}. Demonstrating with pre-loaded mock metrics. Start backend service on port 8000 for live SQLite queries.
          </div>
        </div>
      )}

      {/* Metrics Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Total Borrowers */}
        <div className="bg-slate-900/90 border border-slate-800 hover:border-sky-500/50 p-6 rounded-3xl shadow-xl transition-all hover:scale-[1.02] group relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-sky-500/5 rounded-full blur-2xl group-hover:bg-sky-500/10 transition-all" />
          <div className="flex items-center justify-between relative z-10">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Borrowers</span>
            <div className="p-3 bg-sky-500/10 text-sky-400 rounded-2xl group-hover:bg-sky-500 group-hover:text-white transition-colors">
              <Users className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 relative z-10">
            <div className="text-4xl font-black text-white tracking-tight">
              {loading ? (
                <div className="h-10 w-24 bg-slate-800 animate-pulse rounded-lg" />
              ) : (
                data?.total_borrowers
              )}
            </div>
            <p className="text-xs text-slate-500 mt-2 font-medium">Registered borrowers in database</p>
          </div>
        </div>

        {/* Active Loans */}
        <div className="bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 p-6 rounded-3xl shadow-xl transition-all hover:scale-[1.02] group relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/5 rounded-full blur-2xl group-hover:bg-emerald-500/10 transition-all" />
          <div className="flex items-center justify-between relative z-10">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Active Loans</span>
            <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-2xl group-hover:bg-emerald-500 group-hover:text-white transition-colors">
              <CreditCard className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline justify-between relative z-10">
            <div className="text-4xl font-black text-white tracking-tight">
              {loading ? (
                <div className="h-10 w-24 bg-slate-800 animate-pulse rounded-lg" />
              ) : (
                data?.active_loans
              )}
            </div>
            <span className="bg-emerald-500/10 text-emerald-400 text-xs px-3 py-1 rounded-full font-bold border border-emerald-500/30">
              Active Status
            </span>
          </div>
        </div>

        {/* Total Capital Lent */}
        <div className="bg-slate-900/90 border border-slate-800 hover:border-indigo-500/50 p-6 rounded-3xl shadow-xl transition-all hover:scale-[1.02] group relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 rounded-full blur-2xl group-hover:bg-indigo-500/10 transition-all" />
          <div className="flex items-center justify-between relative z-10">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Capital Lent</span>
            <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-2xl group-hover:bg-indigo-500 group-hover:text-white transition-colors">
              <Wallet className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 relative z-10">
            <div className="text-3xl font-black text-white tracking-tight">
              {loading ? (
                <div className="h-10 w-36 bg-slate-800 animate-pulse rounded-lg" />
              ) : (
                formatCurrency(data?.total_lent || 0)
              )}
            </div>
            <div className="flex items-center gap-1.5 text-xs text-indigo-400 mt-2 font-medium">
              <TrendingUp className="w-4 h-4" />
              <span>Cumulative principal disbursed</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
