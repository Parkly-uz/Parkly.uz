'use client';

import React, { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { Camera, Eye, Play, ShieldAlert, CheckCircle2, Search, RefreshCw, Edit3, Unlock } from 'lucide-react';

interface ANPRLog {
  id: string;
  plate: string;
  confidence: number;
  readTimeMs: number;
  cameraId: string;
  time: string;
}

export default function CamerasPage() {
  const [manualPlate, setManualPlate] = useState('');
  const [selectedGate, setSelectedGate] = useState('GATE-01 (Kirish)');
  const [successMsg, setSuccessMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [anprLogs, setAnprLogs] = useState<ANPRLog[]>([
    { id: 'LOG-101', plate: '01 777 AAA', confidence: 98.4, readTimeMs: 42, cameraId: 'CAM-01 (Kirish)', time: '10:45:12' },
    { id: 'LOG-102', plate: '40 B 321 CIS', confidence: 96.2, readTimeMs: 55, cameraId: 'CAM-02 (Chiqish)', time: '10:44:50' },
    { id: 'LOG-103', plate: '10 Z 999 ZZ', confidence: 99.1, readTimeMs: 38, cameraId: 'CAM-01 (Kirish)', time: '10:42:15' },
    { id: 'LOG-104', plate: '25 X 456 YY', confidence: 95.7, readTimeMs: 61, cameraId: 'CAM-03 (Sektor A)', time: '10:40:05' },
  ]);

  const handleManualOverride = (e: React.FormEvent) => {
    e.preventDefault();
    if (!manualPlate) return;
    setIsSubmitting(true);
    setTimeout(() => {
      setIsSubmitting(false);
      setSuccessMsg(`Qo'lda kiritilgan raqam tasdiqlandi va shlagbaum ochildi: ${manualPlate.toUpperCase()}`);
      setManualPlate('');
      setTimeout(() => setSuccessMsg(''), 4000);
    }, 600);
  };

  return (
    <AppShell>
      <div className="space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold uppercase tracking-wider">
                ANPR & Computer Vision
              </span>
              <h2 className="text-2xl font-bold text-white tracking-tight">ANPR Kameralar Nazorati</h2>
            </div>
            <p className="text-sm text-slate-400 mt-1">Sun&apos;iy intellekt orqali davlat raqamlarini o&apos;qish va qo&apos;lda boshqarish</p>
          </div>
        </div>

        {successMsg && (
          <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-2 shadow-lg">
            <CheckCircle2 className="w-5 h-5" /> {successMsg}
          </div>
        )}

        {/* Video Streams & Manual Override Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Kirish / Chiqish Video Feeds */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
                  <h3 className="text-lg font-bold text-white">Kirish Asosiy Kamera (CAM-01)</h3>
                </div>
                <span className="px-3 py-1 rounded-lg bg-slate-800 text-emerald-400 text-xs font-mono font-bold">
                  MJPEG STREAM • 30 FPS
                </span>
              </div>

              {/* Video Player Mockup */}
              <div className="relative w-full h-72 bg-slate-950 rounded-2xl border border-slate-800 flex items-center justify-center overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px] opacity-40"></div>
                <div className="absolute top-4 left-4 z-10 px-3 py-1 rounded-xl bg-slate-900/80 backdrop-blur-md border border-slate-800 text-xs font-mono text-white flex items-center gap-2">
                  <span className="text-emerald-400">OCR Tanishi:</span> <b className="text-amber-300">01 777 AAA</b> (98.4%)
                </div>
                <div className="text-center space-y-2 relative z-10">
                  <Camera className="w-12 h-12 text-slate-700 mx-auto animate-pulse" />
                  <p className="text-xs text-slate-500 font-mono">rtsp://192.168.1.101:554/live/ch0</p>
                </div>
              </div>
            </div>
          </div>

          {/* Manual Plate Override Panel */}
          <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-3 border-b border-slate-800 pb-4 mb-6">
                <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center">
                  <Edit3 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-base">Qo&apos;lda Kiritish</h3>
                  <p className="text-xs text-slate-400">Xira yoki o&apos;qilmagan raqamlar uchun</p>
                </div>
              </div>

              <form onSubmit={handleManualOverride} className="space-y-4">
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Shlagbaum / Zona</label>
                  <select
                    value={selectedGate}
                    onChange={(e) => setSelectedGate(e.target.value)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  >
                    <option>GATE-01 (Kirish Asosiy)</option>
                    <option>GATE-02 (Chiqish Asosiy)</option>
                    <option>GATE-03 (VIP Kirish)</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Avto Raqami</label>
                  <input
                    type="text"
                    required
                    value={manualPlate}
                    onChange={(e) => setManualPlate(e.target.value)}
                    placeholder="Masalan: 01 A 777 AA"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-amber-300 font-mono font-bold tracking-wider placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full py-3.5 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 font-bold rounded-2xl transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 text-xs"
                >
                  <Unlock className="w-4 h-4" /> Raqamni Tasdiqlash va Shlagbaumni Ochish
                </button>
              </form>
            </div>

            <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 text-[11px] text-slate-400 mt-6 space-y-1">
              <p className="font-bold text-slate-300">Eslatma:</p>
              <p>Qo&apos;lda kiritilgan barcha harakatlar operator audit jurnaliga yozib boriladi.</p>
            </div>
          </div>
        </div>

        {/* Live OCR Recognition Log Table */}
        <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-bold text-white text-base">Jonli OCR Tanish Logi</h3>
              <p className="text-xs text-slate-400">YOLOv8 + OpenCV ANPR motoridan kelgan so&apos;nggi natijalar</p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-950/40">
                  <th className="py-4 px-6">Log ID</th>
                  <th className="py-4 px-6">O&apos;qilgan Raqam</th>
                  <th className="py-4 px-6">Aniqlik Darajasi (Confidence)</th>
                  <th className="py-4 px-6">O&apos;qish Vaqti (Latency)</th>
                  <th className="py-4 px-6">Kamera ID</th>
                  <th className="py-4 px-6">Sana & Vaqt</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-sm">
                {anprLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-mono text-xs text-slate-400">{log.id}</td>
                    <td className="py-4 px-6 font-mono font-bold">
                      <span className="inline-block px-3 py-1 rounded bg-amber-100 text-slate-950 border border-amber-300 text-xs">
                        {log.plate}
                      </span>
                    </td>
                    <td className="py-4 px-6 font-bold text-emerald-400">{log.confidence}%</td>
                    <td className="py-4 px-6 font-mono text-xs text-cyan-400">{log.readTimeMs} ms</td>
                    <td className="py-4 px-6 text-slate-300 text-xs">{log.cameraId}</td>
                    <td className="py-4 px-6 text-slate-400 text-xs">{log.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
