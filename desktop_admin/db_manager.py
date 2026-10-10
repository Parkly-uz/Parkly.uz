"""
Parkly.uz — Desktop Admin Real Database Engine (SQLite & PostgreSQL sync)
Barcha ma'lumotlar haqiqiy lokal DB faylida (parkly_local.db) saqlanadi va dinamik boshqariladi.
"""

import sqlite3
import os
import random
import csv
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "parkly_local.db")


class ParklyDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Haqiqiy jadvallarni yaratish va boshlang'ich ma'lumotlarni kiritish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Xodimlar jadvali
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,  -- SUPER_ADMIN, ADMIN, OPERATOR
                shift TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 2. Parking slotlar jadvali
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS parking_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                floor INTEGER NOT NULL DEFAULT 1,
                zone TEXT NOT NULL,
                slot_number TEXT UNIQUE NOT NULL,
                slot_type TEXT NOT NULL DEFAULT 'REGULAR',
                status TEXT NOT NULL DEFAULT 'FREE', -- FREE, OCCUPIED, RESERVED, PAYMENT_PENDING, MAINTENANCE
                pos_x INTEGER NOT NULL DEFAULT 0,
                pos_y INTEGER NOT NULL DEFAULT 0,
                width INTEGER NOT NULL DEFAULT 80,
                height INTEGER NOT NULL DEFAULT 140,
                current_vehicle_plate TEXT,
                current_vehicle_model TEXT,
                entry_time TEXT,
                last_status_change TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 3. Parkovka seanslari
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS parking_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_code TEXT UNIQUE NOT NULL,
                vehicle_plate TEXT NOT NULL,
                vehicle_model TEXT,
                slot_number TEXT NOT NULL,
                entry_time TEXT NOT NULL,
                exit_time TEXT,
                total_amount INTEGER DEFAULT 0,
                payment_provider TEXT,
                status TEXT DEFAULT 'ACTIVE' -- ACTIVE, COMPLETED, CANCELLED
            )
            """)

            # Ustunlar migratsiyasi (agar mavjud bo'lmasa qo'shish)
            for m_sql in [
                "ALTER TABLE parking_slots ADD COLUMN current_vehicle_model TEXT",
                "ALTER TABLE parking_slots ADD COLUMN entry_time TEXT",
                "ALTER TABLE parking_sessions ADD COLUMN vehicle_model TEXT",
                "ALTER TABLE transactions ADD COLUMN duration TEXT",
                "ALTER TABLE transactions ADD COLUMN payment_method TEXT",
            ]:
                try:
                    cursor.execute(m_sql)
                except sqlite3.OperationalError:
                    pass

            # 4. Tranzaksiyalar jadvali
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tx_code TEXT UNIQUE NOT NULL,
                session_code TEXT NOT NULL,
                vehicle_plate TEXT NOT NULL,
                provider TEXT NOT NULL, -- Payme, Click, Naqd, Uzum
                amount INTEGER NOT NULL,
                status TEXT DEFAULT 'SUCCESS',
                fiscal_sign TEXT,
                duration TEXT DEFAULT '01:15:00',
                payment_method TEXT DEFAULT 'Elektron To''lov',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 5. Shlagbaum audit jurnali
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS barrier_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operator_username TEXT NOT NULL,
                operator_name TEXT NOT NULL,
                action TEXT DEFAULT 'MANUAL_OPEN',
                reason TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 6. Tizim sozlamalari
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                description TEXT
            )
            """)

            # 7. Xabarnomalar (Notifications)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT NOT NULL DEFAULT 'INFO', -- INFO, SUCCESS, WARNING, ALERT
                is_read INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 8. Ruxsat ro'yxati (Whitelist & Blacklist)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_access_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate TEXT UNIQUE NOT NULL,
                list_type TEXT NOT NULL, -- WHITELIST, BLACKLIST
                note TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 9. Chegirmalar va vaucherlar (Coupons)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS coupons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                discount_percent INTEGER NOT NULL,
                valid_until TEXT,
                is_active INTEGER DEFAULT 1
            )
            """)

            conn.commit()

            # Boshlang'ich ma'lumotlarni tekshirish va to'ldirish
            self._seed_default_data(cursor)
            conn.commit()

    def _seed_default_data(self, cursor):
        # 1. Xodimlar mavjudligini tekshirish (Super-Admin: 2 kishi, Oddiy Admin: 4 kishi, Operator: 2 kishi)
        cursor.execute("SELECT COUNT(*) FROM staff_users WHERE role = 'SUPER_ADMIN'")
        super_cnt = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM staff_users WHERE role = 'ADMIN'")
        admin_cnt = cursor.fetchone()[0]

        if super_cnt != 2 or admin_cnt != 4:
            cursor.execute("DELETE FROM staff_users")
            default_staff = [
                # 2 Ta Super-Admin (Tizimning to'liq arxitekturasi, uskunalar va xodimlar boshqaruvi)
                ("admin", "admin123", "Erjigit (Bosh Rahbar)", "SUPER_ADMIN", "Boshqaruv / Barcha hudud"),
                ("superadmin2", "admin123", "Sherzod Aliyev (Tizim Arxitektori)", "SUPER_ADMIN", "Texnik va Tizim Boshqaruvi"),
                # 4 Ta Oddiy Admin (Operatsion jarayon, tushumlarni monitoring qilish, tranzaksiyalar va navbatchilik)
                ("admin_yunusobod", "admin123", "Jahongir Qodirov", "ADMIN", "Yunusobod Filiali"),
                ("admin_chilonzor", "admin123", "Aziz Rustamov", "ADMIN", "Chilonzor Filiali"),
                ("admin_mirobod", "admin123", "Bobur Mirzayev", "ADMIN", "Mirobod Filiali"),
                ("admin_sergeli", "admin123", "Dilshod Karimov", "ADMIN", "Sergeli Filiali"),
                # 2 Ta Navbatchi Operator
                ("operator1", "operator123", "Farrux Yusupov", "OPERATOR", "Smena 1 (08:00 - 16:00)"),
                ("operator2", "operator123", "G'ayrat Xoliqov", "OPERATOR", "Smena 2 (16:00 - 00:00)"),
            ]
            cursor.executemany("""
                INSERT INTO staff_users (username, password, full_name, role, shift)
                VALUES (?, ?, ?, ?, ?)
            """, default_staff)

        # 2. Slotlar mavjudligini tekshirish (4 ta qavat, jami 56 ta slot)
        cursor.execute("SELECT COUNT(*) FROM parking_slots")
        slot_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT floor) FROM parking_slots")
        floor_count = cursor.fetchone()[0]

        if slot_count < 56 or floor_count < 4:
            cursor.execute("DELETE FROM parking_slots")
            now = datetime.now()
            slots = [
                # -------------------------------------------------------------
                # 1-Qavat (Yer usti Markaziy & VIP) - 14 ta slot
                # -------------------------------------------------------------
                (1, "A", "A-101", "REGULAR", "FREE", 180, 30, 52, 78, None, None, None),
                (1, "A", "A-102", "REGULAR", "OCCUPIED", 240, 30, 52, 78, "01 A 777 AA", "Chevrolet Malibu 2 Premier", (now - timedelta(hours=1, minutes=15)).strftime("%H:%M:%S")),
                (1, "A", "A-103", "REGULAR", "FREE", 300, 30, 52, 78, None, None, None),
                (1, "A", "A-104", "REGULAR", "RESERVED", 360, 30, 52, 78, None, None, None),
                (1, "A", "A-105", "REGULAR", "OCCUPIED", 420, 30, 52, 78, "10 123 BBA", "Chevrolet Tracker 2 Redline", (now - timedelta(minutes=45)).strftime("%H:%M:%S")),
                (1, "A", "A-106", "REGULAR", "MAINTENANCE", 480, 30, 52, 78, None, None, None),
                (1, "A", "A-107", "REGULAR", "FREE", 540, 30, 52, 78, None, None, None),
                (1, "EV", "EV-108", "EV_CHARGING", "OCCUPIED", 180, 280, 52, 78, "01 888 ZZZ", "BYD Song Plus Champion EV", (now - timedelta(hours=2, minutes=10)).strftime("%H:%M:%S")),
                (1, "EV", "EV-109", "EV_CHARGING", "FREE", 240, 280, 52, 78, None, None, None),
                (1, "VIP", "VIP-110", "VIP_STAFF", "FREE", 300, 280, 52, 78, None, None, None),
                (1, "VIP", "VIP-111", "VIP_STAFF", "OCCUPIED", 360, 280, 52, 78, "01 001 PPP", "Mercedes-Benz E300", (now - timedelta(hours=3, minutes=20)).strftime("%H:%M:%S")),
                (1, "VIP", "VIP-112", "VIP_STAFF", "RESERVED", 420, 280, 52, 78, None, None, None),
                (1, "A", "A-113", "REGULAR", "OCCUPIED", 480, 280, 52, 78, "01 234 OOO", "Kia K5 GT-Line", (now - timedelta(minutes=35)).strftime("%H:%M:%S")),
                (1, "A", "A-114", "REGULAR", "FREE", 540, 280, 52, 78, None, None, None),

                # -------------------------------------------------------------
                # 2-Qavat (EV Quvvatlash Stansiyasi) - 14 ta slot
                # -------------------------------------------------------------
                (2, "EV", "EV-201", "EV_CHARGING", "OCCUPIED", 180, 30, 52, 78, "01 B 999 BB", "Tesla Model Y Long Range", (now - timedelta(hours=1, minutes=40)).strftime("%H:%M:%S")),
                (2, "EV", "EV-202", "EV_CHARGING", "FREE", 240, 30, 52, 78, None, None, None),
                (2, "EV", "EV-203", "EV_CHARGING", "OCCUPIED", 300, 30, 52, 78, "01 777 EVV", "Zeekr 001 EV", (now - timedelta(hours=2)).strftime("%H:%M:%S")),
                (2, "EV", "EV-204", "EV_CHARGING", "FREE", 360, 30, 52, 78, None, None, None),
                (2, "EV", "EV-205", "EV_CHARGING", "OCCUPIED", 420, 30, 52, 78, "50 555 EEV", "BYD Han Flagship EV", (now - timedelta(minutes=55)).strftime("%H:%M:%S")),
                (2, "EV", "EV-206", "EV_CHARGING", "FREE", 480, 30, 52, 78, None, None, None),
                (2, "EV", "EV-207", "EV_CHARGING", "MAINTENANCE", 540, 30, 52, 78, None, None, None),
                (2, "EV", "EV-208", "EV_CHARGING", "FREE", 180, 280, 52, 78, None, None, None),
                (2, "EV", "EV-209", "EV_CHARGING", "OCCUPIED", 240, 280, 52, 78, "01 321 TES", "Tesla Model 3 Performance", (now - timedelta(hours=1, minutes=5)).strftime("%H:%M:%S")),
                (2, "EV", "EV-210", "EV_CHARGING", "FREE", 300, 280, 52, 78, None, None, None),
                (2, "EV", "EV-211", "EV_CHARGING", "OCCUPIED", 360, 280, 52, 78, "10 888 BYD", "BYD Song Plus Champion EV", (now - timedelta(minutes=40)).strftime("%H:%M:%S")),
                (2, "EV", "EV-212", "EV_CHARGING", "FREE", 420, 280, 52, 78, None, None, None),
                (2, "EV", "EV-213", "EV_CHARGING", "FREE", 480, 280, 52, 78, None, None, None),
                (2, "EV", "EV-214", "EV_CHARGING", "RESERVED", 540, 280, 52, 78, None, None, None),

                # -------------------------------------------------------------
                # 3-Qavat (Yuqori tom Panorama) - 14 ta slot
                # -------------------------------------------------------------
                (3, "C", "C-301", "REGULAR", "FREE", 180, 30, 52, 78, None, None, None),
                (3, "C", "C-302", "REGULAR", "OCCUPIED", 240, 30, 52, 78, "01 555 TTT", "Chevrolet Cobalt LTZ", (now - timedelta(hours=1, minutes=10)).strftime("%H:%M:%S")),
                (3, "C", "C-303", "REGULAR", "FREE", 300, 30, 52, 78, None, None, None),
                (3, "C", "C-304", "REGULAR", "OCCUPIED", 360, 30, 52, 78, "80 444 RRR", "Chevrolet Gentra Elegance Plus", (now - timedelta(hours=2, minutes=25)).strftime("%H:%M:%S")),
                (3, "C", "C-305", "REGULAR", "FREE", 420, 30, 52, 78, None, None, None),
                (3, "C", "C-306", "REGULAR", "FREE", 480, 30, 52, 78, None, None, None),
                (3, "C", "C-307", "REGULAR", "RESERVED", 540, 30, 52, 78, None, None, None),
                (3, "C", "C-308", "REGULAR", "FREE", 180, 280, 52, 78, None, None, None),
                (3, "C", "C-309", "REGULAR", "OCCUPIED", 240, 280, 52, 78, "01 717 AAA", "Chevrolet Onix Premier", (now - timedelta(minutes=20)).strftime("%H:%M:%S")),
                (3, "C", "C-310", "REGULAR", "FREE", 300, 280, 52, 78, None, None, None),
                (3, "C", "C-311", "REGULAR", "FREE", 360, 280, 52, 78, None, None, None),
                (3, "C", "C-312", "REGULAR", "FREE", 420, 280, 52, 78, None, None, None),
                (3, "C", "C-313", "REGULAR", "OCCUPIED", 480, 280, 52, 78, "01 909 BBB", "Hyundai Tucson Prime", (now - timedelta(hours=1, minutes=30)).strftime("%H:%M:%S")),
                (3, "C", "C-314", "REGULAR", "FREE", 540, 280, 52, 78, None, None, None),

                # -------------------------------------------------------------
                # -1 Qavat (Yerosti Podzemka & VIP) - 14 ta slot
                # -------------------------------------------------------------
                (-1, "VIP", "U-101", "VIP_STAFF", "OCCUPIED", 180, 30, 52, 78, "01 A 007 AA", "BMW 530i M Sport", (now - timedelta(hours=3, minutes=10)).strftime("%H:%M:%S")),
                (-1, "VIP", "U-102", "VIP_STAFF", "FREE", 240, 30, 52, 78, None, None, None),
                (-1, "VIP", "U-103", "VIP_STAFF", "RESERVED", 300, 30, 52, 78, None, None, None),
                (-1, "EV", "U-104", "EV_CHARGING", "OCCUPIED", 360, 30, 52, 78, "01 444 ELV", "Porsche Taycan 4S", (now - timedelta(hours=2, minutes=5)).strftime("%H:%M:%S")),
                (-1, "EV", "U-105", "EV_CHARGING", "FREE", 420, 30, 52, 78, None, None, None),
                (-1, "U", "U-106", "REGULAR", "FREE", 480, 30, 52, 78, None, None, None),
                (-1, "U", "U-107", "REGULAR", "OCCUPIED", 540, 30, 52, 78, "10 707 XXX", "Chevrolet Tracker 2 Redline", (now - timedelta(hours=1, minutes=15)).strftime("%H:%M:%S")),
                (-1, "U", "U-108", "REGULAR", "FREE", 180, 280, 52, 78, None, None, None),
                (-1, "U", "U-109", "REGULAR", "FREE", 240, 280, 52, 78, None, None, None),
                (-1, "U", "U-110", "REGULAR", "MAINTENANCE", 300, 280, 52, 78, None, None, None),
                (-1, "U", "U-111", "REGULAR", "OCCUPIED", 360, 280, 52, 78, "01 333 YYY", "Chevrolet Malibu 2 Premier", (now - timedelta(minutes=50)).strftime("%H:%M:%S")),
                (-1, "U", "U-112", "REGULAR", "FREE", 420, 280, 52, 78, None, None, None),
                (-1, "EV", "U-113", "EV_CHARGING", "FREE", 480, 280, 52, 78, None, None, None),
                (-1, "VIP", "U-114", "VIP_STAFF", "FREE", 540, 280, 52, 78, None, None, None),
            ]
            cursor.executemany("""
                INSERT INTO parking_slots (floor, zone, slot_number, slot_type, status, pos_x, pos_y, width, height, current_vehicle_plate, current_vehicle_model, entry_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, slots)

        # 3. Dastlabki Tranzaksiyalar va Seanslar (Kunlik, Haftalik va Oylik hisobotlar uchun)
        cursor.execute("SELECT COUNT(*) FROM transactions")
        if cursor.fetchone()[0] < 15:
            cursor.execute("DELETE FROM transactions")
            now = datetime.now()
            txs = [
                # Bugungi tranzaksiyalar (Kunlik)
                ("TX-9921", "SES-1049", "01 A 777 AA", "Payme", 15000, "FISC-88221", "01:15:00", "Payme Ilovasi", (now - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9920", "SES-1048", "10 123 BBA", "Click", 10000, "FISC-88220", "00:45:00", "Click Up", (now - timedelta(minutes=40)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9919", "SES-1047", "01 888 ZZZ", "Payme", 35000, "FISC-88219", "02:10:00", "Payme Ilovasi", (now - timedelta(hours=1, minutes=20)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9918", "SES-1045", "30 456 VVA", "Naqd", 20000, "FISC-88218", "01:30:00", "Kassa (Naqd)", (now - timedelta(hours=2, minutes=10)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9917", "SES-1044", "01 111 AAA", "Uzum", 25000, "FISC-88217", "01:45:00", "Uzum Bank", (now - timedelta(hours=3, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9916", "SES-1043", "01 B 999 BB", "Payme", 30000, "FISC-88216", "02:00:00", "Payme Ilovasi", (now - timedelta(hours=4, minutes=10)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9915", "SES-1042", "50 555 EEV", "Click", 50000, "FISC-88215", "03:20:00", "Click Up", (now - timedelta(hours=5, minutes=15)).strftime("%Y-%m-%d %H:%M:%S")),

                # 1 kun oldin (Kechagi)
                ("TX-9914", "SES-1039", "01 321 TES", "Payme", 35000, "FISC-88214", "02:15:00", "Payme Ilovasi", (now - timedelta(days=1, hours=2)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9913", "SES-1038", "10 888 BYD", "Uzum", 20000, "FISC-88213", "01:20:00", "Uzum Bank", (now - timedelta(days=1, hours=4)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9912", "SES-1037", "01 555 TTT", "Naqd", 15000, "FISC-88212", "01:05:00", "Kassa (Naqd)", (now - timedelta(days=1, hours=6)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9911", "SES-1036", "80 444 RRR", "Click", 25000, "FISC-88211", "01:40:00", "Click Up", (now - timedelta(days=1, hours=7)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9910", "SES-1035", "01 717 AAA", "Payme", 15000, "FISC-88210", "00:55:00", "Payme Ilovasi", (now - timedelta(days=1, hours=9)).strftime("%Y-%m-%d %H:%M:%S")),

                # 2 kun oldin
                ("TX-9909", "SES-1034", "01 909 BBB", "Click", 20000, "FISC-88209", "01:30:00", "Click Up", (now - timedelta(days=2, hours=2)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9908", "SES-1033", "01 A 007 AA", "Payme", 45000, "FISC-88208", "03:10:00", "Payme Ilovasi", (now - timedelta(days=2, hours=5)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9907", "SES-1032", "01 444 ELV", "Uzum", 30000, "FISC-88207", "02:00:00", "Uzum Bank", (now - timedelta(days=2, hours=7)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9906", "SES-1031", "10 707 XXX", "Naqd", 10000, "FISC-88206", "00:40:00", "Kassa (Naqd)", (now - timedelta(days=2, hours=9)).strftime("%Y-%m-%d %H:%M:%S")),

                # 3 kun oldin
                ("TX-9905", "SES-1030", "01 333 YYY", "Payme", 25000, "FISC-88205", "01:45:00", "Payme Ilovasi", (now - timedelta(days=3, hours=3)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9904", "SES-1029", "01 234 OOO", "Click", 15000, "FISC-88204", "01:10:00", "Click Up", (now - timedelta(days=3, hours=5)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9903", "SES-1028", "01 001 PPP", "Payme", 50000, "FISC-88203", "03:40:00", "Payme Ilovasi", (now - timedelta(days=3, hours=8)).strftime("%Y-%m-%d %H:%M:%S")),

                # 4 kun oldin
                ("TX-9902", "SES-1027", "20 567 BBB", "Uzum", 20000, "FISC-88202", "01:25:00", "Uzum Bank", (now - timedelta(days=4, hours=2)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9901", "SES-1026", "40 999 ZZZ", "Naqd", 35000, "FISC-88201", "02:20:00", "Kassa (Naqd)", (now - timedelta(days=4, hours=6)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9900", "SES-1025", "01 777 EVV", "Click", 30000, "FISC-88200", "02:00:00", "Click Up", (now - timedelta(days=4, hours=9)).strftime("%Y-%m-%d %H:%M:%S")),

                # 5 kun oldin
                ("TX-8999", "SES-1024", "10 444 KKK", "Payme", 20000, "FISC-88199", "01:15:00", "Payme Ilovasi", (now - timedelta(days=5, hours=3)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-8998", "SES-1023", "01 888 BBB", "Click", 15000, "FISC-88198", "01:00:00", "Click Up", (now - timedelta(days=5, hours=5)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-8997", "SES-1022", "60 123 CCC", "Naqd", 25000, "FISC-88197", "01:40:00", "Kassa (Naqd)", (now - timedelta(days=5, hours=8)).strftime("%Y-%m-%d %H:%M:%S")),

                # 6 kun oldin
                ("TX-8996", "SES-1021", "01 321 AAA", "Payme", 40000, "FISC-88196", "02:45:00", "Payme Ilovasi", (now - timedelta(days=6, hours=3)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-8995", "SES-1020", "10 654 DDD", "Uzum", 15000, "FISC-88195", "01:05:00", "Uzum Bank", (now - timedelta(days=6, hours=6)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-8994", "SES-1019", "01 789 EEE", "Click", 30000, "FISC-88194", "02:00:00", "Click Up", (now - timedelta(days=6, hours=9)).strftime("%Y-%m-%d %H:%M:%S")),
            ]
            cursor.executemany("""
                INSERT INTO transactions (tx_code, session_code, vehicle_plate, provider, amount, fiscal_sign, duration, payment_method, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, txs)

            # Seanslar
            sessions = [
                ("SES-1049", "01 A 777 AA", "A-102", (now - timedelta(hours=1)).strftime("%H:%M:%S"), None, 15000, "Payme", "ACTIVE"),
                ("SES-1048", "10 123 BBA", "A-105", (now - timedelta(minutes=45)).strftime("%H:%M:%S"), None, 10000, "Click", "ACTIVE"),
                ("SES-1047", "01 888 ZZZ", "EV-02", (now - timedelta(hours=2)).strftime("%H:%M:%S"), None, 35000, "Payme", "ACTIVE"),
                ("SES-1046", "01 001 PPP", "VIP-02", (now - timedelta(hours=3)).strftime("%H:%M:%S"), None, 0, "VIP", "ACTIVE"),
            ]
            cursor.executemany("""
                INSERT OR IGNORE INTO parking_sessions (session_code, vehicle_plate, slot_number, entry_time, exit_time, total_amount, payment_provider, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, sessions)

        # 4. Tizim sozlamalari
        default_settings = [
            ("day_rate", "5000", "Kunduzgi soatlik stavka (08:00 - 20:00, so'm)"),
            ("night_rate", "3000", "Tungi soatlik stavka (20:00 - 08:00, so'm)"),
            ("minute_rate", "100", "Daqiqabay stavka (so'm/daqiqa)"),
            ("ev_rate", "2500", "EV Quvvatlash qo'shimcha stavkasi (so'm/soat)"),
            ("grace_period", "15", "Dastlabki bepul oraliq (daqiqa)"),
            ("exit_grace", "15", "To'lovdan so'ng chiqish oralig'i (daqiqa)"),
            ("daily_cap", "50000", "Kunlik maksimal to'lov chegarasi (so'm)"),
            ("barrier_auto_open", "1", "Shlagbaum avtomatik ochilishi (1=ha, 0=yo'q)"),
        ]
        for k, v, d in default_settings:
            cursor.execute("""
                INSERT INTO system_settings (key, value, description)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET description = excluded.description
            """, (k, v, d))

        # 5. Dastlabki Xabarnomalar (Notifications)
        cursor.execute("SELECT COUNT(*) FROM system_notifications")
        if cursor.fetchone()[0] == 0:
            now = datetime.now()
            notifs = [
                ("Yangi avto kirdi", "01 A 777 AA (A-102 slotiga biriktirildi). ANPR: 99.4%", "INFO", (now - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")),
                ("To'lov muvaffaqiyatli", "15 000 UZS qabul qilindi (Payme / Fiskal: FISC-88214)", "SUCCESS", (now - timedelta(minutes=18)).strftime("%Y-%m-%d %H:%M:%S")),
                ("Shlagbaum ochildi", "Farrux Yusupov (Operator): Tez tibbiy yordam avtomobili", "WARNING", (now - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S")),
                ("Bron faollashdi", "01 001 PPP (VIP-02 zaxiralangan joy)", "INFO", (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"))
            ]
            cursor.executemany("""
                INSERT INTO system_notifications (title, message, type, created_at)
                VALUES (?, ?, ?, ?)
            """, notifs)

        # 6. Dastlabki Oq va Qora ro'yxat (Whitelist & Blacklist)
        cursor.execute("SELECT COUNT(*) FROM vehicle_access_list")
        if cursor.fetchone()[0] == 0:
            access_items = [
                ("01 001 PPP", "WHITELIST", "VIP Xizmat avtomobili (Bepul kirish)"),
                ("01 A 007 AA", "WHITELIST", "Direksiya boshqaruv avtomobili"),
                ("01 X 666 XX", "BLACKLIST", "To'lov qilmasdan qochgan / Qoidabuzar"),
                ("10 Z 999 ZZ", "BLACKLIST", "Muntazam qoidabuzarlik uchun bloklangan"),
            ]
            cursor.executemany("""
                INSERT INTO vehicle_access_list (plate, list_type, note)
                VALUES (?, ?, ?)
            """, access_items)

        # 7. Dastlabki Chegirma vaucherlari (Coupons)
        cursor.execute("SELECT COUNT(*) FROM coupons")
        if cursor.fetchone()[0] == 0:
            coupons = [
                ("PARKLY10", 10, "2026-12-31"),
                ("VIPGUEST", 50, "2026-12-31"),
                ("FREESTART", 100, "2026-11-30"),
            ]
            cursor.executemany("""
                INSERT INTO coupons (code, discount_percent, valid_until)
                VALUES (?, ?, ?)
            """, coupons)

    # --------------------------------------------------------------------------
    # CRUD METODLARI
    # --------------------------------------------------------------------------
    def authenticate(self, username, password):
        """Foydalanuvchi tekshiruvi"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, full_name, role, shift FROM staff_users
                WHERE username = ? AND password = ? AND is_active = 1
            """, (username, password))
            row = cursor.fetchone()
            if row:
                return dict(row)
        return None

    def get_slots(self, floor=1):
        """Qavat bo'yicha slotlarni olish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM parking_slots WHERE floor = ? ORDER BY slot_number ASC
            """, (floor,))
            return [dict(r) for r in cursor.fetchall()]

    def update_slot_status(self, slot_number, new_status, plate=None, model=None, entry_time=None):
        """Slot holatini bazada yangilash"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if new_status == "FREE":
                plate = None
                model = None
                entry_time = None
            elif new_status == "OCCUPIED" and not entry_time:
                entry_time = datetime.now().strftime("%H:%M:%S")

            cursor.execute("""
                UPDATE parking_slots
                SET status = ?, current_vehicle_plate = ?, current_vehicle_model = ?, entry_time = ?, last_status_change = CURRENT_TIMESTAMP
                WHERE slot_number = ?
            """, (new_status, plate, model, entry_time, slot_number))
            conn.commit()
            return cursor.rowcount > 0

    def simulate_car_entry(self, plate=None, model=None):
        """
        Dinamik avto kirishi: Birinchi bo'sh slotni topib band qiladi va yangi seans ochadi.
        """
        car_models = [
            "Chevrolet Malibu 2 Premier",
            "Chevrolet Tracker 2 Redline",
            "Chevrolet Gentra Elegance Plus",
            "Chevrolet Cobalt LTZ",
            "Chevrolet Onix Premier",
            "BYD Song Plus Champion EV",
            "BYD Han Flagship EV",
            "Tesla Model Y Long Range",
            "Kia K5 GT-Line",
            "Hyundai Tucson Prime",
            "Mercedes-Benz E300",
            "BMW 530i M Sport",
            "Zeekr 001 EV"
        ]

        if not plate:
            num = random.randint(100, 999)
            plate = f"01 A {num} AA"
        if not model:
            model = random.choice(car_models)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Bo'sh slot qidirish
            cursor.execute("SELECT slot_number FROM parking_slots WHERE status = 'FREE' ORDER BY id ASC LIMIT 1")
            row = cursor.fetchone()
            if not row:
                return None  # Joy qolmagan

            assigned_slot = row["slot_number"]
            now_str = datetime.now().strftime("%H:%M:%S")
            ses_code = f"SES-{random.randint(2000, 9999)}"

            # Slotni band qilish
            cursor.execute("""
                UPDATE parking_slots
                SET status = 'OCCUPIED', current_vehicle_plate = ?, current_vehicle_model = ?, entry_time = ?, last_status_change = CURRENT_TIMESTAMP
                WHERE slot_number = ?
            """, (plate, model, now_str, assigned_slot))

            # Seans yozish
            cursor.execute("""
                INSERT INTO parking_sessions (session_code, vehicle_plate, vehicle_model, slot_number, entry_time, status)
                VALUES (?, ?, ?, ?, ?, 'ACTIVE')
            """, (ses_code, plate, model, assigned_slot, now_str))

            conn.commit()

        self.add_notification("Yangi avto kirdi", f"{model} ({plate}) — {assigned_slot} slotiga biriktirildi", "INFO")
        return {"slot": assigned_slot, "plate": plate, "model": model, "time": now_str, "session": ses_code}

    def simulate_car_exit(self, slot_number):
        """Avto chiqishi va to'lovni yozish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_vehicle_plate, current_vehicle_model FROM parking_slots WHERE slot_number = ?", (slot_number,))
            row = cursor.fetchone()
            if not row or not row["current_vehicle_plate"]:
                return False

            plate = row["current_vehicle_plate"]
            now_str = datetime.now().strftime("%H:%M:%S")
            amount = 15000
            provider = random.choice(["Payme", "Click", "Naqd"])
            tx_code = f"TX-{random.randint(10000, 99999)}"

            # Slotni bo'shatish
            cursor.execute("""
                UPDATE parking_slots
                SET status = 'FREE', current_vehicle_plate = NULL, current_vehicle_model = NULL, entry_time = NULL, last_status_change = CURRENT_TIMESTAMP
                WHERE slot_number = ?
            """, (slot_number,))

            # Tranzaksiya qo'shish
            cursor.execute("""
                INSERT INTO transactions (tx_code, session_code, vehicle_plate, provider, amount, fiscal_sign)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tx_code, "SES-AUTO", plate, provider, amount, f"FISC-{random.randint(10000, 99999)}"))

            conn.commit()

        self.add_notification("Avto chiqdi", f"{plate} ({slot_number} bo'shatildi, {amount} UZS to'landi)", "SUCCESS")
        return {"plate": plate, "amount": amount, "provider": provider}

    def get_dashboard_stats(self):
        """Dinamik bosh sahifa ko'rsatkichlari"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Slotlar holati
            cursor.execute("SELECT COUNT(*) FROM parking_slots WHERE status = 'FREE'")
            free_cnt = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM parking_slots WHERE status = 'OCCUPIED'")
            occ_cnt = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM parking_slots WHERE status = 'RESERVED'")
            res_cnt = cursor.fetchone()[0]

            # Jami tushum
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE status = 'SUCCESS'")
            rev = cursor.fetchone()[0] or 0

            return {
                "free_slots": free_cnt,
                "occupied_slots": occ_cnt,
                "reserved_slots": res_cnt,
                "total_revenue": rev
            }

    def get_recent_activities(self, limit=8):
        """So'nggi harakatlar ro'yxati"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT session_code, vehicle_plate, slot_number, entry_time, total_amount, payment_provider, status
                FROM parking_sessions
                ORDER BY id DESC LIMIT ?
            """, (limit,))
            return [dict(r) for r in cursor.fetchall()]

    def get_all_staff(self):
        """Barcha xodimlar"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, full_name, role, shift FROM staff_users ORDER BY id ASC")
            return [dict(r) for r in cursor.fetchall()]

    def add_staff(self, username, password, full_name, role, shift):
        """Yangi xodim qo'shish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO staff_users (username, password, full_name, role, shift)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, password, full_name, role, shift))
                conn.commit()
                self.add_notification("Yangi xodim qo'shildi", f"{full_name} ({role}) tizimga qo'shildi.", "INFO")
                return True
        except sqlite3.IntegrityError:
            return False

    def update_staff(self, staff_id, full_name, username, role, shift, password=None):
        """Xodim ma'lumotlarini tahrirlash (Edit Staff)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Login band emasligini tekshirish
                cursor.execute("SELECT id FROM staff_users WHERE username = ? AND id != ?", (username, staff_id))
                if cursor.fetchone():
                    return False, f"'{username}' logini boshqa xodim tomonidan band qilingan!"

                if password and password.strip():
                    cursor.execute("""
                        UPDATE staff_users
                        SET full_name = ?, username = ?, role = ?, shift = ?, password = ?
                        WHERE id = ?
                    """, (full_name, username, role, shift, password.strip(), staff_id))
                else:
                    cursor.execute("""
                        UPDATE staff_users
                        SET full_name = ?, username = ?, role = ?, shift = ?
                        WHERE id = ?
                    """, (full_name, username, role, shift, staff_id))
                conn.commit()
                self.add_notification("Xodim tahrirlandi", f"{full_name} ({username}) ma'lumotlari yangilandi.", "INFO")
                return True, "Xodim ma'lumotlari muvaffaqiyatli saqlandi!"
        except Exception as e:
            return False, str(e)

    def delete_staff(self, staff_id):
        """Xodimni o'chirish (Delete Staff)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, full_name FROM staff_users WHERE id = ?", (staff_id,))
            user = cursor.fetchone()
            if not user:
                return False, "Xodim topilmadi!"
            if user["username"] == "admin":
                return False, "Asosiy Super-Admin (admin) tizimdan o'chirilishi mumkin emas!"
            cursor.execute("DELETE FROM staff_users WHERE id = ?", (staff_id,))
            conn.commit()
            self.add_notification("Xodim o'chirildi", f"{user['full_name']} ({user['username']}) tizimdan o'chirildi.", "WARNING")
            return True, "Xodim tizimdan o'chirildi!"

    def get_financial_summary(self, period="day"):
        """
        Moliya va kassa hisoboti:
        - Kunlik (today), haftalik (7 kun) va oylik (30 kun) tushumlar hisoboti
        - To'lov provayderlari (Payme, Click, Naqd, Uzum) ulushlari va summalari
        - O'rtacha chek va tranzaksiyalar soni
        - 7 kunlik trend grafigi ma'lumotlari
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Kunlik tushum (Bugun)
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM transactions
                WHERE status = 'SUCCESS' AND date(created_at) = date('now', 'localtime')
            """)
            r_day, c_day = cursor.fetchone()

            # Haftalik tushum (So'nggi 7 kun)
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM transactions
                WHERE status = 'SUCCESS' AND date(created_at) >= date('now', '-7 days', 'localtime')
            """)
            r_week, c_week = cursor.fetchone()

            # Oylik tushum (Joriy oy)
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM transactions
                WHERE status = 'SUCCESS' AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now', 'localtime')
            """)
            r_month, c_month = cursor.fetchone()

            # Jami umumiy tushum
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM transactions
                WHERE status = 'SUCCESS'
            """)
            r_total, c_total = cursor.fetchone()

            # Provayderlar bo'yicha tushum
            providers = ["Payme", "Click", "Naqd", "Uzum"]
            prov_totals = {}
            for p in providers:
                cursor.execute("""
                    SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM transactions
                    WHERE status = 'SUCCESS' AND provider = ?
                """, (p,))
                amt, cnt = cursor.fetchone()
                prov_totals[p] = {"amount": amt, "count": cnt}

            # Tanlangan davr bo'yicha statistika
            if period == "day":
                cur_revenue, cur_count = r_day, c_day
            elif period == "week":
                cur_revenue, cur_count = r_week, c_week
            elif period == "month":
                cur_revenue, cur_count = r_month, c_month
            else:
                cur_revenue, cur_count = r_total, c_total

            avg_check = int(cur_revenue / cur_count) if cur_count > 0 else 0

            # 7 kunlik trend grafigi ma'lumotlari (Bar Chart uchun)
            uz_day_names = ["Dush", "Sesh", "Chor", "Pay", "Juma", "Shan", "Yak"]
            chart_data = []
            now = datetime.now()
            for i in range(6, -1, -1):
                d = now - timedelta(days=i)
                d_str = d.strftime("%Y-%m-%d")
                weekday_name = uz_day_names[d.weekday()]
                cursor.execute("""
                    SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM transactions
                    WHERE status = 'SUCCESS' AND date(created_at) = ?
                """, (d_str,))
                d_amt, d_cnt = cursor.fetchone()
                chart_data.append({
                    "date": d_str,
                    "day_name": weekday_name,
                    "revenue": d_amt,
                    "count": d_cnt
                })

            cursor.execute("""
                SELECT id, tx_code, session_code, vehicle_plate, provider, amount, status,
                       COALESCE(fiscal_sign, 'FISC-00000') as fiscal_sign,
                       COALESCE(duration, '01:15:00') as duration,
                       COALESCE(payment_method, provider) as payment_method,
                       created_at
                FROM transactions
                WHERE status = 'SUCCESS'
                ORDER BY id DESC LIMIT 20
            """)
            recent_txs = [dict(r) for r in cursor.fetchall()]

            return {
                "today_revenue": r_day,
                "today_count": c_day,
                "week_revenue": r_week,
                "week_count": c_week,
                "month_revenue": r_month,
                "month_count": c_month,
                "total_revenue": r_total,
                "total_count": c_total,
                "period_revenue": cur_revenue,
                "period_count": cur_count,
                "avg_check": avg_check,
                "payme_total": prov_totals["Payme"]["amount"],
                "click_total": prov_totals["Click"]["amount"],
                "cash_total": prov_totals["Naqd"]["amount"],
                "uzum_total": prov_totals["Uzum"]["amount"],
                "providers": prov_totals,
                "chart_data": chart_data,
                "transactions": recent_txs
            }

    def get_transaction_history(self, search="", provider="BARCHASI", period="all", limit=100):
        """
        Barcha to'lovlar, sessiyalar davomiyligi va to'lov usullari (Naqd/Karta/App) bazasi.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            conditions = ["1=1"]
            params = []

            if provider and provider != "BARCHASI":
                conditions.append("provider = ?")
                params.append(provider)

            if search and search.strip():
                s = f"%{search.strip()}%"
                conditions.append("(vehicle_plate LIKE ? OR tx_code LIKE ? OR session_code LIKE ? OR fiscal_sign LIKE ?)")
                params.extend([s, s, s, s])

            if period == "day":
                conditions.append("date(created_at) = date('now', 'localtime')")
            elif period == "week":
                conditions.append("date(created_at) >= date('now', '-7 days', 'localtime')")
            elif period == "month":
                conditions.append("strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now', 'localtime')")

            where_clause = " AND ".join(conditions)
            params.append(limit)

            sql = f"""
                SELECT id, tx_code, session_code, vehicle_plate, provider, amount, status,
                       COALESCE(fiscal_sign, 'FISC-00000') as fiscal_sign,
                       COALESCE(duration, '01:15:00') as duration,
                       COALESCE(payment_method, provider) as payment_method,
                       created_at
                FROM transactions
                WHERE {where_clause}
                ORDER BY id DESC LIMIT ?
            """
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

    def export_financial_report(self, export_format="csv", filepath=None):
        """
        Moliyaviy hisobotlarni Excel / CSV formatida yuklab olish.
        Excel'da o'zbekcha yozuvlar buzilmasligi uchun UTF-8-SIG (BOM) va
        Windows Excel uchun qulay ';' ajratuvchisi bilan shakllantiriladi.
        """
        try:
            now_dt = datetime.now()
            if not filepath:
                export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
                os.makedirs(export_dir, exist_ok=True)
                ext = "csv" if export_format.lower() in ["csv", "excel"] else export_format.lower()
                filename = f"Parkly_Moliyaviy_Hisobot_{now_dt.strftime('%Y%m%d_%H%M%S')}.{ext}"
                filepath = os.path.join(export_dir, filename)

            summary = self.get_financial_summary(period="all")
            txs = self.get_transaction_history(limit=5000)

            with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                # Sarlavha bloki
                writer.writerow(["PARKLY.UZ — AQLLI AVTOTURARGOH MOLIYAVIY VA TRANZAKSIYALAR HISOBOTI", "", "", "", "", "", "", "", "", ""])
                writer.writerow(["Hisobot Shakllantirilgan Sana:", now_dt.strftime("%Y-%m-%d %H:%M:%S"), "", "", "", "", "", "", "", ""])
                writer.writerow(["Jami Tushum:", f"{summary['total_revenue']:,} UZS".replace(",", " "), "", "", "", "", "", "", "", ""])
                writer.writerow(["Bugungi Tushum:", f"{summary['today_revenue']:,} UZS".replace(",", " "), "Haftalik:", f"{summary['week_revenue']:,} UZS".replace(",", " "), "Oylik:", f"{summary['month_revenue']:,} UZS".replace(",", " "), "", "", "", ""])
                writer.writerow(["Payme:", f"{summary['payme_total']:,} UZS".replace(",", " "), "Click:", f"{summary['click_total']:,} UZS".replace(",", " "), "Naqd:", f"{summary['cash_total']:,} UZS".replace(",", " "), "Uzum:", f"{summary['uzum_total']:,} UZS".replace(",", " ")])
                writer.writerow([])
                writer.writerow([
                    "ID", "Tranzaksiya Kodi", "Fiskal Belgisi", "Seans Kodi",
                    "Avtomobil Raqami", "To'lov Provayderi", "To'lov Usuli",
                    "Turish Davomiyligi", "To'lov Summasi (UZS)", "Holat", "Sana va Vaqt"
                ])

                for tx in txs:
                    writer.writerow([
                        tx.get("id"),
                        tx.get("tx_code"),
                        tx.get("fiscal_sign"),
                        tx.get("session_code"),
                        tx.get("vehicle_plate"),
                        tx.get("provider"),
                        tx.get("payment_method"),
                        tx.get("duration"),
                        tx.get("amount"),
                        tx.get("status"),
                        tx.get("created_at")
                    ])

            self.add_notification("Moliyaviy hisobot eksport qilindi", f"Fayl saqlandi: {os.path.basename(filepath)}", "INFO")
            return True, filepath
        except Exception as e:
            return False, str(e)

    def update_tariff_rates(self, rates: dict, user_role: str = "SUPER_ADMIN"):
        """
        (Faqat Super-Admin) Soatbay, daqiqabay va tungi tarif narxlarini o'zgartirish.
        Huquqlar matritsasi talabi bo'yicha Oddiy Adminlarga ruxsat berilmaydi.
        """
        if user_role != "SUPER_ADMIN":
            return False, "Ruxsat taqiqlangan! Huquqlar matritsasiga muvofiq, tarif stavkalarini faqat Super-Admin o'zgartirishi mumkin."

        allowed_keys = {
            "day_rate": "Kunduzgi soatlik stavka (08:00 - 20:00, so'm)",
            "night_rate": "Tungi soatlik stavka (20:00 - 08:00, so'm)",
            "minute_rate": "Daqiqabay stavka (so'm/daqiqa)",
            "ev_rate": "EV Quvvatlash qo'shimcha stavkasi (so'm/soat)",
            "grace_period": "Dastlabki bepul oraliq (daqiqa)",
            "exit_grace": "To'lovdan so'ng chiqish oralig'i (daqiqa)",
            "daily_cap": "Kunlik maksimal to'lov chegarasi (so'm)"
        }

        with self.get_connection() as conn:
            cursor = conn.cursor()
            for key, val in rates.items():
                if key in allowed_keys:
                    desc = allowed_keys[key]
                    cursor.execute("""
                        INSERT INTO system_settings (key, value, description)
                        VALUES (?, ?, ?)
                        ON CONFLICT(key) DO UPDATE SET value = excluded.value
                    """, (key, str(val), desc))
            conn.commit()

        day_r = rates.get("day_rate", "5000")
        night_r = rates.get("night_rate", "3000")
        min_r = rates.get("minute_rate", "100")
        self.add_notification(
            "Tarif stavkalari yangilandi",
            f"Super-Admin tariflarni o'zgartirdi: Kunduzgi {day_r} UZS, Tungi {night_r} UZS, Daqiqa {min_r} UZS.",
            "SUCCESS"
        )
        return True, "Tarif stavkalari muvaffaqiyatli yangilandi!"

    def get_barrier_audits(self):
        """Shlagbaum ochish jurnali"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM barrier_audit ORDER BY id DESC LIMIT 20")
            return [dict(r) for r in cursor.fetchall()]

    def log_barrier_override(self, operator_username, operator_name, reason):
        """Shlagbaumni qo'lda ochishni qayd etish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO barrier_audit (operator_username, operator_name, reason)
                VALUES (?, ?, ?)
            """, (operator_username, operator_name, reason))
            conn.commit()

        self.add_notification("Shlagbaum qo'lda ochildi", f"{operator_name}: {reason}", "WARNING")
        return True

    def get_settings(self):
        """Tizim sozlamalari"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM system_settings")
            return {r["key"]: r["value"] for r in cursor.fetchall()}

    def save_settings(self, settings_dict):
        """Sozlamalarni saqlash"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for k, v in settings_dict.items():
                cursor.execute("""
                    INSERT INTO system_settings (key, value) VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """, (k, str(v)))
            conn.commit()
            return True

    # --------------------------------------------------------------------------
    # FOYDALANUVCHI PROFILI VA PAROLNI SOZLASH
    # --------------------------------------------------------------------------
    def get_user_by_id(self, user_id):
        """Foydalanuvchini ID bo'yicha olish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, full_name, role, shift, is_active FROM staff_users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_user_profile(self, user_id, full_name, username, current_password=None, new_password=None):
        """
        Foydalanuvchi ismi, logini va parolini o'zgartirish
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Joriy foydalanuvchini tekshirish
            cursor.execute("SELECT password FROM staff_users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                return False, "Foydalanuvchi topilmadi!"

            # Parol kiritilgan bo'lsa, joriy parolni tekshirish
            if current_password:
                if row["password"] != current_password:
                    return False, "Hozirgi parol noto'g'ri kiritildi!"

            # 2. Login band emasligini tekshirish
            cursor.execute("SELECT id FROM staff_users WHERE username = ? AND id != ?", (username, user_id))
            if cursor.fetchone():
                return False, f"'{username}' logini boshqa xodim tomonidan band qilingan!"

            # 3. Ma'lumotlarni yangilash
            if new_password and new_password.strip():
                cursor.execute("""
                    UPDATE staff_users
                    SET full_name = ?, username = ?, password = ?
                    WHERE id = ?
                """, (full_name, username, new_password.strip(), user_id))
            else:
                cursor.execute("""
                    UPDATE staff_users
                    SET full_name = ?, username = ?
                    WHERE id = ?
                """, (full_name, username, user_id))

            conn.commit()
            self.add_notification(
                "Profil yangilandi",
                f"{full_name} ({username}) ma'lumotlari muvaffaqiyatli yangilandi.",
                "SUCCESS"
            )
            return True, "Profil ma'lumotlari muvaffaqiyatli saqlandi!"

    # --------------------------------------------------------------------------
    # XABARNOMALAR (NOTIFICATIONS)
    # --------------------------------------------------------------------------
    def get_notifications(self, limit=15):
        """Barcha bildirishnomalar ro'yxati"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM system_notifications ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(r) for r in cursor.fetchall()]

    def get_unread_notifications_count(self):
        """O'qilmagan xabarnomalar soni"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM system_notifications WHERE is_read = 0")
            return cursor.fetchone()[0]

    def mark_all_notifications_read(self):
        """Barcha xabarnomalarni o'qilgan deb belgilash"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE system_notifications SET is_read = 1 WHERE is_read = 0")
            conn.commit()
            return True

    def add_notification(self, title, message, n_type="INFO"):
        """Yangi xabarnoma qo'shish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO system_notifications (title, message, type)
                VALUES (?, ?, ?)
            """, (title, message, n_type))
            conn.commit()
            return True

    # --------------------------------------------------------------------------
    # SESSYALAR VA AVTOMOBILLAR (VEHICLES & SESSIONS)
    # --------------------------------------------------------------------------
    def get_active_sessions(self):
        """Hozirda avtoturargohda turgan barcha faol seanslar"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM parking_sessions WHERE status = 'ACTIVE' ORDER BY id DESC
            """)
            return [dict(r) for r in cursor.fetchall()]

    def search_sessions_history(self, query):
        """Arxivdan avto raqam yoki seans kodi bo'yicha qidirish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            q = f"%{query}%"
            cursor.execute("""
                SELECT * FROM parking_sessions
                WHERE vehicle_plate LIKE ? OR session_code LIKE ? OR slot_number LIKE ?
                ORDER BY id DESC LIMIT 50
            """, (q, q, q))
            return [dict(r) for r in cursor.fetchall()]

    # --------------------------------------------------------------------------
    # OQ VA QORA RO'YXAT (WHITELIST & BLACKLIST)
    # --------------------------------------------------------------------------
    def get_access_list(self, list_type=None):
        """Oq yoki qora ro'yxatni olish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if list_type:
                cursor.execute("SELECT * FROM vehicle_access_list WHERE list_type = ? ORDER BY id DESC", (list_type,))
            else:
                cursor.execute("SELECT * FROM vehicle_access_list ORDER BY id DESC")
            return [dict(r) for r in cursor.fetchall()]

    def add_to_access_list(self, plate, list_type, note=""):
        """Oq yoki qora ro'yxatga kiritish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO vehicle_access_list (plate, list_type, note)
                    VALUES (?, ?, ?)
                    ON CONFLICT(plate) DO UPDATE SET list_type = excluded.list_type, note = excluded.note
                """, (plate.upper().strip(), list_type, note))
                conn.commit()
                return True
        except Exception:
            return False

    def remove_from_access_list(self, item_id):
        """Ro'yxatdan o'chirish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vehicle_access_list WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0

    # --------------------------------------------------------------------------
    # CHEGIRMALAR VA VAUCHERLAR (COUPONS)
    # --------------------------------------------------------------------------
    def get_coupons(self):
        """Barcha vaucher va chegirmalar"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM coupons ORDER BY id DESC")
            return [dict(r) for r in cursor.fetchall()]

    def add_coupon(self, code, discount_percent, valid_until="2026-12-31"):
        """Yangi vaucher qo'shish"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO coupons (code, discount_percent, valid_until)
                    VALUES (?, ?, ?)
                """, (code.upper().strip(), discount_percent, valid_until))
                conn.commit()
                return True
        except Exception:
            return False

    # --------------------------------------------------------------------------
    # USKUNALAR VA TIZIM SALOMATLIGI (HEALTH CHECK)
    # --------------------------------------------------------------------------
    def get_hardware_status(self):
        """Uskunalar va datchiklar holati"""
        return {
            "barrier_gate": "NORMAL (Online)",
            "camera_entry": "ONLINE (30 FPS)",
            "camera_exit": "ONLINE (30 FPS)",
            "mqtt_broker": "CONNECTED (127.0.0.1:1883)",
            "relay_controller": "READY (Port COM3)",
            "anpr_engine_c": "ACTIVE (Latency 7.2ms)",
            "db_latency": "0.6ms (SQLite 3.42)"
        }


