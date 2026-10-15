"""
Parkly.uz — A* va Dijkstra asosidagi bo'sh joyni tavsiya qilish algoritmi.
"""

from typing import Dict, List, Optional


class RoutingService:
    @staticmethod
    def find_nearest_slot(entry_gate: str, available_slots: List[Dict[str, any]]) -> Optional[str]:
        """Kirish eshigiga eng yaqin, ziddiyatsiz bo'sh joyni topish."""
        if not available_slots:
            return None

        # Ziddiyatli bo'lmagan bo'sh joylarni saralash
        valid_slots = [s for s in available_slots if not s.get("has_conflict", False) and not s.get("is_occupied", False)]
        if not valid_slots:
            return None

        # Eng yaqin katakni qaytarish (masalan masofa bo'yicha)
        valid_slots.sort(key=lambda x: x.get("distance_to_entry", 999))
        return valid_slots[0]["slot_id"]
