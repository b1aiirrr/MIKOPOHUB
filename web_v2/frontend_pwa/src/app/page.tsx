'use client';

import React, { useState } from 'react';
import Dashboard from '@/components/Dashboard';
import RecordPayment from '@/components/RecordPayment';
import { LayoutDashboard, CreditCard, Building2, Smartphone, Shield, Sparkles } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'payment'>('dashboard');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-sky-500 selection:text-white">
      {/* Top Header / App Bar */}
      <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/80 px-4 sm:px-8 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-sky-500/20 text-white font-extrabold text-lg">
              M
            </div>
            <div>
              <h1 className="text-xl font-black tracking-tight text-white flex items-center gap-2">
                MIKOPOHUB <span className="text-xs bg-sky-500/10 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded-full font-bold">PWA v2.0</span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">Micro-Lending Management Platform</p>
            </div>
          </div>

          <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 p-1.5 rounded-2xl">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-sky-600 text-white shadow-lg shadow-sky-600/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Dashboard</span>
            </button>
            <button
              onClick={() => setActiveTab('payment')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'payment'
                  ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <CreditCard className="w-4 h-4" />
              <span>M-PESA Payment</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-6xl w-full mx-auto p-4 sm:p-8 space-y-8">
        {/* Banner */}
        <div className="bg-gradient-to-r from-sky-900/40 via-indigo-900/30 to-slate-900/50 border border-sky-500/20 p-6 rounded-3xl backdrop-blur-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-sky-500/10 text-sky-400 rounded-2xl border border-sky-500/20 mt-1">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Live "Before & After" Hybrid Architecture</h2>
              <p className="text-sm text-slate-300 max-w-2xl mt-0.5">
                Connected to <code className="text-sky-300 font-mono bg-slate-900/80 px-1.5 py-0.5 rounded border border-slate-800">desktop_legacy/mikopohub.db</code>. Both legacy Tkinter desktop and modern Next.js PWA read and write from the same database.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 text-xs font-semibold text-slate-400 bg-slate-950/60 px-4 py-2 rounded-2xl border border-slate-800">
            <Shield className="w-4 h-4 text-emerald-400" />
            <span>Bcrypt Auth Enabled</span>
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
      <footer className="border-t border-slate-900 py-6 px-4 text-center text-xs text-slate-500 font-medium">
        <p>MikopoHub Web v2.0 &bull; Progressive Web App &bull; Powered by Next.js & FastAPI</p>
      </footer>
    </div>
  );
}
