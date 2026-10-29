'use client';

import React, { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { CreditCard, Download, TrendingUp, DollarSign, Calendar, Search } from 'lucide-react';
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

  return (
    <AppShell>
      <div className="space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-bold uppercase tracking-wider">
                Financial Analytics
              </span>
              <h2 className="text-2xl font-bold text-white tracking-tight">Moliya va Hisobotlar</h2>
            </div>
            <p className="text-sm text-slate-400 mt-1">Daromadlar tahlili, to&apos;lov provayderlari va fiskal tranzaksiyalar</p>
          </div>

          <button
            onClick={handleExportCSV}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition-all shadow-lg shadow-emerald-500/20 cursor-pointer"
          >
            <Download className="w-4 h-4" /> CSV / Excel Eksport
          </button>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Revenue Area Chart (7 days) */}
          <div className="lg:col-span-2 bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 flex flex-col justify-between">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold text-white text-base">So&apos;nggi 7 Kundagi Daromad</h3>
                <p className="text-xs text-slate-400">Kunlik tushumlar dinamikasi (so&apos;m)</p>
              </div>
              <span className="px-3 py-1 rounded-xl bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20">
                Jami: 130.2 mln so&apos;m
              </span>
            </div>

            <div className="w-full h-72">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={revenueData}>
                  <defs>
                    <linearGradient id="colorIncome" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10B981" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="day" stroke="#64748B" fontSize={12} tickLine={false} />
                  <YAxis stroke="#64748B" fontSize={12} tickLine={false} tickFormatter={(val) => `${val / 1000000}M`} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '1rem', color: '#fff' }}
                    formatter={(val: any) => [`${Number(val).toLocaleString()} so'm`, 'Daromad']}
                  />
                  <Area type="monotone" dataKey="income" stroke="#10B981" strokeWidth={3} fillOpacity={1} fill="url(#colorIncome)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Payment Methods Pie Chart */}
          <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 flex flex-col justify-between">
            <div>
              <h3 className="font-bold text-white text-base mb-1">To&apos;lov Turlari Taqsimoti</h3>
              <p className="text-xs text-slate-400">Provayderlar kesimida ulush</p>
            </div>

            <div className="w-full h-56 flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={paymentMethodsData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                    {paymentMethodsData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '1rem', color: '#fff' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-2 gap-2 pt-4 border-t border-slate-800 text-xs">
              {paymentMethodsData.map((item, idx) => (
                <div key={idx} className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></span>
                  <span className="text-slate-300 font-medium">{item.name} ({item.value}%)</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Transactions Table */}
        <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-bold text-white text-base">Tranzaksiyalar Jurnali</h3>
              <p className="text-xs text-slate-400">Fiskal cheklar va muvaffaqiyatli to&apos;lovlar tarixi</p>
            </div>
            <div className="relative w-72">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                type="text"
                placeholder="Chek yoki raqam bo'yicha..."
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
                {transactions.map((tx) => (
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
      </div>
    </AppShell>
  );
}
