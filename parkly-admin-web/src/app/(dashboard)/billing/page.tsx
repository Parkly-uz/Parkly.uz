'use client';

import React, { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { CreditCard, Download, TrendingUp, DollarSign, Calendar, Search, Settings, CheckCircle2, ShieldCheck, Layers, Sparkles } from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

export default function BillingPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'overview' | 'tariffs'>('overview');
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Standart soatlik tariflar
  const [tariffs, setTariffs] = useState({
    dayRate: 10000,          // Kunduzgi soatlik stavka (so'm)
    nightRate: 5000,         // Tungi soatlik stavka (so'm)
    gracePeriod: 10,         // Bepul vaqt (daqiqa)
    weekendMultiplier: 1.2,  // Dam olish kunlari koeffitsiyenti
    overstayPenalty: 50000,  // Ortiqcha turish jarimasi
  });

  // Uzoq muddatli abuna tariflari (1 oy, 3 oy, 6 oy)
  const [selectedPlanKey, setSelectedPlanKey] = useState<'1month' | '3month' | '6month'>('1month');
  const [subscriptionPlans, setSubscriptionPlans] = useState({
    '1month': {
      title: '1 Oylik Standart Abuna',
      durationMonths: 1,
      price: 450000,
      discountPercent: 0,
      vipSlotAccess: true,
      freeOvernightHours: 4,
      description: 'Har kuni cheksiz kirish-chiqish, A-zonada kafolatlangan joy',
    },
    '3month': {
      title: '3 Oylik Optimum Abuna (10% Chegirma)',
      durationMonths: 3,
      price: 1215000,
      discountPercent: 10,
      vipSlotAccess: true,
      freeOvernightHours: 8,
      description: 'Barcha qavatlar va EV quvvatlash stansiyalariga ustuvor kirish',
    },
    '6month': {
      title: '6 Oylik VIP Premium Abuna (20% Chegirma)',
      durationMonths: 6,
      price: 2160000,
      discountPercent: 20,
      vipSlotAccess: true,
      freeOvernightHours: 24,
      description: 'Shaxsiy 4-qavat VIP slot, kechayu-kunduz bepul to\'xtash va Fastline',
    },
  });

  const revenueData = [
    { day: 'Dush', income: 12500000 },
    { day: 'Sesh', income: 14200000 },
    { day: 'Chor', income: 11800000 },
    { day: 'Pay', income: 16400000 },
    { day: 'Jum', income: 19800000 },
    { day: 'Shan', income: 24500000 },
    { day: 'Yak', income: 21000000 },
  ];

  const paymentMethodsData = [
    { name: 'Payme', value: 45, color: '#0066FF' },
    { name: 'Click', value: 30, color: '#10B981' },
    { name: 'Uzum Pay', value: 15, color: '#8B5CF6' },
    { name: 'Naqd pul', value: 10, color: '#F59E0B' },
  ];

  const transactions = [
    { id: 'TX-9041', fiscal: 'FIS-883921', provider: 'Payme', plate: '01 777 AAA', amount: 15000, date: '2026-10-29 10:42', status: 'success' },
    { id: 'TX-9040', fiscal: 'FIS-883920', provider: 'Click', plate: '40 B 321 CIS', amount: 25000, date: '2026-10-29 10:38', status: 'success' },
    { id: 'TX-9039', fiscal: 'FIS-883919', provider: 'Uzum Pay', plate: '10 Z 999 ZZ', amount: 40000, date: '2026-10-29 10:25', status: 'success' },
    { id: 'TX-9038', fiscal: 'FIS-883918', provider: 'Naqd pul', plate: '25 X 456 YY', amount: 10000, date: '2026-10-29 10:15', status: 'success' },
    { id: 'TX-9037', fiscal: 'FIS-883917', provider: 'Payme', plate: '70 O 111 OO', amount: 30000, date: '2026-10-29 10:02', status: 'success' },
  ];

  const handleExportCSV = () => {
    const headers = ['ID', 'Fiskal Chek', 'Provayder', 'Avto Raqam', 'Summa (so\'m)', 'Sana', 'Holati'];
    const rows = transactions.map((t) => [t.id, t.fiscal, t.provider, t.plate, t.amount, t.date, t.status]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'parkly_transactions_report.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleSaveTariffs = (e: React.FormEvent) => {
    e.preventDefault();
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 3000);
  };

  const curPlan = subscriptionPlans[selectedPlanKey];

  return (
    <AppShell>
      <div className="space-y-8">
        {/* Yuqori Panel va Tablar */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">Moliya, Kassa va Tariflar</h2>
            <p className="text-sm text-slate-400 mt-1">Haftalik daromad, to&apos;lov provayderlari va avtoturargoh tarif stavkalari</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="bg-slate-900 p-1.5 rounded-2xl border border-slate-800 flex items-center gap-1">
              <button
                onClick={() => setActiveTab('overview')}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'overview'
                    ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Tushumlar & Grafiklar
              </button>
              <button
                onClick={() => setActiveTab('tariffs')}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
                  activeTab === 'tariffs'
                    ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Settings className="w-3.5 h-3.5" /> Tariflarni Sozlash
              </button>
            </div>

            <button
              onClick={handleExportCSV}
              className="flex items-center gap-2 px-4 py-3 bg-slate-900 hover:bg-slate-800 text-emerald-400 text-xs font-bold rounded-2xl border border-slate-800 transition-colors shadow-lg cursor-pointer"
            >
              <Download className="w-4 h-4" />
              <span>CSV Eksport</span>
            </button>
          </div>
        </div>

        {/* 1-TAB: Tushumlar va Grafiklar */}
        {activeTab === 'overview' && (
          <>
            {/* 3 ta metrika kartochkasi */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-6 rounded-3xl bg-gradient-to-br from-[#0F172A] to-blue-900/30 border border-slate-800 shadow-xl">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Haftalik Jami Tushum</span>
                <h3 className="text-3xl font-extrabold text-white mt-3">120,200,000 <span className="text-xs font-normal text-slate-400">so&apos;m</span></h3>
                <span className="inline-block mt-2 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
                  +14.2% o&apos;tgan haftadan
                </span>
              </div>

              <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Bugungi Sof Foyda (Net Profit)</span>
                <h3 className="text-3xl font-extrabold text-emerald-400 mt-3">11,880,000 <span className="text-xs font-normal text-slate-400">so&apos;m</span></h3>
                <p className="text-xs text-slate-500 mt-2">Kommunal va bank xizmatlari chegirilgach</p>
              </div>

              <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Tranzaksiyalar Soni</span>
                <h3 className="text-3xl font-extrabold text-white mt-3">1,482 <span className="text-xs font-normal text-slate-400">ta</span></h3>
                <p className="text-xs text-slate-500 mt-2">O&apos;rtacha chek: 15,200 so&apos;m</p>
              </div>
            </div>

            {/* Grafiklar qatori */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl">
                <h3 className="font-bold text-white text-base mb-1">Daromadlar Dinamikasi (Oxirgi 7 kun)</h3>
                <p className="text-xs text-slate-400 mb-6">Kunlik tushumlar hajmi (so&apos;mda)</p>
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={revenueData}>
                      <defs>
                        <linearGradient id="incomeGrad" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10B981" stopOpacity={0.4} />
                          <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <XAxis dataKey="day" stroke="#64748B" fontSize={12} tickLine={false} />
                      <YAxis stroke="#64748B" fontSize={12} tickLine={false} tickFormatter={(v) => `${v / 1000000}M`} />
                      <Tooltip
                        contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '16px', color: '#fff' }}
                        formatter={(value: any) => [`${Number(value).toLocaleString()} so'm`, 'Tushum']}
                      />
                      <Area type="monotone" dataKey="income" stroke="#10B981" strokeWidth={3} fillOpacity={1} fill="url(#incomeGrad)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col justify-between">
                <div>
                  <h3 className="font-bold text-white text-base mb-1">To&apos;lov Provayderlari Ulushi</h3>
                  <p className="text-xs text-slate-400 mb-4">Payme, Click, Uzum va Naqd</p>
                  <div className="h-52 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie data={paymentMethodsData} cx="50%" cy="50%" innerRadius={55} outerRadius={80} paddingAngle={5} dataKey="value">
                          {paymentMethodsData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '12px' }} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs pt-4 border-t border-slate-800">
                  {paymentMethodsData.map((m) => (
                    <div key={m.name} className="flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: m.color }}></span>
                      <span className="text-slate-300 font-medium">{m.name}:</span>
                      <span className="text-white font-bold">{m.value}%</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Tranzaksiyalar Jurnali Jadvali */}
            <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h3 className="font-bold text-white text-base">Tranzaksiyalar Jurnali</h3>
                  <p className="text-xs text-slate-400">Fiskal cheklar va muvaffaqiyatli to&apos;lovlar tarixi</p>
                </div>
                <div className="relative w-72">
                  <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Chek yoki avto raqam bo'yicha..."
                    className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  />
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-950/40">
                      <th className="py-4 px-6">Tranzaksiya ID</th>
                      <th className="py-4 px-6">Fiskal Chek</th>
                      <th className="py-4 px-6">Provayder</th>
                      <th className="py-4 px-6">Avto Raqam</th>
                      <th className="py-4 px-6">Summa</th>
                      <th className="py-4 px-6">Sana & Vaqt</th>
                      <th className="py-4 px-6">Holati</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-sm">
                    {transactions
                      .filter((tx) => tx.plate.toLowerCase().includes(searchQuery.toLowerCase()) || tx.fiscal.toLowerCase().includes(searchQuery.toLowerCase()))
                      .map((tx) => (
                        <tr key={tx.id} className="hover:bg-slate-800/40 transition-colors">
                          <td className="py-4 px-6 font-mono text-xs text-slate-400">{tx.id}</td>
                          <td className="py-4 px-6 font-mono font-semibold text-slate-200 text-xs">{tx.fiscal}</td>
                          <td className="py-4 px-6 font-medium text-slate-300">{tx.provider}</td>
                          <td className="py-4 px-6 font-mono font-bold">
                            <span className="inline-block px-2.5 py-0.5 rounded bg-amber-100 text-slate-950 border border-amber-300 text-xs">
                              {tx.plate}
                            </span>
                          </td>
                          <td className="py-4 px-6 font-extrabold text-white">{tx.amount.toLocaleString()} so&apos;m</td>
                          <td className="py-4 px-6 text-slate-400 text-xs">{tx.date}</td>
                          <td className="py-4 px-6">
                            <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold">
                              Muvaffaqiyatli
                            </span>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {/* 2-TAB: Tariflarni Sozlash Paneli (Faqat Super Admin uchun) */}
        {activeTab === 'tariffs' && (
          <div className="space-y-8 max-w-5xl">
            {/* Standart Soatlik Tariflar */}
            <div className="p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
              <div className="flex items-center justify-between border-b border-slate-800 pb-5">
                <div>
                  <h3 className="text-xl font-bold text-white flex items-center gap-2">
                    <Settings className="w-5 h-5 text-emerald-400" /> Standart Soatlik Tariflar & SLA
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">Soatlik stavkalar, bepul vaqt (Grace Period) va dam olish kunlari narxlari</p>
                </div>
                <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4" /> Super Admin Huquqi
                </span>
              </div>

              {saveSuccess && (
                <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Yangi tarif stavkalari muvaffaqiyatli saqlandi va barcha shlagbaumlarga uzatildi!</span>
                </div>
              )}

              <form onSubmit={handleSaveTariffs} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Kunduzgi Soatlik Narx (08:00 - 20:00)</label>
                  <div className="relative">
                    <input
                      type="number"
                      value={tariffs.dayRate}
                      onChange={(e) => setTariffs({ ...tariffs, dayRate: Number(e.target.value) })}
                      className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-white font-bold text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                    />
                    <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">so&apos;m / soat</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Tungi Soatlik Narx (20:00 - 08:00)</label>
                  <div className="relative">
                    <input
                      type="number"
                      value={tariffs.nightRate}
                      onChange={(e) => setTariffs({ ...tariffs, nightRate: Number(e.target.value) })}
                      className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-white font-bold text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                    />
                    <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">so&apos;m / soat</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Bepul Vaqt (Grace Period)</label>
                  <div className="relative">
                    <input
                      type="number"
                      value={tariffs.gracePeriod}
                      onChange={(e) => setTariffs({ ...tariffs, gracePeriod: Number(e.target.value) })}
                      className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-emerald-400 font-extrabold text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                    />
                    <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">daqiqa (Qat&apos;iy SLA)</span>
                  </div>
                  <p className="text-[11px] text-slate-500">Ushbu muddat ichida chiqqan transportdan to&apos;lov olinmaydi.</p>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Dam Olish Kunlari Koeffitsiyenti</label>
                  <div className="relative">
                    <input
                      type="number"
                      step="0.1"
                      value={tariffs.weekendMultiplier}
                      onChange={(e) => setTariffs({ ...tariffs, weekendMultiplier: Number(e.target.value) })}
                      className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-white font-bold text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                    />
                    <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">koeffitsiyent (x)</span>
                  </div>
                  <p className="text-[11px] text-slate-500">Shanba va Yakshanba kunlari standart narxga ko&apos;paytiriladi.</p>
                </div>

                <div className="md:col-span-2 pt-2 flex justify-end">
                  <button
                    type="submit"
                    className="px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-2xl text-xs transition-all shadow-lg shadow-emerald-500/20 cursor-pointer"
                  >
                    Soatlik Tariflarni Saqlash 💾
                  </button>
                </div>
              </form>
            </div>

            {/* Uzoq Muddatli Fastline Abunalari (Dropdown orqali 1 oy, 3 oy, 6 oy sozlash) */}
            <div className="p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
                <div>
                  <h3 className="text-xl font-bold text-white flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-amber-400" /> Uzoq Muddatli Fastline Abunalarini Sozlash
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">1 oylik, 3 oylik va 6 oylik doimiy mijozlar uchun maxsus tarif rejalarini boshqarish</p>
                </div>

                {/* Dropdown Reja Tanlagich */}
                <div className="relative">
                  <select
                    value={selectedPlanKey}
                    onChange={(e) => setSelectedPlanKey(e.target.value as any)}
                    className="px-4 py-2.5 bg-slate-950 border border-amber-500/40 text-amber-300 font-bold rounded-2xl text-xs focus:outline-none focus:ring-2 focus:ring-amber-500/30 cursor-pointer pr-8"
                  >
                    <option value="1month">📅 1 Oylik Standart Abuna</option>
                    <option value="3month">🌟 3 Oylik Optimum (10% chegirma)</option>
                    <option value="6month">👑 6 Oylik VIP Premium (20% chegirma)</option>
                  </select>
                </div>
              </div>

              {/* Tanlangan Reja Sozlamalari Formasi */}
              <div className="bg-slate-950/60 p-6 rounded-2xl border border-slate-800 space-y-6">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-4">
                  <div>
                    <h4 className="font-extrabold text-white text-base">{curPlan.title}</h4>
                    <p className="text-xs text-slate-400 mt-0.5">{curPlan.description}</p>
                  </div>
                  <span className="px-3 py-1 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/30 font-mono text-xs font-bold">
                    Muddat: {curPlan.durationMonths} oy
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Abuna Narxi</label>
                    <div className="relative">
                      <input
                        type="number"
                        value={curPlan.price}
                        onChange={(e) => {
                          const val = Number(e.target.value);
                          setSubscriptionPlans({
                            ...subscriptionPlans,
                            [selectedPlanKey]: { ...curPlan, price: val },
                          });
                        }}
                        className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-2xl text-white font-extrabold text-sm focus:outline-none focus:ring-2 focus:ring-amber-500/20"
                      />
                      <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">so&apos;m</span>
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Chegirma Foizi</label>
                    <div className="relative">
                      <input
                        type="number"
                        value={curPlan.discountPercent}
                        onChange={(e) => {
                          const val = Number(e.target.value);
                          setSubscriptionPlans({
                            ...subscriptionPlans,
                            [selectedPlanKey]: { ...curPlan, discountPercent: val },
                          });
                        }}
                        className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-2xl text-emerald-400 font-extrabold text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                      />
                      <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">% chegirma</span>
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Bepul Tungi Soatlar</label>
                    <div className="relative">
                      <input
                        type="number"
                        value={curPlan.freeOvernightHours}
                        onChange={(e) => {
                          const val = Number(e.target.value);
                          setSubscriptionPlans({
                            ...subscriptionPlans,
                            [selectedPlanKey]: { ...curPlan, freeOvernightHours: val },
                          });
                        }}
                        className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-2xl text-cyan-400 font-extrabold text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
                      />
                      <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">soat / sutka</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-slate-800/80">
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      id="vipAccess"
                      checked={curPlan.vipSlotAccess}
                      onChange={(e) => {
                        setSubscriptionPlans({
                          ...subscriptionPlans,
                          [selectedPlanKey]: { ...curPlan, vipSlotAccess: e.target.checked },
                        });
                      }}
                      className="w-4 h-4 rounded text-emerald-500 focus:ring-emerald-400 bg-slate-900 border-slate-700"
                    />
                    <label htmlFor="vipAccess" className="text-xs font-semibold text-slate-300 cursor-pointer">
                      4-Qavat VIP va EV zaryadlash stansiyasiga ustuvor kirish ruxsati
                    </label>
                  </div>

                  <button
                    onClick={() => {
                      setSaveSuccess(true);
                      setTimeout(() => setSaveSuccess(false), 3000);
                    }}
                    className="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-emerald-500 hover:from-amber-400 hover:to-emerald-400 text-slate-950 font-bold rounded-xl text-xs transition-all shadow-md shadow-amber-500/20 cursor-pointer"
                  >
                    Ushbu Abunani Saqlash 💾
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
