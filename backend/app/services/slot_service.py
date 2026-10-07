"""
Parkly.uz — ParkingSlot Service (Business Logic & State Machine)
"""

from typing import List, Optional, Dict
from datetime import datetime
from app.models.parking_slot import ParkingSlot, SlotStatus, SlotType
from app.schemas.parking_slot import ParkingSlotCreate, ParkingSlotStatusUpdate, SlotSimulatorEvent


class ParkingSlotService:
    def __init__(self, db_session):
        self.db = db_session

    def get_by_number(self, parking_lot_id: int, slot_number: str) -> Optional[ParkingSlot]:
        """Slot raqami bo'yicha qidirish"""
        return self.db.query(ParkingSlot).filter(
            ParkingSlot.parking_lot_id == parking_lot_id,
            ParkingSlot.slot_number == slot_number
        ).first()

    def get_all_by_lot(
        self,
        parking_lot_id: int,
        floor: Optional[int] = None,
        zone: Optional[str] = None,
        slot_type: Optional[SlotType] = None,
        status: Optional[SlotStatus] = None
    ) -> List[ParkingSlot]:
        """Filtrlar bilan parkovka slotlari ro'yxatini olish"""
        query = self.db.query(ParkingSlot).filter(ParkingSlot.parking_lot_id == parking_lot_id)

        if floor is not None:
            query = query.filter(ParkingSlot.floor == floor)
        if zone:
            query = query.filter(ParkingSlot.zone == zone)
        if slot_type:
            query = query.filter(ParkingSlot.slot_type == slot_type)
        if status:
            query = query.filter(ParkingSlot.status == status)

        return query.order_by(ParkingSlot.floor, ParkingSlot.zone, ParkingSlot.slot_number).all()

    def create_slot(self, slot_data: ParkingSlotCreate) -> ParkingSlot:
        """Yangi slot yaratish"""
        existing = self.get_by_number(slot_data.parking_lot_id, slot_data.slot_number)
        if existing:
            raise ValueError(f"Slot {slot_data.slot_number} ushbu parkovkada allaqachon mavjud!")

        slot = ParkingSlot(
            parking_lot_id=slot_data.parking_lot_id,
            floor=slot_data.floor,
            zone=slot_data.zone,
            slot_number=slot_data.slot_number,
            slot_type=slot_data.slot_type,
            pos_x=slot_data.pos_x,
            pos_y=slot_data.pos_y,
            width=slot_data.width,
            height=slot_data.height,
            rotation=slot_data.rotation,
            status=SlotStatus.FREE
        )
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def update_status(
        self,
        parking_lot_id: int,
        slot_number: str,
        update_data: ParkingSlotStatusUpdate
    ) -> ParkingSlot:
        """Slot holatini xavfsiz o'zgartirish (State Transition)"""
        slot = self.get_by_number(parking_lot_id, slot_number)
        if not slot:
            raise ValueError(f"Slot '{slot_number}' topilmadi!")

        # O'tish mumkinligini tekshirish
        if not slot.can_transition_to(update_data.status):
            raise ValueError(
                f"Holatni '{slot.status.value}' dan '{update_data.status.value}' ga o'tkazib bo'lmaydi!"
            )

        slot.status = update_data.status
        slot.last_status_change = datetime.utcnow()

        if update_data.status == SlotStatus.OCCUPIED:
            slot.current_vehicle_plate = update_data.vehicle_plate
            slot.current_session_id = update_data.session_id
        elif update_data.status == SlotStatus.FREE:
            slot.current_vehicle_plate = None
            slot.current_session_id = None

        self.db.commit()
        self.db.refresh(slot)
        return slot

    def handle_simulator_event(self, parking_lot_id: int, event: SlotSimulatorEvent) -> Dict:
        """
        C/C++ Simulyatoridan keluvchi to'g'ridan-to'g'ri hodisani qayta ishlash
        """
        slot = self.get_by_number(parking_lot_id, event.slot_number)
        if not slot:
            return {"status": "error", "message": f"Slot {event.slot_number} topilmadi"}

        update_dto = ParkingSlotStatusUpdate(
            status=event.new_status,
            vehicle_plate=event.vehicle_plate if event.new_status == SlotStatus.OCCUPIED else None
        )
        updated_slot = self.update_status(parking_lot_id, event.slot_number, update_dto)

        return {
            "status": "success",
            "slot_number": updated_slot.slot_number,
            "current_status": updated_slot.status.value,
            "plate": updated_slot.current_vehicle_plate,
            "timestamp": updated_slot.last_status_change.isoformat()
        }
