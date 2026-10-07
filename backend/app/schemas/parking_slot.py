"""
Parkly.uz — ParkingSlot Pydantic Validation Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.parking_slot import SlotType, SlotStatus


class ParkingSlotBase(BaseModel):
    parking_lot_id: int = Field(..., description="Avtoturargoh ID'si")
    floor: int = Field(1, description="Qavat raqami (masalan: 1, 2, -1)")
    zone: str = Field(..., max_length=10, description="Zona (A, B, EV, VIP)")
    slot_number: str = Field(..., max_length=20, description="Slot raqami (A-101, EV-01)")
    slot_type: SlotType = Field(SlotType.REGULAR, description="Slot turi")
    pos_x: int = Field(0, description="2D X koordinatasi")
    pos_y: int = Field(0, description="2D Y koordinatasi")
    width: int = Field(60, description="Slot eni pikselda")
    height: int = Field(120, description="Slot bo'yi pikselda")
    rotation: int = Field(0, description="Aylanish burchagi")


class ParkingSlotCreate(ParkingSlotBase):
    pass


class ParkingSlotUpdate(BaseModel):
    slot_type: Optional[SlotType] = None
    pos_x: Optional[int] = None
    pos_y: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    rotation: Optional[int] = None


class ParkingSlotStatusUpdate(BaseModel):
    status: SlotStatus = Field(..., description="Yangi holat")
    vehicle_plate: Optional[str] = Field(None, max_length=20, description="Avtomobil davlat raqami")
    session_id: Optional[int] = Field(None, description="Bog'langan sessiya ID")


class ParkingSlotResponse(ParkingSlotBase):
    id: int
    status: SlotStatus
    current_vehicle_plate: Optional[str] = None
    current_session_id: Optional[int] = None
    last_status_change: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SlotSimulatorEvent(BaseModel):
    """
    C/C++ Simulyatordan keluvchi kirish/chiqish hodisasi
    """
    slot_number: str = Field(..., description="Slot raqami (masalan: 'A-101')")
    new_status: SlotStatus = Field(..., description="Yangi holat (OCCUPIED / FREE)")
    vehicle_plate: Optional[str] = Field(None, description="O'zbekiston davlat raqami (01A777AA)")
