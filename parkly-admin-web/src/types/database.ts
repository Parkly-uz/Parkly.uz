export type SlotStatus = 'available' | 'occupied' | 'reserved' | 'maintenance';
export type SlotFloor = 1 | 2 | 3 | 4;
export type SessionStatus = 'active' | 'completed' | 'cancelled';
export type UserRole = 'SUPER_ADMIN' | 'ADMIN' | 'operator' | 'supervisor';
export type TransactionType = 'cash' | 'click' | 'payme' | 'uzum';

export interface ParkingSlot {
  id: string;
  slot_number: string;
  floor: SlotFloor;
  status: SlotStatus;
  current_plate?: string;
  vehicle_type?: 'sedan' | 'suv' | 'truck' | 'ev';
  updated_at: string;
}

export interface ParkingSession {
  id: string;
  slot_id: string;
  slot_number: string;
  plate_number: string;
  entry_time: string;
  exit_time?: string;
  fee_amount?: number;
  status: SessionStatus;
  created_at: string;
}

export interface UserPermissions {
  can_view_3d_map: boolean;
  can_manage_slots: boolean;
  can_view_cameras: boolean;
  can_override_ocr: boolean;
  can_view_blacklist: boolean;
  can_edit_blacklist: boolean;
  can_emergency_open: boolean;
  can_view_finance: boolean;
  can_export_reports: boolean;
  can_edit_tariffs: boolean;
}

export interface StaffUser {
  id: number | string;
  username: string;
  full_name: string;
  email?: string;
  role: 'SUPER_ADMIN' | 'ADMIN';
  is_active: boolean;
  permissions: UserPermissions;
  created_at?: string;
}

export interface Transaction {
  id: string;
  session_id: string;
  amount: number;
  payment_method: TransactionType;
  status: 'success' | 'pending' | 'failed';
  created_at: string;
}
