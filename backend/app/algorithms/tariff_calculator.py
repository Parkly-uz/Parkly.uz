"""
Parkly.uz — Tariff & Parking Fee Calculation Algorithm
Ushbu algoritm mashinaning turgan vaqti, tarifi, kechki/kunduzgi stavkalari va bepul oraliqlarini hisoblaydi.
"""

import math
from datetime import datetime, timedelta
from typing import Dict, Any


class TariffCalculator:
    """
    Parkovka xizmati narxini hisoblash algoritmi.
    
    Qoidalar:
    - Bepul oraliq (Grace Period): dastlabki 15 daqiqa bepul.
    - Soatlik yaxlitlash: 15 daqiqadan o'tgach, har bir boshlangan soat to'liq 1 soat hisoblanadi.
    - Kunduzgi tarif (08:00 - 20:00): 5,000 so'm / soat.
    - Tungi tarif (20:00 - 08:00): 3,000 so'm / soat.
    - Maksimal kunlik to'lov (Daily Cap): 50,000 so'm (foydalanuvchiga ortiqcha yuk tushmasligi uchun).
    - EV zaryadlash qo'shimchasi: +10,000 so'm / soat.
    - To'lovdan so'ng chiqish vaqti (Exit Grace Period): 15 daqiqa.
    """

    GRACE_PERIOD_MINUTES = 15
    EXIT_GRACE_MINUTES = 15
    DAY_HOURLY_RATE = 5000     # 08:00 - 20:00
    NIGHT_HOURLY_RATE = 3000   # 20:00 - 08:00
    DAILY_CAP_AMOUNT = 50000   # 24 soat uchun maksimal chegara
    EV_SURCHARGE_HOURLY = 10000

    @classmethod
    def calculate_fee(
        cls,
        entry_time: datetime,
        exit_time: datetime,
        is_ev_charging: bool = False,
        discount_percent: float = 0.0
    ) -> Dict[str, Any]:
        """
        Umumiy turgan vaqt bo'yicha to'lov summasini hisoblaydi.
        """
        if exit_time <= entry_time:
            return {
                "total_minutes": 0,
                "billable_hours": 0,
                "base_fee": 0,
                "ev_surcharge": 0,
                "discount_amount": 0,
                "final_amount": 0,
                "is_grace_period": True
            }

        duration = exit_time - entry_time
        total_minutes = int(duration.total_seconds() // 60)

        # 1. Grace Period (Dastlabki 15 daqiqa ichida chiqib ketsa - 0 so'm)
        if total_minutes <= cls.GRACE_PERIOD_MINUTES:
            return {
                "total_minutes": total_minutes,
                "billable_hours": 0,
                "base_fee": 0,
                "ev_surcharge": 0,
                "discount_amount": 0,
                "final_amount": 0,
                "is_grace_period": True,
                "description": "15 daqiqalik bepul oraliqda chiqildi."
            }

        # 2. To'lanadigan soatlarni yaxlitlash (masalan 16 min -> 1 soat, 65 min -> 2 soat)
        billable_hours = math.ceil(total_minutes / 60)

        # 3. Vaqt oralig'i bo'yicha hisoblash (kunduzgi va tungi)
        current = entry_time
        base_fee = 0
        for _ in range(billable_hours):
            hour_of_day = current.hour
            if 8 <= hour_of_day < 20:
                base_fee += cls.DAY_HOURLY_RATE
            else:
                base_fee += cls.NIGHT_HOURLY_RATE
            current += timedelta(hours=1)

        # 4. Kunlik maksimal cheklov (Har 24 soatlik bloklar uchun)
        days = billable_hours // 24
        remaining_hours = billable_hours % 24
        if days > 0:
            capped_days_fee = days * cls.DAILY_CAP_AMOUNT
            base_fee = min(base_fee, capped_days_fee + (remaining_hours * cls.DAY_HOURLY_RATE))
        else:
            base_fee = min(base_fee, cls.DAILY_CAP_AMOUNT)

        # 5. EV (Elektromobil zaryadlash) qo'shimchasi
        ev_surcharge = 0
        if is_ev_charging:
            ev_surcharge = billable_hours * cls.EV_SURCHARGE_HOURLY

        gross_amount = base_fee + ev_surcharge

        # 6. Chegirmalar (Abonent yoki promo kod)
        discount_amount = int(gross_amount * (discount_percent / 100.0))
        final_amount = max(0, gross_amount - discount_amount)

        return {
            "total_minutes": total_minutes,
            "billable_hours": billable_hours,
            "base_fee": base_fee,
            "ev_surcharge": ev_surcharge,
            "discount_amount": discount_amount,
            "final_amount": final_amount,
            "is_grace_period": False,
            "description": f"{billable_hours} soat xizmat haqi hisoblandi."
        }
