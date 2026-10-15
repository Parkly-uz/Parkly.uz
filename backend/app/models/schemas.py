"""
Parkly.uz — SQLAlchemy 2.0 ma'lumotlar bazasi modellari.
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SessionStatus(str, Enum):
    APPROACHING_GATE = "APPROACHING_GATE"
    PLATE_RECOGNIZED = "PLATE_RECOGNIZED"
    BARRIER_OPENED_ENTRY = "BARRIER_OPENED_ENTRY"
    PARKED_OCCUPIED = "PARKED_OCCUPIED"
    APPROACHING_EXIT = "APPROACHING_EXIT"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    DEFERRED_DEBT = "DEFERRED_DEBT"
    SESSION_COMPLETED = "SESSION_COMPLETED"


class ParkingSession(Base):
    """Avtomobilning kirishdan chiqishgacha bo'lgan to'liq sessiyasi."""
    __tablename__ = "parking_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    plate_number: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    vehicle_model: Mapped[str] = mapped_column(String(64), default="Unknown")
    vehicle_color: Mapped[str] = mapped_column(String(32), default="Unknown")
    
    allocated_slot: Mapped[str] = mapped_column(String(16), nullable=True)
    status: Mapped[SessionStatus] = mapped_column(SQLEnum(SessionStatus), default=SessionStatus.APPROACHING_GATE)
    
    enter_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    exit_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    total_fee: Mapped[float] = mapped_column(Float, default=0.0)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deferred_debt: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # ⏱️ 10 daqiqalik SLA monitoringi
    sla_wait_seconds: Mapped[float] = mapped_column(Float, default=0.0)
    sla_breached: Mapped[bool] = mapped_column(Boolean, default=False)


class ParkingSlot(Base):
    """Parkovka kataklari va datchiklar."""
    __tablename__ = "parking_slots"

    slot_id: Mapped[str] = mapped_column(String(16), primary_key=True)  # masalan: A-01
    sector: Mapped[str] = mapped_column(String(8), nullable=False)       # masalan: A
    floor: Mapped[int] = mapped_column(Integer, default=1)
    
    is_occupied: Mapped[bool] = mapped_column(Boolean, default=False)
    current_plate: Mapped[str] = mapped_column(String(16), nullable=True)
    has_conflict: Mapped[bool] = mapped_column(Boolean, default=False)  # Datchik va Kamera ziddiyati
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Qora quti xavfsizlik va favqulodda hodisalar jurnali."""
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    operator_username: Mapped[str] = mapped_column(String(32), default="SYSTEM")
    plate_number: Mapped[str] = mapped_column(String(16), nullable=True)
    reason: Mapped[str] = mapped_column(String(255), nullable=True)
    photo_evidence_url: Mapped[str] = mapped_column(String(512), nullable=True)
