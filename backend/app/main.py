"""
Parkly.uz — Smart Parking Management System Main FastAPI Application
Barcha ANPR, algoritm, to'lov (Click, Payme, Uzum) va admin panel API endpointlarini boshqaruvchi asosiy server.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.algorithms.gate_controller import GateController, GateAction
from app.algorithms.spot_allocator import SpotAllocator
from app.algorithms.tariff_calculator import TariffCalculator

app = FastAPI(
    title="Parkly.uz — Smart Parking API",
    version="2.12.0",
    description="No-Operator Cashless Smart Parking System with ANPR, ESP32 Integration & 10-Min SLA Watchdog."
)

# CORS sozlamalari (Admin Panel va Mobile App uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic modellari (Request / Response schemas)
class VehicleEntryRequest(BaseModel):
    plate_number: str = Field(..., example="01A777AA")
    vehicle_type: str = Field(default="REGULAR", example="REGULAR")  # REGULAR, EV_CHARGING
    is_staff: bool = Field(default=False)
    available_slots: List[Dict[str, Any]] = Field(default_factory=list)


class VehicleExitRequest(BaseModel):
    plate_number: str = Field(..., example="01A777AA")
    session_data: Dict[str, Any]
    payment_status: str = Field(default="PENDING", example="SUCCESS")  # PENDING, SUCCESS


class PaymentWebhookRequest(BaseModel):
    provider: str = Field(..., example="PAYME")  # PAYME, CLICK, UZUM
    transaction_id: str
    amount: float
    session_id: str
    status: str


@app.get("/")
def read_root():
    return {
        "system": "Parkly.uz Smart Parking API",
        "status": "online",
        "version": "2.12.0",
        "sla_max_wait_minutes": 10.0
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/v1/gate/entry")
def process_vehicle_entry(payload: VehicleEntryRequest):
    """
    Mashina kirish postidan o'tganda ANPR orqali o'qilgan raqamni qabul qilish
    va shlagbaum / slot taqsimlash qarorini qaytarish.
    """
    # Agar xodim (Staff) bo'lsa, to'lovsiz va maxsus ruxsat bilan kiritiladi
    if payload.is_staff:
        return {
            "action": GateAction.OPEN_BARRIER,
            "message": f"Xush kelibsiz, Hurmatli Xodim ({payload.plate_number})!",
            "assigned_slot": "STAFF-ZONE",
            "is_staff": True
        }

    result = GateController.process_entry(
        plate_number=payload.plate_number,
        vehicle_type=payload.vehicle_type,
        available_slots=payload.available_slots
    )
    return result


@app.post("/api/v1/gate/exit")
def process_vehicle_exit(payload: VehicleExitRequest):
    """
    Mashina chiqish postiga kelganda naqd pulsiz (Cashless) to'lov va shlagbaum ochish tekshiruvi.
    Operator talab etilmaydi — to'liq avtomatlashgan.
    """
    result = GateController.process_exit(
        plate_number=payload.plate_number,
        session=payload.session_data,
        payment_status=payload.payment_status
    )
    return result


@app.post("/api/v1/payments/webhook")
def payment_webhook(payload: PaymentWebhookRequest):
    """
    Click, Payme va Uzum Pay to'lov tizimlaridan keladigan webhook so'rovlarini qabul qilish.
    """
    if payload.status == "SUCCESS":
        # Tranzaksiya muvaffaqiyatli yakunlandi, seansni yangilash va shlagbaunga signal berish
        return {
            "status": "OK",
            "message": f"To'lov qabul qilindi ({payload.provider}). Seans yopildi.",
            "session_id": payload.session_id
        }
    else:
        raise HTTPException(status_code=400, detail="Payment failed or pending.")


@app.get("/api/v1/slots/status")
def get_parking_slots_status():
    """
    Admin Panel va Isometric Xarita uchun barcha slotlarning real vaqtda holatini qaytarish.
    """
    # Test / Mock ma'lumotlar (real holatda PostgreSQL dan olinadi)
    return {
        "parking_lot": "Parkly Central — Tashkent City Mall",
        "total_slots": 12,
        "free_slots": 5,
        "occupied_slots": 4,
        "reserved_slots": 2,
        "maintenance_slots": 1,
        "slots": [
            {"slot_number": "A-101", "floor": 1, "zone": "A", "status": "FREE", "slot_type": "REGULAR", "pos_x": 50, "pos_y": 50},
            {"slot_number": "A-102", "floor": 1, "zone": "A", "status": "OCCUPIED", "slot_type": "REGULAR", "pos_x": 130, "pos_y": 50},
            {"slot_number": "EV-01", "floor": 1, "zone": "EV", "status": "FREE", "slot_type": "EV_CHARGING", "pos_x": 50, "pos_y": 220},
            {"slot_number": "VIP-01", "floor": 1, "zone": "VIP", "status": "FREE", "slot_type": "VIP_STAFF", "pos_x": 50, "pos_y": 390},
        ]
    }
