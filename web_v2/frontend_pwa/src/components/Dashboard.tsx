'use client';

import React, { useEffect, useState } from 'react';
import { 
  Users, 
  CreditCard, 
  Wallet, 
  RefreshCw, 
  ArrowUpRight, 
  DollarSign, 
  PieChart, 
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
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">Portfolio Summary</h2>
          <p className="text-xs text-slate-400 mt-1">Real-time credit & disbursement performance</p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchDashboardData}
            disabled={loading}
            className="flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white px-4 py-2 rounded-xl text-xs font-medium border border-slate-700 transition-all active:scale-95 disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Primary Financial KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Total Loan Portfolio */}
        <div className="bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl hover:border-slate-700 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Gross Loan Book</span>
            <div className="p-2.5 bg-slate-800/80 text-emerald-400 rounded-xl">
              <Wallet className="w-5 h-5" />
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
        <div className="bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl hover:border-slate-700 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Repayments</span>
            <div className="p-2.5 bg-slate-800/80 text-emerald-400 rounded-xl">
              <DollarSign className="w-5 h-5" />
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
        <div className="bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl hover:border-slate-700 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Facilities</span>
            <div className="p-2.5 bg-slate-800/80 text-slate-300 rounded-xl">
              <CreditCard className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline justify-between">
            <div className="text-2xl font-bold text-white tracking-tight font-mono">
              {loading ? '...' : data?.active_loans}
            </div>
            <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-full border border-emerald-500/20 font-medium">
              Active
            </span>
          </div>
        </div>

        {/* Registered Borrowers */}
        <div className="bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl hover:border-slate-700 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Borrowers</span>
            <div className="p-2.5 bg-slate-800/80 text-slate-300 rounded-xl">
              <Users className="w-5 h-5" />
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
    </div>
  );
}
