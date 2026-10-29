'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Lock, User, ArrowRight, ShieldCheck, Sparkles, KeyRound, Check } from 'lucide-react';

// Rasmiy Jamoa A'zolari va Hisoblar Bazasi (Login va Parollar)
export const TEAM_ACCOUNTS = [
  {
    name: 'Samaxov Dilshod',
    username: 'dilshod_pm',
    email: 'dilshod@parkly.uz',
    password: 'Parkly2026!Pm',
    role: 'SUPER_ADMIN',
    roleLabel: 'Super Admin (PM)',
    color: 'emerald'
  },
  {
    name: 'Erjigitov Mirhamid',
    username: 'mirhamid_be',
    email: 'mirhamid@parkly.uz',
    password: 'Parkly2026!Lead',
    role: 'SUPER_ADMIN',
    roleLabel: 'Super Admin (Lead)',
    color: 'emerald'
  },
  {
    name: 'Tohirjonov Hikmatilla',
    username: 'hikmatilla_fe',
    email: 'hikmatilla@parkly.uz',
    password: 'Parkly2026!Fe',
    role: 'ADMIN',
    roleLabel: 'Admin (Frontend)',
    color: 'cyan'
  },
  {
    name: 'Mamasarulov Jaloliddin',
    username: 'jaloliddin_iot',
    email: 'jaloliddin@parkly.uz',
    password: 'Parkly2026!Iot',
    role: 'ADMIN',
    roleLabel: 'Admin (IoT)',
    color: 'cyan'
  },
  {
    name: 'Saidov Abbosxon',
    username: 'abbosxon_qa',
    email: 'abbosxon@parkly.uz',
    password: 'Parkly2026!Qa',
    role: 'ADMIN',
    roleLabel: 'Admin (QA)',
    color: 'cyan'
  },
  {
    name: 'Omirboyev Said',
    username: 'omirboyev_cv',
    email: 'omirboyev@parkly.uz',
    password: 'Parkly2026!Cv',
    role: 'ADMIN',
    roleLabel: 'Admin (CV/ANPR)',
    color: 'cyan'
  },
  // Standart test hisoblar
  {
    name: 'Bosh Administrator',
    username: 'admin',
    email: 'admin@parkly.uz',
    password: 'admin123',
    role: 'SUPER_ADMIN',
    roleLabel: 'Super Admin (Test)',
    color: 'emerald'
  },
  {
    name: 'Navbatchi Operator',
    username: 'operator',
    email: 'operator@parkly.uz',
    password: 'operator123',
    role: 'OPERATOR',
    roleLabel: 'Operator (Test)',
    color: 'amber'
  }
];

