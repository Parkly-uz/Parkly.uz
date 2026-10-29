'use client';

import React, { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { ShieldAlert, AlertTriangle, CheckCircle2, Lock, Unlock, RefreshCw, Power } from 'lucide-react';

export default function AlertsPage() {
  const [barrierStatus, setBarrierStatus] = useState<'open' | 'closed'>('closed');
  const [isLoading, setIsLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const handleToggleBarrier = (action: 'open' | 'closed') => {
    setIsLoading(true);
    setSuccessMsg('');
    setTimeout(() => {
      setBarrierStatus(action);
      setIsLoading(false);
      setSuccessMsg(action === 'open' ? 'Shlagbaum favqulodda ochildi!' : 'Shlagbaum yopildi va bloklandi.');
    }, 600);
  };

  return (
    <AppShell>
      <div className="space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs font-bold uppercase tracking-wider">
                Emergency & Hardware
              </span>
              <h2 className="text-2xl font-bold text-white tracking-tight">Favqulodda Holatlar va Shlagbaum Nazorati</h2>
            </div>
            <p className="text-sm text-slate-400 mt-1">FastAPI orqali shlagbaumlarni favqulodda boshqarish va xavfsizlik loglari</p>
          </div>
        </div>

        {successMsg && (
          <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-2 shadow-lg">
            <CheckCircle2 className="w-5 h-5" /> {successMsg}
          </div>
        )}

        {/* Barrier Control Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl p-8 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold text-white">Asosiy Kirish Shlagbaumi (#GATE-01)</h3>
                <p className="text-xs text-slate-400 mt-1">MQTT / Modbus TCP orqali to&apos;g&apos;ridan-to&apos;g&apos;ri ulanish</p>
              </div>
              <span className={`px-4 py-1.5 rounded-full text-xs font-bold ${
                barrierStatus === 'open' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
              }`}>
                {barrierStatus === 'open' ? 'OCHIQ (OPEN)' : 'YOPIQ (CLOSED)'}
              </span>
            </div>

            <div className="py-12 flex flex-col items-center justify-center text-center space-y-4">
              <div className={`w-24 h-24 rounded-3xl flex items-center justify-center transition-all shadow-2xl ${
                barrierStatus === 'open' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-400 border border-rose-500/40'
              }`}>
                {barrierStatus === 'open' ? <Unlock className="w-12 h-12" /> : <Lock className="w-12 h-12" />}
              </div>
              <div>
                <h4 className="text-lg font-bold text-white">Shlagbaum holati: {barrierStatus === 'open' ? 'Ochiq' : 'Yopiq'}</h4>
                <p className="text-xs text-slate-400 max-w-sm mt-1">
                  Favqulodda vaziyatlarda yoki xodim ruxsati bilan shlagbaumni masofadan turib ochishingiz mumkin.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 pt-6 border-t border-slate-800">
              <button
                onClick={() => handleToggleBarrier('open')}
                disabled={isLoading || barrierStatus === 'open'}
                className="py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-2xl text-sm transition-all shadow-lg shadow-emerald-500/20 cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <Unlock className="w-4 h-4" /> Favqulodda Ochish
              </button>
              <button
                onClick={() => handleToggleBarrier('closed')}
                disabled={isLoading || barrierStatus === 'closed'}
                className="py-4 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded-2xl text-sm transition-all shadow-lg shadow-rose-600/20 cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <Lock className="w-4 h-4" /> Majburiy Yopish
              </button>
            </div>
          </div>

          {/* Active Alerts List */}
          <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-white text-base">Xavfsizlik Ogohlantirishlari</h3>
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            </div>

            <div className="space-y-3 flex-1 overflow-y-auto">
              {[
                { title: 'CAM-05 Offline', time: '09:12 AM', level: 'warning', desc: 'Kamera aloqasi uzildi (Ping timeout)' },
                { title: 'Ruxsatsiz kirish urunishi', time: '08:45 AM', level: 'danger', desc: 'Raqamsiz mashina o\'tishga urindi (#GATE-02)' },
                { title: 'Slot #A-102 uzoq turish', time: '07:30 AM', level: 'info', desc: 'Belgilangan vaqtdan oshdi (12 soat)' },
              ].map((alert, idx) => (
                <div key={idx} className="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-white">{alert.title}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                      alert.level === 'danger' ? 'bg-rose-500/20 text-rose-400' : alert.level === 'warning' ? 'bg-amber-500/20 text-amber-400' : 'bg-blue-500/20 text-blue-400'
                    }`}>
                      {alert.level.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{alert.desc}</p>
                  <p className="text-[10px] text-slate-600">{alert.time}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
