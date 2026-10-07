-- ============================================================================
-- Parkly.uz — Parking Slot & Core Database Schema (PostgreSQL)
-- ============================================================================

-- 1. ENUM Tiplari
CREATE TYPE slot_type_enum AS ENUM (
    'REGULAR',       -- Standart yengil avtomobillar
    'EV_CHARGING',   -- Elektromobillar (quvvatlash stansiyasi bor)
    'VIP_STAFF',     -- VIP va xodimlar uchun ajratilgan
    'ACCESSIBLE'     -- Maxsus ehtiyojli / Nogironlar uchun
);

CREATE TYPE slot_status_enum AS ENUM (
    'FREE',             -- Bo'sh (yashil)
    'OCCUPIED',         -- Band / Mashina turibdi (qizil)
    'RESERVED',         -- Oldindan bron qilingan (sariq)
    'PAYMENT_PENDING',  -- To'lov kutilmoqda (to'q sariq)
    'MAINTENANCE'       -- Ta'mirlashda / Yopiq (kulrang)
);

-- 2. Avtoturargohlar Jadvali (Parking Lots)
CREATE TABLE IF NOT EXISTS parking_lots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    address TEXT NOT NULL,
    total_floors INT DEFAULT 1,
    total_slots INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Parking Slots Jadvali
CREATE TABLE IF NOT EXISTS parking_slots (
    id SERIAL PRIMARY KEY,
    parking_lot_id INT NOT NULL REFERENCES parking_lots(id) ON DELETE CASCADE,
    
    -- Manzillash
    floor INT NOT NULL DEFAULT 1,                       -- Qavat (masalan: 1, 2, -1)
    zone VARCHAR(10) NOT NULL,                          -- Zona (masalan: 'A', 'B', 'VIP', 'EV')
    slot_number VARCHAR(20) NOT NULL,                   -- Unikal raqam (masalan: 'A-101', 'EV-01', 'VIP-05')
    
    -- Turi va Holati
    slot_type slot_type_enum NOT NULL DEFAULT 'REGULAR',
    status slot_status_enum NOT NULL DEFAULT 'FREE',
    
    -- 2D Koordinatalar (Desktop interaktiv xarita uchun)
    pos_x INT NOT NULL DEFAULT 0,                       -- X koordinata (piksel / grid)
    pos_y INT NOT NULL DEFAULT 0,                       -- Y koordinata
    width INT NOT NULL DEFAULT 60,                      -- Slot eni (chizma uchun)
    height INT NOT NULL DEFAULT 120,                    -- Slot bo'yi
    rotation INT NOT NULL DEFAULT 0,                    -- Aylanish burchagi (0, 45, 90 gradus)
    
    -- Joriy seans va transport ma'lumotlari
    current_vehicle_plate VARCHAR(20) DEFAULT NULL,     -- Agar band bo'lsa: '01A777AA'
    current_session_id INT DEFAULT NULL,
    
    -- Vaqt belgilari
    last_status_change TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Unikallik cheklovi: Bitta parkovkada ikkita bir xil slot_number bo'lishi mumkin emas
    CONSTRAINT uq_parking_lot_slot_number UNIQUE (parking_lot_id, slot_number)
);

-- 4. Tezkor Qidiruv Indekslari
CREATE INDEX IF NOT EXISTS idx_parking_slots_lot_status ON parking_slots(parking_lot_id, status);
CREATE INDEX IF NOT EXISTS idx_parking_slots_type ON parking_slots(slot_type);
CREATE INDEX IF NOT EXISTS idx_parking_slots_number ON parking_slots(slot_number);
CREATE INDEX IF NOT EXISTS idx_parking_slots_plate ON parking_slots(current_vehicle_plate);

-- 5. Boshlang'ich test ma'lumotlari (Seeder)
INSERT INTO parking_lots (id, name, address, total_floors, total_slots)
VALUES (1, 'Parkly Central — Tashkent City Mall', 'Toshkent sh., Shayxontohur t.', 2, 20)
ON CONFLICT (id) DO NOTHING;

-- 1-qavat: A zona (Standart), EV zona (Elektromobil), VIP zona
INSERT INTO parking_slots (parking_lot_id, floor, zone, slot_number, slot_type, status, pos_x, pos_y)
VALUES 
    -- Standart joylar (Zone A)
    (1, 1, 'A', 'A-101', 'REGULAR', 'FREE', 50, 50),
    (1, 1, 'A', 'A-102', 'REGULAR', 'OCCUPIED', 130, 50),
    (1, 1, 'A', 'A-103', 'REGULAR', 'FREE', 210, 50),
    (1, 1, 'A', 'A-104', 'REGULAR', 'RESERVED', 290, 50),
    (1, 1, 'A', 'A-105', 'REGULAR', 'PAYMENT_PENDING', 370, 50),
    (1, 1, 'A', 'A-106', 'REGULAR', 'MAINTENANCE', 450, 50),
    
    -- Elektromobillar (EV Charging)
    (1, 1, 'EV', 'EV-01', 'EV_CHARGING', 'FREE', 50, 220),
    (1, 1, 'EV', 'EV-02', 'EV_CHARGING', 'OCCUPIED', 130, 220),
    (1, 1, 'EV', 'EV-03', 'EV_CHARGING', 'FREE', 210, 220),

    -- VIP va Xodimlar joylari
    (1, 1, 'VIP', 'VIP-01', 'VIP_STAFF', 'FREE', 50, 390),
    (1, 1, 'VIP', 'VIP-02', 'VIP_STAFF', 'RESERVED', 130, 390),
    (1, 1, 'VIP', 'VIP-03', 'VIP_STAFF', 'OCCUPIED', 210, 390)
ON CONFLICT DO NOTHING;
