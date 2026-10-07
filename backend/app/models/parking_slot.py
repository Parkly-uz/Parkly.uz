"""
Parkly.uz — ParkingSlot SQLAlchemy Model
"""

from enum import Enum
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SlotType(str, Enum):
    REGULAR = "REGULAR"             # Standart yengil avtomobillar
    EV_CHARGING = "EV_CHARGING"     # Elektromobillar (quvvatlash stansiyasi)
    VIP_STAFF = "VIP_STAFF"         # VIP va xodimlar uchun
    ACCESSIBLE = "ACCESSIBLE"       # Maxsus ehtiyojli / Nogironlar


class SlotStatus(str, Enum):
    FREE = "FREE"                         # Bo'sh (yashil)
    OCCUPIED = "OCCUPIED"                 # Band (qizil)
    RESERVED = "RESERVED"                 # Oldindan bron qilingan (sariq)
    PAYMENT_PENDING = "PAYMENT_PENDING"   # To'lov kutilmoqda (to'q sariq)
    MAINTENANCE = "MAINTENANCE"           # Ta'mirlashda / Yopiq (kulrang)


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parking_lot_id = Column(Integer, nullable=False, index=True)

    # Joylashuv va Manzil
    floor = Column(Integer, nullable=False, default=1)
    zone = Column(String(10), nullable=False)               # 'A', 'B', 'EV', 'VIP'
    slot_number = Column(String(20), nullable=False, index=True)  # 'A-101', 'EV-01'

    # Tur va Holat
    slot_type = Column(
        SQLEnum(SlotType),
        nullable=False,
        default=SlotType.REGULAR
    )
    status = Column(
        SQLEnum(SlotStatus),
        nullable=False,
        default=SlotStatus.FREE
    )

    # 2D Koordinatalar (Desktop interaktiv xarita)
    pos_x = Column(Integer, nullable=False, default=0)
    pos_y = Column(Integer, nullable=False, default=0)
    width = Column(Integer, nullable=False, default=60)
    height = Column(Integer, nullable=False, default=120)
    rotation = Column(Integer, nullable=False, default=0)

    # Joriy band qilgan transport vositasi
    current_vehicle_plate = Column(String(20), nullable=True)
    current_session_id = Column(Integer, nullable=True)

    # Vaqtlar
    last_status_change = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("parking_lot_id", "slot_number", name="uq_parking_lot_slot_number"),
        Index("idx_slots_lot_status", "parking_lot_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<ParkingSlot {self.slot_number} [{self.slot_type.value}]: {self.status.value}>"

    def can_transition_to(self, new_status: SlotStatus) -> bool:
        """
        Holatlar o'tish qoidasi (State Machine) tekshiruvi.
        """
        valid_transitions = {
            SlotStatus.FREE: [SlotStatus.OCCUPIED, SlotStatus.RESERVED, SlotStatus.MAINTENANCE],
            SlotStatus.RESERVED: [SlotStatus.OCCUPIED, SlotStatus.FREE, SlotStatus.MAINTENANCE],
            SlotStatus.OCCUPIED: [SlotStatus.PAYMENT_PENDING, SlotStatus.FREE, SlotStatus.MAINTENANCE],
            SlotStatus.PAYMENT_PENDING: [SlotStatus.FREE, SlotStatus.OCCUPIED],
            SlotStatus.MAINTENANCE: [SlotStatus.FREE],
        }
        return new_status in valid_transitions.get(self.status, [])
