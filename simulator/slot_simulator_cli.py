"""
Parkly.uz — Virtual Parking Slot & Traffic CLI Simulator
Ushbu skript C/C++ va Python asosidagi sensorlar oqimini konsolda simulyatsiya qiladi.
"""

import time
import random
import sys
from datetime import datetime

# Slotlar ro'yxati (Aniq raqamlar bo'yicha)
SLOTS = [
    {"slot": "A-101", "type": "REGULAR", "status": "FREE", "plate": None},
    {"slot": "A-102", "type": "REGULAR", "status": "FREE", "plate": None},
    {"slot": "A-103", "type": "REGULAR", "status": "FREE", "plate": None},
    {"slot": "A-104", "type": "REGULAR", "status": "FREE", "plate": None},
    {"slot": "A-105", "type": "REGULAR", "status": "FREE", "plate": None},
    {"slot": "EV-01", "type": "EV_CHARGING", "status": "FREE", "plate": None},
    {"slot": "EV-02", "type": "EV_CHARGING", "status": "FREE", "plate": None},
    {"slot": "VIP-01", "type": "VIP_STAFF", "status": "FREE", "plate": None},
    {"slot": "VIP-02", "type": "VIP_STAFF", "status": "FREE", "plate": None},
]

REGIONS = ["01", "10", "30", "40", "50", "60", "70", "80", "85", "90"]
LETTERS = "ABDEFGHJKLMNOPRSTUVXYZ"

def generate_uz_plate():
    """O'zbekiston davlat raqamini generatsiya qilish (01 A 777 AA yoki 01 123 AAA)"""
    region = random.choice(REGIONS)
    is_business = random.choice([True, False])
    if is_business:
        num = random.randint(100, 999)
        l1 = random.choice(LETTERS)
        l2 = random.choice(LETTERS)
        l3 = random.choice(LETTERS)
        return f"{region} {num} {l1}{l2}{l3}"
    else:
        l1 = random.choice(LETTERS)
        num = random.randint(100, 999)
        l2 = random.choice(LETTERS)
        l3 = random.choice(LETTERS)
        return f"{region} {l1} {num} {l2}{l3}"

def render_dashboard():
    """Konsolda jonli holat jadvalini ko'rsatish"""
    print("\033[H\033[J", end="")  # Ekranni tozalash
    print("=" * 68)
    print(" 🚗 PARKLY.UZ — VIRTUAL SENSOR VA SLOT SIMULYATORI (CLI ENGINE)")
    print(f" Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Hudud: Tashkent Central (Lot #1)")
    print("=" * 68)
    print(f"{'SLOT':<10} | {'TURI':<14} | {'HOLATI':<16} | {'TRANSPORT RAQAMI':<18}")
    print("-" * 68)

    color_map = {
        "FREE": "\033[92m[BO'SH]\033[0m",
        "OCCUPIED": "\033[91m[BAND]\033[0m",
        "RESERVED": "\033[93m[BRON]\033[0m",
        "PAYMENT_PENDING": "\033[33m[TO'LOV]\033[0m",
        "MAINTENANCE": "\033[90m[TA'MIR]\033[0m"
    }

    for item in SLOTS:
        status_colored = color_map.get(item["status"], item["status"])
        plate_str = item["plate"] if item["plate"] else "---"
        print(f"{item['slot']:<10} | {item['type']:<14} | {status_colored:<25} | {plate_str:<18}")

    print("=" * 68)
    print("💡 To'xtatish uchun: Ctrl + C bosing")

def run_simulation(interval=2.0):
    print("Simulyator ishga tushmoqda...")
    try:
        while True:
            # Tasodifiy bitta slotni tanlash
            target = random.choice(SLOTS)

            if target["status"] == "FREE":
                # Mashina kelib to'xtadi
                target["status"] = "OCCUPIED"
                target["plate"] = generate_uz_plate()
            elif target["status"] == "OCCUPIED":
                # Mashina chiqish oldi to'lov holatiga o'tdi yoki chiqib ketdi
                coin = random.random()
                if coin < 0.4:
                    target["status"] = "PAYMENT_PENDING"
                else:
                    target["status"] = "FREE"
                    target["plate"] = None
            elif target["status"] == "PAYMENT_PENDING":
                # To'lov to'landi va chiqib ketdi
                target["status"] = "FREE"
                target["plate"] = None
            elif target["status"] == "RESERVED":
                # Bron qilingan mashina keldi
                target["status"] = "OCCUPIED"
                target["plate"] = generate_uz_plate()

            render_dashboard()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n⏹️ Simulyator muvaffaqiyatli to'xtatildi.")

if __name__ == "__main__":
    interval_sec = 2.0
    if len(sys.argv) > 1:
        try:
            interval_sec = float(sys.argv[1])
        except ValueError:
            pass
    run_simulation(interval_sec)
