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
  ArrowRight,
  TrendingUp,
  Activity,
  PlusCircle
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    'dashboard' | 'borrowers' | 'loans' | 'pushforward' | 'payment' | 'ledger' | 'formfees' | 'collateral'
  >('dashboard');

  return (
    <div className="min-h-screen bg-[#090b10] text-slate-100 flex flex-col font-sans selection:bg-emerald-600 selection:text-white relative overflow-hidden">
      {/* Background Radial Glow Effects */}
      <div className="infinity-glow-bg w-[600px] h-[600px] bg-emerald-500/5 top-[-150px] left-[-150px]" />
      <div className="infinity-glow-bg w-[500px] h-[500px] bg-sky-500/5 top-[30%] right-[-150px]" />

      {/* TOP HEADER NAVIGATION BAR */}
      <header className="sticky top-0 z-50 bg-[#090b10]/90 backdrop-blur-xl border-b border-slate-800/80 px-4 sm:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative w-9 h-9 rounded-xl overflow-hidden border border-slate-700/80 shadow-md">
              <Image 
                src="/logo.png" 
                alt="MikopoHub Logo" 
                fill 
                className="object-cover" 
                priority 
              />
            </div>
            <div>
              <h1 className="text-base font-extrabold text-white tracking-tight font-sans">MikopoHub</h1>
              <p className="text-[11px] text-slate-400">Micro-Lending Management Platform</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button 
              onClick={() => setActiveTab('payment')}
              className="bg-emerald-600 hover:bg-emerald-500 text-white font-semibold px-4 py-2 rounded-xl text-xs flex items-center gap-2 transition-all shadow-lg shadow-emerald-600/20 active:scale-95"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Record Payment</span>
            </button>
            <button 
              onClick={() => setActiveTab('loans')}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all active:scale-95 hidden sm:flex"
            >
              <PlusCircle className="w-3.5 h-3.5 text-emerald-400" />
              <span>Issue Loan</span>
            </button>
          </div>
        </div>
      </header>

      {/* HERO SECTION */}
      <section className="relative pt-10 pb-8 px-4 sm:px-8 border-b border-slate-800/60 bg-gradient-to-b from-slate-900/40 via-slate-950/60 to-[#090b10]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Activity className="w-3.5 h-3.5" />
              <span>Enterprise Credit Portfolio Engine</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-white tracking-tight leading-tight">
              Modern Micro-Lending & Servicing Platform
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Automated borrower accounts, 20% compound interest servicing, M-PESA STK Push payment allocation, and collateral security tracking.
            </p>
          </div>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-2 gap-3 w-full md:w-auto font-mono text-xs">
            <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-2xl">
              <div className="text-slate-400 text-[10px] uppercase">Loan Book</div>
              <div className="text-lg font-bold text-white mt-0.5">KES 685,000</div>
            </div>
            <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-2xl">
              <div className="text-slate-400 text-[10px] uppercase">Active Facilities</div>
              <div className="text-lg font-bold text-emerald-400 mt-0.5">19 Accounts</div>
            </div>
          </div>
        </div>
      </section>

      {/* SINGLE-ROW HORIZONTAL NAVIGATION TABS (NO LINE WRAPPING) */}
      <div className="sticky top-[61px] z-40 bg-[#090b10]/95 backdrop-blur-md border-b border-slate-800/80 px-4 sm:px-8 py-2">
        <div className="max-w-7xl mx-auto flex items-center gap-2 overflow-x-auto no-scrollbar py-1">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'dashboard'
                ? 'bg-slate-800 text-white border border-slate-700 shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <LayoutDashboard className="w-3.5 h-3.5 text-sky-400" />
            <span>Dashboard</span>
          </button>

          <button
            onClick={() => setActiveTab('borrowers')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'borrowers'
                ? 'bg-slate-800 text-white border border-slate-700 shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <Users className="w-3.5 h-3.5 text-indigo-400" />
            <span>Borrowers</span>
          </button>

          <button
            onClick={() => setActiveTab('loans')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'loans'
                ? 'bg-slate-800 text-white border border-slate-700 shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <CreditCard className="w-3.5 h-3.5 text-emerald-400" />
            <span>Loans Engine</span>
          </button>

          <button
            onClick={() => setActiveTab('pushforward')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'pushforward'
                ? 'bg-slate-800 text-white border border-slate-700 shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <FastForward className="w-3.5 h-3.5 text-amber-400" />
            <span>Push Forward</span>
          </button>

          <button
            onClick={() => setActiveTab('payment')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'payment'
                ? 'bg-emerald-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <Send className="w-3.5 h-3.5 text-emerald-300" />
            <span>M-PESA Pay</span>
          </button>

          <button
            onClick={() => setActiveTab('ledger')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'ledger'
                ? 'bg-slate-800 text-white border border-slate-700 shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
            <span>Ledger</span>
          </button>

          <button
            onClick={() => setActiveTab('formfees')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'formfees'
                ? 'bg-slate-800 text-white border border-slate-700 shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <FileText className="w-3.5 h-3.5 text-cyan-400" />
            <span>Form Fees</span>
          </button>

          <button
            onClick={() => setActiveTab('collateral')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'collateral'
                ? 'bg-slate-800 text-white border border-slate-700 shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <Shield className="w-3.5 h-3.5 text-purple-400" />
            <span>Collateral</span>
          </button>
        </div>
      </div>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-8 space-y-6 relative z-10">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'borrowers' && <BorrowersManager />}
        {activeTab === 'loans' && <LoansManager />}
        {activeTab === 'pushforward' && <PushForwardManager />}
        {activeTab === 'payment' && <RecordPayment />}
        {activeTab === 'ledger' && <PaymentsLedger />}
        {activeTab === 'formfees' && <FormFeesManager />}
        {activeTab === 'collateral' && <CollateralManager />}
      </main>

      {/* FOOTER */}
      <footer className="border-t border-slate-800/80 py-6 px-4 text-center text-xs text-slate-500 font-sans relative z-10">
        MikopoHub Financial Systems &bull; Micro-Lending Management Platform
      </footer>
    </div>
  );
}
