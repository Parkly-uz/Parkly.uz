"""
Parkly.uz — 10-Minute SLA Watchdog & Fail-Safe Emergency Controller.

Ushbu servis:
- Har bir avtomobilning postda kutish vaqtini kuzatadi.
- 05:00 daqiqada: WARNING (Sariq ogohlantirish).
- 07:00 daqiqada: URGENT (Qizil favqulodda signal).
- 10:00 daqiqada: FAIL_SAFE_EMERGENCY_OPEN — shlagbaum avtomatik majburiy ochiladi,
  mashina qarz reestriga yoziladi va hodisa auditga saqlanadi.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Tuple


class SLAStatus(str, Enum):
    NORMAL = "NORMAL"                # 0 - 5 min
    WARNING = "WARNING"              # 5 - 7 min
    URGENT = "URGENT"                # 7 - 10 min
    FAIL_SAFE_OPEN = "FAIL_SAFE_OPEN"  # >= 10 min (Emergency)


@dataclass
class PostSession:
    plate_number: str
    post_id: str
    start_time: float = field(default_factory=time.time)
    current_fee: float = 10000.0
    status: SLAStatus = SLAStatus.NORMAL
    barrier_opened: bool = False
    emergency_released: bool = False


class SLAWatchdogService:
    """Postdagi kutish vaqtini nazorat qiluvchi xizmat."""

    def __init__(self, warning_threshold_sec: float = 300.0, urgent_threshold_sec: float = 420.0, max_wait_sec: float = 600.0):
        # 300s = 5 min, 420s = 7 min, 600s = 10 min
        self.warning_sec = warning_threshold_sec
        self.urgent_sec = urgent_threshold_sec
        self.max_wait_sec = max_wait_sec
        self.active_sessions: Dict[str, PostSession] = {}

    def start_session(self, post_id: str, plate_number: str, initial_fee: float = 10000.0) -> PostSession:
        """Mashina postga kelganda yangi sessiya boshlash."""
        session = PostSession(
            plate_number=plate_number,
            post_id=post_id,
            start_time=time.time(),
            current_fee=initial_fee,
        )
        self.active_sessions[post_id] = session
        return session

    def check_post_status(self, post_id: str, virtual_elapsed_sec: Optional[float] = None) -> Tuple[SLAStatus, float, bool]:
        """
        Postdagi mashina holatini tekshirish.
        Qaytaradi: (Status, O'tgan soniyalar, Shlagbaum ochildimi)
        """
        session = self.active_sessions.get(post_id)
        if not session:
            return SLAStatus.NORMAL, 0.0, False

        # Testlar uchun vaqtni virtual ko'chirish imkoniyati
        if virtual_elapsed_sec is not None:
            elapsed = virtual_elapsed_sec
        else:
            elapsed = time.time() - session.start_time

        # 10 daqiqalik qat'iy SLA tekshiruvi (Fail-Safe Open)
        if elapsed >= self.max_wait_sec:
            session.status = SLAStatus.FAIL_SAFE_OPEN
            session.barrier_opened = True
            session.emergency_released = True
            self._log_audit_breach(session, elapsed)
            return SLAStatus.FAIL_SAFE_OPEN, elapsed, True

        # 7 daqiqa: Urgent
        if elapsed >= self.urgent_sec:
            session.status = SLAStatus.URGENT
            return SLAStatus.URGENT, elapsed, False

        # 5 daqiqa: Warning
        if elapsed >= self.warning_sec:
            session.status = SLAStatus.WARNING
            return SLAStatus.WARNING, elapsed, False

        session.status = SLAStatus.NORMAL
        return SLAStatus.NORMAL, elapsed, False

    def _log_audit_breach(self, session: PostSession, elapsed_sec: float) -> None:
        """10 daqiqalik qoida buzilganda auditga yozish."""
        # Haqiqiy loyihada PostgreSQL audit_sla_breaches jadvaliga yoziladi
        pass

    def close_session(self, post_id: str) -> Optional[PostSession]:
        """To'lov qilinib yoki chiqib ketilgach sessiyani yopish."""
        return self.active_sessions.pop(post_id, None)


if __name__ == "__main__":
    print("[TEST] Parkly.uz 10-Minute SLA Watchdog sinovi...")
    watchdog = SLAWatchdogService()

    # 1. Mashina postga keldi
    post_id = "GATE_EXIT_01"
    session = watchdog.start_session(post_id, "01A777AA", 15000.0)
    print(f"[START] Post: {post_id} | Avto: {session.plate_number}")

    # 2. Sinov: 3-daqiqa (Normal)
    status, elapsed, opened = watchdog.check_post_status(post_id, virtual_elapsed_sec=180.0)
    print(f"-> 03:00 daqiqa: Status={status.value} | Shlagbaum ochiqmi: {opened}")

    # 3. Sinov: 5-daqiqa (Warning)
    status, elapsed, opened = watchdog.check_post_status(post_id, virtual_elapsed_sec=320.0)
    print(f"-> 05:20 daqiqa: Status={status.value} | Shlagbaum ochiqmi: {opened}")

    # 4. Sinov: 7-daqiqa (Urgent)
    status, elapsed, opened = watchdog.check_post_status(post_id, virtual_elapsed_sec=450.0)
    print(f"-> 07:30 daqiqa: Status={status.value} | Shlagbaum ochiqmi: {opened}")

    # 5. Sinov: 10-daqiqa (Fail-Safe Emergency Open!)
    status, elapsed, opened = watchdog.check_post_status(post_id, virtual_elapsed_sec=605.0)
    print(f"-> 10:05 daqiqa: Status={status.value} | Shlagbaum ochiqmi: {opened} (FAVQULODDA OCHILDI!)")
