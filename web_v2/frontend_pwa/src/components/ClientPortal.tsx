'use client';

import React, { useEffect, useState } from 'react';
import { 
  CreditCard, 
  Send, 
  PlusCircle, 
  CheckCircle, 
  Clock, 
  DollarSign, 
  Receipt,
  AlertCircle,
  RefreshCw,
  UserCheck
} from 'lucide-react';

interface ClientPortalProps {
  user: any;
}

export default function ClientPortal({ user }: ClientPortalProps) {
  const [loans, setLoans] = useState<any[]>([]);
  const [payments, setPayments] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // New Loan Request State
  const [requestAmount, setRequestAmount] = useState<string>('');
  const [requestPurpose, setRequestPurpose] = useState<string>('');
  const [requesting, setRequesting] = useState<boolean>(false);
  const [requestMsg, setRequestMsg] = useState<string | null>(null);

  // Direct Pay State
  const [payLoanId, setPayLoanId] = useState<number | null>(null);
  const [payAmount, setPayAmount] = useState<string>('');
  const [payPhone, setPayPhone] = useState<string>('254700000000');
  const [paying, setPaying] = useState<boolean>(false);
  const [payMsg, setPayMsg] = useState<string | null>(null);

  const fetchClientData = async () => {
    if (!user || !user.borrower_id) return;
    setLoading(true);
    try {
      const [loansRes, paymentsRes] = await Promise.all([
        fetch(`http://localhost:8000/api/client/my-loans?borrower_id=${user.borrower_id}`),
        fetch(`http://localhost:8000/api/client/my-payments?borrower_id=${user.borrower_id}`)
      ]);

      if (loansRes.ok) {
        const lData = await loansRes.json();
        setLoans(lData.data || []);
      }
      if (paymentsRes.ok) {
        const pData = await paymentsRes.json();
        setPayments(pData.data || []);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClientData();
  }, [user]);

  const handleApplyLoan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !user.borrower_id) return;
    setRequesting(true);
    setRequestMsg(null);

    try {
      const res = await fetch('http://localhost:8000/api/loans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          borrower_id: user.borrower_id,
          principal: parseFloat(requestAmount),
          interest_rate: 20.0
        })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Loan request failed');

      setRequestMsg(`Loan request approved! Facility #${data.loan_number} issued successfully.`);
      setRequestAmount('');
      setRequestPurpose('');
      fetchClientData();
    } catch (err: any) {
      setRequestMsg(`Error: ${err.message}`);
    } finally {
      setRequesting(false);
    }
  };

  const handleMakePayment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!payLoanId) return;
    setPaying(true);
    setPayMsg(null);

    try {
      const res = await fetch('http://localhost:8000/api/payments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          loan_id: payLoanId,
          amount: parseFloat(payAmount),
          payment_method: 'M-PESA STK Push',
          phone_number: payPhone
        })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Payment allocation failed');

      setPayMsg(`M-PESA STK Push completed! Allocated KES ${payAmount}`);
      setPayAmount('');
      setPayLoanId(null);
      fetchClientData();
    } catch (err: any) {
      setPayMsg(`Error: ${err.message}`);
    } finally {
      setPaying(false);
    }
  };

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(val);
  };

  return (
    <div className="space-y-8">
      {/* Borrower Welcome Header */}
      <div className="bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-lg">
            <UserCheck className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">Borrower Client Portal</h2>
            <p className="text-xs text-slate-400 mt-0.5">Welcome, <span className="text-emerald-400 font-semibold">{user.username}</span> &bull; Account #{user.borrower_id}</p>
          </div>
        </div>

        <button
          onClick={fetchClientData}
          disabled={loading}
          className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-xl text-xs font-semibold border border-slate-700 transition-all"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} /> Refresh Portal
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Columns: Active Loans & Repayments */}
        <div className="lg:col-span-2 space-y-6">
          {/* Active Facilities Card */}
          <div className="bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <CreditCard className="w-4 h-4 text-emerald-400" /> My Active Loan Facilities
              </h3>
              <span className="text-xs font-mono text-slate-400">{loans.length} Facilities</span>
            </div>

            {loading ? (
              <div className="text-xs text-slate-400 py-6 text-center">Loading loans...</div>
            ) : loans.length === 0 ? (
              <div className="p-8 text-center text-xs text-slate-400 bg-[#0b0d12] rounded-xl border border-slate-800">
                You have no active loans at present. Apply for a facility on the right!
              </div>
            ) : (
              <div className="space-y-3">
                {loans.map((loan) => (
                  <div key={loan.id} className="bg-[#0b0d12] border border-[#2a2f3d] p-4 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-sm font-bold text-emerald-400">{loan.loan_number}</span>
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full ${
                          loan.status === 'ACTIVE' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-slate-800 text-slate-400'
                        }`}>
                          {loan.status}
                        </span>
                      </div>
                      <div className="text-xs text-slate-300 mt-1">
                        Issued: {loan.issue_date} &bull; Due: <span className="text-amber-400 font-mono">{loan.due_date}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-4 w-full sm:w-auto justify-between sm:justify-end">
                      <div className="text-right">
                        <div className="text-xs text-slate-400">Remaining Balance</div>
                        <div className="text-base font-bold text-white font-mono">{formatCurrency(loan.principal)}</div>
                      </div>
                      {loan.status === 'ACTIVE' && (
                        <button
                          onClick={() => { setPayLoanId(loan.id); setPayAmount((loan.principal * 0.2).toString()); }}
                          className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold px-3 py-2 rounded-xl flex items-center gap-1.5 shadow"
                        >
                          <Send className="w-3.5 h-3.5" /> Pay
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Payment Receipts History */}
          <div className="bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Receipt className="w-4 h-4 text-cyan-400" /> Payment Receipt History
            </h3>

            {payments.length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-400 bg-[#0b0d12] rounded-xl border border-slate-800">
                No payment receipts recorded yet.
              </div>
            ) : (
              <div className="divide-y divide-slate-800/80">
                {payments.map((p) => (
                  <div key={p.id} className="py-3 flex items-center justify-between text-xs">
                    <div>
                      <div className="font-semibold text-white">Payment #{p.id} &bull; <span className="font-mono text-emerald-400">{p.loan_number}</span></div>
                      <div className="text-[11px] text-slate-400 mt-0.5">{p.payment_date} via {p.payment_method}</div>
                    </div>
                    <div className="text-right font-mono">
                      <div className="font-bold text-emerald-400">{formatCurrency(p.amount)}</div>
                      <div className="text-[10px] text-slate-500">Ref: {p.reference_number || 'STK-AUTO'}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right 1 Column: Loan Request & Quick M-PESA STK Push Form */}
        <div className="space-y-6">
          {/* Quick Loan Request */}
          <div className="bg-[#161922] border border-[#2a2f3d] p-6 rounded-2xl space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <PlusCircle className="w-4 h-4 text-emerald-400" /> Apply for Loan Facility
            </h3>
            <p className="text-xs text-slate-400">Interest rate: 20% compound per monthly period.</p>

            {requestMsg && (
              <div className="p-3 text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-xl">
                {requestMsg}
              </div>
            )}

            <form onSubmit={handleApplyLoan} className="space-y-3">
              <div>
                <label className="text-xs text-slate-300 font-semibold block mb-1">Requested Principal (KES)</label>
                <input
                  type="number"
                  required
                  min="1000"
                  value={requestAmount}
                  onChange={(e) => setRequestAmount(e.target.value)}
                  placeholder="e.g. 25000"
                  className="w-full bg-[#0b0d12] border border-[#2a2f3d] rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div>
                <label className="text-xs text-slate-300 font-semibold block mb-1">Purpose / Notes</label>
                <input
                  type="text"
                  value={requestPurpose}
                  onChange={(e) => setRequestPurpose(e.target.value)}
                  placeholder="Business inventory expansion"
                  className="w-full bg-[#0b0d12] border border-[#2a2f3d] rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <button
                type="submit"
                disabled={requesting}
                className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 rounded-xl text-xs flex items-center justify-center gap-2 transition-all shadow"
              >
                {requesting ? 'Submitting...' : 'Submit Loan Request'}
              </button>
            </form>
          </div>

          {/* Quick Pay Modal Box */}
          {payLoanId && (
            <div className="bg-[#161922] border border-emerald-500/40 p-6 rounded-2xl space-y-4 shadow-xl">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Send className="w-4 h-4 text-emerald-400" /> M-PESA STK Push Payment
              </h3>

              {payMsg && (
                <div className="p-3 text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-xl">
                  {payMsg}
                </div>
              )}

              <form onSubmit={handleMakePayment} className="space-y-3">
                <div>
                  <label className="text-xs text-slate-300 font-semibold block mb-1">Amount to Pay (KES)</label>
                  <input
                    type="number"
                    required
                    value={payAmount}
                    onChange={(e) => setPayAmount(e.target.value)}
                    className="w-full bg-[#0b0d12] border border-[#2a2f3d] rounded-xl px-3.5 py-2.5 text-xs text-white font-mono"
                  />
                </div>

                <div>
                  <label className="text-xs text-slate-300 font-semibold block mb-1">M-PESA Phone Number</label>
                  <input
                    type="text"
                    required
                    value={payPhone}
                    onChange={(e) => setPayPhone(e.target.value)}
                    className="w-full bg-[#0b0d12] border border-[#2a2f3d] rounded-xl px-3.5 py-2.5 text-xs text-white font-mono"
                  />
                </div>

                <div className="flex items-center gap-2 pt-1">
                  <button
                    type="submit"
                    disabled={paying}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 rounded-xl text-xs transition-all shadow"
                  >
                    {paying ? 'Processing...' : 'Confirm STK Push'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setPayLoanId(null)}
                    className="px-3 py-2.5 bg-slate-800 text-slate-300 text-xs rounded-xl font-semibold"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
