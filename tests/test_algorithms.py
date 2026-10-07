"""
Parkly.uz — Algoritmlar uchun Unit Testlar
Ushbu testlar barcha 4 ta parkovka algoritmlarining to'g'riligini tekshiradi.
"""

import sys
import os
from datetime import datetime, timedelta

# Windows konsolida UTF-8 xavfsiz chiqarish
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Import yo'lini qo'shamiz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.algorithms.spot_allocator import SpotAllocator
from app.algorithms.tariff_calculator import TariffCalculator
from app.algorithms.reservation_matcher import ReservationMatcher
from app.algorithms.gate_controller import GateController, GateAction


def test_spot_allocator():
    print("▶️ [TEST 1] Spot Allocator tekshirilmoqda...")
    slots = [
        {"slot_number": "A-101", "floor": 1, "pos_x": 100, "pos_y": 100, "slot_type": "REGULAR", "status": "FREE"},
        {"slot_number": "A-102", "floor": 1, "pos_x": 500, "pos_y": 500, "slot_type": "REGULAR", "status": "FREE"},
        {"slot_number": "EV-01", "floor": 1, "pos_x": 150, "pos_y": 150, "slot_type": "EV_CHARGING", "status": "FREE"},
        {"slot_number": "VIP-01", "floor": 1, "pos_x": 50, "pos_y": 50, "slot_type": "VIP_STAFF", "status": "FREE"},
    ]

    # 1. Standart avtomobil eng yaqin REGULAR joyni olishi kerak (A-101)
    best_regular = SpotAllocator.allocate_best_spot(slots, entry_gate_pos=(0, 0), vehicle_type="REGULAR")
    assert best_regular["slot_number"] == "A-101", f"Kutilgan: A-101, Olindi: {best_regular['slot_number']}"

    # 2. Elektromobil EV joyni olishi kerak (EV-01)
    best_ev = SpotAllocator.allocate_best_spot(slots, entry_gate_pos=(0, 0), vehicle_type="EV_CHARGING")
    assert best_ev["slot_number"] == "EV-01", f"Kutilgan: EV-01, Olindi: {best_ev['slot_number']}"

    print("   ✅ Spot Allocator muvaffaqiyatli o'tdi!")


def test_tariff_calculator():
    print("▶️ [TEST 2] Tariff Calculator tekshirilmoqda...")
    now = datetime(2026, 10, 7, 10, 0, 0)  # 10:00 (Kunduzgi)

    # 1. 10 daqiqa (Grace period) -> 0 so'm
    res_grace = TariffCalculator.calculate_fee(now, now + timedelta(minutes=10))
    assert res_grace["final_amount"] == 0
    assert res_grace["is_grace_period"] is True

    # 2. 25 daqiqa -> 1 soatlik narx (5,000 so'm)
    res_1h = TariffCalculator.calculate_fee(now, now + timedelta(minutes=25))
    assert res_1h["final_amount"] == 5000
    assert res_1h["billable_hours"] == 1

    # 3. 2 soat 5 daqiqa -> 3 soatlik narx (15,000 so'm)
    res_3h = TariffCalculator.calculate_fee(now, now + timedelta(hours=2, minutes=5))
    assert res_3h["final_amount"] == 15000

    print("   ✅ Tariff Calculator muvaffaqiyatli o'tdi!")


def test_reservation_matcher():
    print("▶️ [TEST 3] Reservation Matcher tekshirilmoqda...")
    base_time = datetime(2026, 10, 7, 12, 0, 0)
    existing_res = [
        {"start_time": base_time, "end_time": base_time + timedelta(hours=2), "status": "CONFIRMED"}  # 12:00 - 14:00
    ]

    # 1. 13:00 - 15:00 so'ralsa -> Kesishadi (False)
    available, conflict = ReservationMatcher.check_availability(
        "A-101",
        base_time + timedelta(hours=1),
        base_time + timedelta(hours=3),
        existing_res
    )
    assert available is False
    assert conflict is not None

    # 2. 14:30 - 16:00 so'ralsa -> Bo'sh (True)
    available_ok, _ = ReservationMatcher.check_availability(
        "A-101",
        base_time + timedelta(hours=2, minutes=30),
        base_time + timedelta(hours=4),
        existing_res
    )
    assert available_ok is True

    print("   ✅ Reservation Matcher muvaffaqiyatli o'tdi!")


def test_gate_controller():
    print("▶️ [TEST 4] Gate Controller tekshirilmoqda...")
    now = datetime(2026, 10, 7, 14, 0, 0)

    # 1. Grace periodda chiqish
    session_grace = {"entry_time": now - timedelta(minutes=12), "payment_status": "UNPAID"}
    exit_grace = GateController.process_exit(session_grace, current_time=now)
    assert exit_grace["action"] == GateAction.OPEN_BARRIER

    # 2. To'lanmagan chiqish (1 soat o'tgan)
    session_unpaid = {"entry_time": now - timedelta(hours=1), "payment_status": "UNPAID"}
    exit_unpaid = GateController.process_exit(session_unpaid, current_time=now)
    assert exit_unpaid["action"] == GateAction.REQUIRE_PAYMENT
    assert exit_unpaid["amount_due"] > 0

    print("   ✅ Gate Controller muvaffaqiyatli o'tdi!")


if __name__ == "__main__":
    print("\n🚀 PARKLY.UZ ALGORITMLARINI TEKSHIRISH TESTLARI BOSHLANDI:\n")
    test_spot_allocator()
    test_tariff_calculator()
    test_reservation_matcher()
    test_gate_controller()
    print("\n🎉 BARCHA ALGORITMLAR 100% XATOSIZ VA MUVAFFAQIYATLI ISHLADI!\n")