export default function LoginPage() {
  const router = useRouter();
  const [loginInput, setLoginInput] = useState('mirhamid_be');
  const [password, setPassword] = useState('Parkly2026!Lead');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedUser, setSelectedUser] = useState<any>(TEAM_ACCOUNTS[1]);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    setTimeout(() => {
      const cleanInput = loginInput.trim().replace(/^@/, '').toLowerCase();
      const account = TEAM_ACCOUNTS.find(
        (acc) =>
          (acc.username.toLowerCase() === cleanInput || acc.email.toLowerCase() === cleanInput) &&
          acc.password === password
      );

      if (account) {
        // Sessiya ma'lumotlarini saqlash
        if (typeof window !== 'undefined') {
          localStorage.setItem('parkly_user', JSON.stringify(account));
          document.cookie = `parkly_token=valid_token_${account.username}; path=/`;
          document.cookie = `user_role=${account.role}; path=/`;
        }
        router.push('/');
      } else {
        setError('Login yoki parol noto\'g\'ri! Quyidagi ro\'yxatdan bir klikda tanlang.');
        setIsLoading(false);
      }
    }, 600);
  };

  const selectAccount = (acc: typeof TEAM_ACCOUNTS[0]) => {
    setLoginInput(acc.username);
    setPassword(acc.password);
    setSelectedUser(acc);
    setError('');
  };

  return (
    <div className="min-h-screen grid grid-cols-1 lg:grid-cols-2 bg-slate-950 font-sans">
      {/* Chap qism: Brending va Tavsif */}
      <div className="hidden lg:flex flex-col justify-between p-12 bg-gradient-to-br from-slate-900 via-slate-950 to-emerald-950 border-r border-slate-800 relative overflow-hidden">
        <div className="absolute -top-24 -left-24 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute -bottom-24 -right-24 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="flex items-center gap-3 relative z-10">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-500 to-cyan-400 flex items-center justify-center font-bold text-slate-950 shadow-xl shadow-emerald-500/20 text-xl">
            P
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Parkly.uz</h1>
            <p className="text-xs text-emerald-400 font-mono tracking-widest uppercase">Smart Parking Ecosystem</p>
          </div>
        </div>

        <div className="relative z-10 space-y-6 max-w-lg">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" /> Next-Gen Web Admin v2.0
          </div>
          <h2 className="text-4xl font-extrabold text-white tracking-tight leading-tight">
            Avtoturargohni sun&apos;iy intellekt va 3D bilan boshqaring.
          </h2>
          <p className="text-slate-400 text-base leading-relaxed">
            ANPR raqam tanish, real vaqt rejimidagi 4 qavatli 3D slot monitoringi va shlagbaum nazorati endi yagona platformada.
          </p>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md space-y-2">
            <p className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <KeyRound className="w-4 h-4 text-emerald-400" /> Rasmiy Jamoa Loginlari:
            </p>
            <p className="text-xs text-slate-400">
              Super Adminlar: <code className="text-emerald-400 font-bold">dilshod_pm</code>, <code className="text-emerald-400 font-bold">mirhamid_be</code><br />
              Adminlar: <code className="text-cyan-400">hikmatilla_fe</code>, <code className="text-cyan-400">jaloliddin_iot</code>, <code className="text-cyan-400">abbosxon_qa</code>, <code className="text-cyan-400">omirboyev_cv</code>
            </p>
          </div>
        </div>

        <div className="relative z-10 flex items-center gap-6 text-xs text-slate-500 border-t border-slate-800/80 pt-6">
          <span>© 2026 Parkly.uz</span>
          <span>•</span>
          <span>Xavfsiz shifrlangan RBAC ulanish</span>
        </div>
      </div>

      {/* O'ng qism: Login Forma va Xodimlar ro'yxati */}
      <div className="flex items-center justify-center p-6 lg:p-12 bg-slate-900 overflow-y-auto max-h-screen">
        <div className="w-full max-w-md space-y-6 bg-slate-900/80 p-8 rounded-3xl border border-slate-800 shadow-2xl backdrop-blur-xl">
          <div className="text-center space-y-2">
            <h3 className="text-2xl font-bold text-white tracking-tight">Tizimga kirish</h3>
            <p className="text-xs text-slate-400">Admin yoki jamoa hisob ma&apos;lumotlarini kiriting</p>
          </div>

          {error && (
            <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Login yoki Email</label>
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="text"
                  required
                  value={loginInput}
                  onChange={(e) => setLoginInput(e.target.value)}
                  placeholder="mirhamid_be yoki admin@parkly.uz"
                  className="w-full pl-11 pr-4 py-3 bg-slate-950/60 border border-slate-800 rounded-2xl text-sm text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Parol</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-11 pr-4 py-3 bg-slate-950/60 border border-slate-800 rounded-2xl text-sm text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3.5 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 font-bold rounded-2xl transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {isLoading ? (
                <span className="w-5 h-5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></span>
              ) : (
                <>
                  <span>Kirish ({selectedUser ? selectedUser.roleLabel : 'Boshqaruv'})</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* 1-Klikda Tezkor To'ldirish Ro'yxati */}
          <div className="space-y-2.5 pt-4 border-t border-slate-800/80">
            <p className="text-[11px] font-semibold text-slate-400 text-center uppercase tracking-wider">
              👇 1-Klikda Xodimni Tanlang (Avto-to&apos;ldirish):
            </p>

            <div className="space-y-1.5 max-h-52 overflow-y-auto pr-1">
              {TEAM_ACCOUNTS.slice(0, 6).map((acc) => {
                const isSelected = loginInput.toLowerCase().includes(acc.username);
                return (
                  <button
                    key={acc.username}
                    type="button"
                    onClick={() => selectAccount(acc)}
                    className={`w-full text-left p-2.5 rounded-xl border transition-all flex items-center justify-between cursor-pointer ${
                      isSelected
                        ? 'bg-emerald-500/15 border-emerald-500/50 text-white'
                        : 'bg-slate-950/40 hover:bg-slate-800/60 border-slate-800 text-slate-300'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <div
                        className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold ${
                          acc.role === 'SUPER_ADMIN'
                            ? 'bg-emerald-500/20 text-emerald-400'
                            : 'bg-cyan-500/20 text-cyan-400'
                        }`}
                      >
                        {acc.name[0]}
                      </div>
                      <div>
                        <p className="text-xs font-semibold leading-tight text-white">{acc.name}</p>
                        <p className="text-[10px] text-slate-400 font-mono">@{acc.username}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <span
                        className={`text-[9px] font-bold px-2 py-0.5 rounded-md uppercase tracking-wider ${
                          acc.role === 'SUPER_ADMIN'
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                            : 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                        }`}
                      >
                        {acc.role === 'SUPER_ADMIN' ? 'Super' : 'Admin'}
                      </span>
                      {isSelected && <Check className="w-3.5 h-3.5 text-emerald-400" />}
                    </div>
                  </button>
                );
              })}
            </div>

            <div className="grid grid-cols-2 gap-2 pt-1">
              <button
                type="button"
                onClick={() => selectAccount(TEAM_ACCOUNTS[6])}
                className="py-2 px-3 rounded-xl bg-slate-950 hover:bg-slate-800 text-emerald-400 text-xs font-semibold border border-slate-800 transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
              >
                <ShieldCheck className="w-3.5 h-3.5" /> Test Super
              </button>
              <button
                type="button"
                onClick={() => selectAccount(TEAM_ACCOUNTS[7])}
                className="py-2 px-3 rounded-xl bg-slate-950 hover:bg-slate-800 text-amber-400 text-xs font-semibold border border-slate-800 transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
              >
                <User className="w-3.5 h-3.5" /> Test Operator
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
