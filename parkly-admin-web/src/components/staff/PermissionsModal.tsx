'use client';

import React from 'react';
import { StaffUser, UserPermissions } from '@/types/database';
import { X, Check } from 'lucide-react';
import { supabase } from '@/lib/supabase/client';

interface PermissionsModalProps {
  staff: StaffUser;
  isOpen: boolean;
  onClose: () => void;
  onSave: (updatedStaff: StaffUser) => void;
}

const PERMISSION_LABELS: Record<keyof UserPermissions, string> = {
  can_view_3d_map: "3D Xarita & Slotlarni ko'rish",
  can_manage_slots: "Slotlarni qo'lda bo'shatish/band qilish",
  can_view_cameras: "Jonli kameralarni ko'rish",
  can_override_ocr: "Kamera OCR xatosini qo'lda to'g'rilash",
  can_view_blacklist: "Qora ro'yxat (Blacklist)ni ko'rish",
  can_edit_blacklist: "Qora ro'yxatga mashina qo'shish/o'chirish",
  can_emergency_open: "Shlagbaumni favqulodda ochish (Emergency Open)",
  can_view_finance: "Moliya va daromadlarni ko'rish",
  can_export_reports: "Excel/CSV eksport qilish",
  can_edit_tariffs: "Tarif stavkalarini o'zgartirish",
};

export default function PermissionsModal({ staff, isOpen, onClose, onSave }: PermissionsModalProps) {
  const [permissions, setPermissions] = React.useState<UserPermissions>(staff.permissions);
  const [isSaving, setIsSaving] = React.useState(false);

  React.useEffect(() => {
    setPermissions(staff.permissions);
  }, [staff]);

  if (!isOpen) return null;

  const handleToggle = (key: keyof UserPermissions) => {
    setPermissions((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Supabase update simulation
      const { error } = await supabase
        .from('staff_users')
        .update({ permissions })
        .eq('id', staff.id);

      if (error) {
        console.warn('Supabase update note:', error.message);
      }

      onSave({
        ...staff,
        permissions,
      });
      onClose();
    } catch (err) {
      console.error(err);
      onSave({ ...staff, permissions });
      onClose();
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl w-full max-w-xl p-6 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <span className="text-emerald-400 text-lg">⚙️</span>
            <div>
              <h3 className="text-base font-bold text-white">{staff.full_name} uchun ruxsatlarni sozlash</h3>
              <p className="text-xs text-slate-400 font-mono">@{staff.username} • {staff.role}</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-3 max-h-[55vh] overflow-y-auto pr-1">
          {(Object.keys(PERMISSION_LABELS) as Array<keyof UserPermissions>).map((key) => {
            const isEnabled = permissions[key];
            return (
              <div
                key={key}
                onClick={() => handleToggle(key)}
                className="flex items-center justify-between p-3.5 rounded-2xl bg-slate-950 border border-slate-800/80 hover:border-slate-700 transition-all cursor-pointer select-none"
              >
                <span className="text-xs font-semibold text-slate-200">{PERMISSION_LABELS[key]}</span>
                <div className="flex items-center gap-3">
                  <span className={`text-[10px] font-mono ${isEnabled ? 'text-emerald-400' : 'text-slate-500'}`}>
                    {isEnabled ? '(Ruxsat etilgan)' : "(Cheklangan)"}
                  </span>
                  <div
                    className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors duration-200 ease-in-out ${
                      isEnabled ? 'bg-emerald-500' : 'bg-slate-800'
                    }`}
                  >
                    <div
                      className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-200 ease-in-out ${
                        isEnabled ? 'translate-x-6' : 'translate-x-0'
                      }`}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
          <button
            type="button"
            onClick={onClose}
            className="px-5 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-2xl text-xs transition-all cursor-pointer"
          >
            Bekor qilish
          </button>
          <button
            type="button"
            disabled={isSaving}
            onClick={handleSave}
            className="px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold rounded-2xl text-xs transition-all shadow-lg shadow-emerald-500/20 cursor-pointer disabled:opacity-50"
          >
            {isSaving ? 'Saqlanmoqda...' : 'SAQLASH 💾'}
          </button>
        </div>
      </div>
    </div>
  );
}
