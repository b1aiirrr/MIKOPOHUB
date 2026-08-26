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
  Menu,
  X,
  PlusCircle,
  FilePlus2,
  Receipt
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    'dashboard' | 'borrowers' | 'loans' | 'pushforward' | 'payment' | 'ledger' | 'formfees' | 'collateral'
  >('dashboard');

  const [sidebarOpen, setSidebarOpen] = useState<boolean>(false);

  const navCategories = [
    {
      title: "PORTFOLIO & CORE",
      items: [
        { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, color: 'text-sky-400' },
        { id: 'borrowers', label: 'Borrowers', icon: Users, color: 'text-indigo-400' },
        { id: 'loans', label: 'Loans Engine', icon: CreditCard, color: 'text-emerald-400' },
      ]
    },
    {
      title: "TRANSACTIONS",
      items: [
        { id: 'pushforward', label: 'Push Forward', icon: FastForward, color: 'text-amber-400' },
        { id: 'payment', label: 'M-PESA Pay', icon: Send, color: 'text-emerald-400', highlight: true },
        { id: 'ledger', label: 'Ledger', icon: DollarSign, color: 'text-emerald-400' },
      ]
    },
    {
      title: "ADMIN & SECURITY",
      items: [
        { id: 'formfees', label: 'Form Fees', icon: FileText, color: 'text-cyan-400' },
        { id: 'collateral', label: 'Collateral', icon: Shield, color: 'text-purple-400' },
      ]
    }
  ];

  const getActiveTabTitle = () => {
    switch (activeTab) {
      case 'dashboard': return 'Portfolio Overview';
      case 'borrowers': return 'Borrowers Management';
      case 'loans': return 'Credit & Loans Servicing';
      case 'pushforward': return 'Push Forward Calculator';
      case 'payment': return 'M-PESA Payment Allocation';
      case 'ledger': return 'General Payments Ledger';
      case 'formfees': return 'Form Fees & Registration';
      case 'collateral': return 'Collateral Physical Registry';
      default: return 'MikopoHub';
    }
  };

  return (
    <div className="min-h-screen bg-[#090b10] text-slate-100 flex font-sans selection:bg-emerald-600 selection:text-white relative overflow-hidden">
      {/* Background Radial Glow Effects */}
      <div className="infinity-glow-bg w-[500px] h-[500px] bg-emerald-500/5 top-[-100px] left-[-100px]" />
      <div className="infinity-glow-bg w-[400px] h-[400px] bg-sky-500/5 bottom-[-100px] right-[-100px]" />

      {/* MOBILE SIDEBAR OVERLAY BACKDROP */}
      {sidebarOpen && (
        <div 
          onClick={() => setSidebarOpen(false)}
          className="fixed inset-0 bg-black/70 backdrop-blur-sm z-40 lg:hidden"
        />
      )}

      {/* FIXED VERTICAL SIDEBAR */}
      <aside className={`fixed lg:static top-0 bottom-0 left-0 z-50 w-64 bg-[#0d1017] border-r border-slate-800/80 flex flex-col transition-transform duration-300 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      }`}>
        {/* Sidebar Header Brand */}
        <div className="p-5 border-b border-slate-800/80 flex items-center justify-between">
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
              <p className="text-[10px] text-slate-400">Micro-Lending Engine</p>
            </div>
          </div>
          <button 
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden text-slate-400 hover:text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Sidebar Navigation Links */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {navCategories.map((cat, idx) => (
            <div key={idx} className="space-y-2">
              <div className="px-3 text-[10px] font-mono text-slate-500 font-semibold tracking-wider">
                {cat.title}
              </div>
              <div className="space-y-1">
                {cat.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = activeTab === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => {
                        setActiveTab(item.id as any);
                        setSidebarOpen(false);
                      }}
                      className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                        isActive 
                          ? item.highlight 
                            ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20' 
                            : 'bg-slate-800 text-white border border-slate-700/80 shadow-md'
                          : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${isActive ? 'text-white' : item.color}`} />
                      <span>{item.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </aside>

      {/* MAIN CONTENT WORKSPACE */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* MINIMAL TOP HEADER BAR WITH REQUEST & PAYMENT TABS */}
        <header className="sticky top-0 z-30 bg-[#090b10]/95 backdrop-blur-xl border-b border-slate-800/80 px-4 sm:px-8 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 bg-slate-900 border border-slate-800 rounded-xl text-slate-300"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">{getActiveTabTitle()}</h2>
            </div>
          </div>

          {/* TOP HEADER QUICK TABS: REQUEST LOAN & M-PESA PAYMENT */}
          <div className="flex items-center gap-2 bg-[#161922] border border-[#2a2f3d] p-1 rounded-xl">
            <button 
              onClick={() => setActiveTab('loans')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'loans' 
                  ? 'bg-emerald-600 text-white shadow-md' 
                  : 'text-slate-300 hover:text-white hover:bg-slate-800'
              }`}
            >
              <FilePlus2 className="w-3.5 h-3.5" />
              <span>Request Loan</span>
            </button>

            <button 
              onClick={() => setActiveTab('payment')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'payment' 
                  ? 'bg-emerald-600 text-white shadow-md' 
                  : 'text-slate-300 hover:text-white hover:bg-slate-800'
              }`}
            >
              <Receipt className="w-3.5 h-3.5 text-emerald-300" />
              <span>Record Payment</span>
            </button>
          </div>
        </header>

        {/* MAIN MODULE VIEW CONTAINER */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-8 space-y-6">
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'borrowers' && <BorrowersManager />}
          {activeTab === 'loans' && <LoansManager />}
          {activeTab === 'pushforward' && <PushForwardManager />}
          {activeTab === 'payment' && <RecordPayment />}
          {activeTab === 'ledger' && <PaymentsLedger />}
          {activeTab === 'formfees' && <FormFeesManager />}
          {activeTab === 'collateral' && <CollateralManager />}
        </main>
      </div>
    </div>
  );
}
