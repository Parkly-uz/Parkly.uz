'use client';

import React, { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import dynamic from 'next/dynamic';
import { Box, Layers, Info, CheckCircle2, ShieldAlert, Car, RefreshCw } from 'lucide-react';

// Dynamic import for Three.js canvas to prevent SSR window issues
const ParkingScene = dynamic(() => import('@/components/map3d/ParkingScene'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-slate-950 text-slate-400">
      <div className="flex flex-col items-center gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-emerald-500" />
        <p className="text-sm font-medium">3D Dvigatel yuklanmoqda...</p>
      </div>
    </div>
  ),
});

export default function Map3DPage() {
  const [activeFloor, setActiveFloor] = useState<number | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<string | null>('F1-03');

  return (
    <AppShell>
      <div className="space-y-6 h-[calc(100vh-7rem)] flex flex-col">
        {/* Top Header info & Controls */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 p-6 rounded-3xl border border-slate-800 shadow-xl shrink-0">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs font-bold uppercase tracking-wider">
                Three.js WebGL
              </span>
              <h2 className="text-2xl font-bold text-white tracking-tight">3D Avtoturargoh Xaritasi</h2>
            </div>
            <p className="text-sm text-slate-400 mt-1">4 qavatli majmuaning real vaqt rejimidagi uch o&apos;lchamli modeli</p>
          </div>

          {/* Floor Selector Buttons */}
          <div className="flex items-center gap-2 bg-slate-950 p-1.5 rounded-2xl border border-slate-800">
            <button
              onClick={() => setActiveFloor(null)}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                activeFloor === null
                  ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Barchasi (4 Qavat)
            </button>
            {[1, 2, 3, 4].map((floor) => (
              <button
                key={floor}
                onClick={() => setActiveFloor(floor)}
                className={`px-3 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  activeFloor === floor
                    ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {floor}-Qavat
              </button>
            ))}
          </div>
        </div>

        {/* Main 3D Canvas and Side Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1 min-h-0">
          {/* 3D Canvas Viewport */}
          <div className="lg:col-span-3 bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl overflow-hidden relative flex flex-col">
            <div className="absolute top-4 left-4 z-10 flex items-center gap-2 bg-slate-950/80 backdrop-blur-md px-3.5 py-2 rounded-2xl border border-slate-800 text-xs text-slate-300">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>OrbitControls: Sichqoncha orqali aylantiring va yaqinlashing</span>
            </div>
            <div className="flex-1 w-full h-full">
              <ParkingScene
                activeFloor={activeFloor}
                selectedSlot={selectedSlot}
                onSelectSlot={(slot) => setSelectedSlot(slot)}
              />
            </div>
          </div>

          {/* Right Inspector Panel */}
          <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 flex flex-col justify-between">
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <h3 className="font-bold text-white text-base">Slot Inspèktori</h3>
                <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono font-bold">
                  {selectedSlot || 'Tanlanmagan'}
                </span>
              </div>

              {selectedSlot ? (
                <div className="space-y-4">
                  <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Holati:</span>
                      <span className="font-bold text-emerald-400">Erkin (Available)</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Qavat:</span>
                      <span className="font-bold text-slate-200">Qavat {selectedSlot.charAt(1)}</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Sensor:</span>
                      <span className="font-bold text-slate-200">MQTT Connected (#IoT-04)</span>
                    </div>
                  </div>

                  <div className="p-4 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-300 text-xs space-y-1">
                    <p className="font-bold flex items-center gap-1.5">
                      <Info className="w-4 h-4" /> Tezkor harakatlar
                    </p>
                    <p className="text-blue-200/80">Ushbu slotni band qilish yoki texnik xizmatga o&apos;tkazish mumkin.</p>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-slate-500 text-sm">
                  3D xaritadan biron bir slotni tanlang
                </div>
              )}
            </div>

            <div className="space-y-3 pt-6 border-t border-slate-800">
              <button className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-2xl text-xs transition-all shadow-lg shadow-emerald-500/20 cursor-pointer">
                Slotni Bron Qilish
              </button>
              <button className="w-full py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-2xl text-xs transition-all cursor-pointer">
                Xizmat Ko&apos;rsatishga O&apos;tkazish
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
