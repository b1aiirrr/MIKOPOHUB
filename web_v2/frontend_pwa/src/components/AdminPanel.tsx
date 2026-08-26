'use client';

import React, { useState, useEffect } from 'react';
import AuditLogMonitor from './AuditLogMonitor';
import { 
  ShieldCheck, 
  Users, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  Database, 
  Key, 
  RefreshCw, 
  FileText, 
  Activity,
  UserPlus,
  Lock,
  Zap,
  Sliders,
  DollarSign
} from 'lucide-react';

interface AdminPanelProps {
  user?: any;
}

export default function AdminPanel({ user }: AdminPanelProps) {
  const [activeAdminTab, setActiveAdminTab] = useState<'overview' | 'audit' | 'users' | 'approvals' | 'settings'>('overview');
  const [pendingLoans, setPendingLoans] = useState<any[]>([]);
  const [userList, setUserList] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    setLoading(true);
    try {
      // Mock / API dynamic data for admin management
      setPendingLoans([
        { id: 104, borrower_name: "Tony Blair", amount: 25000, interest_rate: 10, term: "3 Months", status: "PENDING", date: "2026-08-26" },
        { id: 105, borrower_name: "Mary Wambui", amount: 50000, interest_rate: 12, term: "6 Months", status: "PENDING", date: "2026-08-26" },
      ]);
      setUserList([
        { id: 1, username: "admin", role: "ADMIN", email: "admin@mikopohub.com", created: "2026-08-25" },
        { id: 2, username: "tonyblaiirr", role: "CLIENT", email: "tonyblaiirr@gmail.com", created: "2026-08-26" },
        { id: 3, username: "mary_wambui", role: "CLIENT", email: "mary@gmail.com", created: "2026-08-26" },
      ]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveLoan = (loanId: number) => {
    setPendingLoans(prev => prev.filter(l => l.id !== loanId));
    setActionMessage(`Loan #${loanId} facility successfully APPROVED!`);
    setTimeout(() => setActionMessage(null), 4000);
  };

  const handleRejectLoan = (loanId: number) => {
    setPendingLoans(prev => prev.filter(l => l.id !== loanId));
    setActionMessage(`Loan #${loanId} facility REJECTED.`);
    setTimeout(() => setActionMessage(null), 4000);
  };

  return (
    <div className="space-y-6">
      {/* Admin Panel Header Banner */}
      <div className="relative overflow-hidden bg-gradient-to-r from-[#161922] via-[#1a1f2e] to-[#0f1117] border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl">
        <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative z-10">
          <div className="flex items-center gap-4">
            <div className="p-3.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-2xl shadow-lg">
              <ShieldCheck className="w-8 h-8" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-xl sm:text-2xl font-black text-white tracking-tight">MikopoHub Admin Operations Panel</h1>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  SYSTEM ADMIN MODE
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">
                Full administrative control center for user management, credit approvals, database audit trail, and system configuration.
              </p>
            </div>
          </div>

          <button
            onClick={fetchAdminData}
            className="self-start sm:self-auto bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all shadow"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh System Data</span>
          </button>
        </div>
      </div>

      {actionMessage && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded-xl text-xs font-bold flex items-center gap-2 animate-fadeIn">
          <CheckCircle2 className="w-4 h-4" />
          <span>{actionMessage}</span>
        </div>
      )}

      {/* Admin Tab Switcher */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-3">
        <button
          onClick={() => setActiveAdminTab('overview')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all ${
            activeAdminTab === 'overview'
              ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20'
              : 'bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <Activity className="w-4 h-4" /> System Overview
        </button>

        <button
          onClick={() => setActiveAdminTab('approvals')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all relative ${
            activeAdminTab === 'approvals'
              ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20'
              : 'bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <CheckCircle2 className="w-4 h-4" /> Facility Approvals
          {pendingLoans.length > 0 && (
            <span className="ml-1 px-1.5 py-0.2 bg-amber-500 text-black font-black text-[10px] rounded-full">
              {pendingLoans.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveAdminTab('users')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all ${
            activeAdminTab === 'users'
              ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20'
              : 'bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <Users className="w-4 h-4" /> User Management
        </button>

        <button
          onClick={() => setActiveAdminTab('audit')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all ${
            activeAdminTab === 'audit'
              ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/20'
              : 'bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <ShieldCheck className="w-4 h-4" /> Security & Audit Logs
        </button>
      </div>

      {/* TAB CONTENT: OVERVIEW */}
      {activeAdminTab === 'overview' && (
        <div className="space-y-6">
          {/* Quick Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-[#161922] border border-[#2a2f3d] rounded-2xl p-5 space-y-2">
              <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
                <span>Active Users</span>
                <Users className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-2xl font-black text-white">{userList.length} Accounts</div>
              <div className="text-[11px] text-emerald-400 font-mono">1 Admin | {userList.length - 1} Clients</div>
            </div>

            <div className="bg-[#161922] border border-[#2a2f3d] rounded-2xl p-5 space-y-2">
              <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
                <span>Pending Approvals</span>
                <Clock className="w-4 h-4 text-amber-400" />
              </div>
              <div className="text-2xl font-black text-amber-400">{pendingLoans.length} Loans</div>
              <div className="text-[11px] text-slate-400 font-mono">Awaiting admin review</div>
            </div>

            <div className="bg-[#161922] border border-[#2a2f3d] rounded-2xl p-5 space-y-2">
              <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
                <span>Database Engine</span>
                <Database className="w-4 h-4 text-sky-400" />
              </div>
              <div className="text-2xl font-black text-white">SQLite WAL</div>
              <div className="text-[11px] text-emerald-400 font-mono">Shared mikopohub.db</div>
            </div>

            <div className="bg-[#161922] border border-[#2a2f3d] rounded-2xl p-5 space-y-2">
              <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
                <span>Security Token</span>
                <Key className="w-4 h-4 text-purple-400" />
              </div>
              <div className="text-2xl font-black text-white">Bcrypt + JWT</div>
              <div className="text-[11px] text-purple-400 font-mono">Encrypted Sessions</div>
            </div>
          </div>

          {/* Pending Approvals Quick Teaser */}
          {pendingLoans.length > 0 && (
            <div className="bg-[#161922] border border-amber-500/30 rounded-2xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-amber-500/10 text-amber-400 rounded-xl">
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-white">Action Required: Loan Requests Awaiting Approval</h3>
                    <p className="text-xs text-slate-400">Review pending facility applications from borrower clients</p>
                  </div>
                </div>
                <button
                  onClick={() => setActiveAdminTab('approvals')}
                  className="bg-amber-500 hover:bg-amber-400 text-black font-bold px-3.5 py-1.5 rounded-xl text-xs transition-all shadow"
                >
                  Review Approvals
                </button>
              </div>
            </div>
          )}

          {/* Audit Logs Teaser */}
          <AuditLogMonitor />
        </div>
      )}

      {/* TAB CONTENT: FACILITY APPROVALS */}
      {activeAdminTab === 'approvals' && (
        <div className="bg-[#161922] border border-[#2a2f3d] rounded-2xl p-6 space-y-6">
          <div>
            <h3 className="text-lg font-bold text-white">Facility Application Approvals</h3>
            <p className="text-xs text-slate-400">Approve or reject borrower loan applications</p>
          </div>

          {pendingLoans.length === 0 ? (
            <div className="p-8 text-center bg-[#0b0d12] border border-slate-800 rounded-xl space-y-2">
              <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
              <p className="text-sm font-semibold text-slate-300">All caught up! No pending loan requests.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {pendingLoans.map((loan) => (
                <div key={loan.id} className="p-4 bg-[#0b0d12] border border-slate-800 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-white">{loan.borrower_name}</span>
                      <span className="text-xs font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-300">Loan #{loan.id}</span>
                    </div>
                    <div className="text-xs text-slate-400">
                      Amount: <span className="text-emerald-400 font-bold font-mono">KES {loan.amount.toLocaleString()}</span> | Interest: {loan.interest_rate}% | Term: {loan.term}
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleApproveLoan(loan.id)}
                      className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all shadow"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" /> Approve Loan
                    </button>
                    <button
                      onClick={() => handleRejectLoan(loan.id)}
                      className="bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 px-3.5 py-2 rounded-xl text-xs font-bold transition-all"
                    >
                      <XCircle className="w-3.5 h-3.5" /> Reject
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB CONTENT: USER MANAGEMENT */}
      {activeAdminTab === 'users' && (
        <div className="bg-[#161922] border border-[#2a2f3d] rounded-2xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-bold text-white">Registered User Accounts</h3>
              <p className="text-xs text-slate-400">Manage client accounts and administrator permissions</p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-mono">
                  <th className="py-3 px-4">User ID</th>
                  <th className="py-3 px-4">Username</th>
                  <th className="py-3 px-4">Gmail / Email</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Created Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {userList.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-800/30">
                    <td className="py-3 px-4 font-mono text-slate-400">#{u.id}</td>
                    <td className="py-3 px-4 font-bold text-white">{u.username}</td>
                    <td className="py-3 px-4 text-slate-300 font-mono">{u.email || '-'}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        u.role === 'ADMIN' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-sky-500/20 text-sky-400 border border-sky-500/30'
                      }`}>
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">{u.created}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB CONTENT: AUDIT LOGS */}
      {activeAdminTab === 'audit' && (
        <AuditLogMonitor />
      )}
    </div>
  );
}

function Clock(props: any) {
  return (
    <svg {...props} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" strokeWidth="2" />
      <path strokeWidth="2" d="M12 6v6l4 2" />
    </svg>
  );
}
