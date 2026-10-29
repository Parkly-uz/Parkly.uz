'use client';

import React, { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { StaffUser } from '@/types/database';
import { TEAM_ACCOUNTS } from '@/lib/auth';
import { Shield, Plus, Sliders, Edit3, Trash2, CheckCircle2, UserCheck, UserX, X } from 'lucide-react';
import PermissionsModal from '@/components/staff/PermissionsModal';
import AddEditStaffModal from '@/components/staff/AddEditStaffModal';
import { usePermission } from '@/hooks/usePermission';

export default function StaffManagementPage() {
  const { isSuperAdmin } = usePermission();
  const [successMsg, setSuccessMsg] = useState('');

  // Initial staff list based on team members and mock database
  const [staffList, setStaffList] = useState<StaffUser[]>([
    {
      id: 1,
      username: 'dilshod_pm',
      full_name: 'Samaxov Dilshod',
      role: 'SUPER_ADMIN',
      is_active: true,
      permissions: {
        can_view_3d_map: true,
        can_manage_slots: true,
        can_view_cameras: true,
        can_override_ocr: true,
        can_view_blacklist: true,
        can_edit_blacklist: true,
        can_emergency_open: true,
        can_view_finance: true,
        can_export_reports: true,
        can_edit_tariffs: true,
      },
    },
    {
      id: 2,
      username: 'mirhamid_be',
      full_name: 'Erjigitov Mirhamid',
      role: 'SUPER_ADMIN',
      is_active: true,
      permissions: {
        can_view_3d_map: true,
        can_manage_slots: true,
        can_view_cameras: true,
        can_override_ocr: true,
        can_view_blacklist: true,
        can_edit_blacklist: true,
        can_emergency_open: true,
        can_view_finance: true,
        can_export_reports: true,
        can_edit_tariffs: true,
      },
    },
    {
      id: 3,
      username: 'hikmatilla_fe',
      full_name: 'Tohirjonov Hikmatilla',
      role: 'ADMIN',
      is_active: true,
      permissions: {
        can_view_3d_map: true,
        can_manage_slots: false,
        can_view_cameras: true,
        can_override_ocr: true,
        can_view_blacklist: true,
        can_edit_blacklist: false,
        can_emergency_open: false,
        can_view_finance: true,
        can_export_reports: false,
        can_edit_tariffs: false,
      },
    },
    {
      id: 4,
      username: 'jaloliddin_iot',
      full_name: 'Mamasarulov Jaloliddin',
      role: 'ADMIN',
      is_active: true,
      permissions: {
        can_view_3d_map: true,
        can_manage_slots: true,
        can_view_cameras: true,
        can_override_ocr: false,
        can_view_blacklist: true,
        can_edit_blacklist: false,
        can_emergency_open: true,
        can_view_finance: false,
        can_export_reports: false,
        can_edit_tariffs: false,
      },
    },
    {
      id: 5,
      username: 'abbosxon_qa',
      full_name: 'Saidov Abbosxon',
      role: 'ADMIN',
      is_active: false,
      permissions: {
        can_view_3d_map: false,
        can_manage_slots: false,
        can_view_cameras: false,
        can_override_ocr: false,
        can_view_blacklist: false,
        can_edit_blacklist: false,
        can_emergency_open: false,
        can_view_finance: false,
        can_export_reports: false,
        can_edit_tariffs: false,
      },
    },
  ]);

  const [selectedStaffForPerms, setSelectedStaffForPerms] = useState<StaffUser | null>(null);
  const [selectedStaffForEdit, setSelectedStaffForEdit] = useState<StaffUser | null>(null);
  const [showAddEditModal, setShowAddEditModal] = useState(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState<number | string | null>(null);

  const countActivePermissions = (perms: StaffUser['permissions']) => {
    return Object.values(perms).filter(Boolean).length;
  };

  const handleSaveStaff = (staffData: Partial<StaffUser>) => {
    if (selectedStaffForEdit) {
      // Edit existing
      setStaffList((prev) =>
        prev.map((s) => (s.id === selectedStaffForEdit.id ? { ...s, ...staffData } as StaffUser : s))
      );
      setSuccessMsg(`Xodim ma'lumotlari yangilandi: ${staffData.full_name}`);
    } else {
      // Add new
      const newStaff: StaffUser = {
        id: Date.now(),
        username: staffData.username || 'new_admin',
        full_name: staffData.full_name || 'Yangi Admin',
        role: staffData.role || 'ADMIN',
        is_active: staffData.is_active ?? true,
        permissions: {
          can_view_3d_map: true,
          can_manage_slots: false,
          can_view_cameras: true,
          can_override_ocr: false,
          can_view_blacklist: true,
          can_edit_blacklist: false,
          can_emergency_open: false,
          can_view_finance: false,
          can_export_reports: false,
          can_edit_tariffs: false,
        },
      };
      setStaffList([...staffList, newStaff]);
      setSuccessMsg(`Yangi admin qo'shildi: ${newStaff.full_name}`);
    }
    setSelectedStaffForEdit(null);
    setTimeout(() => setSuccessMsg(''), 4000);
  };

  const handleDeleteStaff = (id: number | string) => {
    setStaffList((prev) => prev.filter((s) => s.id !== id));
    setDeleteConfirmId(null);
    setSuccessMsg('Xodim muvaffaqiyatli o\'chirildi.');
    setTimeout(() => setSuccessMsg(''), 4000);
  };

  const handleUpdatePermissions = (updatedStaff: StaffUser) => {
    setStaffList((prev) => prev.map((s) => (s.id === updatedStaff.id ? updatedStaff : s)));
    setSuccessMsg(`${updatedStaff.full_name} huquqlari saqlandi!`);
    setTimeout(() => setSuccessMsg(''), 4000);
  };

  return (
    <AppShell>
      <div className="space-y-8 max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 text-xs font-bold uppercase tracking-wider">
                Super Admin Security & RBAC
              </span>
              <h2 className="text-2xl font-bold text-white tracking-tight">Xodimlar va Dinamik Huquqlar Matritsasi</h2>
            </div>
            <p className="text-sm text-slate-400 mt-1">Admin va operatorlarni boshqarish, nozik huquqlarni (Granular Permissions) sozlash</p>
          </div>

          <button
            onClick={() => {
              setSelectedStaffForEdit(null);
              setShowAddEditModal(true);
            }}
            className="flex items-center gap-2 px-5 py-3 rounded-2xl bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 font-extrabold text-xs transition-all shadow-lg shadow-emerald-500/20 cursor-pointer"
          >
            <Plus className="w-4 h-4" /> Yangi Admin Qo&apos;shish
          </button>
        </div>

        {successMsg && (
          <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-2 shadow-lg">
            <CheckCircle2 className="w-5 h-5" /> {successMsg}
          </div>
        )}

        {/* Staff Table */}
        <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-950/40">
                  <th className="py-4 px-6">ID</th>
                  <th className="py-4 px-6">F.I.SH. & Login</th>
                  <th className="py-4 px-6">Roli (RBAC)</th>
                  <th className="py-4 px-6">Holati</th>
                  <th className="py-4 px-6">Faol Ruxsatlar</th>
                  <th className="py-4 px-6 text-right">Amallar</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-sm">
                {staffList.map((staff) => {
                  const activeCount = countActivePermissions(staff.permissions);
                  return (
                    <tr key={staff.id} className="hover:bg-slate-800/40 transition-colors">
                      <td className="py-4 px-6 font-mono text-xs text-slate-400">#{staff.id}</td>
                      <td className="py-4 px-6">
                        <div className="font-bold text-white">{staff.full_name}</div>
                        <div className="text-xs text-slate-400 font-mono">@{staff.username}</div>
                      </td>
                      <td className="py-4 px-6">
                        <span
                          className={`px-3 py-1 rounded-xl text-xs font-bold ${
                            staff.role === 'SUPER_ADMIN'
                              ? 'bg-purple-500/15 text-purple-400 border border-purple-500/30'
                              : 'bg-blue-500/15 text-blue-400 border border-blue-500/30'
                          }`}
                        >
                          {staff.role}
                        </span>
                      </td>
                      <td className="py-4 px-6">
                        <span
                          className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold ${
                            staff.is_active
                              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                              : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                          }`}
                        >
                          <span
                            className={`w-2 h-2 rounded-full ${
                              staff.is_active ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'
                            }`}
                          ></span>
                          {staff.is_active ? 'Faol' : 'Bloklangan'}
                        </span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="font-mono font-bold text-amber-300 bg-amber-500/10 px-2.5 py-1 rounded-lg border border-amber-500/20 text-xs">
                          {activeCount} / 10 ta
                        </span>
                      </td>
                      <td className="py-4 px-6 text-right space-x-2">
                        <button
                          title="Huquqlarni sozlash"
                          onClick={() => setSelectedStaffForPerms(staff)}
                          className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 transition-all cursor-pointer inline-flex items-center gap-1 text-xs font-bold px-3"
                        >
                          <Sliders className="w-3.5 h-3.5" /> Huquqlar
                        </button>
                        <button
                          title="Tahrirlash"
                          onClick={() => {
                            setSelectedStaffForEdit(staff);
                            setShowAddEditModal(true);
                          }}
                          className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-blue-400 transition-all cursor-pointer inline-flex items-center"
                        >
                          <Edit3 className="w-4 h-4" />
                        </button>
                        <button
                          title="O'chirish"
                          onClick={() => setDeleteConfirmId(staff.id)}
                          className="p-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 transition-all cursor-pointer inline-flex items-center"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modals */}
        {selectedStaffForPerms && (
          <PermissionsModal
            staff={selectedStaffForPerms}
            isOpen={Boolean(selectedStaffForPerms)}
            onClose={() => setSelectedStaffForPerms(null)}
            onSave={handleUpdatePermissions}
          />
        )}

        <AddEditStaffModal
          isOpen={showAddEditModal}
          staffToEdit={selectedStaffForEdit}
          onClose={() => {
            setShowAddEditModal(false);
            setSelectedStaffForEdit(null);
          }}
          onSave={handleSaveStaff}
        />

        {/* Delete Confirmation Modal */}
        {deleteConfirmId && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
            <div className="bg-slate-900 rounded-3xl border border-slate-800 p-6 w-full max-w-sm space-y-4 text-center">
              <h3 className="text-lg font-bold text-white">Xodimni o&apos;chirishni tasdiqlaysizmi?</h3>
              <p className="text-xs text-slate-400">Bu amal qaytarilmaydi va xodim tizimga kira olmaydi.</p>
              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => setDeleteConfirmId(null)}
                  className="flex-1 py-2.5 bg-slate-800 text-slate-300 rounded-xl text-xs font-bold cursor-pointer"
                >
                  Bekor qilish
                </button>
                <button
                  onClick={() => handleDeleteStaff(deleteConfirmId)}
                  className="flex-1 py-2.5 bg-rose-600 text-white rounded-xl text-xs font-bold cursor-pointer"
                >
                  O&apos;chirish
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
