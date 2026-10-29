import AppShell from '@/components/layout/AppShell';
import { Car, ShieldCheck, Clock, ArrowUpRight, TrendingUp, AlertCircle, BookmarkCheck } from 'lucide-react';

export default function DashboardPage() {
  const recentActivities = [
    { id: '1', plate: '01 | 777 AAA', slot: 'A-101', type: 'Kirish', time: '10:42 AM', floor: 1, status: 'success' },
    { id: '2', plate: '40 | B 321 CIS', slot: 'B-205', type: 'Kirish', time: '10:38 AM', floor: 2, status: 'success' },
    { id: '3', plate: '10 | Z 999 ZZ', slot: 'C-312', type: 'Chiqish', time: '10:25 AM', floor: 3, status: 'exit' },
    { id: '4', plate: '25 | X 456 YY', slot: 'A-108', type: 'Kirish', time: '10:15 AM', floor: 1, status: 'success' },
    { id: '5', plate: '70 | O 111 OO', slot: 'D-401', type: 'Chiqish', time: '10:02 AM', floor: 4, status: 'exit' },
  ];

  return (
    <AppShell>
      <div className="space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">Dashboard & Monitoring</h2>
            <p className="text-sm text-slate-400 mt-1">Real vaqt rejimidagi ko&apos;rsatkichlar va jonli faoliyat jurnali</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-emerald-500/10 text-emerald-400 text-xs font-semibold border border-emerald-500/20">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              Supabase Realtime Active
            </span>
          </div>
        </div>

        {/* 4 ta asosiy statistika kartasi */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Card 1: Bugungi jami tushum */}
          <div className="relative overflow-hidden p-6 rounded-3xl bg-gradient-to-br from-[#0F172A] via-slate-900 to-[#0066FF]/30 border border-slate-800 shadow-xl flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Bugungi jami tushum</span>
              <div className="w-10 h-10 rounded-2xl bg-blue-500/20 text-blue-400 flex items-center justify-center">
                <TrendingUp className="w-5 h-5" />
              </div>
            </div>
            <div className="mt-4">
              <h3 className="text-3xl font-extrabold text-white tracking-tight">14,850,000 <span className="text-xs font-normal text-slate-400">so&apos;m</span></h3>
              <span className="inline-flex items-center gap-1 mt-2 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
                <ArrowUpRight className="w-3.5 h-3.5" /> +18.4% kechagiga nisbatan
              </span>
            </div>
          </div>

          {/* Card 2: Bo'sh joylar soni */}
          <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Bo&apos;sh joylar</span>
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold">
                ERKIN
              </span>
            </div>
            <div className="mt-4">
              <h3 className="text-3xl font-extrabold text-white tracking-tight">358 <span className="text-sm font-normal text-slate-500">/ 1200</span></h3>
              <p className="text-xs text-slate-400 mt-2">4 ta qavat bo&apos;yicha jami bo&apos;sh slotlar</p>
            </div>
          </div>

          {/* Card 3: Band joylar soni */}
          <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Band joylar</span>
              <span className="px-3 py-1 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs font-bold">
                BAND
              </span>
            </div>
            <div className="mt-4">
              <h3 className="text-3xl font-extrabold text-white tracking-tight">792 <span className="text-sm font-normal text-slate-500">/ 1200</span></h3>
              <p className="text-xs text-slate-400 mt-2">Hozirda avtoturargohda turganlar</p>
            </div>
          </div>

          {/* Card 4: Oldindan bronlar */}
          <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Oldindan bronlar</span>
              <span className="px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 text-xs font-bold">
                REZERV
              </span>
            </div>
            <div className="mt-4">
              <h3 className="text-3xl font-extrabold text-white tracking-tight">50 <span className="text-sm font-normal text-slate-500">ta</span></h3>
              <p className="text-xs text-slate-400 mt-2">Keyingi 2 soat ichida kutilmoqda</p>
            </div>
          </div>
        </div>

        {/* Jonli faollik jurnali */}
        <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-bold text-white">Jonli faollik jurnali (Recent Activity)</h3>
              <p className="text-xs text-slate-400">ANPR kameralari orqali qayd etilgan oxirgi avtomashinalar</p>
            </div>
            <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl transition-colors cursor-pointer">
              Barchasini ko&apos;rish
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  <th className="py-3.5 px-4">Avtomobil Raqami</th>
                  <th className="py-3.5 px-4">Slot</th>
                  <th className="py-3.5 px-4">Qavat</th>
                  <th className="py-3.5 px-4">Holati</th>
                  <th className="py-3.5 px-4">Vaqti</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-sm">
                {recentActivities.map((act) => (
                  <tr key={act.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-4 font-mono font-bold">
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-amber-100 text-slate-950 border border-amber-300 shadow-xs tracking-wider text-xs">
                        {act.plate}
                      </span>
                    </td>
                    <td className="py-4 px-4 font-semibold text-slate-200">{act.slot}</td>
                    <td className="py-4 px-4 text-slate-400">{act.floor}-Qavat</td>
                    <td className="py-4 px-4">
                      <span className={`inline-flex px-2.5 py-1 rounded-lg text-xs font-semibold ${
                        act.status === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}>
                        {act.type}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-slate-400 text-xs flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5 text-slate-500" /> {act.time}
                    </td>
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
