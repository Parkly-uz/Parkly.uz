"""
Parkly.uz — Fully Automated Gate & Cashless Payment Access Control State Machine
Operator talab etilmaydigan, to'liq avtomatlashtirilgan kirish/chiqish shlagbaum va naqd pulsiz (Cashless / Auto-Payment) to'lov mantiqi.
"""

import sys
import os

_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional
from app.algorithms.spot_allocator import SpotAllocator
from app.algorithms.tariff_calculator import TariffCalculator


class GateAction(str, Enum):
    OPEN_BARRIER = "OPEN_BARRIER"               # Shlagbaumni ochish signali
    DENY_ACCESS = "DENY_ACCESS"                 # Kirishni taqiqlash (joy yo'q)
    REQUIRE_AUTO_PAYMENT = "REQUIRE_AUTO_PAYMENT" # Chiqishda avto-to'lov talab qilish (Cashless)
    EMERGENCY_FAIL_SAFE = "EMERGENCY_FAIL_SAFE"   # SLA buzilganda favqulodda ochish


class GateController:
    """
    To'liq avtomatlashgan shlagbaum va avto-to'lov boshqaruvchisi.
    """

    MAX_ALLOWED_WAIT_MINUTES = 10.0  # Qat'iy SLA: Maksimal kutish 10 daqiqa

    @classmethod
    def process_entry(
        cls,
        plate_number: str,
        vehicle_type: str,
        available_slots: list,
        active_reservation: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Kirish to'sig'idagi to'liq avtomatlashgan qaror.
        """
        # 1. Bron qilingan joy mavjudligi
        if active_reservation:
            target_slot = active_reservation.get("slot_number")
            return {
                "action": GateAction.OPEN_BARRIER,
                "message": f"Xush kelibsiz! Bron qilingan joyingiz: {target_slot}",
                "assigned_slot": target_slot,
                "is_reserved": True
            }

        # 2. Optimal bo'sh joyni avtomatik topish
        allocated_slot = SpotAllocator.allocate_best_spot(
            available_slots=available_slots,
            vehicle_type=vehicle_type
        )

        if not allocated_slot:
            return {
                "action": GateAction.DENY_ACCESS,
                "message": "Kechirasiz, avtoturargoh to'lgan! Bo'sh joy mavjud emas.",
                "assigned_slot": None,
                "is_reserved": False
            }

        return {
            "action": GateAction.OPEN_BARRIER,
            "message": f"Xush kelibsiz! Ajratilgan joy: {allocated_slot['slot_number']}",
            "assigned_slot": allocated_slot['slot_number'],
            "is_reserved": False
        }

    @classmethod
    def process_exit(
        cls,
        plate_number: str,
        session: Dict[str, Any],
        payment_status: str,
        exit_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Chiqish to'sig'idagi to'liq avtomatlashgan naqd pulsiz (Cashless) to'lov va shlagbaum ochish mantiqi.
        Operator talab etilmaydi — avtomatik tarzda to'lov holati tekshiriladi.
        """
        ex_time = exit_time or datetime.now()
        entry_time = session.get("entry_time")
        is_ev = session.get("is_ev_charging", False)

        # 1. Hisob-kitob qilish
        fee_result = TariffCalculator.calculate_fee(
            entry_time=entry_time,
            exit_time=ex_time,
            is_ev_charging=is_ev
        )

        final_amount = fee_result["final_amount"]

        # 2. Agar bepul oraliqda (Grace period) bo'lsa yoki to'lov allaqachon muvaffaqiyatli qilingan bo'lsa
        if fee_result["is_grace_period"] or payment_status == "SUCCESS":
            return {
                "action": GateAction.OPEN_BARRIER,
                "message": "To'lov tasdiqlandi. Oq yo'l!",
                "amount_due": 0,
                "fee_details": fee_result,
                "is_paid": True
            }

        # 3. Agar to'lov qilinmagan bo'lsa -> Avtomatik to'lov talab qilish (Mobile app, QR yoki Card terminal)
        if final_amount > 0 and payment_status != "SUCCESS":
            return {
                "action": GateAction.REQUIRE_AUTO_PAYMENT,
                "message": f"Iltimos, avto-to'lovni amalga oshiring: {final_amount:,.0f} so'm",
                "amount_due": final_amount,
                "fee_details": fee_result,
                "is_paid": False
            }

        return {
            "action": GateAction.OPEN_BARRIER,
            "message": "Oq yo'l!",
            "amount_due": 0,
            "fee_details": fee_result,
            "is_paid": True
        }

    @classmethod
    def evaluate_wait_time_sla(cls, wait_minutes: float) -> Dict[str, Any]:
        """
        10-daqiqalik qat'iy SLA Watchdog nazoratchisi:
        - < 5 min: Normal
        - 5 - 7 min: Sariq ogohlantirish
        - 7 - 10 min: Qizil eskalatsiya
        - >= 10 min: Fail-safe avtomatik shlagbaum ochish (Emergency open)
        """
        if wait_minutes < 5.0:
            return {
                "level": "NORMAL",
                "color": "#10b981",
                "action": "CONTINUE",
                "force_open": False
            }
        elif wait_minutes < 7.0:
            return {
                "level": "WARNING",
                "color": "#f59e0b",
                "action": "NOTIFY_SYSTEM",
                "force_open": False
            }
        elif wait_minutes < cls.MAX_ALLOWED_WAIT_MINUTES:
            return {
                "level": "CRITICAL",
                "color": "#ef4444",
                "action": "ALERT_SUPER_ADMIN",
                "force_open": False
            }
        else:
            return {
                "level": "FAIL_SAFE",
                "color": "#dc2626",
                "action": GateAction.EMERGENCY_FAIL_SAFE,
                "message": "SLA BUZILDI! 10 daqiqadan oshdi — shlagbaum avtomatik ochilmoqda!",
                "force_open": True
            }
