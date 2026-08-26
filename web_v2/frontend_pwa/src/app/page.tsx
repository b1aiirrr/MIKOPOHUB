'use client';

import React, { useState } from 'react';
import Dashboard from '@/components/Dashboard';
import BorrowersManager from '@/components/BorrowersManager';
import LoansManager from '@/components/LoansManager';
import PushForwardManager from '@/components/PushForwardManager';
import RecordPayment from '@/components/RecordPayment';
import PaymentsLedger from '@/components/PaymentsLedger';
import FormFeesManager from '@/components/FormFeesManager';
import CollateralManager from '@/components/CollateralManager';

import { 
  LayoutDashboard, 
  Users, 
  CreditCard, 
  FastForward, 
  Send, 
  DollarSign, 
  FileText, 
  Shield, 
  Database,
  Server,
  Smartphone,
  ChevronDown
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    'dashboard' | 'borrowers' | 'loans' | 'pushforward' | 'payment' | 'ledger' | 'formfees' | 'collateral'
  >('dashboard');

  const tickerItems = [
    { label: "M-PESA Daraja Gateway", val: "STK Push Ready", color: "text-emerald-400" },
    { label: "Shared Core Database", val: "desktop_legacy/mikopohub.db", color: "text-sky-400" },
    { label: "Security Engine", val: "Bcrypt Salted Hash v2", color: "text-indigo-400" },
    { label: "Loan Interest Rate", val: "20.0% Monthly Compound", color: "text-amber-400" },
    { label: "Collateral Security", val: "Motorcycles, Titles & Devices", color: "text-purple-400" },
    { label: "Progressive Web App", val: "Offline Cache Enabled", color: "text-teal-400" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-sky-500 selection:text-white relative overflow-hidden">
      {/* Ambient Glow Effects */}
      <div className="infinity-glow-bg w-[500px] h-[500px] bg-sky-500/10 top-[-100px] left-[-100px]" />
      <div className="infinity-glow-bg w-[400px] h-[400px] bg-emerald-500/10 bottom-[-100px] right-[-100px]" />

      {/* INFINITY TICKER MARQUEE BAR */}
      <div className="py-2.5 infinity-ticker-container text-xs font-mono">
        <div className="infinity-ticker-track">
          {[...Array(3)].map((_, loopIdx) => (
            <div key={loopIdx} className="inline-flex items-center gap-8 px-4">
              {tickerItems.map((item, idx) => (
                <div key={idx} className="inline-flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-600" />
                  <span className="text-slate-400 uppercase text-[10px] tracking-wider">{item.label}:</span>
                  <span className={`font-semibold ${item.color}`}>{item.val}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* 2117 INFINITE LOOP FIXED NAVBAR */}
      <header className="tm-navbar px-4 sm:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-500 flex items-center justify-center text-white font-black text-lg shadow-lg shadow-sky-500/20">
              M
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold text-white tracking-tight font-sans">MikopoHub</h1>
                <span className="text-[10px] font-mono bg-sky-500/10 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded-full font-semibold">
                  Infinite Loop Edition
                </span>
              </div>
              <p className="text-xs text-slate-400">Micro-Lending Management Platform</p>
            </div>
          </div>

          {/* Module Navigation Pill Buttons */}
          <div className="flex flex-wrap items-center gap-1 bg-slate-900/90 border border-slate-800 p-1.5 rounded-2xl w-full lg:w-auto overflow-x-auto shadow-xl">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'dashboard' ? 'tm-btn-primary' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" /> Dashboard
            </button>

            <button
              onClick={() => setActiveTab('borrowers')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'borrowers' ? 'tm-btn-primary' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Users className="w-3.5 h-3.5 text-sky-400" /> Borrowers
            </button>

            <button
              onClick={() => setActiveTab('loans')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'loans' ? 'tm-btn-primary' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <CreditCard className="w-3.5 h-3.5 text-emerald-400" /> Loans Engine
            </button>

            <button
              onClick={() => setActiveTab('pushforward')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'pushforward' ? 'tm-btn-primary' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <FastForward className="w-3.5 h-3.5 text-amber-400" /> Push Forward
            </button>

            <button
              onClick={() => setActiveTab('payment')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'payment' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Send className="w-3.5 h-3.5 text-emerald-300" /> M-PESA Pay
            </button>

            <button
              onClick={() => setActiveTab('ledger')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'ledger' ? 'tm-btn-primary' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <DollarSign className="w-3.5 h-3.5 text-emerald-400" /> Ledger
            </button>

            <button
              onClick={() => setActiveTab('formfees')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'formfees' ? 'tm-btn-primary' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <FileText className="w-3.5 h-3.5 text-indigo-400" /> Form Fees
            </button>

            <button
              onClick={() => setActiveTab('collateral')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'collateral' ? 'tm-btn-primary' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Shield className="w-3.5 h-3.5 text-purple-400" /> Collateral
            </button>
          </div>
        </div>
      </header>

      {/* Main App Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-8 space-y-6 relative z-10">
        {/* Architecture Context Banner */}
        <div className="tm-content-box p-4 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-sky-400 flex-shrink-0" />
            <span>
              Shared Core Database: <code className="text-sky-300 font-mono bg-slate-950 px-2 py-0.5 rounded border border-slate-800">desktop_legacy/mikopohub.db</code>
            </span>
          </div>
          <div className="flex items-center gap-4 text-slate-400 font-mono text-[11px]">
            <span className="flex items-center gap-1.5 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" /> 100% Parity Active
            </span>
            <span className="flex items-center gap-1.5">
              <Smartphone className="w-3.5 h-3.5 text-sky-400" /> PWA Cache Enabled
            </span>
          </div>
        </div>

        {/* Dynamic Tab Views */}
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'borrowers' && <BorrowersManager />}
        {activeTab === 'loans' && <LoansManager />}
        {activeTab === 'pushforward' && <PushForwardManager />}
        {activeTab === 'payment' && <RecordPayment />}
        {activeTab === 'ledger' && <PaymentsLedger />}
        {activeTab === 'formfees' && <FormFeesManager />}
        {activeTab === 'collateral' && <CollateralManager />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-6 px-4 text-center text-xs text-slate-500 font-mono relative z-10">
        MikopoHub Financial Systems &bull; Merged 2117 Infinite Loop Design &bull; Next.js 16 & FastAPI
      </footer>
    </div>
  );
}
