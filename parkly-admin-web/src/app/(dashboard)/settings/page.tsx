'use client';

import React, { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { Settings, Server, Shield, Users, Plus, CheckCircle2, Wifi, Power, Lock, Unlock, X, Sliders } from 'lucide-react';

interface StaffMember {
  id: string;
  name: string;
  email: string;
  role: 'Super Admin' | 'Admin' | 'Operator';
  shift: 'Kunduzgi' | 'Tungi';
  status: 'active' | 'offline';
}

interface PermissionItem {
  id: string;
  title: string;
  enabled: boolean;
  statusText: string;
  badgeType: 'on' | 'off' | 'forbidden';
}

export default function SettingsPage() {
  const [successMsg, setSuccessMsg] = useState('');
  const [isEmergencyAllOpen, setIsEmergencyAllOpen] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);

  // Granular Permission Modal State
  const [showPermissionsModal, setShowPermissionsModal] = useState(false);
  const [selectedStaff, setSelectedStaff] = useState<StaffMember | null>(null);
  const [permissions, setPermissions] = useState<PermissionItem[]>([
    { id: 'p1', title: "3D Xarita & Slotlarni ko'rish", enabled: true, statusText: '', badgeType: 'on' },
    { id: 'p2', title: "Slotlarni qo'lda bo'shatish/band qilish", enabled: false, statusText: "(O'chirilgan)", badgeType: 'off' },
    { id: 'p3', title: "Jonli Kameralar streamini ko'rish", enabled: true, statusText: '', badgeType: 'on' },
    { id: 'p4', title: "Kamera OCR xatosini qo'lda to'g'rilash", enabled: true, statusText: '', badgeType: 'on' },
    { id: 'p5', title: "Qora ro'yxat (Blacklist)ni ko'rish", enabled: true, statusText: '', badgeType: 'on' },
    { id: 'p6', title: "Qora ro'yxatga yangi mashina QO'SHISH", enabled: false, statusText: "(O'chirilgan)", badgeType: 'off' },
    { id: 'p7', title: "Shlagbaumni FAVQULODDA ochish", enabled: false, statusText: "(Taqiqlangan)", badgeType: 'forbidden' },
    { id: 'p8', title: "Moliya & Kassa hisobotlarini ko'rish", enabled: true, statusText: '', badgeType: 'on' },
    { id: 'p9', title: "Excel / CSV eksport qilish", enabled: false, statusText: "(O'chirilgan)", badgeType: 'off' },
    { id: 'p10', title: "Tarif stavkalarini o'zgartirish", enabled: false, statusText: "(Taqiqlangan)", badgeType: 'forbidden' },
  ]);

  // New Staff Form State
  const [newName, setNewName] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newRole, setNewRole] = useState<'Super Admin' | 'Admin' | 'Operator'>('Operator');
  const [newShift, setNewShift] = useState<'Kunduzgi' | 'Tungi'>('Kunduzgi');

  const [staffList, setStaffList] = useState<StaffMember[]>([
    { id: 'STF-01', name: 'Alisher Doniyorov', email: 'admin@parkly.uz', role: 'Super Admin', shift: 'Kunduzgi', status: 'active' },
    { id: 'STF-02', name: 'Jasur Karimov', email: 'operator@parkly.uz', role: 'Operator', shift: 'Kunduzgi', status: 'active' },
    { id: 'STF-03', name: 'Tohirjonov Hikmatilla', email: 'hikmatilla@parkly.uz', role: 'Admin', shift: 'Tungi', status: 'active' },
    { id: 'STF-04', name: 'Sardor Rahimov', email: 'sardor@parkly.uz', role: 'Admin', shift: 'Kunduzgi', status: 'offline' },
  ]);

  const handleEmergencyAll = () => {
    setIsEmergencyAllOpen(true);
    setSuccessMsg('DIQQAT! Barcha to\'siqlar va shlagbaumlar favqulodda rejimda ochildi!');
    setTimeout(() => setSuccessMsg(''), 5000);
  };

  const handleAddStaff = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName || !newEmail) return;

    const newMember: StaffMember = {
      id: `STF-0${staffList.length + 1}`,
      name: newName,
      email: newEmail,
      role: newRole,
      shift: newShift,
      status: 'active',
    };

    setStaffList([...staffList, newMember]);
    setNewName('');
    setNewEmail('');
    setShowAddModal(false);
    setSuccessMsg('Yangi xodim muvaffaqiyatli qo\'shildi!');
    setTimeout(() => setSuccessMsg(''), 4000);
  };

  const handleOpenPermissions = (staff: StaffMember) => {
    setSelectedStaff(staff);
    // Adjust permissions mockup based on staff role
    if (staff.role === 'Super Admin') {
      setPermissions(permissions.map(p => ({ ...p, enabled: true, statusText: '', badgeType: 'on' })));
    } else {
      // Default granular perms for Admin / Operator
      setPermissions([
        { id: 'p1', title: "3D Xarita & Slotlarni ko'rish", enabled: true, statusText: '', badgeType: 'on' },
        { id: 'p2', title: "Slotlarni qo'lda bo'shatish/band qilish", enabled: false, statusText: "(O'chirilgan)", badgeType: 'off' },
        { id: 'p3', title: "Jonli Kameralar streamini ko'rish", enabled: true, statusText: '', badgeType: 'on' },
        { id: 'p4', title: "Kamera OCR xatosini qo'lda to'g'rilash", enabled: true, statusText: '', badgeType: 'on' },
        { id: 'p5', title: "Qora ro'yxat (Blacklist)ni ko'rish", enabled: true, statusText: '', badgeType: 'on' },
        { id: 'p6', title: "Qora ro'yxatga yangi mashina QO'SHISH", enabled: false, statusText: "(O'chirilgan)", badgeType: 'off' },
        { id: 'p7', title: "Shlagbaumni FAVQULODDA ochish", enabled: false, statusText: "(Taqiqlangan)", badgeType: 'forbidden' },
        { id: 'p8', title: "Moliya & Kassa hisobotlarini ko'rish", enabled: true, statusText: '', badgeType: 'on' },
        { id: 'p9', title: "Excel / CSV eksport qilish", enabled: false, statusText: "(O'chirilgan)", badgeType: 'off' },
        { id: 'p10', title: "Tarif stavkalarini o'zgartirish", enabled: false, statusText: "(Taqiqlangan)", badgeType: 'forbidden' },
      ]);
    }
    setShowPermissionsModal(true);
  };

  const togglePermission = (id: string) => {
    setPermissions(prev =>
      prev.map(p => {
        if (p.id === id) {
          const nextEnabled = !p.enabled;
          return {
            ...p,
            enabled: nextEnabled,
            statusText: nextEnabled ? '' : p.badgeType === 'forbidden' ? '(Taqiqlangan)' : "(O'chirilgan)",
            badgeType: nextEnabled ? 'on' : p.badgeType
          };
        }
        return p;
      })
    );
  };

  const handleSavePermissions = () => {
    setShowPermissionsModal(false);
    setSuccessMsg(`${selectedStaff?.name} uchun maxsus ruxsatlar muvaffaqiyatli saqlandi!`);
    setTimeout(() => setSuccessMsg(''), 4000);
  };

  return (
    <AppShell>
      <div className="space-y-8 max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold uppercase tracking-wider">
                Hardware & RBAC
              </span>
              <h2 className="text-2xl font-bold text-white tracking-tight">Uskunalar va Xodimlar Sozlamalari</h2>
            </div>
            <p className="text-sm text-slate-400 mt-1">ESP32 mikrocontrollerlar, MQTT broker va RBAC rollar boshqaruvi</p>
          </div>

          <button
            onClick={handleEmergencyAll}
            className="flex items-center gap-2 px-5 py-3 rounded-2xl bg-rose-600 hover:bg-rose-500 text-white font-extrabold text-xs transition-all shadow-lg shadow-rose-600/30 cursor-pointer animate-pulse"
          >
            <Shield className="w-4 h-4" /> Barcha To&apos;siqlarni Ochish (Emergency Open All)
          </button>
        </div>

        {successMsg && (
          <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-2 shadow-lg">
            <CheckCircle2 className="w-5 h-5" /> {successMsg}
          </div>
        )}

        {/* Hardware Status Cards */}
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-white">Hardware & IoT Holati</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* ESP32 Kirish */}
            <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">ESP32 #GATE-01</span>
                <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 text-xs font-semibold flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Online
                </span>
              </div>
              <div>
                <h4 className="text-base font-bold text-white">Kirish Shlagbaumi</h4>
                <p className="text-xs text-slate-400 font-mono mt-1">IP: 192.168.1.50 • Ping: 12ms</p>
              </div>
              <div className="flex items-center justify-between text-xs pt-3 border-t border-slate-800 text-slate-400">
                <span>Signal kuchi: -64 dBm</span>
                <span className="text-emerald-400 font-semibold">Barqaror</span>
              </div>
            </div>

            {/* ESP32 Chiqish */}
            <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">ESP32 #GATE-02</span>
                <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 text-xs font-semibold flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Online
                </span>
              </div>
              <div>
                <h4 className="text-base font-bold text-white">Chiqish Shlagbaumi</h4>
                <p className="text-xs text-slate-400 font-mono mt-1">IP: 192.168.1.51 • Ping: 14ms</p>
              </div>
              <div className="flex items-center justify-between text-xs pt-3 border-t border-slate-800 text-slate-400">
                <span>Signal kuchi: -68 dBm</span>
                <span className="text-emerald-400 font-semibold">Barqaror</span>
              </div>
            </div>

            {/* EMQX MQTT Broker */}
            <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Broker / MQTT</span>
                <span className="px-2.5 py-1 rounded-lg bg-cyan-500/10 text-cyan-400 text-xs font-semibold flex items-center gap-1.5">
                  <Wifi className="w-3.5 h-3.5" /> Connected
                </span>
              </div>
              <div>
                <h4 className="text-base font-bold text-white">EMQX Broker</h4>
                <p className="text-xs text-slate-400 font-mono mt-1">mqtt://broker.parkly.uz:1883</p>
              </div>
              <div className="flex items-center justify-between text-xs pt-3 border-t border-slate-800 text-slate-400">
                <span>Klientlar: 14 ta</span>
                <span className="text-cyan-400 font-semibold">SSL Secure</span>
              </div>
            </div>
          </div>
        </div>

        {/* Staff & RBAC Table */}
        <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-white text-base">Xodimlar va Rollar (RBAC)</h3>
              <p className="text-xs text-slate-400">Tizim foydalanuvchilari va ularning huquqlari</p>
            </div>
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl text-xs transition-all shadow-md shadow-emerald-500/20 cursor-pointer"
            >
              <Plus className="w-4 h-4" /> Yangi Xodim Qo&apos;shish
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-950/40">
                  <th className="py-4 px-6">ID</th>
                  <th className="py-4 px-6">Ism & Familiya</th>
                  <th className="py-4 px-6">Email</th>
                  <th className="py-4 px-6">Roli (RBAC)</th>
                  <th className="py-4 px-6">Smena</th>
                  <th className="py-4 px-6">Holati</th>
                  <th className="py-4 px-6 text-right">Huquqlar</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-sm">
                {staffList.map((staff) => (
                  <tr key={staff.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-mono text-xs text-slate-400">{staff.id}</td>
                    <td className="py-4 px-6 font-bold text-white">{staff.name}</td>
                    <td className="py-4 px-6 text-slate-300 text-xs">{staff.email}</td>
                    <td className="py-4 px-6">
                      <span className={`px-2.5 py-1 rounded-lg text-xs font-bold ${
                        staff.role === 'Super Admin' ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20' : staff.role === 'Admin' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                      }`}>
                        {staff.role}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-slate-300 text-xs">{staff.shift}</td>
                    <td className="py-4 px-6">
                      <span className={`px-2.5 py-1 rounded-lg text-xs font-semibold ${
                        staff.status === 'active' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-400'
                      }`}>
                        {staff.status === 'active' ? 'Faol' : 'Offline'}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={() => handleOpenPermissions(staff)}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 text-xs font-bold transition-all cursor-pointer border border-slate-700"
                      >
                        <Sliders className="w-3.5 h-3.5" /> Huquqlarni sozlash
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Add Staff Modal */}
        {showAddModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
            <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl w-full max-w-md p-6 space-y-6">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <h3 className="text-lg font-bold text-white">Yangi Xodim Qo&apos;shish</h3>
                <button onClick={() => setShowAddModal(false)} className="text-slate-400 hover:text-white">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleAddStaff} className="space-y-4">
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Ism & Familiya</label>
                  <input
                    type="text"
                    required
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    placeholder="Masalan: Anvar Bekov"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Email Manzil</label>
                  <input
                    type="email"
                    required
                    value={newEmail}
                    onChange={(e) => setNewEmail(e.target.value)}
                    placeholder="anvar@parkly.uz"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Rol (RBAC)</label>
                  <select
                    value={newRole}
                    onChange={(e) => setNewRole(e.target.value as any)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  >
                    <option value="Operator">Operator</option>
                    <option value="Admin">Admin</option>
                    <option value="Super Admin">Super Admin</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Smena</label>
                  <select
                    value={newShift}
                    onChange={(e) => setNewShift(e.target.value as any)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  >
                    <option value="Kunduzgi">Kunduzgi</option>
                    <option value="Tungi">Tungi</option>
                  </select>
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-2xl text-xs transition-all cursor-pointer"
                  >
                    Bekor qilish
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-2xl text-xs transition-all shadow-lg shadow-emerald-500/20 cursor-pointer"
                  >
                    Saqlash
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Granular Permissions Modal */}
        {showPermissionsModal && selectedStaff && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
            <div className="bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl w-full max-w-2xl p-6 space-y-6">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div className="flex items-center gap-2">
                  <span className="text-emerald-400 font-bold">⚙️</span>
                  <h3 className="text-lg font-bold text-white">{selectedStaff.name} uchun ruxsatlarni sozlash</h3>
                </div>
                <button onClick={() => setShowPermissionsModal(false)} className="text-slate-400 hover:text-white">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-3 max-h-[60vh] overflow-y-auto pr-2">
                {permissions.map((item) => (
                  <div
                    key={item.id}
                    className="flex items-center justify-between p-3.5 rounded-2xl bg-slate-950 border border-slate-800 hover:border-slate-700 transition-all"
                  >
                    <span className="text-sm font-medium text-slate-200">{item.title}</span>
                    <div className="flex items-center gap-3">
                      {item.statusText && (
                        <span className={`text-xs ${item.badgeType === 'forbidden' ? 'text-rose-400' : 'text-slate-500'}`}>
                          {item.statusText}
                        </span>
                      )}
                      <button
                        onClick={() => togglePermission(item.id)}
                        className={`px-4 py-1.5 rounded-xl font-bold text-xs transition-all cursor-pointer ${
                          item.enabled
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow-md'
                            : 'bg-slate-800 text-slate-400 border border-slate-700'
                        }`}
                      >
                        {item.enabled ? 'ON 🟢' : 'OFF ⚪'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowPermissionsModal(false)}
                  className="px-5 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-2xl text-xs transition-all cursor-pointer"
                >
                  Bekor qilish
                </button>
                <button
                  type="button"
                  onClick={handleSavePermissions}
                  className="px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-2xl text-xs transition-all shadow-lg shadow-emerald-500/20 cursor-pointer"
                >
                  SAQLASH 💾
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
