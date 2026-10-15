"""
Parkly.uz — Asosiy FastAPI ilovasi va Real-time endpoints.
"""

from datetime import datetime
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.app.core.config import settings
from backend.app.services.billing_service import BillingService
from backend.app.services.routing_service import RoutingService
from backend.app.vision.camera_logic_pipeline import CameraLogicPipeline

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",
    description="Next-Gen Unattended Smart Parking Management API",
)

camera_pipeline = CameraLogicPipeline()


class EnterRequest(BaseModel):
    gate_id: str
    plate_number: str
    vehicle_model: str = "Unknown"


class ExitRequest(BaseModel):
    gate_id: str
    plate_number: str


# Xotiradagi faol sessiyalar (Mock kesh)
active_sessions = {}


@app.get("/")
def read_root():
    return {
        "project": settings.PROJECT_NAME,
        "version": "2.0.0",
        "status": "ONLINE",
        "unattended_mode": True,
        "cashless": True,
    }


@app.post("/api/v1/gate/enter")
def gate_enter(req: EnterRequest):
    """Avtomobil kirishi, bo'sh joy tayinlash va shlagbaumni ochish."""
    # Raqamni tekshirish
    is_valid = camera_pipeline.validator.is_valid(req.plate_number)
    session_id = f"SES-{uuid.uuid4().hex[:8].upper()}"

    # Bo'sh joy tayinlash
    dummy_slots = [
        {"slot_id": "A-01", "is_occupied": True, "distance_to_entry": 5},
        {"slot_id": "B-04", "is_occupied": False, "has_conflict": False, "distance_to_entry": 12},
        {"slot_id": "C-10", "is_occupied": False, "has_conflict": False, "distance_to_entry": 25},
    ]
    allocated_slot = RoutingService.find_nearest_slot(req.gate_id, dummy_slots)

    active_sessions[req.plate_number] = {
        "session_id": session_id,
        "enter_time": datetime.utcnow(),
        "plate_number": req.plate_number,
        "allocated_slot": allocated_slot,
    }

    return {
        "session_id": session_id,
        "barrier_command": "OPEN",
        "allocated_slot": allocated_slot,
        "is_valid_plate": is_valid,
        "requires_fallback_talon": not is_valid,
    }


@app.post("/api/v1/gate/exit")
def gate_exit(req: ExitRequest):
    """Chiqishda to'lov hisoblash va QR havola berish."""
    session = active_sessions.get(req.plate_number)
    now = datetime.utcnow()

    if not session:
        # Avto topilmasa -> No-Automation zaxira qarziga chiqarish
        return {
            "session_id": "UNKNOWN",
            "barrier_command": "OPEN",
            "note": "No-automation fallback: plate registered to deferred debt register",
            "is_deferred_debt": True,
        }

    duration, fee = BillingService.calculate_fee(session["enter_time"], now)
    qr_url = BillingService.generate_dynamic_qr_url(session["session_id"], fee)

    return {
        "session_id": session["session_id"],
        "duration_minutes": duration,
        "total_fee_sum": fee,
        "qr_payment_url": qr_url,
        "barrier_command": "OPEN" if fee == 0 else "WAIT_FOR_PAYMENT",
        "sla_max_wait_seconds": settings.SLA_MAX_WAIT_SECONDS,
    }
