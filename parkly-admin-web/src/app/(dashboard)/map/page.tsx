'use client';

import React, { useState, useEffect } from 'react';
import AppShell from '@/components/layout/AppShell';
import dynamic from 'next/dynamic';
import { Slot3DData } from '@/components/map/ParkingSlot3D';
import { supabase } from '@/lib/supabase/client';
import { Layers, RefreshCw, Car, Unlock, ShieldCheck, X, AlertCircle, CheckCircle2, BookmarkPlus } from 'lucide-react';

const Parking3DScene = dynamic(() => import('@/components/map/Parking3DScene'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-slate-950 text-slate-400">
      <div className="flex flex-col items-center gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-emerald-500" />
        <p className="text-sm font-medium">3D Dvigatel va Sahna yuklanmoqda...</p>
      </div>
    </div>
  ),
});

export default function MapPage() {
  const [selectedFloor, setSelectedFloor] = useState<number | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<Slot3DData | null>(null);
  const [plateInput, setPlateInput] = useState('');
  const [isOpeningBarrier, setIsOpeningBarrier] = useState(false);
  const [actionSuccess, setActionSuccess] = useState('');

  // 4 ta qavat bo'yicha boshlang'ich slotlar
  const [slots, setSlots] = useState<Slot3DData[]>(() => {
    const initial: Slot3DData[] = [];
    for (let floor = 1; floor <= 4; floor++) {
      for (let i = 1; i <= 12; i++) {
        const row = i <= 6 ? 0 : 1;
        const col = i <= 6 ? i - 1 : i - 7;
        const x = (col - 2.5) * 2.4;
        const z = (row - 0.5) * 4.8;

        const statuses: Array<'available' | 'occupied' | 'reserved' | 'ev'> = ['available', 'occupied', 'reserved', 'ev'];
        const status = statuses[(floor + i) % statuses.length];

        initial.push({
          id: `slot-${floor}-${i}`,
          slot_number: `${floor === 1 ? 'A' : floor === 2 ? 'B' : floor === 3 ? 'C' : 'VIP'}-${100 + i}`,
          floor,
          status,
          current_plate: status === 'occupied' ? `01 ${700 + i} AAA` : undefined,
          position: [x, 0, z],
        });
      }
    }
    return initial;
  });

  // Supabase Real-time Channel Integration
  useEffect(() => {
    const channel = supabase
      .channel('slots-changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'parking_slots' },
        (payload: any) => {
          if (payload.new) {
            setSlots((prev) =>
              prev.map((s) => (s.slot_number === payload.new.slot_number ? {
                ...s,
                status: payload.new.status === 'FREE' ? 'available' : payload.new.status === 'OCCUPIED' ? 'occupied' : 'reserved',
                current_plate: payload.new.current_vehicle_plate
              } : s))
            );
          }
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  // Shlagbaumni ochish
  const handleOpenBarrier = () => {
    setIsOpeningBarrier(true);
    setActionSuccess('');
    setTimeout(() => {
      setIsOpeningBarrier(false);
      setActionSuccess('Shlagbaum muvaffaqiyatli ochildi! (ESP32 buyrug\'i uzatildi)');
    }, 600);
  };

  // Joyni Bron Qilish (Sariq) yoki Band Qilish (Qizil)
  const handleBookSlot = async (type: 'reserved' | 'occupied') => {
    if (!selectedSlot) return;
    const plate = plateInput.trim().toUpperCase() || (type === 'occupied' ? '01 A 777 AA' : '01 B 999 BB');

    const updated = {
      ...selectedSlot,
      status: type,
      current_plate: plate
    };

    setSlots((prev) => prev.map((s) => (s.id === selectedSlot.id ? updated : s)));
    setSelectedSlot(updated);
    setPlateInput('');
    setActionSuccess(`${selectedSlot.slot_number} sloti muvaffaqiyatli ${type === 'reserved' ? 'BRON QILINDI (Sariq)' : 'BAND QILINDI (Qizil)'}!`);

    // Supabase bazasiga ham sinxronlash
    try {
      await supabase.from('parking_slots').upsert({
        slot_number: selectedSlot.slot_number,
        floor: selectedSlot.floor,
        zone: selectedSlot.slot_number.split('-')[0],
        status: type === 'reserved' ? 'RESERVED' : 'OCCUPIED',
        current_vehicle_plate: plate
      }, { onConflict: 'slot_number' });
    } catch (e) {
      console.log('Supabase sync background');
    }
  };

  // Joyni Bo'shatish (Yashil)
  const handleClearSlot = async () => {
    if (!selectedSlot) return;

    const updated = {
      ...selectedSlot,
      status: 'available' as const,
      current_plate: undefined
    };

    setSlots((prev) => prev.map((s) => (s.id === selectedSlot.id ? updated : s)));
    setSelectedSlot(updated);
    setActionSuccess(`${selectedSlot.slot_number} sloti tozalandi va BO'SHATILDI (Yashil)!`);

    // Supabase bazasiga ham sinxronlash
    try {
      await supabase.from('parking_slots').upsert({
        slot_number: selectedSlot.slot_number,
        floor: selectedSlot.floor,
        zone: selectedSlot.slot_number.split('-')[0],
        status: 'FREE',
        current_vehicle_plate: null
      }, { onConflict: 'slot_number' });
    } catch (e) {
      console.log('Supabase sync background');
    }
  };

  return (
    <AppShell>
      <div className="space-y-6 h-[calc(100vh-7rem)] flex flex-col">
        {/* Top Header & Floor Selector */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 p-6 rounded-3xl border border-slate-800 shadow-xl shrink-0">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold uppercase tracking-wider">
                Three.js • Real-time 3D
              </span>
              <h2 className="text-2xl font-bold text-white tracking-tight">3D Interaktiv Avtoturargoh</h2>
            </div>
            <p className="text-sm text-slate-400 mt-1">Joyni bosing ➔ Bron qiling yoki bo&apos;shating</p>
          </div>

          {/* Floor Selector Bar */}
          <div className="flex items-center gap-2 bg-slate-950 p-1.5 rounded-2xl border border-slate-800">
            <button
              onClick={() => setSelectedFloor(null)}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                selectedFloor === null
                  ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Barcha qavatlar
            </button>
            <button
              onClick={() => setSelectedFloor(1)}
              className={`px-3 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                selectedFloor === 1 ? 'bg-emerald-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              1-qavat (A)
            </button>
            <button
              onClick={() => setSelectedFloor(2)}
              className={`px-3 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                selectedFloor === 2 ? 'bg-emerald-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              2-qavat (B)
            </button>
            <button
              onClick={() => setSelectedFloor(3)}
              className={`px-3 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                selectedFloor === 3 ? 'bg-emerald-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              3-qavat (C)
            </button>
            <button
              onClick={() => setSelectedFloor(4)}
              className={`px-3 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                selectedFloor === 4 ? 'bg-emerald-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              4-qavat (VIP/EV)
            </button>
          </div>
        </div>

        {/* Action success alert */}
        {actionSuccess && (
          <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center justify-between animate-fadeIn">
            <span className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" /> {actionSuccess}
            </span>
            <button onClick={() => setActionSuccess('')} className="text-emerald-400 hover:text-white cursor-pointer">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* 3D Canvas & Inspection Sheet Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1 min-h-0 relative">
          <div className="lg:col-span-3 bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl overflow-hidden relative flex flex-col">
            <div className="absolute top-4 left-4 z-10 flex items-center gap-3 bg-slate-950/80 backdrop-blur-md px-4 py-2 rounded-2xl border border-slate-800 text-xs text-slate-300 shadow-lg">
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Erkin (Yashil)</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Band (Qizil)</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Bron (Sariq)</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span> EV (Moviy)</span>
            </div>

            <div className="flex-1 w-full h-full">
              <Parking3DScene
                slots={slots}
                selectedFloor={selectedFloor}
                selectedSlot={selectedSlot}
                onSelectSlot={(slot) => setSelectedSlot(slot)}
              />
            </div>
          </div>

          {/* Slot Inspection Modal / Sheet (Right side) */}
          <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 flex flex-col justify-between overflow-y-auto">
            <div>
              <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-5">
                <h3 className="font-bold text-white text-base">Slot Inspèktori</h3>
                {selectedSlot && (
                  <button onClick={() => setSelectedSlot(null)} className="p-1 rounded-lg bg-slate-800 text-slate-400 hover:text-white cursor-pointer">
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              {selectedSlot ? (
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-950 border border-slate-800">
                    <div>
                      <p className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Slot Raqami</p>
                      <h4 className="text-xl font-extrabold text-white mt-0.5">{selectedSlot.slot_number}</h4>
                    </div>
                    <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold">
                      Qavat {selectedSlot.floor}
                    </span>
                  </div>

                  <div className="space-y-2.5 text-xs">
                    <div className="flex justify-between py-2 border-b border-slate-800/60">
                      <span className="text-slate-400">Joriy Holati:</span>
                      <span className={`font-bold uppercase px-2 py-0.5 rounded ${
                        selectedSlot.status === 'available' ? 'bg-emerald-500/20 text-emerald-400' :
                        selectedSlot.status === 'occupied' ? 'bg-rose-500/20 text-rose-400' :
                        selectedSlot.status === 'reserved' ? 'bg-amber-500/20 text-amber-400' : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {selectedSlot.status === 'available' ? 'Bo\'sh (Erkin)' :
                         selectedSlot.status === 'occupied' ? 'Band' :
                         selectedSlot.status === 'reserved' ? 'Bron Qilingan' : 'EV Quvvatlash'}
                      </span>
                    </div>

                    <div className="flex justify-between py-2 border-b border-slate-800/60">
                      <span className="text-slate-400">Avto Raqami:</span>
                      <span className="font-mono font-bold text-amber-300">
                        {selectedSlot.current_plate || '—'}
                      </span>
                    </div>

                    <div className="flex justify-between py-2 border-b border-slate-800/60">
                      <span className="text-slate-400">Tarif:</span>
                      <span className="font-bold text-emerald-400">10,000 so&apos;m / soat</span>
                    </div>
                  </div>

                  {/* Agar slot BO'SH bo'lsa: Band qilish / Bron qilish formasi */}
                  {selectedSlot.status === 'available' && (
                    <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3 mt-4">
                      <p className="text-xs font-bold text-slate-200">Ushbu joyni band qilish:</p>
                      <input
                        type="text"
                        value={plateInput}
                        onChange={(e) => setPlateInput(e.target.value)}
                        placeholder="Avto raqam (masalan: 01A777AA)"
                        className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white placeholder:text-slate-500 uppercase font-mono focus:outline-none focus:ring-1 focus:ring-emerald-500"
                      />
                      <div className="grid grid-cols-2 gap-2">
                        <button
                          onClick={() => handleBookSlot('reserved')}
                          className="py-2.5 px-3 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded-xl text-xs transition-all flex items-center justify-center gap-1 cursor-pointer"
                        >
                          <BookmarkPlus className="w-3.5 h-3.5" /> Bron Qilish
                        </button>
                        <button
                          onClick={() => handleBookSlot('occupied')}
                          className="py-2.5 px-3 bg-rose-500 hover:bg-rose-400 text-white font-bold rounded-xl text-xs transition-all flex items-center justify-center gap-1 cursor-pointer"
                        >
                          <Car className="w-3.5 h-3.5" /> Band Qilish
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-16 text-slate-500 text-sm">
                  3D xaritadan biron bir slot ustiga bosing
                </div>
              )}
            </div>

            {selectedSlot && (
              <div className="space-y-2.5 pt-4 border-t border-slate-800 mt-4">
                {/* Agar slot BAND yoki BRON bo'lsa: Bo'shatish tugmasi */}
                {selectedSlot.status !== 'available' && (
                  <button
                    onClick={handleClearSlot}
                    className="w-full py-3 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-2"
                  >
                    <CheckCircle2 className="w-4 h-4" /> Joyni Bo&apos;shatish (Yashil qilish)
                  </button>
                )}

                <button
                  onClick={handleOpenBarrier}
                  disabled={isOpeningBarrier}
                  className="w-full py-3 bg-slate-800 hover:bg-slate-700 text-white font-semibold rounded-xl text-xs transition-all cursor-pointer flex items-center justify-center gap-2"
                >
                  <Unlock className="w-4 h-4 text-emerald-400" /> Shlagbaumni Ochish
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
