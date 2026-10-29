'use client';

import React, { useState, useEffect } from 'react';
import { StaffUser } from '@/types/database';
import { X, User, Lock, Shield } from 'lucide-react';

interface AddEditStaffModalProps {
  isOpen: boolean;
  staffToEdit?: StaffUser | null;
  onClose: () => void;
  onSave: (staff: Partial<StaffUser>, password?: string) => void;
}

export default function AddEditStaffModal({ isOpen, staffToEdit, onClose, onSave }: AddEditStaffModalProps) {
  const [fullName, setFullName] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'SUPER_ADMIN' | 'ADMIN'>('ADMIN');
  const [isActive, setIsActive] = useState(true);

  useEffect(() => {
    if (staffToEdit) {
      setFullName(staffToEdit.full_name);
      setUsername(staffToEdit.username);
      setRole(staffToEdit.role);
      setIsActive(staffToEdit.is_active);
      setPassword('');
    } else {
      setFullName('');
      setUsername('');
      setPassword('');
      setRole('ADMIN');
      setIsActive(true);
    }
  }, [staffToEdit, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!fullName || !username) return;

    onSave(
      {
        full_name: fullName,
        username,
        role,
        is_active: isActive,
      },
      password
    );
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl w-full max-w-md p-6 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
              <User className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white">
              {staffToEdit ? 'Adminni Tahrirlash' : 'Yangi Admin Qo\'shish'}
            </h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 uppercase">F.I.SH. (To&apos;liq Ismi)</label>
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Masalan: Samaxov Dilshod"
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white focus:outline-none focus:border-emerald-500"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 uppercase">Login (Username)</label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="dilshod_pm"
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white font-mono focus:outline-none focus:border-emerald-500"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 uppercase">
              {staffToEdit ? 'Yangi Parol (bo\'sh qoldirish mumkin)' : 'Parol'}
            </label>
            <input
              type="password"
              required={!staffToEdit}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white font-mono focus:outline-none focus:border-emerald-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300 uppercase">Rol (RBAC)</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value as any)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="ADMIN">ADMIN</option>
                <option value="SUPER_ADMIN">SUPER_ADMIN</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300 uppercase">Holati</label>
              <select
                value={isActive ? 'active' : 'blocked'}
                onChange={(e) => setIsActive(e.target.value === 'active')}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="active">🟢 Faol</option>
                <option value="blocked">🔴 Bloklangan</option>
              </select>
            </div>
          </div>

          <div className="flex gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-2xl text-xs transition-all cursor-pointer"
            >
              Bekor qilish
            </button>
            <button
              type="submit"
              className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold rounded-2xl text-xs transition-all shadow-lg shadow-emerald-500/20 cursor-pointer"
            >
              {staffToEdit ? 'Saqlash' : 'Qo\'shish'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
