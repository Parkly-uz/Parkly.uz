'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  LayoutDashboard,
  Box,
  Camera,
  Users,
  CreditCard,
  Settings,
  LogOut,
  Bell,
  Search,
  ChevronLeft,
  ChevronRight,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Car,
  X
} from 'lucide-react';

interface NotificationItem {
  id: string;
  title: string;
  message: string;
  time: string;
  type: 'info' | 'warning' | 'success';
  read: boolean;
}

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [collapsed, setCollapsed] = useState(false);
  const [currentUser, setCurrentUser] = useState<{ fullName: string; role: string; username: string }>({
    fullName: 'Erjigitov Mirhamid',
    role: 'SUPER_ADMIN',
    username: 'mirhamid_be',
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('parkly_user');
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          setCurrentUser(parsed);
        } catch (e) {}
      }
    }
  }, []);

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('parkly_user');
      document.cookie = 'parkly_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      document.cookie = 'user_role=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      document.cookie = 'user_name=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
    router.push('/login');
  };

  const navItems = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: '3D Map', href: '/map', icon: Box },
    { name: 'Cameras & ANPR', href: '/cameras', icon: Camera },
    { name: 'Sessions', href: '/sessions', icon: Users },
    { name: 'Billing', href: '/billing', icon: CreditCard },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <aside
      className={`relative bg-slate-950 text-slate-300 flex flex-col border-r border-slate-800 transition-all duration-300 ${
        collapsed ? 'w-20' : 'w-64'
      }`}
    >
      <div className="h-16 flex items-center justify-between px-5 border-b border-slate-800">
        <div className={`flex items-center gap-3 overflow-hidden ${collapsed ? 'hidden' : 'flex'}`}>
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-400 flex items-center justify-center font-bold text-slate-950 shadow-lg shrink-0">
            P
          </div>
          <div>
            <h1 className="font-bold text-base text-white tracking-tight">Parkly.uz</h1>
            <p className="text-[10px] text-emerald-400 font-mono">Smart Admin v2.0</p>
          </div>
        </div>
        {collapsed && (
          <div className="mx-auto w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-400 flex items-center justify-center font-bold text-slate-950 shadow-lg">
            P
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white transition-colors border border-slate-800 cursor-pointer"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      <nav className="flex-1 px-3 py-6 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3.5 py-3 rounded-xl font-medium transition-all group ${
                isActive
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm'
                  : 'text-slate-400 hover:bg-slate-900 hover:text-white'
              }`}
              title={collapsed ? item.name : undefined}
            >
              <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-emerald-400' : 'text-slate-500 group-hover:text-slate-300'}`} />
              {!collapsed && <span className="text-sm truncate">{item.name}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="p-3 border-t border-slate-800 space-y-2">
        {!collapsed && (
          <div className="flex items-center gap-3 px-3 py-2 bg-slate-900/60 rounded-xl border border-slate-800/80">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold flex items-center justify-center text-xs shrink-0 border border-emerald-500/30">
              {currentUser.fullName ? currentUser.fullName[0] : 'U'}
            </div>
            <div className="overflow-hidden">
              <h4 className="text-xs font-bold text-white truncate">{currentUser.fullName}</h4>
              <p className="text-[10px] text-emerald-400 font-mono">
                {currentUser.role === 'SUPER_ADMIN' ? 'Super Admin' : 'Admin'}
              </p>
            </div>
          </div>
        )}
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 w-full px-3.5 py-2.5 rounded-xl text-rose-400 hover:bg-rose-500/10 transition-colors font-medium text-xs cursor-pointer"
          title="Chiqish"
        >
          <LogOut className="w-5 h-5 shrink-0" />
          {!collapsed && <span>Chiqish</span>}
        </button>
      </div>
    </aside>
  );
}

