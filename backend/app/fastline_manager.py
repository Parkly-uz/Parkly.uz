#!/usr/bin/env python3
"""
Parkly.uz — Fastline (Express Lane) Management System
-----------------------------------------------------
Handles high-speed automated entry/exit for active monthly subscribers (1, 3, 6-month passes)
and VIP staff without ticket issuance or payment processing delays.
"""

import sys
import json
import argparse
from datetime import datetime, timedelta

# Simulated active subscriptions database
ACTIVE_SUBSCRIPTIONS = {
    "01A777AA": {"plan": "QUARTERLY_PASS", "expires": "2027-01-21", "owner": "Erjigit S.", "tier": "VIP"},
    "01888ZZZ": {"plan": "MONTHLY_PASS", "expires": "2026-11-15", "owner": "Sherzod A.", "tier": "SUBSCRIBER"},
    "01001PPP": {"plan": "ANNUAL_VIP", "expires": "2027-10-01", "owner": "Parkly Management", "tier": "VIP_STAFF"}
}

def process_fastline_crossing(plate_number: str, gate_type: str = "ENTRY") -> dict:
    """
    Validates if a vehicle is eligible for Fastline express crossing.
    """
    cleaned_plate = plate_number.strip().upper().replace(" ", "")
    result = {
        "plate_number": cleaned_plate,
        "gate_type": gate_type,
        "fastline_eligible": False,
        "action": "STANDARD_QUEUE",
        "message": "Obuna topilmadi. Oddiy tartibda davom eting.",
        "timestamp": datetime.now().isoformat()
    }

    if cleaned_plate in ACTIVE_SUBSCRIPTIONS:
        sub = ACTIVE_SUBSCRIPTIONS[cleaned_plate]
        exp_date = datetime.strptime(sub["expires"], "%Y-%m-%d")

        if exp_date >= datetime.now():
            result["fastline_eligible"] = True
            result["action"] = "OPEN_BARRIER_INSTANT"
            result["owner"] = sub["owner"]
            result["tier"] = sub["tier"]
            result["message"] = f"Fastline Express: Xush kelibsiz, {sub['owner']}! ({sub['plan']}) Shlagbaum ochildi."
        else:
            result["action"] = "EXPIRED_SUBSCRIPTION"
            result["message"] = "Obuna muddati tugagan! Iltimos, obunani yangilang."

    return result

def main():
    parser = argparse.ArgumentParser(description="Parkly.uz Fastline Express Gate Manager")
    parser.add_argument("--plate", help="Vehicle license plate to check")
    parser.add_argument("--gate", default="ENTRY", choices=["ENTRY", "EXIT"], help="Gate direction")
    parser.add_argument("--sample", action="store_true", help="Run sample Fastline checks")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    if args.sample:
        samples = ["01A777AA", "01888ZZZ", "10123BBA", "01001PPP"]
        results = [process_fastline_crossing(p) for p in samples]
        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:
            print("--- Parkly.uz Fastline Express Sample Test ---")
            for r in results:
                print(f"Plate: {r['plate_number']} | Eligible: {r['fastline_eligible']} | Action: {r['action']} | Msg: {r['message']}")
        sys.exit(0)

    if not args.plate:
        parser.print_help()
        sys.exit(1)

    res = process_fastline_crossing(args.plate, args.gate)
    if args.output == "json":
        print(json.dumps(res, indent=2))
    else:
        print(f"Plate: {res['plate_number']}")
        print(f"Fastline Eligible: {res['fastline_eligible']}")
        print(f"Action: {res['action']}")
        print(f"Message: {res['message']}")

    sys.exit(0 if res["fastline_eligible"] else 1)

if __name__ == "__main__":
    main()
