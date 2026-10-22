# 🗄️ Parkly.uz — Core Baza Sxemasi va SQLite/PostgreSQL Ma'lumotlar Modeli

Ushbu hujjat **Parkly.uz** aqlli avtoturargoh tizimining markaziy ma'lumotlar bazasi arxitekturasi, ERD (Entity-Relationship) munosabatlari, jadvallar strukturasi, indekslar va ma'lumotlar turlarini to'liq tavsiflaydi. Tizim **gibrid arxitekturada** ishlaydi: lokal oflayn stansiyada **SQLite (`parkly_local.db`)**, markaziy bulutli/tarmoq serverida esa **PostgreSQL** qo'llab-quvvatlanadi.

---

## 📐 1. ERD (Entity-Relationship Diagramma) Strukturasi

```text
+-------------------+        +--------------------+        +---------------------+
|   parking_lots    | 1    * |   parking_slots    | 1    * |  parking_sessions   |
+-------------------+------->+--------------------+------->+---------------------+
| id (PK)           |        | id (PK)            |        | id (PK)             |
| name              |        | parking_lot_id(FK) |        | session_code (UQ)   |
| total_floors      |        | floor, zone, slot  |        | vehicle_plate       |
| total_slots       |        | slot_type, status  |        | slot_number         |
+-------------------+        | pos_x, pos_y       |        | entry_time          |
                             +--------------------+        | exit_time           |
                                                           | total_amount        |
                                                           | status (ACTIVE/...) |
                                                           +----------+----------+
                                                                      | 1
                                                                      |
                                                                      | *
+-------------------+        +--------------------+        +----------v----------+
|    staff_users    |        |   subscriptions    |        |    transactions     |
+-------------------+        +--------------------+        +---------------------+
| id (PK)           |        | id (PK)            |        | id (PK)             |
| username (UQ)     |        | vehicle_plate (UQ) |        | tx_code (UQ)        |
| password_hash     |        | driver_name, phone |        | session_code (FK)   |
| full_name         |        | plan (1, 3, 6 oy)  |        | provider (Payme...) |
| role (SUPER/ADMIN)|        | start_date         |        | amount              |
| shift, is_active  |        | end_date, is_active|        | status, fiscal_sign |
+-------------------+        +--------------------+        +---------------------+
```

---

## 🗃️ 2. Jadvallar Ro'yxati va Tavsifi

| № | Jadval Nomi | Asosiy Vazifasi | Qo'llaniladigan Modul |
|---|---|---|---|
| 1 | `parking_lots` | Avtoturargoh obyektlari va filiallari | Markaziy Boshqaruv |
| 2 | `parking_slots` | Barcha qavatlardagi to'xtash o'rinlari va 2D/3D koordinatalari | 3D İzometrik Xarita |
| 3 | `parking_sessions`| Kirgan mashinalar, vaqtlar va faol sessiyalar | Sessiyalar & ANPR |
| 4 | `transactions` | Click, Payme, Uzum va kassa to'lovlari | Moliya & Billing |
| 5 | `subscriptions` | 1, 3, 6 oylik uzoq muddatli obunalar (Fastline) | Fastline & Obunalar |
| 6 | `staff_users` | Jamoa a'zolari, login, parol va RBAC huquqlari | Xodimlar & RBAC |
| 7 | `vehicle_access_list` | Whitelist (VIP/Tez yordam) va Blacklist (Firibgarlik) | Xavfsizlik & Anti-Cheat |
| 8 | `barrier_audit` | Shlagbaumni favqulodda (10 min Fail-Safe) ochish jurnali | IoT & Xavfsizlik |
| 9 | `system_settings` | Kunlik/tungi tariflar, grace period va sig'im | Tizim Sozlamalari |
| 10 | `system_notifications` | Real vaqt xabarnomalari (Notification Bell) | Desktop Admin Panel |
| 11 | `coupons` | Chegirma kodlari va vaucherlar | Moliya & Promokodlar |

---

## 💻 3. To'liq SQL DDL Sxemasi (PostgreSQL & SQLite Moslashuvchan)

Quyidagi SQL skripti PostgreSQL va SQLite (INTEGER PRIMARY KEY AUTOINCREMENT) formatlariga to'liq mos keladi:

