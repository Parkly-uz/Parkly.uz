'use client';

import React, { useState, useEffect } from 'react';
import AppShell from '@/components/layout/AppShell';
import { Users, Search, Filter, ShieldAlert, Clock, CheckCircle2, ArrowRight, Download } from 'lucide-react';

interface SessionItem {
  id: string;
  plate: string;
  slot: string;
  floor: number;
  entryTime: Date;
  status: 'active' | 'completed' | 'grace';
}

export default function SessionsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'active' | 'grace'>('all');
  const [successMsg, setSuccessMsg] = useState('');
  const [isMounted, setIsMounted] = useState(false);

  // Mock sessions with entry time initialized safely on client mount
  const [sessions, setSessions] = useState<SessionItem[]>([]);

  useEffect(() => {
    setIsMounted(true);
    setSessions([
      { id: 'SES-001', plate: '01 777 AAA', slot: 'A-101', floor: 1, entryTime: new Date(Date.now() - 45 * 60 * 1000), status: 'active' },
      { id: 'SES-002', plate: '40 B 321 CIS', slot: 'B-205', floor: 2, entryTime: new Date(Date.now() - 8 * 60 * 1000), status: 'grace' },
      { id: 'SES-003', plate: '10 Z 999 ZZ', slot: 'C-312', floor: 3, entryTime: new Date(Date.now() - 120 * 60 * 1000), status: 'active' },
      { id: 'SES-004', plate: '25 X 456 YY', slot: 'A-108', floor: 1, entryTime: new Date(Date.now() - 5 * 60 * 1000), status: 'grace' },
      { id: 'SES-005', plate: '70 O 111 OO', slot: 'D-401', floor: 4, entryTime: new Date(Date.now() - 300 * 60 * 1000), status: 'active' },
    ]);
  }, []);

  // Live timer tick every second
  const [, setTick] = useState(0);
  useEffect(() => {
    const timer = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatDuration = (entry: Date) => {
    const diffMs = Date.now() - entry.getTime();
    const diffSec = Math.floor(diffMs / 1000);
    const hrs = Math.floor(diffSec / 3600);
    const mins = Math.floor((diffSec % 3600) / 60);
    const secs = diffSec % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const calculateFee = (entry: Date) => {
    const diffMins = Math.floor((Date.now() - entry.getTime()) / (1000 * 60));
    if (diffMins <= 10) return 0; // Grace period free
    const hours = Math.ceil(diffMins / 60);
    return hours * 5000; // 5000 sum per hour
  };

  const handleExitSession = async (sessionId: string, plate: string) => {
    try {
      console.log(`Calling FastAPI /api/v1/gate/exit for session ${sessionId}, plate ${plate}`);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
      setSuccessMsg(`Seans yakunlandi va shlagbaum ochildi (${plate})`);
      setTimeout(() => setSuccessMsg(''), 4000);
    } catch (error) {
      console.error('Error exiting session:', error);
    }
  };

  const filteredSessions = sessions.filter((s) => {
    const matchesSearch = s.plate.toLowerCase().includes(searchQuery.toLowerCase()) || s.slot.toLowerCase().includes(searchQuery.toLowerCase());
    if (filterStatus === 'active') return matchesSearch && s.status === 'active';
    if (filterStatus === 'grace') return matchesSearch && (Date.now() - s.entryTime.getTime()) / (1000 * 60) <= 10;
    return matchesSearch;
  });

  if (!isMounted) return null;

  return (
    <AppShell>
      <div className="space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold uppercase tracking-wider">
                Live Parking Sessions
              </span>
              <h2 className="text-2xl font-bold text-white tracking-tight">Jonli To&apos;xtash Seanslari</h2>
            </div>
            <p className="text-sm text-slate-400 mt-1">Real vaqt rejimidagi taymerlar, grace period va shlagbaum boshqaruvi</p>
          </div>
        </div>

        {successMsg && (
          <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5" /> {successMsg}
          </div>
        )}

        {/* Filters & Search */}
        <div className="bg-slate-900 p-6 rounded-3xl border border-slate-800 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Avto raqam yoki slot bo'yicha qidirish..."
              className="w-full pl-11 pr-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
            />
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            <button
              onClick={() => setFilterStatus('all')}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                filterStatus === 'all' ? 'bg-emerald-500 text-slate-950 shadow-md' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              Barchasi ({sessions.length})
            </button>
            <button
              onClick={() => setFilterStatus('grace')}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                filterStatus === 'grace' ? 'bg-emerald-500 text-slate-950 shadow-md' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              Grace Period (Bepul)
            </button>
          </div>
        </div>

        {/* Sessions Table */}
        <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-950/40">
                  <th className="py-4 px-6">ID</th>
                  <th className="py-4 px-6">Avto Raqam</th>
                  <th className="py-4 px-6">Slot</th>
                  <th className="py-4 px-6">Kirish Vaqti</th>
                  <th className="py-4 px-6">Davomiyligi (Timer)</th>
                  <th className="py-4 px-6">Hisoblangan Summa</th>
                  <th className="py-4 px-6">Status</th>
                  <th className="py-4 px-6 text-right">Amallar</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-sm">
                {filteredSessions.map((s) => {
                  const diffMins = Math.floor((Date.now() - s.entryTime.getTime()) / (1000 * 60));
                  const isGrace = diffMins <= 10;
                  const fee = calculateFee(s.entryTime);

                  return (
                    <tr key={s.id} className="hover:bg-slate-800/40 transition-colors">
                      <td className="py-4 px-6 font-mono text-xs text-slate-400">{s.id}</td>
                      <td className="py-4 px-6 font-mono font-bold">
                        <span className="inline-block px-3 py-1 rounded-lg bg-amber-100 text-slate-950 border border-amber-300 shadow-xs tracking-wider text-xs">
                          {s.plate}
                        </span>
                      </td>
                      <td className="py-4 px-6 font-semibold text-slate-200">{s.slot} <span className="text-xs text-slate-500 font-normal">({s.floor}-qavat)</span></td>
                      <td className="py-4 px-6 text-slate-400 text-xs">{s.entryTime.toLocaleTimeString()}</td>
                      <td className="py-4 px-6 font-mono text-emerald-400 font-bold text-xs flex items-center gap-1.5 pt-5">
                        <Clock className="w-3.5 h-3.5 text-emerald-500" /> {formatDuration(s.entryTime)}
                      </td>
                      <td className="py-4 px-6 font-bold text-white">
                        {fee === 0 ? <span className="text-emerald-400 font-semibold">0 so&apos;m</span> : `${fee.toLocaleString()} so'm`}
                      </td>
                      <td className="py-4 px-6">
                        {isGrace ? (
                          <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold">
                            Grace Period (Bepul)
                          </span>
                        ) : (
                          <span className="px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold">
                            Faol Seans
                          </span>
                        )}
                      </td>
                      <td className="py-4 px-6 text-right">
                        <button
                          onClick={() => handleExitSession(s.id, s.plate)}
                          className="px-4 py-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs font-bold transition-all cursor-pointer"
                        >
                          Shlagbaumni Ochish
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
