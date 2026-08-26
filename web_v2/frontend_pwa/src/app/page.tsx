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
  Shield
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    'dashboard' | 'borrowers' | 'loans' | 'pushforward' | 'payment' | 'ledger' | 'formfees' | 'collateral'
  >('dashboard');

  const tickerItems = [
    { label: "M-PESA Gateway", val: "Active", color: "text-emerald-400" },
    { label: "Interest Rate", val: "20.0% Monthly", color: "text-slate-300" },
    { label: "Collateral Registry", val: "Secured", color: "text-slate-300" },
    { label: "System Status", val: "Operational", color: "text-emerald-400" },
  ];

  return (
    <div className="min-h-screen bg-[#0f1117] text-slate-100 flex flex-col font-sans selection:bg-emerald-600 selection:text-white relative overflow-hidden">
      {/* Ambient Glow Lights */}
      <div className="infinity-glow-bg w-[500px] h-[500px] bg-emerald-500/5 top-[-100px] left-[-100px]" />
      <div className="infinity-glow-bg w-[400px] h-[400px] bg-slate-600/5 bottom-[-100px] right-[-100px]" />

      {/* INFINITY TICKER MARQUEE BAR */}
      <div className="py-2.5 infinity-ticker-container text-xs font-mono">
        <div className="infinity-ticker-track">
          {[...Array(4)].map((_, loopIdx) => (
            <div key={loopIdx} className="inline-flex items-center gap-8 px-4">
              {tickerItems.map((item, idx) => (
                <div key={idx} className="inline-flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-slate-400 uppercase text-[10px] tracking-wider">{item.label}:</span>
                  <span className={`font-semibold ${item.color}`}>{item.val}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* CLEAN HEADER NAVBAR */}
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
              <h1 className="text-lg font-bold text-white tracking-tight font-sans">MikopoHub</h1>
              <p className="text-xs text-slate-400">Micro-Lending Management Platform</p>
            </div>
          </div>

          {/* Module Navigation Pill Buttons */}
          <div className="flex flex-wrap items-center gap-1 bg-[#161922] border border-[#2a2f3d] p-1.5 rounded-2xl w-full lg:w-auto overflow-x-auto shadow-xl">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'dashboard' ? 'bg-emerald-600 text-white font-bold shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" /> Dashboard
            </button>

            <button
              onClick={() => setActiveTab('borrowers')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'borrowers' ? 'bg-emerald-600 text-white font-bold shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Users className="w-3.5 h-3.5 text-slate-300" /> Borrowers
            </button>

            <button
              onClick={() => setActiveTab('loans')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'loans' ? 'bg-emerald-600 text-white font-bold shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <CreditCard className="w-3.5 h-3.5 text-slate-300" /> Loans Engine
            </button>

            <button
              onClick={() => setActiveTab('pushforward')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'pushforward' ? 'bg-emerald-600 text-white font-bold shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <FastForward className="w-3.5 h-3.5 text-amber-400" /> Push Forward
            </button>

            <button
              onClick={() => setActiveTab('payment')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'payment' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Send className="w-3.5 h-3.5 text-emerald-300" /> M-PESA Pay
            </button>

            <button
              onClick={() => setActiveTab('ledger')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'ledger' ? 'bg-emerald-600 text-white font-bold shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <DollarSign className="w-3.5 h-3.5 text-slate-300" /> Ledger
            </button>

            <button
              onClick={() => setActiveTab('formfees')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'formfees' ? 'bg-emerald-600 text-white font-bold shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <FileText className="w-3.5 h-3.5 text-slate-300" /> Form Fees
            </button>

            <button
              onClick={() => setActiveTab('collateral')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'collateral' ? 'bg-emerald-600 text-white font-bold shadow-md' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Shield className="w-3.5 h-3.5 text-slate-300" /> Collateral
            </button>
          </div>
        </div>
      </header>

      {/* Main App Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-8 space-y-6 relative z-10">
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

      {/* Clean Footer */}
      <footer className="border-t border-[#2a2f3d] py-6 px-4 text-center text-xs text-slate-500 font-sans relative z-10">
        MikopoHub Financial Systems &bull; Micro-Lending Management Platform
      </footer>
    </div>
  );
}
