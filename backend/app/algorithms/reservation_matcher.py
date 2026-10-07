"""
Parkly.uz — Reservation Conflict & Overlap Detection Algorithm
Ushbu algoritm bitta slotga vaqt kesishuvlarisiz (to'qnashuvsiz) bron qilishni ta'minlaydi.
"""

from datetime import datetime
from typing import List, Dict, Optional, Tuple


class ReservationMatcher:
    """
    Joyni bron qilishda vaqt oraliqlarini tahlil qiluvchi algoritm.
    
    To'qnashuv sharti:
    Ikki oraliq [A_start, A_end] va [B_start, B_end] kesishadi, agar:
    max(A_start, B_start) < min(A_end, B_end)
    """

    @staticmethod
    def is_overlap(
        start_a: datetime,
        end_a: datetime,
        start_b: datetime,
        end_b: datetime
    ) -> bool:
        """Ikkita vaqt oralig'i o'zaro kesishishini tekshirish"""
        return max(start_a, start_b) < min(end_a, end_b)

    @classmethod
    def check_availability(
        cls,
        slot_number: str,
        requested_start: datetime,
        requested_end: datetime,
        existing_reservations: List[Dict]
    ) -> Tuple[bool, Optional[Dict]]:
        """
        Slot ko'rsatilgan vaqt oralig'ida bo'shmi yoki yo'qmi tekshiradi.
        
        :return: (is_available, conflicting_reservation)
        """
        if requested_end <= requested_start:
            raise ValueError("Tugash vaqti boshlanish vaqtidan keyin bo'lishi shart!")

        for res in existing_reservations:
            # Faqat faol va bekor qilinmagan bronlarni tekshiramiz
            if res.get("status") in ["CANCELLED", "EXPIRED"]:
                continue

            res_start = res["start_time"]
            res_end = res["end_time"]

            if cls.is_overlap(requested_start, requested_end, res_start, res_end):
                return False, res

        return True, None

    @classmethod
    def find_first_available_slot(
        cls,
        all_slots: List[Dict],
        reservations_by_slot: Dict[str, List[Dict]],
        requested_start: datetime,
        requested_end: datetime,
        slot_type: str = "REGULAR"
    ) -> Optional[str]:
        """
        Agar tanlangan slot band bo'lsa, xuddi shu turdagi birinchi bo'sh slotni topib beradi.
        """
        for slot in all_slots:
            if slot.get("slot_type") != slot_type:
                continue

            slot_num = slot.get("slot_number")
            existing = reservations_by_slot.get(slot_num, [])

            is_free, _ = cls.check_availability(slot_num, requested_start, requested_end, existing)
            if is_free:
                return slot_num

        return None