```sql
-- ============================================================================
-- PARKLY.UZ — CORE DATABASE SCHEMA DDL
-- ============================================================================

-- 1. Xodimlar va RBAC jadvali (Staff Users)
CREATE TABLE IF NOT EXISTS staff_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(30) NOT NULL,            -- 'SUPER_ADMIN', 'ADMIN'
    shift VARCHAR(100) NOT NULL,          -- Lavozim / Vazifa tavsifi
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Avtoturargoh obyektlari (Parking Lots)
CREATE TABLE IF NOT EXISTS parking_lots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    address TEXT NOT NULL,
    total_floors INTEGER DEFAULT 2,
    total_slots INTEGER DEFAULT 56,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Parking Slotlari (To'xtash O'rinlari)
CREATE TABLE IF NOT EXISTS parking_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_lot_id INTEGER DEFAULT 1,
    floor INTEGER NOT NULL DEFAULT 1,             -- 1, 2, 3, -1
    zone VARCHAR(10) NOT NULL,                    -- 'A', 'B', 'EV', 'VIP'
    slot_number VARCHAR(20) UNIQUE NOT NULL,      -- 'A-101', 'EV-01'
    slot_type VARCHAR(30) NOT NULL DEFAULT 'REGULAR', -- 'REGULAR', 'EV_CHARGING', 'VIP_STAFF', 'ACCESSIBLE'
    status VARCHAR(30) NOT NULL DEFAULT 'FREE',   -- 'FREE', 'OCCUPIED', 'RESERVED', 'PAYMENT_PENDING', 'MAINTENANCE'
    pos_x INTEGER NOT NULL DEFAULT 0,             -- 2D X piksel
    pos_y INTEGER NOT NULL DEFAULT 0,             -- 2D Y piksel
    width INTEGER NOT NULL DEFAULT 52,
    height INTEGER NOT NULL DEFAULT 78,
    rotation INTEGER DEFAULT 0,
    current_vehicle_plate VARCHAR(20) DEFAULT NULL,
    current_vehicle_model VARCHAR(100) DEFAULT NULL,
    entry_time TIMESTAMP DEFAULT NULL,
    last_status_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Avtoturargoh Seanslari (Parking Sessions)
CREATE TABLE IF NOT EXISTS parking_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_code VARCHAR(50) UNIQUE NOT NULL,     -- 'SES-1049'
    vehicle_plate VARCHAR(20) NOT NULL,           -- '01A777AA'
    vehicle_model VARCHAR(100),
    slot_number VARCHAR(20) NOT NULL,
    entry_time TIMESTAMP NOT NULL,
    exit_time TIMESTAMP DEFAULT NULL,
    duration_minutes INTEGER DEFAULT 0,
    total_amount INTEGER DEFAULT 0,
    payment_provider VARCHAR(50) DEFAULT NULL,    -- 'Payme', 'Click', 'Uzum', 'Naqd'
    status VARCHAR(30) DEFAULT 'ACTIVE'           -- 'ACTIVE', 'COMPLETED', 'CANCELLED'
);

-- 5. Tranzaksiyalar (To'lovlar)
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tx_code VARCHAR(50) UNIQUE NOT NULL,          -- 'TX-9921'
    session_code VARCHAR(50) NOT NULL,
    vehicle_plate VARCHAR(20) NOT NULL,
    provider VARCHAR(50) NOT NULL,                -- 'Payme', 'Click', 'Uzum', 'Kassa'
    amount INTEGER NOT NULL,
    status VARCHAR(30) DEFAULT 'SUCCESS',         -- 'SUCCESS', 'PENDING', 'FAILED'
    fiscal_sign VARCHAR(100) DEFAULT NULL,        -- 'FISC-88221'
    duration VARCHAR(30) DEFAULT '01:00:00',
    payment_method VARCHAR(50) DEFAULT 'Avtomatik To''lov',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Uzoq Muddatli Obunalar (Subscriptions & Fastline)
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_plate VARCHAR(20) UNIQUE NOT NULL,
    driver_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    plan_type VARCHAR(30) NOT NULL,               -- '1_MONTH', '3_MONTHS', '6_MONTHS'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    fastline_enabled INTEGER DEFAULT 1,          -- 1 = To'xtovsiz shlagbaum
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Ruxsat va Taqiqlash Ro'yxati (Access Control List)
CREATE TABLE IF NOT EXISTS vehicle_access_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate VARCHAR(20) UNIQUE NOT NULL,
    list_type VARCHAR(20) NOT NULL,               -- 'WHITELIST', 'BLACKLIST'
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Shlagbaum Favqulodda Ochilish Jurnali (Barrier Audit)
CREATE TABLE IF NOT EXISTS barrier_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_username VARCHAR(50) NOT NULL,
    operator_name VARCHAR(100) NOT NULL,
    action VARCHAR(50) DEFAULT 'MANUAL_OPEN',     -- 'MANUAL_OPEN', 'FAILSAFE_EMERGENCY'
    reason TEXT NOT NULL,                         -- '10 minutlik kutish limiti' yoki 'Texnik nosozlik'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Tizim va Tarif Sozlamalari (System Settings)
CREATE TABLE IF NOT EXISTS system_settings (
    key VARCHAR(50) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT
);

-- 10. Bildirishnomalar Jurnali (System Notifications)
CREATE TABLE IF NOT EXISTS system_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(20) DEFAULT 'INFO',              -- 'INFO', 'SUCCESS', 'WARNING', 'ALERT'
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Chegirmalar va Promokodlar (Coupons)
CREATE TABLE IF NOT EXISTS coupons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(30) UNIQUE NOT NULL,
    discount_percent INTEGER NOT NULL,
    valid_until DATE,
    is_active INTEGER DEFAULT 1
);

-- ============================================================================
-- INDEKSLAR (Tezkor Qidiruv va Yuqori Unumdorlik Uchun)
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_slots_floor_status ON parking_slots(floor, status);
CREATE INDEX IF NOT EXISTS idx_slots_plate ON parking_slots(current_vehicle_plate);
CREATE INDEX IF NOT EXISTS idx_sessions_plate ON parking_sessions(vehicle_plate);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON parking_sessions(status);
CREATE INDEX IF NOT EXISTS idx_tx_session ON transactions(session_code);
CREATE INDEX IF NOT EXISTS idx_subs_plate ON subscriptions(vehicle_plate, is_active);
```

