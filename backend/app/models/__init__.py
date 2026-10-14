"""Parkly.uz Database Models Package"""
from app.models.parking_slot import ParkingSlot, SlotStatus, SlotType, Base

__all__ = ["ParkingSlot", "SlotStatus", "SlotType", "Base"]
