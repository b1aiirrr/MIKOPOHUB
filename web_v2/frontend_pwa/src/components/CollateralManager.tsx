'use client';

import React, { useState, useEffect } from 'react';
import { Shield, Plus, Search, Tag, CheckCircle, Lock, Unlock } from 'lucide-react';

interface CollateralItem {
  id: number;
  collateral_number: string;
  loan_id: number;
  loan_number: string;
  borrower_name: string;
  security_type: string;
  description: string;
  estimated_value: number;
  serial_number: string;
  condition: string;
  date_received: string;
  status: string;
}

export default function CollateralManager() {
  const [items, setItems] = useState<CollateralItem[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [formData, setFormData] = useState({
    loan_id: '1',
    security_type: 'Motorcycle',
    description: '',
    estimated_value: '',
    serial_number: '',
    condition: 'Good',
    notes: '',
  });

  const fetchCollateral = async () => {
    setLoading(true);
    try {
      const url = search 
        ? `http://localhost:8000/api/collateral?search=${encodeURIComponent(search)}`
        : 'http://localhost:8000/api/collateral';
      const res = await fetch(url);
      const json = await res.json();
      setItems(json.data || []);
    } catch {
      setItems([
        { id: 1, collateral_number: 'COL-0001', loan_id: 1, loan_number: 'LN-0001', borrower_name: 'David Kamau', security_type: 'Motorcycle', description: 'TVS HLX 150 Red', estimated_value: 120000, serial_number: 'KMCR-892A', condition: 'Good', date_received: '2026-08-01', status: 'HELD' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCollateral();
  }, [search]);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.description) return;

    try {
      await fetch('http://localhost:8000/api/collateral', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          loan_id: parseInt(formData.loan_id),
          security_type: formData.security_type,
          description: formData.description,
          estimated_value: parseFloat(formData.estimated_value || '0'),
          serial_number: formData.serial_number,
          condition: formData.condition,
          notes: formData.notes,
        }),
      });
      setShowModal(false);
      setFormData({ loan_id: '1', security_type: 'Motorcycle', description: '', estimated_value: '', serial_number: '', condition: 'Good', notes: '' });
      fetchCollateral();
    } catch {
      alert('Failed to register collateral.');
    }
  };

  const toggleStatus = async (item: CollateralItem) => {
    const newStatus = item.status === 'HELD' ? 'RELEASED' : 'HELD';
    try {
      await fetch(`http://localhost:8000/api/collateral/${item.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });
      fetchCollateral();
    } catch {
      alert('Failed to update collateral status.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Shield className="w-5 h-5 text-purple-400" /> Collateral & Security Registry
          </h2>
          <p className="text-xs text-slate-400 mt-1">Register and manage physical collateral items secured against loans</p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="bg-purple-600 hover:bg-purple-500 text-white font-medium px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 transition-all"
        >
          <Plus className="w-4 h-4" /> Add Security Item
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          placeholder="Search collateral number, loan number, type, or serial number..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 text-white text-xs rounded-xl pl-11 pr-4 py-3 outline-none focus:border-purple-500"
        />
      </div>

      {/* Collateral Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 uppercase text-[10px] tracking-wider font-mono">
            <tr>
              <th className="py-3.5 px-4">Collateral No</th>
              <th className="py-3.5 px-4">Loan / Borrower</th>
              <th className="py-3.5 px-4">Security Type</th>
              <th className="py-3.5 px-4">Description</th>
              <th className="py-3.5 px-4">Est. Value</th>
              <th className="py-3.5 px-4">Serial / Reg No</th>
              <th className="py-3.5 px-4">Status</th>
              <th className="py-3.5 px-4">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {loading ? (
              <tr>
                <td colSpan={8} className="py-8 text-center text-slate-500 font-mono">Loading collateral registry...</td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={8} className="py-8 text-center text-slate-500 font-mono">No collateral records found</td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-4 font-mono text-purple-400 font-medium">{item.collateral_number}</td>
                  <td className="py-3.5 px-4">
                    <div className="font-semibold text-white">{item.loan_number}</div>
                    <div className="text-[11px] text-slate-500 font-mono">{item.borrower_name}</div>
                  </td>
                  <td className="py-3.5 px-4">{item.security_type}</td>
                  <td className="py-3.5 px-4">{item.description}</td>
                  <td className="py-3.5 px-4 font-mono font-bold text-white">
                    {item.estimated_value ? `KES ${item.estimated_value.toLocaleString()}` : '-'}
                  </td>
                  <td className="py-3.5 px-4 font-mono">{item.serial_number || '-'}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2.5 py-0.5 rounded font-mono font-bold text-[10px] ${
                      item.status === 'HELD'
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }`}>
                      {item.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <button
                      onClick={() => toggleStatus(item)}
                      className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded text-[11px] border border-slate-700 flex items-center gap-1"
                    >
                      {item.status === 'HELD' ? <Unlock className="w-3 h-3 text-emerald-400" /> : <Lock className="w-3 h-3 text-amber-400" />}
                      {item.status === 'HELD' ? 'Release' : 'Hold'}
                    </button>
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
            <h3 className="text-base font-bold text-white">Register Collateral Item</h3>
            <form onSubmit={handleRegister} className="space-y-3">
              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">Loan ID *</label>
                <input
                  type="number"
                  required
                  value={formData.loan_id}
                  onChange={(e) => setFormData({ ...formData, loan_id: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-purple-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">Security Type</label>
                <select
                  value={formData.security_type}
                  onChange={(e) => setFormData({ ...formData, security_type: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-purple-500"
                >
                  <option value="Motorcycle">Motorcycle</option>
                  <option value="Motor Vehicle">Motor Vehicle</option>
                  <option value="Land / Title Deed">Land / Title Deed</option>
                  <option value="Electronics / TV">Electronics / TV</option>
                  <option value="Phone / Laptop">Phone / Laptop</option>
                  <option value="Jewelry / Business Equipment">Jewelry / Business Equipment</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-400 mb-1">Description *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. TVS HLX 150 Red Motorbike"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-purple-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-medium text-slate-400 mb-1">Est. Value (KES)</label>
                  <input
                    type="number"
                    placeholder="120000"
                    value={formData.estimated_value}
                    onChange={(e) => setFormData({ ...formData, estimated_value: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-purple-500 font-mono"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-slate-400 mb-1">Serial / Reg No</label>
                  <input
                    type="text"
                    placeholder="KMCR-892A"
                    value={formData.serial_number}
                    onChange={(e) => setFormData({ ...formData, serial_number: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 text-white rounded-xl p-2.5 text-xs outline-none focus:border-purple-500 font-mono"
                  />
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
                  className="flex-1 bg-purple-600 hover:bg-purple-500 text-white font-medium py-2.5 rounded-xl text-xs"
                >
                  Save Collateral
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