---

## 👥 4. Boshlang'ich Jamoa Ma'lumotlari (Staff Users Seeder)

Tizim o'rnatilganda avtomatik quyidagi 6 ta rasmiy jamoa a'zosi bazaga kiritiladi:

```sql
INSERT INTO staff_users (username, password, full_name, role, shift)
VALUES 
    ('dilshod_pm', 'parkly2026', 'Samaxov Dilshod', 'SUPER_ADMIN', 'Product Manager (PM)'),
    ('mirhamid_be', 'parkly2026', 'Erjigitov Mirhamid', 'SUPER_ADMIN', 'Backend & Algoritmlar (Bosh Rahbar)'),
    ('hikmatilla_fe', 'parkly2026', 'Tohirjonov Hikmatilla', 'ADMIN', 'Frontend & Desktop Admin Panel'),
    ('jaloliddin_iot', 'parkly2026', 'Mamasarulov Jaloliddin', 'ADMIN', 'IoT & Mikrokontroller (ESP32)'),
    ('abbosxon_qa', 'parkly2026', 'Saidov Abbosxon', 'ADMIN', 'QA (Sifat Nazorati) & DevOps'),
    ('omirboyev_cv', 'parkly2026', 'Omirboyev Said', 'ADMIN', 'Computer Vision (ANPR/OCR)')
ON CONFLICT (username) DO NOTHING;
```

---

## ⚙️ 5. Standart Tarif Sozlamalari (Default Settings Seeder)

```sql
INSERT INTO system_settings (key, value, description) VALUES
    ('day_rate_hourly', '5000', 'Kunduzgi soatlik stavka (08:00 - 20:00) UZS'),
    ('night_rate_hourly', '3000', 'Tungi soatlik stavka (20:00 - 08:00) UZS'),
    ('grace_period_entry', '15', 'Kirishdan keyingi bepul muddat (daqiqa)'),
    ('grace_period_exit', '15', 'To''lovdan so''ng chiqish uchun berilgan vaqt (daqiqa)'),
    ('daily_cap_amount', '50000', '24 soatlik maksimal limit (UZS)'),
    ('barrier_auto_open', '1', 'Avtomatik shlagbaum ochilishi (1=ha, 0=yo''q)'),
    ('max_wait_sla_minutes', '10', 'Favqulodda shlagbaum ochilish muddati (Fail-Safe daqiqa)')
ON CONFLICT (key) DO NOTHING;
```
