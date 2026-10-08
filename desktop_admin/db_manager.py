"""
Parkly.uz — Desktop Admin Real Database Engine (SQLite & PostgreSQL sync)
Barcha ma'lumotlar haqiqiy lokal DB faylida (parkly_local.db) saqlanadi va dinamik boshqariladi.
"""

import sqlite3
import os
import random
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
                last_status_change TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 3. Parkovka seanslari
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS parking_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_code TEXT UNIQUE NOT NULL,
                vehicle_plate TEXT NOT NULL,
                slot_number TEXT NOT NULL,
                entry_time TEXT NOT NULL,
                exit_time TEXT,
                total_amount INTEGER DEFAULT 0,
                payment_provider TEXT,
                status TEXT DEFAULT 'ACTIVE' -- ACTIVE, COMPLETED, CANCELLED
            )
            """)

            # 4. Tranzaksiyalar jadvali
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tx_code TEXT UNIQUE NOT NULL,
                session_code TEXT NOT NULL,
                vehicle_plate TEXT NOT NULL,
                provider TEXT NOT NULL, -- Payme, Click, Naqd
                amount INTEGER NOT NULL,
                status TEXT DEFAULT 'SUCCESS',
                fiscal_sign TEXT,
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

            conn.commit()

            # Boshlang'ich ma'lumotlarni tekshirish va to'ldirish
            self._seed_default_data(cursor)
            conn.commit()

    def _seed_default_data(self, cursor):
        # 1. Xodimlar mavjudligini tekshirish
        cursor.execute("SELECT COUNT(*) FROM staff_users")
        if cursor.fetchone()[0] == 0:
            default_staff = [
                ("admin", "admin123", "Erjigit (Bosh Rahbar)", "SUPER_ADMIN", "Barcha hudud"),
                ("manager", "manager123", "Sherzod Aliyev", "ADMIN", "Filial 1"),
                ("admin_chilonzor", "admin123", "Jahongir Qodirov", "ADMIN", "Filial 2"),
                ("operator1", "operator123", "Aziz Rustamov", "OPERATOR", "Smena 1 (08:00 - 16:00)"),
                ("operator2", "operator123", "Bobur Mirzayev", "OPERATOR", "Smena 2 (16:00 - 00:00)"),
                ("operator3", "operator123", "Dilshod Karimov", "OPERATOR", "Smena 3 (00:00 - 08:00)"),
                ("operator4", "operator123", "Farrux Yusupov", "OPERATOR", "Zaxira 1"),
                ("operator5", "operator123", "G'ayrat Xoliqov", "OPERATOR", "Zaxira 2"),
            ]
            cursor.executemany("""
                INSERT INTO staff_users (username, password, full_name, role, shift)
                VALUES (?, ?, ?, ?, ?)
            """, default_staff)

        # 2. Slotlar mavjudligini tekshirish
        cursor.execute("SELECT COUNT(*) FROM parking_slots")
        if cursor.fetchone()[0] == 0:
            slots = [
                # 1-Qavat: A-Zona (Standart)
                (1, "A", "A-101", "REGULAR", "FREE", 50, 50, 80, 140, None),
                (1, "A", "A-102", "REGULAR", "OCCUPIED", 150, 50, 80, 140, "01 A 777 AA"),
                (1, "A", "A-103", "REGULAR", "FREE", 250, 50, 80, 140, None),
                (1, "A", "A-104", "REGULAR", "RESERVED", 350, 50, 80, 140, None),
                (1, "A", "A-105", "REGULAR", "PAYMENT_PENDING", 450, 50, 80, 140, "10 123 BBA"),
                (1, "A", "A-106", "REGULAR", "MAINTENANCE", 550, 50, 80, 140, None),

                # 1-Qavat: EV-Zona (Elektromobillar)
                (1, "EV", "EV-01", "EV_CHARGING", "FREE", 50, 240, 80, 140, None),
                (1, "EV", "EV-02", "EV_CHARGING", "OCCUPIED", 150, 240, 80, 140, "01 888 ZZZ"),
                (1, "EV", "EV-03", "EV_CHARGING", "FREE", 250, 240, 80, 140, None),

                # 1-Qavat: VIP-Zona
                (1, "VIP", "VIP-01", "VIP_STAFF", "FREE", 350, 240, 80, 140, None),
                (1, "VIP", "VIP-02", "VIP_STAFF", "OCCUPIED", 450, 240, 80, 140, "01 001 PPP"),
                (1, "VIP", "VIP-03", "VIP_STAFF", "RESERVED", 550, 240, 80, 140, None),

                # 2-Qavat Slotlari
                (2, "B", "B-201", "REGULAR", "FREE", 50, 50, 80, 140, None),
                (2, "B", "B-202", "REGULAR", "FREE", 150, 50, 80, 140, None),
                (2, "B", "B-203", "REGULAR", "OCCUPIED", 250, 50, 80, 140, "01 B 999 BB"),
                (2, "B", "B-204", "REGULAR", "FREE", 350, 50, 80, 140, None),
                (2, "B", "B-205", "REGULAR", "FREE", 450, 50, 80, 140, None),
                (2, "B", "B-206", "REGULAR", "FREE", 550, 50, 80, 140, None),
                (2, "EV", "EV-21", "EV_CHARGING", "FREE", 50, 240, 80, 140, None),
                (2, "EV", "EV-22", "EV_CHARGING", "FREE", 150, 240, 80, 140, None),
            ]
            cursor.executemany("""
                INSERT INTO parking_slots (floor, zone, slot_number, slot_type, status, pos_x, pos_y, width, height, current_vehicle_plate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, slots)

        # 3. Dastlabki Tranzaksiyalar va Seanslar
        cursor.execute("SELECT COUNT(*) FROM transactions")
        if cursor.fetchone()[0] == 0:
            now = datetime.now()
            txs = [
                ("TX-9901", "SES-1049", "01 A 777 AA", "Payme", 15000, "FISC-88214", (now - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9902", "SES-1048", "10 123 BBA", "Click", 10000, "FISC-88213", (now - timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9903", "SES-1047", "01 888 ZZZ", "Payme", 35000, "FISC-88212", (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9904", "SES-1045", "30 456 VVA", "Naqd", 20000, "FISC-88211", (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")),
                ("TX-9905", "SES-1044", "01 111 AAA", "Payme", 50000, "FISC-88210", (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")),
            ]
            cursor.executemany("""
                INSERT INTO transactions (tx_code, session_code, vehicle_plate, provider, amount, fiscal_sign, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, txs)

            # Seanslar
            sessions = [
                ("SES-1049", "01 A 777 AA", "A-102", (now - timedelta(hours=1)).strftime("%H:%M:%S"), None, 15000, "Payme", "ACTIVE"),
                ("SES-1048", "10 123 BBA", "A-105", (now - timedelta(minutes=45)).strftime("%H:%M:%S"), None, 10000, "Click", "ACTIVE"),
                ("SES-1047", "01 888 ZZZ", "EV-02", (now - timedelta(hours=2)).strftime("%H:%M:%S"), None, 35000, "Payme", "ACTIVE"),
                ("SES-1046", "01 001 PPP", "VIP-02", (now - timedelta(hours=3)).strftime("%H:%M:%S"), None, 0, "VIP", "ACTIVE"),
            ]
            cursor.executemany("""
                INSERT INTO parking_sessions (session_code, vehicle_plate, slot_number, entry_time, exit_time, total_amount, payment_provider, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, sessions)

        # 4. Tizim sozlamalari
        cursor.execute("SELECT COUNT(*) FROM system_settings")
        if cursor.fetchone()[0] == 0:
            settings = [
                ("day_rate", "5000", "Kunduzgi soatlik stavka (08:00 - 20:00)"),
                ("night_rate", "3000", "Tungi soatlik stavka (20:00 - 08:00)"),
                ("grace_period", "15", "Dastlabki bepul oraliq (daqiqa)"),
                ("exit_grace", "15", "To'lovdan so'ng chiqish oralig'i (daqiqa)"),
                ("daily_cap", "50000", "Kunlik maksimal to'lov chegarasi (so'm)"),
                ("barrier_auto_open", "1", "Shlagbaum avtomatik ochilishi (1=ha, 0=yo'q)"),
            ]
            cursor.executemany("""
                INSERT INTO system_settings (key, value, description)
                VALUES (?, ?, ?)
            """, settings)

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

    def update_slot_status(self, slot_number, new_status, plate=None):
        """Slot holatini bazada yangilash"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE parking_slots
                SET status = ?, current_vehicle_plate = ?, last_status_change = CURRENT_TIMESTAMP
                WHERE slot_number = ?
            """, (new_status, plate, slot_number))
            conn.commit()
            return cursor.rowcount > 0

    def simulate_car_entry(self, plate=None):
        """
        Dinamik avto kirishi: Birinchi bo'sh slotni topib band qiladi va yangi seans ochadi.
        """
        if not plate:
            num = random.randint(100, 999)
            plate = f"01 A {num} AA"

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
                SET status = 'OCCUPIED', current_vehicle_plate = ?, last_status_change = CURRENT_TIMESTAMP
                WHERE slot_number = ?
            """, (plate, assigned_slot))

            # Seans yozish
            cursor.execute("""
                INSERT INTO parking_sessions (session_code, vehicle_plate, slot_number, entry_time, status)
                VALUES (?, ?, ?, ?, 'ACTIVE')
            """, (ses_code, plate, assigned_slot, now_str))

            conn.commit()

        self.add_notification("Yangi avto kirdi", f"{plate} ({assigned_slot} slotiga biriktirildi)", "INFO")
        return {"slot": assigned_slot, "plate": plate, "time": now_str, "session": ses_code}

    def simulate_car_exit(self, slot_number):
        """Avto chiqishi va to'lovni yozish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_vehicle_plate FROM parking_slots WHERE slot_number = ?", (slot_number,))
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
                SET status = 'FREE', current_vehicle_plate = NULL, last_status_change = CURRENT_TIMESTAMP
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
                return True
        except sqlite3.IntegrityError:
            return False

    def get_financial_summary(self):
        """Moliya va kassa hisoboti"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT SUM(amount) FROM transactions WHERE provider = 'Payme'")
            payme = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(amount) FROM transactions WHERE provider = 'Click'")
            click = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(amount) FROM transactions WHERE provider = 'Naqd'")
            cash = cursor.fetchone()[0] or 0

            cursor.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 20")
            txs = [dict(r) for r in cursor.fetchall()]

            return {
                "payme_total": payme,
                "click_total": click,
                "cash_total": cash,
                "transactions": txs
            }

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

