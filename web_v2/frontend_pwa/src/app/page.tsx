'use client';

import React, { useState } from 'react';
import Image from 'next/image';
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
  Smartphone
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    'dashboard' | 'borrowers' | 'loans' | 'pushforward' | 'payment' | 'ledger' | 'formfees' | 'collateral'
  >('dashboard');

  const tickerItems = [
    { label: "M-PESA Daraja Gateway", val: "STK Push Ready", color: "text-emerald-400" },
    { label: "Shared Core Database", val: "desktop_legacy/mikopohub.db", color: "text-slate-300" },
    { label: "Security Engine", val: "Bcrypt Salted Hash v2", color: "text-slate-300" },
    { label: "Loan Interest Rate", val: "20.0% Monthly Compound", color: "text-amber-400" },
    { label: "Collateral Security", val: "Motorcycles, Titles & Devices", color: "text-slate-300" },
    { label: "Progressive Web App", val: "Offline Cache Enabled", color: "text-slate-300" },
  ];

  return (
    <div className="min-h-screen bg-[#0f1117] text-slate-100 flex flex-col font-sans selection:bg-slate-700 selection:text-white relative overflow-hidden">
      {/* Ambient Gray Glow Lights */}
      <div className="infinity-glow-bg w-[500px] h-[500px] bg-slate-700/10 top-[-100px] left-[-100px]" />
      <div className="infinity-glow-bg w-[400px] h-[400px] bg-slate-600/10 bottom-[-100px] right-[-100px]" />

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

      {/* FIXED NAVBAR WITH LOGO */}
      <header className="tm-navbar px-4 sm:px-8 py-3.5 border-b border-[#2a2f3d]">
        <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="relative w-10 h-10 rounded-xl overflow-hidden border border-slate-700 shadow-md">
              <Image 
                src="/logo.png" 
                alt="MikopoHub Logo" 
                fill 
                className="object-cover" 
                priority 
              />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold text-white tracking-tight font-sans">MikopoHub</h1>
                <span className="text-[10px] font-mono bg-slate-800 text-slate-300 border border-slate-700 px-2 py-0.5 rounded-full font-semibold">
                  Slate Gray Edition
                </span>
              </div>
              <p className="text-xs text-slate-400">Micro-Lending Management Platform</p>
            </div>
          </div>

          {/* Module Navigation Pill Buttons */}
          <div className="flex flex-wrap items-center gap-1 bg-[#161922] border border-[#2a2f3d] p-1.5 rounded-2xl w-full lg:w-auto overflow-x-auto shadow-xl">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'dashboard' ? 'bg-slate-800 text-white border border-slate-600 font-semibold shadow' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" /> Dashboard
            </button>

            <button
              onClick={() => setActiveTab('borrowers')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'borrowers' ? 'bg-slate-800 text-white border border-slate-600 font-semibold shadow' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Users className="w-3.5 h-3.5 text-slate-300" /> Borrowers
            </button>

            <button
              onClick={() => setActiveTab('loans')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'loans' ? 'bg-slate-800 text-white border border-slate-600 font-semibold shadow' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <CreditCard className="w-3.5 h-3.5 text-slate-300" /> Loans Engine
            </button>

            <button
              onClick={() => setActiveTab('pushforward')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'pushforward' ? 'bg-slate-800 text-white border border-slate-600 font-semibold shadow' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <FastForward className="w-3.5 h-3.5 text-amber-400" /> Push Forward
            </button>

            <button
              onClick={() => setActiveTab('payment')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'payment' ? 'bg-emerald-600 text-white shadow' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Send className="w-3.5 h-3.5 text-emerald-300" /> M-PESA Pay
            </button>

            <button
              onClick={() => setActiveTab('ledger')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'ledger' ? 'bg-slate-800 text-white border border-slate-600 font-semibold shadow' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <DollarSign className="w-3.5 h-3.5 text-slate-300" /> Ledger
            </button>

            <button
              onClick={() => setActiveTab('formfees')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'formfees' ? 'bg-slate-800 text-white border border-slate-600 font-semibold shadow' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <FileText className="w-3.5 h-3.5 text-slate-300" /> Form Fees
            </button>

            <button
              onClick={() => setActiveTab('collateral')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'collateral' ? 'bg-slate-800 text-white border border-slate-600 font-semibold shadow' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Shield className="w-3.5 h-3.5 text-slate-300" /> Collateral
            </button>
          </div>
        </div>
      </header>

      {/* Main App Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-8 space-y-6 relative z-10">
        {/* Architecture Context Banner */}
        <div className="tm-content-box p-4 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-slate-400 flex-shrink-0" />
            <span>
              Shared Database Mode: <code className="text-slate-200 font-mono bg-[#0b0d12] px-2 py-0.5 rounded border border-[#2a2f3d]">desktop_legacy/mikopohub.db</code>
            </span>
          </div>
          <div className="flex items-center gap-4 text-slate-400 font-mono text-[11px]">
            <span className="flex items-center gap-1.5 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" /> All 7 Modules Parity
            </span>
            <span className="flex items-center gap-1.5">
              <Smartphone className="w-3.5 h-3.5 text-slate-400" /> PWA Favicon & Logo Active
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
      <footer className="border-t border-[#2a2f3d] py-6 px-4 text-center text-xs text-slate-500 font-mono relative z-10">
        MikopoHub Financial Systems &bull; Slate Gray & Charcoal Edition &bull; Next.js 16 & FastAPI
      </footer>
    </div>
  );
}
