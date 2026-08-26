'use client';

import React, { useState } from 'react';
import Dashboard from '@/components/Dashboard';
import RecordPayment from '@/components/RecordPayment';
import { 
  LayoutDashboard, 
  CreditCard, 
  Database, 
  ShieldCheck, 
  Layers,
  ArrowUpRight,
  Server,
  Smartphone
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'payment'>('dashboard');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-sky-500 selection:text-white">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-50 bg-slate-950/90 backdrop-blur-md border-b border-slate-800/80 px-4 sm:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 font-bold text-base">
              M
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-semibold text-white tracking-tight">MikopoHub</h1>
                <span className="text-[11px] font-mono bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">
                  v2.0 PWA
                </span>
              </div>
              <p className="text-xs text-slate-400">Micro-Lending & Credit Portfolio Engine</p>
            </div>
          </div>

          <div className="flex items-center gap-1 bg-slate-900 border border-slate-800/80 p-1 rounded-xl">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-medium transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-slate-800 text-white shadow-sm border border-slate-700/50'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" />
              <span>Dashboard</span>
            </button>
            <button
              onClick={() => setActiveTab('payment')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-medium transition-all ${
                activeTab === 'payment'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
              }`}
            >
              <CreditCard className="w-3.5 h-3.5" />
              <span>Record Payment</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-8 space-y-6">
        {/* Sub-header Context Bar */}
        <div className="bg-slate-900/40 border border-slate-800/60 p-4 rounded-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-sky-400 flex-shrink-0" />
            <span>
              Shared Database Mode: <code className="text-slate-200 font-mono bg-slate-950 px-1.5 py-0.5 rounded border border-slate-800">desktop_legacy/mikopohub.db</code>
            </span>
          </div>
          <div className="flex items-center gap-4 text-slate-400 font-mono">
            <span className="flex items-center gap-1.5">
              <Server className="w-3.5 h-3.5 text-emerald-400" /> FastAPI Core
            </span>
            <span className="flex items-center gap-1.5">
              <Smartphone className="w-3.5 h-3.5 text-sky-400" /> PWA Service Worker Ready
            </span>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'dashboard' ? (
          <Dashboard />
        ) : (
          <div className="py-4">
            <RecordPayment />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-5 px-4 text-center text-xs text-slate-500 font-mono">
        MikopoHub Financial Systems &bull; Shared Core Architecture &bull; Next.js & FastAPI
      </footer>
    </div>
  );
}
