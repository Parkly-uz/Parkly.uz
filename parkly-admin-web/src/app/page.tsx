import React from 'react';
import { Sidebar, Header } from '@/components/layout';
import { Car, ShieldCheck, Cpu, AlertTriangle, ArrowUpRight, Clock } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex h-screen bg-slate-100 overflow-hidden font-sans">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header />

        <main className="flex-1 overflow-y-auto p-8 space-y-8">
          {/* Top Welcome / Status Bar */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
            <div>
              <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Avtoturargoh Boshqaruv Markazi</h2>
              <p className="text-sm text-slate-500 mt-1">Real-time monitoring, 3D vizualizatsiya va shlagbaum nazorati</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
                FastAPI & Supabase Ulangan
              </span>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Jami Joylar</p>
                <h3 className="text-3xl font-bold text-slate-900 mt-2">1,200</h3>
                <span className="text-xs text-emerald-600 font-medium flex items-center gap-1 mt-1">
                  <ArrowUpRight className="w-3.5 h-3.5" /> 4 qavatli majmua
                </span>
              </div>
              <div className="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center text-slate-700">
                <Car className="w-6 h-6" />
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Band Qilingan</p>
                <h3 className="text-3xl font-bold text-emerald-600 mt-2">842</h3>
                <span className="text-xs text-emerald-600 font-medium flex items-center gap-1 mt-1">
                  <ArrowUpRight className="w-3.5 h-3.5" /> 70.1% to&apos;lalik
                </span>
              </div>
              <div className="w-12 h-12 rounded-2xl bg-emerald-50 flex items-center justify-center text-emerald-600">
                <ShieldCheck className="w-6 h-6" />
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">ANPR Kameralar</p>
                <h3 className="text-3xl font-bold text-slate-900 mt-2">24 / 24</h3>
                <span className="text-xs text-emerald-600 font-medium flex items-center gap-1 mt-1">
                  Barchasi ishlayapti
                </span>
              </div>
              <div className="w-12 h-12 rounded-2xl bg-cyan-50 flex items-center justify-center text-cyan-600">
                <Cpu className="w-6 h-6" />
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Favqulodda Holat</p>
                <h3 className="text-3xl font-bold text-slate-900 mt-2">0</h3>
                <span className="text-xs text-slate-500 font-medium flex items-center gap-1 mt-1">
                  Muammolar yo&apos;q
                </span>
              </div>
              <div className="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center text-slate-700">
                <AlertTriangle className="w-6 h-6" />
              </div>
            </div>
          </div>

          {/* 3D Parking Simulation Placeholder & Live Feed */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 bg-slate-900 rounded-2xl p-6 text-white border border-slate-800 shadow-lg flex flex-col justify-between min-h-[420px]">
              <div className="flex items-center justify-between">
                <div>
                  <span className="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 text-xs font-mono">Three.js Ready</span>
                  <h3 className="text-xl font-bold mt-2">3D Avtoturargoh Simulyatsiyasi (4 Qavat)</h3>
                </div>
                <div className="flex gap-2">
                  <button className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium transition-colors">1-Qavat</button>
                  <button className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium transition-colors">2-Qavat</button>
                  <button className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium transition-colors">3-Qavat</button>
                  <button className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium transition-colors">4-Qavat</button>
                </div>
              </div>

              <div className="flex flex-col items-center justify-center py-16 text-center">
                <div className="w-20 h-20 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4 shadow-xl">
                  <Car className="w-10 h-10 animate-bounce" />
                </div>
                <h4 className="text-lg font-bold text-white">Sprint 2 da 3D Dvigatel Ulanadi</h4>
                <p className="text-sm text-slate-400 max-w-md mt-1">
                  @react-three/fiber va Three.js yordamida interaktiv 4 qavatli 3D avtoturargoh modeli shu yerda render qilinadi.
                </p>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-400 border-t border-slate-800 pt-4">
                <span>OrbitControls: Faol</span>
                <span>FPS: 60.0</span>
              </div>
            </div>

            {/* Recent Activity / Uzbek License Plates */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-slate-900">So&apos;nggi Kirishlar (ANPR)</h3>
                <Clock className="w-4 h-4 text-slate-400" />
              </div>

              <div className="space-y-3 flex-1">
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="px-2.5 py-1 bg-amber-100 border border-amber-300 rounded text-xs font-mono font-bold text-slate-900 shadow-xs">
                      01 A 777 AA
                    </div>
                    <div>
                      <p className="text-xs font-bold text-slate-800">Slot #A-102</p>
                      <p className="text-[10px] text-slate-500">10:42 AM • Qavat 1</p>
                    </div>
                  </div>
                  <span className="px-2 py-1 bg-emerald-50 text-emerald-600 rounded-lg text-xs font-semibold">Kirish</span>
                </div>

                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="px-2.5 py-1 bg-amber-100 border border-amber-300 rounded text-xs font-mono font-bold text-slate-900 shadow-xs">
                      40 B 321 CIS
                    </div>
                    <div>
                      <p className="text-xs font-bold text-slate-800">Slot #B-205</p>
                      <p className="text-[10px] text-slate-500">10:38 AM • Qavat 2</p>
                    </div>
                  </div>
                  <span className="px-2 py-1 bg-emerald-50 text-emerald-600 rounded-lg text-xs font-semibold">Kirish</span>
                </div>

                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="px-2.5 py-1 bg-amber-100 border border-amber-300 rounded text-xs font-mono font-bold text-slate-900 shadow-xs">
                      10 Z 999 ZZ
                    </div>
                    <div>
                      <p className="text-xs font-bold text-slate-800">Slot #C-312</p>
                      <p className="text-[10px] text-slate-500">10:25 AM • Qavat 3</p>
                    </div>
                  </div>
                  <span className="px-2 py-1 bg-rose-50 text-rose-600 rounded-lg text-xs font-semibold">Chiqish</span>
                </div>
              </div>

              <button className="w-full mt-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-semibold transition-colors">
                Barcha jurnallarni ko&apos;rish
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
