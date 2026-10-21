#!/usr/bin/env python3
"""
Parkly.uz — Anti-Cheating & Fraud Detection Validator
-----------------------------------------------------
Detects license plate cloning, double-entry mismatches, forged plates,
and unauthorized manual barrier bypass attempts.
"""

import sys
import json
import argparse
from datetime import datetime

# Active vehicles currently inside the parking lot (Simulated DB ledger)
ACTIVE_PARKING_LEDGER = {
    "01A777AA": {"entry_time": "2026-10-21T13:00:00", "slot": "A-101", "session_id": "SES-1050"}
}

def validate_anti_cheat(plate_number: str, action_type: str = "ENTRY") -> dict:
    """
    Validates anti-cheating rules for an incoming or exiting vehicle.
    """
    cleaned_plate = plate_number.strip().upper().replace(" ", "")
    result = {
        "plate_number": cleaned_plate,
        "action_type": action_type,
        "fraud_detected": False,
        "fraud_type": "NONE",
        "severity": "LOW",
        "message": "Validatsiya muvaffaqiyatli o'tdi. Shubhali belgilar yo'q.",
        "timestamp": datetime.now().isoformat()
    }

    if not cleaned_plate or len(cleaned_plate) < 5:
        result["fraud_detected"] = True
        result["fraud_type"] = "INVALID_PLATE_FORMAT"
        result["severity"] = "MEDIUM"
        result["message"] = "Davlat raqami formati noto'g'ri yoki juda qisqa."
        return result

    if action_type == "ENTRY":
        # Check if vehicle is ALREADY inside (Cloned plate / Double entry attempt)
        if cleaned_plate in ACTIVE_PARKING_LEDGER:
            slot_name = ACTIVE_PARKING_LEDGER[cleaned_plate]["slot"]
            result["fraud_detected"] = True
            result["fraud_type"] = "CLONED_PLATE_OR_DOUBLE_ENTRY"
            result["severity"] = "HIGH"
            result["message"] = f"DIQQAT! Ushbu raqam ({cleaned_plate}) allaqachon avtoturargoh ichida ({slot_name}) ro'yxatda turibdi. Ehtimoliy klonlangan raqam!"
            return result

    elif action_type == "EXIT":
        # Check if vehicle is trying to exit WITHOUT entering (Bypass / Ticket skipping)
        if cleaned_plate not in ACTIVE_PARKING_LEDGER:
            result["fraud_detected"] = True
            result["fraud_type"] = "EXIT_WITHOUT_ENTRY_BYPASS"
            result["severity"] = "HIGH"
            result["message"] = f"DIQQAT! Ushbu raqam ({cleaned_plate}) kirish seansiga ega emas. Shlagbaumdan noqonuniy o'tish (Bypass) urinishi!"
            return result

    return result

def main():
    parser = argparse.ArgumentParser(description="Parkly.uz Anti-Cheating & Fraud Validator")
    parser.add_argument("--plate", help="Vehicle license plate to validate")
    parser.add_argument("--action", default="ENTRY", choices=["ENTRY", "EXIT"], help="Action type")
    parser.add_argument("--sample", action="store_true", help="Run sample anti-cheat test scenarios")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    if args.sample:
        scenarios = [
            ("01A777AA", "ENTRY"),  # Should trigger double entry / clone alert (already inside)
            ("09B999BB", "EXIT"),   # Should trigger exit without entry alert (never entered)
            ("10123BBA", "ENTRY")   # Should pass
        ]
        results = [validate_anti_cheat(p, act) for p, act in scenarios]
        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:
            print("--- Parkly.uz Anti-Cheating Sample Test ---")
            for r in results:
                print(f"[{'FRAUD' if r['fraud_detected'] else 'SAFE'}] Plate: {r['plate_number']} | Type: {r['fraud_type']} | Msg: {r['message']}")
        sys.exit(0)

    if not args.plate:
        parser.print_help()
        sys.exit(1)

    res = validate_anti_cheat(args.plate, args.action)
    if args.output == "json":
        print(json.dumps(res, indent=2))
    else:
        print(f"Fraud Detected: {res['fraud_detected']}")
        print(f"Fraud Type: {res['fraud_type']}")
        print(f"Severity: {res['severity']}")
        print(f"Message: {res['message']}")

    sys.exit(2 if res["fraud_detected"] else 0)

if __name__ == "__main__":
    main()
