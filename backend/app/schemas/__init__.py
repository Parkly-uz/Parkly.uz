"""Parkly.uz Validation Schemas Package"""
from app.schemas.parking_slot import (
    ParkingSlotBase,
    ParkingSlotCreate,
    ParkingSlotUpdate,
    ParkingSlotStatusUpdate,
    ParkingSlotResponse,
    SlotSimulatorEvent,
)

__all__ = [
    "ParkingSlotBase",
    "ParkingSlotCreate",
    "ParkingSlotUpdate",
    "ParkingSlotStatusUpdate",
    "ParkingSlotResponse",
    "SlotSimulatorEvent",
]
