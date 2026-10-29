'use client';

import { useState, useEffect } from 'react';
import { UserPermissions } from '@/types/database';

const DEFAULT_PERMISSIONS: UserPermissions = {
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
};

const SUPER_ADMIN_PERMISSIONS: UserPermissions = {
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
};

export function usePermission() {
  const [role, setRole] = useState<'SUPER_ADMIN' | 'ADMIN'>('SUPER_ADMIN');
  const [permissions, setPermissions] = useState<UserPermissions>(SUPER_ADMIN_PERMISSIONS);

  useEffect(() => {
    // Read role from cookie or localStorage
    const match = document.cookie.match(new RegExp('(^| )user_role=([^;]+)'));
    const userRole = match ? match[2] : 'SUPER_ADMIN';

    if (userRole === 'ADMIN') {
      setRole('ADMIN');
      setPermissions(DEFAULT_PERMISSIONS);
    } else {
      setRole('SUPER_ADMIN');
      setPermissions(SUPER_ADMIN_PERMISSIONS);
    }
  }, []);

  const isSuperAdmin = role === 'SUPER_ADMIN';

  const hasPermission = (permissionKey: keyof UserPermissions): boolean => {
    if (isSuperAdmin) return true;
    return permissions[permissionKey] ?? false;
  };

  return {
    role,
    permissions,
    isSuperAdmin,
    hasPermission,
  };
}
