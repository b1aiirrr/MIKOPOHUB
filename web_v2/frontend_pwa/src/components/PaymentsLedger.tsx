'use client';

import React, { useState, useEffect } from 'react';
import { DollarSign, Search, Calendar, FileSpreadsheet } from 'lucide-react';

interface PaymentRecord {
  id: number;
  loan_id: number;
  loan_number: string;
  borrower_name: string;
  payment_date: string;
  amount: number;
  interest_portion: number;
  principal_portion: number;
  payment_method: string;
  reference_number: string;
}

export default function PaymentsLedger() {
  const [payments, setPayments] = useState<PaymentRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPayments = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/payments');
      const json = await res.json();
      setPayments(json.data || []);
    } catch {
      setPayments([
        { id: 1, loan_id: 1, loan_number: 'LN-0001', borrower_name: 'David Kamau', payment_date: '2026-08-15', amount: 10000, interest_portion: 10000, principal_portion: 0, payment_method: 'M-PESA Buy Goods Till', reference_number: 'QGK7892X' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" /> Repayment Audit Ledger
          </h2>
          <p className="text-xs text-slate-400 mt-1">Audit log of all payments allocated to interest and principal</p>
        </div>
      </div>

      {/* Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase text-[10px] tracking-wider font-mono">
            <tr>
              <th className="py-3.5 px-4">Payment ID</th>
              <th className="py-3.5 px-4">Loan / Borrower</th>
              <th className="py-3.5 px-4">Date</th>
              <th className="py-3.5 px-4">Total Amount</th>
              <th className="py-3.5 px-4">Interest Paid</th>
              <th className="py-3.5 px-4">Principal Paid</th>
              <th className="py-3.5 px-4">Method / Reference</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {loading ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-slate-500 font-mono">Loading payments...</td>
              </tr>
            ) : payments.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-slate-500 font-mono">No payment transactions found</td>
              </tr>
            ) : (
              payments.map((p) => (
                <tr key={p.id} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-4 font-mono text-emerald-400">#PAY-{p.id}</td>
                  <td className="py-3.5 px-4">
                    <div className="font-semibold text-white">{p.loan_number}</div>
                    <div className="text-[11px] text-slate-500 font-mono">{p.borrower_name}</div>
                  </td>
                  <td className="py-3.5 px-4 font-mono">{p.payment_date}</td>
                  <td className="py-3.5 px-4 font-mono font-bold text-white">KES {p.amount.toLocaleString()}</td>
                  <td className="py-3.5 px-4 font-mono text-emerald-400">KES {p.interest_portion.toLocaleString()}</td>
                  <td className="py-3.5 px-4 font-mono text-sky-400">KES {p.principal_portion.toLocaleString()}</td>
                  <td className="py-3.5 px-4 font-mono text-slate-400 text-[11px]">
                    <div>{p.payment_method}</div>
                    <div className="text-slate-500 font-bold">{p.reference_number || '-'}</div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
