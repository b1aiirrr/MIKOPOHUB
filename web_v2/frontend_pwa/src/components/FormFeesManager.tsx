'use client';

import React, { useState, useEffect } from 'react';
import { FileText, CheckCircle2, Clock, Plus, Search } from 'lucide-react';

interface FormFee {
  id: number;
  borrower_id: number;
  borrower_name: string;
  borrower_number: string;
  phone: string;
  requested_amount: number;
  fee_amount: number;
  payment_status: string;
  payment_method: string;
  reference_number: string;
  payment_date: string;
}

export default function FormFeesManager() {
  const [fees, setFees] = useState<FormFee[]>([]);
  const [loading, setLoading] = useState(true);
  const [payFeeId, setPayFeeId] = useState<number | null>(null);
  const [refNo, setRefNo] = useState('');

  const fetchFees = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/form-fees');
      const json = await res.json();
      setFees(json.data || []);
    } catch {
      setFees([
        { id: 1, borrower_id: 1, borrower_name: 'David Kamau', borrower_number: 'BRW-0001', phone: '0712345678', requested_amount: 50000, fee_amount: 500, payment_status: 'UNPAID', payment_method: '', reference_number: '', payment_date: '' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFees();
  }, []);

  const handlePayFee = async (feeId: number) => {
    if (!refNo.trim()) return;
    try {
      await fetch(`http://localhost:8000/api/form-fees/${feeId}/pay`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          payment_method: 'M-PESA',
          reference_number: refNo.trim(),
        }),
      });
      setPayFeeId(null);
      setRefNo('');
      fetchFees();
    } catch {
      alert('Failed to update form fee status.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-indigo-400" /> Application Form Fees
          </h2>
          <p className="text-xs text-slate-400 mt-1">Track processing form fees required prior to loan disbursement</p>
        </div>
      </div>

      {/* Form Fees Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase text-[10px] tracking-wider font-mono">
            <tr>
              <th className="py-3.5 px-4">Fee ID</th>
              <th className="py-3.5 px-4">Borrower</th>
              <th className="py-3.5 px-4">Requested Loan</th>
              <th className="py-3.5 px-4">Form Fee</th>
              <th className="py-3.5 px-4">Status</th>
              <th className="py-3.5 px-4">Action / Reference</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {loading ? (
              <tr>
                <td colSpan={6} className="py-8 text-center text-slate-500 font-mono">Loading form fees...</td>
              </tr>
            ) : fees.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-8 text-center text-slate-500 font-mono">No form fee records found</td>
              </tr>
            ) : (
              fees.map((f) => (
                <tr key={f.id} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-4 font-mono text-indigo-400">#FEE-{f.id}</td>
                  <td className="py-3.5 px-4">
                    <div className="font-semibold text-white">{f.borrower_name}</div>
                    <div className="text-[11px] text-slate-500 font-mono">{f.borrower_number}</div>
                  </td>
                  <td className="py-3.5 px-4 font-mono">KES {f.requested_amount.toLocaleString()}</td>
                  <td className="py-3.5 px-4 font-mono font-bold text-white">KES {f.fee_amount.toLocaleString()}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2.5 py-0.5 rounded font-mono font-bold text-[10px] ${
                      f.payment_status === 'PAID'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    }`}>
                      {f.payment_status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    {f.payment_status === 'PAID' ? (
                      <span className="font-mono text-slate-400 text-[11px]">{f.reference_number || 'PAID'}</span>
                    ) : payFeeId === f.id ? (
                      <div className="flex items-center gap-2">
                        <input
                          type="text"
                          placeholder="M-PESA Ref"
                          value={refNo}
                          onChange={(e) => setRefNo(e.target.value)}
                          className="bg-slate-950 border border-slate-800 text-white rounded p-1 text-xs w-28 font-mono uppercase"
                        />
                        <button
                          onClick={() => handlePayFee(f.id)}
                          className="bg-emerald-600 hover:bg-emerald-500 text-white px-2 py-1 rounded text-xs"
                        >
                          Save
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => setPayFeeId(f.id)}
                        className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1 rounded text-[11px] border border-slate-700"
                      >
                        Mark Paid
                      </button>
                    )}
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