export function Header() {
  const [timeStr, setTimeStr] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [barrierMsg, setBarrierMsg] = useState('');
  const notifRef = useRef<HTMLDivElement>(null);

  const [notifications, setNotifications] = useState<NotificationItem[]>([
    {
      id: '1',
      title: 'Kirish Shlagbaumi',
      message: '01 | 777 AAA avtomobili kirish postidan o\'tdi (Slot A-102)',
      time: '1 daqiqa oldin',
      type: 'success',
      read: false,
    },
    {
      id: '2',
      title: 'SLA Ogohlantirish',
      message: 'Slot B-205 dagi mashina to\'xtash muddati 8 daqiqadan oshdi',
      time: '5 daqiqa oldin',
      type: 'warning',
      read: false,
    },
    {
      id: '3',
      title: 'To\'lov Qabul Qilindi',
      message: 'Payme orqali 15,000 so\'m to\'lov amalga oshirildi (FIS-883921)',
      time: '12 daqiqa oldin',
      type: 'info',
      read: true,
    },
    {
      id: '4',
      title: 'ESP32 Status',
      message: 'ESP32-CAM kirish kontrolleri barqaror ulandi (RSSI: -58dBm)',
      time: '25 daqiqa oldin',
      type: 'info',
      read: true,
    },
  ]);

  const unreadCount = notifications.filter((n) => !n.read).length;

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  // Tashqariga bosilganda bildirishnomalar oynasini yopish
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) {
        setShowNotifications(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const markAllRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  const handleOpenBarrier = () => {
    setBarrierMsg('Shlagbaum muvaffaqiyatli ochildi! (ESP32 buyrug\'i yuborildi)');
    setTimeout(() => setBarrierMsg(''), 3000);
  };

  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 px-8 flex items-center justify-between shadow-md relative z-30">
      <div className="flex items-center gap-6 w-96">
        <div className="relative w-full">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Avto raqam, slot yoki xodim..."
            className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        {barrierMsg && (
          <div className="px-3 py-1.5 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 text-xs font-bold animate-pulse">
            {barrierMsg}
          </div>
        )}

        <div className="hidden md:flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-medium text-slate-300">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <span>System Online</span>
        </div>

        <div className="hidden lg:block font-mono text-xs text-slate-400 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800">
          {timeStr || '12:00:00'}
        </div>

        {/* Bildirishnomalar (Notification Bell + Popover) */}
        <div className="relative" ref={notifRef}>
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:bg-slate-800 text-slate-400 hover:text-white transition-colors cursor-pointer"
            title="Bildirishnomalar"
          >
            <Bell className="w-4 h-4" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-[10px] font-bold text-white flex items-center justify-center animate-pulse">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-3 w-80 sm:w-96 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden z-50">
              <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
                <div className="flex items-center gap-2">
                  <h4 className="font-bold text-sm text-white">Bildirishnomalar</h4>
                  {unreadCount > 0 && (
                    <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 text-[10px] font-bold">
                      {unreadCount} yangi
                    </span>
                  )}
                </div>
                <button
                  onClick={markAllRead}
                  className="text-[11px] text-emerald-400 hover:underline font-medium cursor-pointer"
                >
                  Hammasi o&apos;qildi
                </button>
              </div>

              <div className="max-h-80 overflow-y-auto divide-y divide-slate-800/60">
                {notifications.map((n) => (
                  <div
                    key={n.id}
                    className={`p-3.5 hover:bg-slate-800/40 transition-colors flex gap-3 ${
                      !n.read ? 'bg-slate-950/40' : ''
                    }`}
                  >
                    <div className="mt-0.5 shrink-0">
                      {n.type === 'success' && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                      {n.type === 'warning' && <AlertTriangle className="w-4 h-4 text-amber-400" />}
                      {n.type === 'info' && <Car className="w-4 h-4 text-cyan-400" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <p className="text-xs font-bold text-white truncate">{n.title}</p>
                        <span className="text-[10px] text-slate-500 shrink-0">{n.time}</span>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5 leading-snug">{n.message}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="p-2.5 bg-slate-950/80 border-t border-slate-800 text-center">
                <Link
                  href="/alerts"
                  onClick={() => setShowNotifications(false)}
                  className="text-xs text-slate-400 hover:text-emerald-400 font-semibold"
                >
                  Barcha xabarnomalarni ko&apos;rish →
                </Link>
              </div>
            </div>
          )}
        </div>

        <button
          onClick={handleOpenBarrier}
          className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 hover:bg-rose-500/20 text-xs font-bold transition-colors cursor-pointer"
        >
          <ShieldAlert className="w-4 h-4" />
          <span>Shlagbaum Ochish</span>
        </button>
      </div>
    </header>
  );
}

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden font-sans text-slate-100">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-8 bg-slate-900/50">{children}</main>
      </div>
    </div>
  );
}
