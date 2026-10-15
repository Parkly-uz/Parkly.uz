"""
Parkly.uz — Tizimning asosiy sinov testlari (Unittest formatida).
"""

import unittest
from datetime import datetime, timedelta
from backend.app.core.config import settings
from backend.app.core.security import check_permission
from backend.app.services.billing_service import BillingService
from backend.app.services.routing_service import RoutingService
from backend.app.services.sla_watchdog import SLAWatchdogService, SLAStatus
from backend.app.vision.camera_logic_pipeline import UzbekPlateValidator


class TestParklyCoreEngine(unittest.TestCase):
    def test_uzbek_plate_validation(self):
        """O'zbekiston raqamlari tekshiruvi."""
        self.assertTrue(UzbekPlateValidator.is_valid("01A777AA"))
        self.assertTrue(UzbekPlateValidator.is_valid("01 777 AAA"))
        self.assertFalse(UzbekPlateValidator.is_valid("INVALID_PLATE"))

    def test_billing_grace_period(self):
        """15 daqiqa ichida chiqilsa to'lov 0 so'm bo'lishi kerak."""
        enter = datetime(2026, 10, 15, 10, 0, 0)
        exit_time = enter + timedelta(minutes=14)
        duration, fee = BillingService.calculate_fee(enter, exit_time)
        self.assertEqual(duration, 14)
        self.assertEqual(fee, 0.0)

    def test_billing_hourly_day(self):
        """Kunduzgi 2 soat to'xtash uchun 10,000 so'm."""
        enter = datetime(2026, 10, 15, 10, 0, 0)
        exit_time = enter + timedelta(minutes=65)  # 1 soat 5 daqiqa -> 2 soat
        duration, fee = BillingService.calculate_fee(enter, exit_time, occupancy_rate=0.5)
        self.assertEqual(duration, 65)
        self.assertEqual(fee, 10000.0)

    def test_sla_10min_fail_safe(self):
        """10 daqiqa to'xtab qolganda shlagbaum majburiy ochilishi shart."""
        watchdog = SLAWatchdogService()
        watchdog.start_session("GATE_01", "01A777AA")

        # 10:05 daqiqa o'tdi
        status, elapsed, opened = watchdog.check_post_status("GATE_01", virtual_elapsed_sec=605.0)
        self.assertEqual(status, SLAStatus.FAIL_SAFE_OPEN)
        self.assertTrue(opened)

    def test_rbac_security_rules(self):
        """Admin tarifni o'zgartira olmasligi, Super-Admin esa o'zgartirishi kerak."""
        self.assertTrue(check_permission("admin", "change_tariffs"))
        self.assertFalse(check_permission("admin_yunusobod", "change_tariffs"))
        self.assertFalse(check_permission("operator1", "change_tariffs"))


if __name__ == "__main__":
    unittest.main()
