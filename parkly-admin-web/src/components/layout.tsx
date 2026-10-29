import React from 'react';
import Link from 'next/link';
import { LayoutDashboard, Car, ShieldAlert, Cpu, Settings, LogOut, Bell, Search } from 'lucide-react';

export function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-slate-100 flex flex-col border-r border-slate-800">
      <div className="h-16 flex items-center px-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-emerald-500 flex items-center justify-center font-bold text-slate-950 shadow-lg shadow-emerald-500/20">
            P
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-wide text-white">Parkly.uz</h1>
            <p className="text-xs text-slate-400 font-mono">Smart Admin v2.0</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-1.5">
        <Link
          href="/"
          className="flex items-center gap-3 px-4 py-3 rounded-xl bg-emerald-500/10 text-emerald-400 font-medium transition-colors"
        >
          <LayoutDashboard className="w-5 h-5" />
          <span>Dashboard & 3D</span>
        </Link>
        <Link
          href="/slots"
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-slate-300 hover:bg-slate-800/60 hover:text-white transition-colors"
        >
          <Car className="w-5 h-5 text-slate-400" />
          <span>Avto Slotlar</span>
        </Link>
        <Link
          href="/hardware"
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-slate-300 hover:bg-slate-800/60 hover:text-white transition-colors"
        >
          <Cpu className="w-5 h-5 text-slate-400" />
          <span>Apparat & ANPR</span>
        </Link>
        <Link
          href="/alerts"
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-slate-300 hover:bg-slate-800/60 hover:text-white transition-colors"
        >
          <ShieldAlert className="w-5 h-5 text-slate-400" />
          <span>Favqulodda / Alert</span>
        </Link>
        <Link
          href="/settings"
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-slate-300 hover:bg-slate-800/60 hover:text-white transition-colors"
        >
          <Settings className="w-5 h-5 text-slate-400" />
          <span>Sozlamalar</span>
        </Link>
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button className="flex items-center gap-3 w-full px-4 py-3 rounded-xl text-rose-400 hover:bg-rose-500/10 transition-colors font-medium">
          <LogOut className="w-5 h-5" />
          <span>Chiqish</span>
        </button>
      </div>
    </aside>
  );
}

export function Header() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 px-8 flex items-center justify-between shadow-xs">
      <div className="flex items-center gap-4 w-96">
        <div className="relative w-full">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Avto raqam yoki slot qidirish..."
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all text-slate-800 placeholder:text-slate-400"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="relative p-2.5 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-600 transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
        </button>

        <div className="flex items-center gap-3 pl-4 border-l border-slate-200">
          <div className="w-10 h-10 rounded-xl bg-slate-900 text-white font-bold flex items-center justify-center text-sm shadow-md">
            AD
          </div>
          <div className="hidden md:block">
            <h4 className="text-sm font-bold text-slate-800">Adminstrator</h4>
            <p className="text-xs text-slate-500">Super Admin</p>
          </div>
        </div>
      </div>
    </header>
  );
}
