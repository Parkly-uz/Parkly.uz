"""
Parkly.uz — Optimal Parking Spot Allocation Algorithm
Ushbu algoritm kirib kelgan avtomobilga eng yaqin, turiga mos va qulay bo'sh joyni ajratadi.
"""

import math
from typing import List, Dict, Optional, Tuple


class SpotAllocator:
    """
    Parkovkaga kirgan avtomobil uchun eng maqbul bo'sh joyni aniqlash algoritmi.
    
    Qoidalar:
    1. Tip mosligi:
       - Elektromobil -> EV_CHARGING birinchi o'rinda (agar bo'lmasa REGULAR)
       - Standart avto -> REGULAR (EV yoki VIP ga ruxsatsiz qo'yilmaydi)
       - VIP avto -> VIP_STAFF
    2. Masofa va Qavat evristikasi (Cost Function):
       - Masofa: D = sqrt((slot.x - gate.x)^2 + (slot.y - gate.y)^2)
       - Qavat jarimasi: har bir yuqori/pastki qavat uchun +200 ball
       - Eng kichik xarajat (Cost) ga ega bo'lgan joy birinchi tanlanadi.
    """

    FLOOR_PENALTY_WEIGHT = 200.0  # Qavat o'zgarishi uchun qo'shimcha og'irlik

    @staticmethod
    def calculate_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """Evklid masofasini hisoblash"""
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    @classmethod
    def allocate_best_spot(
        cls,
        available_slots: List[Dict],
        entry_gate_pos: Tuple[int, int] = (0, 0),
        entry_floor: int = 1,
        vehicle_type: str = "REGULAR",
        is_vip: bool = False
    ) -> Optional[Dict]:
        """
        Bo'sh slotlar ro'yxatidan eng optimalini tanlaydi.
        
        :param available_slots: status='FREE' bo'lgan slotlar ro'yxati
        :param entry_gate_pos: Kirish shlagbaumi koordinatasi (x, y)
        :param entry_floor: Kirish eshigi joylashgan qavat
        :param vehicle_type: 'REGULAR', 'EV_CHARGING'
        :param is_vip: Foydalanuvchi VIP maqomiga egami
        :return: Eng optimal slot yoki None (agar joy qolmagan bo'lsa)
        """
        if not available_slots:
            return None

        candidates = []

        for slot in available_slots:
            # 1. Faqat bo'sh joylarni ko'rib chiqamiz
            if slot.get("status") != "FREE":
                continue

            slot_type = slot.get("slot_type", "REGULAR")

            # 2. Tip bo'yicha filtrlash
            if is_vip:
                # VIP foydalanuvchiga VIP yoki REGULAR berilishi mumkin
                pass
            elif vehicle_type == "EV_CHARGING":
                if slot_type not in ["EV_CHARGING", "REGULAR"]:
                    continue
            else:
                # Standart avtomobillarga VIP yoki EV joylar berilmaydi
                if slot_type in ["VIP_STAFF", "EV_CHARGING"]:
                    continue

            # 3. Masofa va xarajatni (Cost) hisoblash
            slot_pos = (slot.get("pos_x", 0), slot.get("pos_y", 0))
            distance = cls.calculate_distance(entry_gate_pos, slot_pos)
            
            floor_diff = abs(slot.get("floor", 1) - entry_floor)
            floor_cost = floor_diff * cls.FLOOR_PENALTY_WEIGHT

            # EV mashina uchun EV joyga bonus (chegirma)
            type_bonus = 0.0
            if vehicle_type == "EV_CHARGING" and slot_type == "EV_CHARGING":
                type_bonus = -150.0  # EV joy ustuvor tanlanishi uchun

            total_cost = distance + floor_cost + type_bonus
            candidates.append((total_cost, slot))

        if not candidates:
            return None

        # Eng kichik xarajatli (eng yaqin va mos) slotni topamiz
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]
