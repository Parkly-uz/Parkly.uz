"""
Parkly.uz — Gate & Barrier Access Control State Machine
Kirish va chiqish shlagbaumini xavfsiz boshqarish algoritmi.
"""

from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional
from app.algorithms.spot_allocator import SpotAllocator
from app.algorithms.tariff_calculator import TariffCalculator


class GateAction(str, Enum):
    OPEN_BARRIER = "OPEN_BARRIER"       # Shlagbaumni ochish signali
    DENY_ACCESS = "DENY_ACCESS"         # Kirishni taqiqlash (joy yo'q / bloklangan)
    REQUIRE_PAYMENT = "REQUIRE_PAYMENT" # Chiqishda to'lov talab qilish


class GateController:
    """
    Shlagbaum va to'siqlar mantiqiy nazoratchisi.
    """

    @classmethod
    def process_entry(
        cls,
        plate_number: str,
        vehicle_type: str,
        available_slots: list,
        active_reservation: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Kirish to'sig'idagi mantiqiy qaror.
        """
        # 1. Agar avtomobil oldindan joy bron qilgan bo'lsa
        if active_reservation:
            target_slot = active_reservation.get("slot_number")
            return {
                "action": GateAction.OPEN_BARRIER,
                "message": f"Xush kelibsiz! Sizning bron qilingan joyingiz: {target_slot}",
                "assigned_slot": target_slot,
                "is_reserved": True
            }

        # 2. Optimal bo'sh joyni topish
        allocated_slot = SpotAllocator.allocate_best_spot(
            available_slots=available_slots,
            vehicle_type=vehicle_type
        )

        if not allocated_slot:
            return {
                "action": GateAction.DENY_ACCESS,
                "message": "Kechirasiz, parkovkada bo'sh joy qolmagan!",
                "assigned_slot": None,
                "is_reserved": False
            }

        return {
            "action": GateAction.OPEN_BARRIER,
            "message": f"Xush kelibsiz! Sizga ajratilgan joy: {allocated_slot['slot_number']}",
            "assigned_slot": allocated_slot['slot_number'],
            "is_reserved": False
        }

    @classmethod
    def process_exit(
        cls,
        session_info: Dict[str, Any],
        current_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Chiqish to'sig'idagi mantiqiy qaror.
        """
        if not session_info:
            return {
                "action": GateAction.DENY_ACCESS,
                "message": "Faol parkovka sessiyasi topilmadi! Operatorga murojaat qiling."
            }

        now = current_time or datetime.utcnow()
        entry_time = session_info["entry_time"]
        payment_status = session_info.get("payment_status", "UNPAID")
        paid_at = session_info.get("paid_at")

        # 1. Narxni hisoblash
        fee_calc = TariffCalculator.calculate_fee(entry_time, now)

        # 2. Dastlabki 15 daqiqalik bepul oraliqda bo'lsa
        if fee_calc["is_grace_period"]:
            return {
                "action": GateAction.OPEN_BARRIER,
                "message": "15 daqiqalik bepul oraliq. Oq yo'l!",
                "amount_due": 0
            }

        # 3. Agar to'lov to'langan bo'lsa
        if payment_status == "PAID" and paid_at:
            exit_diff_minutes = (now - paid_at).total_seconds() / 60.0
            if exit_diff_minutes <= TariffCalculator.EXIT_GRACE_MINUTES:
                return {
                    "action": GateAction.OPEN_BARRIER,
                    "message": "To'lov tasdiqlangan. Oq yo'l!",
                    "amount_due": 0
                }
            else:
                # To'lovdan keyin 15 daqiqadan ko'p qolib ketgan (Overstay)
                extra_fee = TariffCalculator.calculate_fee(paid_at, now)["final_amount"]
                return {
                    "action": GateAction.REQUIRE_PAYMENT,
                    "message": "To'lovdan keyingi chiqish vaqti (15 min) o'tib ketdi. Qo'shimcha to'lov qiling.",
                    "amount_due": extra_fee
                }

        # 4. To'lov qilinmagan bo'lsa
        return {
            "action": GateAction.REQUIRE_PAYMENT,
            "message": f"To'lov kutilmoqda: {fee_calc['final_amount']} so'm.",
            "amount_due": fee_calc["final_amount"],
            "total_minutes": fee_calc["total_minutes"]
        }
