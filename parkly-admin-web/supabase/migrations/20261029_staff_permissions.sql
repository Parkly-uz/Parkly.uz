-- Migration script: Add granular permissions JSONB column to staff_users table
-- Parkly.uz Enterprise Smart Parking Platform

ALTER TABLE staff_users ADD COLUMN IF NOT EXISTS permissions JSONB DEFAULT '{
  "can_view_3d_map": true,
  "can_manage_slots": false,
  "can_view_cameras": true,
  "can_override_ocr": false,
  "can_view_blacklist": true,
  "can_edit_blacklist": false,
  "can_emergency_open": false,
  "can_view_finance": false,
  "can_export_reports": false,
  "can_edit_tariffs": false
}'::jsonb;

-- Example query to update a specific staff member's permissions:
-- UPDATE staff_users
-- SET permissions = permissions || '{"can_manage_slots": true, "can_emergency_open": true}'::jsonb
-- WHERE username = 'hikmatilla_fe';
