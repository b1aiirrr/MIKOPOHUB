'use client';

import React, { useState, useEffect } from 'react';
import { CreditCard, PlusCircle, Search, Calendar, DollarSign, CheckCircle, Clock } from 'lucide-react';

interface Loan {
  id: number;
  loan_number: string;
  borrower_id: number;
  borrower_name: string;
  borrower_phone: string;
  principal: number;
  interest_rate: number;
  issue_date: string;
  due_date: string;
  status: string;
}

export default function LoansManager() {
  const [loans, setLoans] = useState<Loan[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [formData, setFormData] = useState({
    borrower_id: '1',
    principal: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const fetchLoans = async () => {
    setLoading(true);
    try {
      const url = search 
        ? `http://localhost:8000/api/loans?search=${encodeURIComponent(search)}`
        : 'http://localhost:8000/api/loans';
      const res = await fetch(url);
      const json = await res.json();
      setLoans(json.data || []);
    } catch {
      setLoans([
        { id: 1, loan_number: 'LN-0001', borrower_id: 1, borrower_name: 'David Kamau', borrower_phone: '0712345678', principal: 50000, interest_rate: 20, issue_date: '2026-08-01', due_date: '2026-08-31', status: 'ACTIVE' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLoans();
  }, [search]);

  const handleIssueLoan = async (e: React.FormEvent) => {
    e.preventDefault();
    const principalNum = parseFloat(formData.principal);
    if (isNaN(principalNum) || principalNum <= 0) return;

    setSubmitting(true);
    setMessage(null);

    try {
      const res = await fetch('http://localhost:8000/api/loans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          borrower_id: parseInt(formData.borrower_id),
          principal: principalNum,
          interest_rate: 20.0,
        }),
      });
      const data = await res.json();
      setMessage(`Loan ${data.loan_number} issued with KES ${data.interest_due} monthly interest.`);
      setFormData({ borrower_id: '1', principal: '' });
      setShowModal(false);
      fetchLoans();
    } catch {
      setMessage('Failed to issue loan.');
    } finally {
      setSubmitting(false);
    }
  };

  const calculatedInterest = parseFloat(formData.principal || '0') * 0.20;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <CreditCard className="w-5 h-5 text-emerald-400" /> Loans Engine (20% Interest Rate)
          </h2>
          <p className="text-xs text-slate-400 mt-1">Issue loan facilities, calculate monthly schedules, and track statuses</p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 transition-all"
        >
          <PlusCircle className="w-4 h-4" /> Issue New Loan
        </button>
      </div>

      {message && (
        <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-4 rounded-xl text-xs flex items-center gap-2">
          <CheckCircle className="w-4 h-4" /> {message}
        </div>
      )}

      {/* Search Bar */}
      <div className="relative">
        <Search className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          placeholder="Search by loan number, borrower name, or phone..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 text-white text-xs rounded-xl pl-11 pr-4 py-3 outline-none focus:border-emerald-500"
        />
      </div>

      {/* Loans Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase text-[10px] tracking-wider font-mono">
            <tr>
              <th className="py-3.5 px-4">Loan No</th>
              <th className="py-3.5 px-4">Borrower</th>
              <th className="py-3.5 px-4">Remaining Principal</th>
              <th className="py-3.5 px-4">Interest Rate</th>
              <th className="py-3.5 px-4">Issue Date</th>
              <th className="py-3.5 px-4">Due Date</th>
              <th className="py-3.5 px-4">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {loading ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-slate-500 font-mono">Loading loans...</td>
              </tr>
            ) : loans.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-slate-500 font-mono">No loan facilities found</td>
              </tr>
            ) : (
              loans.map((l) => (
                <tr key={l.id} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-4 font-mono text-emerald-400 font-medium">{l.loan_number}</td>
                  <td className="py-3.5 px-4">
                    <div className="font-semibold text-white">{l.borrower_name}</div>
                    <div className="text-[11px] text-slate-500 font-mono">{l.borrower_phone}</div>
                  </td>
                  <td className="py-3.5 px-4 font-mono font-bold text-white">
                    KES {l.principal.toLocaleString()}
                  </td>
                  <td className="py-3.5 px-4 font-mono">{l.interest_rate}% / month</td>
                  <td className="py-3.5 px-4 font-mono">{l.issue_date}</td>
                  <td className="py-3.5 px-4 font-mono">{l.due_date}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2.5 py-0.5 rounded font-mono font-bold text-[10px] ${
                      l.status === 'ACTIVE'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-slate-800 text-slate-400'
                    }`}>
                      {l.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Form */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-md space-y-4">
            <h3 className="text-base font-bold text-white">Issue Loan Facility</h3>
            <form onSubmit={handleIssueLoan} className="space-y-4">
              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">Borrower ID *</label>
                <input
                  type="number"
                  required
                  value={formData.borrower_id}
                  onChange={(e) => setFormData({ ...formData, borrower_id: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">Principal Amount (KES) *</label>
                <input
                  type="number"
                  required
                  placeholder="e.g. 50000"
                  value={formData.principal}
                  onChange={(e) => setFormData({ ...formData, principal: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs space-y-1">
                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Interest Rate:</span>
                  <span className="text-white font-bold">20.0% / month</span>
                </div>
                <div className="flex justify-between text-slate-400 font-mono">
                  <span>Calculated Monthly Interest:</span>
                  <span className="text-emerald-400 font-bold">KES {calculatedInterest.toLocaleString()}</span>
                </div>
              </div>

              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium py-2.5 rounded-xl text-xs"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2.5 rounded-xl text-xs disabled:opacity-50"
                >
                  {submitting ? 'Issuing Loan...' : 'Confirm & Issue Loan'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
