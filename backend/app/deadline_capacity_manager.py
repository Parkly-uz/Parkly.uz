#!/usr/bin/env python3
"""
Parkly.uz — Deadline & Capacity Management Module
-------------------------------------------------
Monitors real-time parking capacity, occupancy thresholds, reservation expiration deadlines,
and session overstay limits.
"""

import sys
import json
import argparse
from datetime import datetime, timedelta

# Simulated parking zone capacities and states
PARKING_CAPACITY_STATE = {
    "total_capacity": 150,
    "occupied_count": 142,
    "reserved_count": 5,
    "zones": {
        "A": {"capacity": 80, "occupied": 78},
        "EV": {"capacity": 20, "occupied": 19},
        "VIP": {"capacity": 50, "occupied": 45}
    }
}

# Simulated active reservations with arrival deadlines
ACTIVE_RESERVATIONS = [
    {"reservation_id": "RES-301", "plate": "01Z999ZZ", "slot": "A-108", "expires_at": "2026-10-20T14:45:00", "status": "ACTIVE"}
]

def check_capacity_status() -> dict:
    """
    Computes current occupancy rate and determines if the parking lot is near full or full.
    """
    total = PARKING_CAPACITY_STATE["total_capacity"]
    occupied = PARKING_CAPACITY_STATE["occupied_count"]
    occupancy_pct = round((occupied / total) * 100, 2)

    status = "NORMAL"
    message = "Avtoturargoh sig'imi normal darajada."

    if occupancy_pct >= 100.0:
        status = "FULL"
        message = "DIQQAT! Avtoturargoh to'lgan (100%). Kirish vaqtincha bloklandi."
    elif occupancy_pct >= 90.0:
        status = "NEAR_FULL"
        message = "OGOHLANTIRISH: Avtoturargoh sig'imi 90% dan oshdi. Qolgan joylar kam!"

    return {
        "total_capacity": total,
        "occupied_count": occupied,
        "free_count": total - occupied,
        "occupancy_percentage": occupancy_pct,
        "capacity_status": status,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

def check_reservation_deadlines() -> list:
    """
    Checks if any slot reservation has expired without vehicle arrival (15 min grace limit).
    If expired, releases the slot back to FREE.
    """
    now = datetime.now()
    expired_actions = []

    for res in ACTIVE_RESERVATIONS:
        if res["status"] == "ACTIVE":
            exp_time = datetime.strptime(res["expires_at"], "%Y-%m-%dT%H:%M:%S")
            if now > exp_time:
                res["status"] = "EXPIRED"
                expired_actions.append({
                    "reservation_id": res["reservation_id"],
                    "plate": res["plate"],
                    "slot": res["slot"],
                    "action": "RELEASE_SLOT",
                    "reason": "Reservation deadline exceeded (15 min limit). Slot freed."
                })

    return expired_actions

def main():
    parser = argparse.ArgumentParser(description="Parkly.uz Deadline & Capacity Manager")
    parser.add_argument("--check-capacity", action="store_true", help="Check overall capacity status")
    parser.add_argument("--check-deadlines", action="store_true", help="Check expired reservations and deadlines")
    parser.add_argument("--sample", action="store_true", help="Run full capacity and deadline diagnostic report")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    if args.sample or (not args.check_capacity and not args.check_deadlines):
        cap_report = check_capacity_status()
        deadline_report = check_reservation_deadlines()
        combined = {
            "capacity_report": cap_report,
            "expired_reservations": deadline_report
        }

        if args.output == "json":
            print(json.dumps(combined, indent=2))
        else:
            print("--- Parkly.uz Capacity & Deadline Report ---")
            print(f"Total Capacity: {cap_report['total_capacity']} | Occupied: {cap_report['occupied_count']} ({cap_report['occupancy_percentage']}%)")
            print(f"Status: {cap_report['capacity_status']} — {cap_report['message']}")
            print(f"Expired Reservations Handled: {len(deadline_report)}")
            for item in deadline_report:
                print(f"  -> Res: {item['reservation_id']} | Slot: {item['slot']} | Action: {item['action']}")
        sys.exit(0)

    if args.check_capacity:
        res = check_capacity_status()
        print(json.dumps(res, indent=2) if args.output == "json" else f"Status: {res['capacity_status']} ({res['occupancy_percentage']}%) — {res['message']}")

    if args.check_deadlines:
        res = check_reservation_deadlines()
        print(json.dumps(res, indent=2) if args.output == "json" else f"Expired Reservations: {len(res)}")

    sys.exit(0)

if __name__ == "__main__":
    main()
