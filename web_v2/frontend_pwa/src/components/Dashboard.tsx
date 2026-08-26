'use client';

import React, { useEffect, useState } from 'react';
import { 
  Users, 
  CreditCard, 
  Wallet, 
  TrendingUp, 
  RefreshCw, 
  ArrowUpRight, 
  ArrowDownRight,
  Database,
  Activity,
  DollarSign,
  PieChart,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

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

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/dashboard');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const result: DashboardSummary = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message || 'Offline Mode');
      // High quality fallback demonstration data
      setData({
        total_borrowers: 42,
        active_loans: 19,
        total_lent: 685000,
        total_repaid: 412000,
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

  const calculateRepaymentRate = () => {
    if (!data || data.total_lent === 0) return 0;
    return Math.min(100, Math.round((data.total_repaid / data.total_lent) * 100));
  };

  return (
    <div className="space-y-8">
      {/* Top Banner / Sync Bar */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-slate-900/90 border border-slate-800/80 p-6 rounded-2xl backdrop-blur-xl">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-sky-400">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h2 className="text-xl font-semibold text-white tracking-tight">Portfolio Summary</h2>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                Live Sync
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 font-mono">
              Database Source: desktop_legacy/mikopohub.db
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          {error && (
            <div className="flex items-center gap-2 text-xs text-amber-400 bg-amber-500/10 px-3 py-1.5 rounded-lg border border-amber-500/20">
              <AlertCircle className="w-4 h-4" />
              <span>Offline Preview</span>
            </div>
          )}
          <button
            onClick={fetchDashboardData}
            disabled={loading}
            className="flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white px-4 py-2 rounded-xl text-xs font-medium border border-slate-700/60 transition-all active:scale-95 disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh Metrics</span>
          </button>
        </div>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Total Loan Portfolio */}
        <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl hover:border-slate-700 transition-all group">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Gross Loan Book</span>
            <div className="p-2 bg-sky-500/10 text-sky-400 rounded-lg">
              <Wallet className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-4">
            <div className="text-2xl font-bold text-white tracking-tight font-mono">
              {loading ? '...' : formatCurrency(data?.total_lent || 0)}
            </div>
            <div className="flex items-center gap-1 mt-2 text-xs text-emerald-400 font-medium">
              <ArrowUpRight className="w-3.5 h-3.5" />
              <span>Total principal disbursed</span>
            </div>
          </div>
        </div>

        {/* Total Repayments */}
        <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl hover:border-slate-700 transition-all group">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Repayments</span>
            <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-4">
            <div className="text-2xl font-bold text-white tracking-tight font-mono">
              {loading ? '...' : formatCurrency(data?.total_repaid || 0)}
            </div>
            <div className="flex items-center gap-1 mt-2 text-xs text-slate-400 font-medium">
              <PieChart className="w-3.5 h-3.5 text-emerald-400" />
              <span>{calculateRepaymentRate()}% portfolio recovered</span>
            </div>
          </div>
        </div>

        {/* Active Loans */}
        <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl hover:border-slate-700 transition-all group">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Facilities</span>
            <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg">
              <CreditCard className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline justify-between">
            <div className="text-2xl font-bold text-white tracking-tight font-mono">
              {loading ? '...' : data?.active_loans}
            </div>
            <span className="text-xs text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20 font-medium">
              Outstanding
            </span>
          </div>
        </div>

        {/* Total Registered Borrowers */}
        <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl hover:border-slate-700 transition-all group">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Borrower Directory</span>
            <div className="p-2 bg-amber-500/10 text-amber-400 rounded-lg">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline justify-between">
            <div className="text-2xl font-bold text-white tracking-tight font-mono">
              {loading ? '...' : data?.total_borrowers}
            </div>
            <span className="text-xs text-slate-400 font-medium">Accounts</span>
          </div>
        </div>
      </div>

      {/* Operational Analytics Table */}
      <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-800/80 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-white tracking-tight">System Status & Architecture</h3>
          <span className="text-xs text-slate-400 font-mono">FastAPI v2.0 &bull; SQLite Shared Core</span>
        </div>

        <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-2">
            <div className="text-xs font-medium text-slate-400 uppercase tracking-wider">Database Engine</div>
            <div className="text-sm font-medium text-white flex items-center gap-2">
              <Database className="w-4 h-4 text-sky-400" />
              <span>SQLite Embedded Storage</span>
            </div>
            <p className="text-xs text-slate-500">Shared WAL mode connection with Tkinter desktop software.</p>
          </div>

          <div className="space-y-2">
            <div className="text-xs font-medium text-slate-400 uppercase tracking-wider">Authentication Model</div>
            <div className="text-sm font-medium text-white flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-400" />
              <span>Bcrypt Salted Hash Verification</span>
            </div>
            <p className="text-xs text-slate-500">Upgraded from legacy hardcoded credentials.</p>
          </div>

          <div className="space-y-2">
            <div className="text-xs font-medium text-slate-400 uppercase tracking-wider">Payment Gateway</div>
            <div className="text-sm font-medium text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-amber-400" />
              <span>Safaricom Daraja API Ready</span>
            </div>
            <p className="text-xs text-slate-500">STK Push webhook & Buy Goods Till integration ready.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
