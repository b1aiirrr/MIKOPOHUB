'use client';

import React, { useState, useEffect } from 'react';
import { Users, Search, UserPlus, Phone, MapPin, CreditCard, RefreshCw, AlertCircle, CheckCircle } from 'lucide-react';

interface Borrower {
  id: number;
  borrower_number: string;
  full_name: string;
  phone: string;
  national_id: string;
  location: string;
  created_at: string;
  total_loans: number;
  active_loans: number;
}

export default function BorrowersManager() {
  const [borrowers, setBorrowers] = useState<Borrower[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [formData, setFormData] = useState({
    full_name: '',
    phone: '',
    national_id: '',
    location: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const fetchBorrowers = async () => {
    setLoading(true);
    try {
      const url = search 
        ? `http://localhost:8000/api/borrowers?search=${encodeURIComponent(search)}`
        : 'http://localhost:8000/api/borrowers';
      const res = await fetch(url);
      const json = await res.json();
      setBorrowers(json.data || []);
    } catch (err) {
      // Demo data
      setBorrowers([
        { id: 1, borrower_number: 'BRW-0001', full_name: 'David Kamau', phone: '0712345678', national_id: '32984712', location: 'Nairobi', created_at: '2026-08-01', total_loans: 2, active_loans: 1 },
        { id: 2, borrower_number: 'BRW-0002', full_name: 'Sarah Wanjiku', phone: '0723456789', national_id: '28471920', location: 'Kiambu', created_at: '2026-08-10', total_loans: 1, active_loans: 1 },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBorrowers();
  }, [search]);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.full_name || !formData.phone) return;
    setSubmitting(true);
    setMessage(null);

    try {
      const res = await fetch('http://localhost:8000/api/borrowers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      setMessage(`Registered ${data.borrower_number} successfully!`);
      setFormData({ full_name: '', phone: '', national_id: '', location: '' });
      setShowModal(false);
      fetchBorrowers();
    } catch {
      setMessage('Failed to register borrower.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-sky-400" /> Borrower Directory
          </h2>
          <p className="text-xs text-slate-400 mt-1">Manage borrower accounts and contact profiles</p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="bg-sky-600 hover:bg-sky-500 text-white font-medium px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 transition-all"
        >
          <UserPlus className="w-4 h-4" /> Add New Borrower
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
          placeholder="Search by name, phone, ID, or BRW number..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 text-white text-xs rounded-xl pl-11 pr-4 py-3 outline-none focus:border-sky-500"
        />
      </div>

      {/* Borrowers Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase text-[10px] tracking-wider font-mono">
            <tr>
              <th className="py-3.5 px-4">Borrower No</th>
              <th className="py-3.5 px-4">Full Name</th>
              <th className="py-3.5 px-4">Phone</th>
              <th className="py-3.5 px-4">National ID</th>
              <th className="py-3.5 px-4">Location</th>
              <th className="py-3.5 px-4">Active Loans</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {loading ? (
              <tr>
                <td colSpan={6} className="py-8 text-center text-slate-500 font-mono">Loading borrowers...</td>
              </tr>
            ) : borrowers.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-8 text-center text-slate-500 font-mono">No borrowers found</td>
              </tr>
            ) : (
              borrowers.map((b) => (
                <tr key={b.id} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-4 font-mono text-sky-400 font-medium">{b.borrower_number}</td>
                  <td className="py-3.5 px-4 font-semibold text-white">{b.full_name}</td>
                  <td className="py-3.5 px-4 font-mono">{b.phone}</td>
                  <td className="py-3.5 px-4 font-mono">{b.national_id || '-'}</td>
                  <td className="py-3.5 px-4">{b.location || '-'}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2 py-0.5 rounded font-mono font-medium text-[11px] ${
                      b.active_loans > 0 ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {b.active_loans} Active
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
            <h3 className="text-base font-bold text-white">Register New Borrower</h3>
            <form onSubmit={handleRegister} className="space-y-3">
              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">Full Name *</label>
                <input
                  type="text"
                  required
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">Phone Number *</label>
                <input
                  type="tel"
                  required
                  placeholder="0712345678"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-sky-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">National ID Number</label>
                <input
                  type="text"
                  value={formData.national_id}
                  onChange={(e) => setFormData({ ...formData, national_id: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-sky-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">Location / Address</label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-sky-500"
                />
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
                  className="flex-1 bg-sky-600 hover:bg-sky-500 text-white font-medium py-2.5 rounded-xl text-xs disabled:opacity-50"
                >
                  {submitting ? 'Registering...' : 'Save Borrower'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
