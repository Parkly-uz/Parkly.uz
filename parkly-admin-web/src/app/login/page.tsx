'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Lock, User, ArrowRight, Sparkles } from 'lucide-react';
import { TEAM_ACCOUNTS } from '@/lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const [loginInput, setLoginInput] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Parollar lug'ati
  const PASSWORDS: Record<string, string> = {
    dilshod_pm: 'Parkly2026!Pm',
    mirhamid_be: 'Parkly2026!Lead',
    hikmatilla_fe: 'Parkly2026!Fe',
    jaloliddin_iot: 'Parkly2026!Iot',
    abbosxon_qa: 'Parkly2026!Qa',
    omirboyev_cv: 'Parkly2026!Cv',
    admin: 'admin123',
    operator: 'operator123',
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    setTimeout(() => {
      const cleanInput = loginInput.trim().replace(/^@/, '').toLowerCase();

      // Email yoki username bo'yicha qidirish
      let foundUsername = '';
      if (cleanInput.includes('@')) {
        const prefix = cleanInput.split('@')[0];
        foundUsername = prefix;
      } else {
        foundUsername = cleanInput;
      }

      // Maxsus hisoblar
      if (foundUsername === 'admin' && password === 'admin123') {
        saveSession('admin', 'Bosh Administrator', 'SUPER_ADMIN');
        return;
      }
      if (foundUsername === 'operator' && password === 'operator123') {
        saveSession('operator', 'Navbatchi Operator', 'ADMIN');
        return;
      }

      const account = TEAM_ACCOUNTS[foundUsername];
      const correctPass = PASSWORDS[foundUsername];

      if (account && correctPass && password === correctPass) {
        saveSession(account.username, account.fullName, account.role);
      } else {
        setError('Login yoki parol noto\'g\'ri! Iltimos, ma\'lumotlaringizni qayta tekshiring.');
        setIsLoading(false);
      }
    }, 600);
  };

  const saveSession = (username: string, fullName: string, role: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('parkly_user', JSON.stringify({ username, fullName, role }));
      document.cookie = `parkly_token=valid_token_${username}; path=/; max-age=86400`;
      document.cookie = `user_role=${role}; path=/; max-age=86400`;
      document.cookie = `user_name=${encodeURIComponent(fullName)}; path=/; max-age=86400`;
    }
    router.push('/');
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
        </div>

        <div className="relative z-10 flex items-center gap-6 text-xs text-slate-500 border-t border-slate-800/80 pt-6">
          <span>© 2026 Parkly.uz</span>
          <span>•</span>
          <span>Xavfsiz shifrlangan RBAC ulanish</span>
        </div>
      </div>

      {/* O'ng qism: Toza Login Forma (Avto-to'ldirishsiz) */}
      <div className="flex items-center justify-center p-6 lg:p-12 bg-slate-900">
        <div className="w-full max-w-md space-y-6 bg-slate-900/80 p-8 rounded-3xl border border-slate-800 shadow-2xl backdrop-blur-xl">
          <div className="text-center space-y-2">
            <div className="lg:hidden inline-flex w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-500 to-cyan-400 items-center justify-center font-bold text-slate-950 shadow-lg text-xl mb-2">
              P
            </div>
            <h3 className="text-2xl font-bold text-white tracking-tight">Tizimga kirish</h3>
            <p className="text-xs text-slate-400">Admin yoki operator hisob ma&apos;lumotlarini kiriting</p>
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
                  placeholder="mirhamid_be yoki admin"
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
              className="w-full py-3.5 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 font-bold rounded-2xl transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 mt-2"
            >
              {isLoading ? (
                <span className="w-5 h-5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></span>
              ) : (
                <>
                  <span>Kirish</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
