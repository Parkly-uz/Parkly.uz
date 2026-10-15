"""
Parkly.uz — Hisob-kitob, dinamik QR to'lov va qarz boshqaruvi.
"""

import math
from datetime import datetime
from typing import Tuple
from backend.app.core.config import settings


class BillingService:
    @staticmethod
    def calculate_fee(enter_time: datetime, exit_time: datetime, occupancy_rate: float = 0.5) -> Tuple[int, float]:
        """
        Tarif qoidalari bo'yicha to'lovni hisoblash:
        - 15 daqiqagacha: 0 so'm (Grace period)
        - To'lalik > 85%: 8,000 so'm/soat (Peak)
        - Kunduzgi: 5,000 so'm/soat
        - Tungi: 3,000 so'm/soat
        """
        duration_seconds = max(0.0, (exit_time - enter_time).total_seconds())
        duration_minutes = int(duration_seconds / 60)

        # 1. Bepul oraliq
        if duration_minutes <= settings.GRACE_PERIOD_MINUTES:
            return duration_minutes, 0.0

        # 2. 24 soatlik fiksirlangan kunlik tarif
        if duration_minutes >= 1440:
            days = math.ceil(duration_minutes / 1440)
            return duration_minutes, float(days * settings.RATE_DAILY_FIXED)

        # 3. Soatlarni yuqoriga yaxlitlash
        hours = math.ceil(duration_minutes / 60)

        # 4. Tig'iz vaqt tekshiruvi
        if occupancy_rate >= 0.85:
            rate = settings.RATE_PEAK_HOURLY
        else:
            exit_hour = exit_time.hour
            # Kunduzgi (08:00 - 20:00) yoki Tungi
            if 8 <= exit_hour < 20:
                rate = settings.RATE_DAY_HOURLY
            else:
                rate = settings.RATE_NIGHT_HOURLY

        total = float(hours * rate)
        return duration_minutes, total

    @staticmethod
    def generate_dynamic_qr_url(session_id: str, amount: float) -> str:
        """Payme / Click uchun dinamik to'lov havolasi."""
        return f"https://checkout.parkly.uz/pay?session={session_id}&amount={int(amount)}"
