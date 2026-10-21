#!/usr/bin/env python3
"""
Parkly.uz — Payment Check Blacklist & Fraud Prevention Filter
-------------------------------------------------------------
Validates payment check IDs, transaction hashes, and digital receipts
against a fraud blacklist to prevent fake, spoofed, or re-used payment slips.
"""

import sys
import json
import argparse
from datetime import datetime

# Known blacklisted or previously used transaction hashes / fake receipts (simulated ledger)
BLACKLISTED_TRANSACTIONS = {
    "TX-FAKE-9999",
    "TX-EXPIRED-001",
    "TX-REUSED-123",
    "TX-SPOOFED-777",
    "CHECK-NULL-000"
}

USED_TRANSACTION_LEDGER = set()

def check_payment_validity(tx_id: str, provider: str, amount: float, signature: str = "") -> dict:
    """
    Checks if a payment check/transaction is valid or blacklisted/reused.
    """
    result = {
        "transaction_id": tx_id,
        "provider": provider,
        "amount": amount,
        "status": "APPROVED",
        "reason": "OK",
        "timestamp": datetime.now().isoformat()
    }

    if not tx_id or not tx_id.strip():
        result["status"] = "REJECTED"
        result["reason"] = "EMPTY_TRANSACTION_ID"
        return result

    cleaned_tx = tx_id.strip().upper()

    # 1. Blacklist check
    if cleaned_tx in BLACKLISTED_TRANSACTIONS:
        result["status"] = "BLACKLISTED"
        result["reason"] = "Transaction is blacklisted as fraudulent or fake."
        return result

    # 2. Re-use check (Double-spending / Replay attack)
    if cleaned_tx in USED_TRANSACTION_LEDGER:
        result["status"] = "REJECTED"
        result["reason"] = "DOUBLE_SPEND_ATTEMPT: Receipt/Transaction ID has already been used."
        return result

    # 3. Amount validation check
    if amount <= 0:
        result["status"] = "REJECTED"
        result["reason"] = "INVALID_AMOUNT: Amount must be greater than zero."
        return result

    # Mark as used in ledger
    USED_TRANSACTION_LEDGER.add(cleaned_tx)
    return result

def main():
    parser = argparse.ArgumentParser(description="Parkly.uz Payment Check Blacklist & Fraud Filter")
    parser.add_argument("--tx", help="Transaction ID or Check Hash to verify")
    parser.add_argument("--provider", default="PAYME", help="Payment provider (CLICK, PAYME, UZUM)")
    parser.add_argument("--amount", type=float, default=15000.0, help="Payment amount in UZS")
    parser.add_argument("--sample", action="store_true", help="Run sample verification tests")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    if args.sample:
        samples = [
            ("TX-992145", "PAYME", 15000.0),
            ("TX-FAKE-9999", "CLICK", 20000.0),
            ("TX-992145", "PAYME", 15000.0),  # Reused attempt
            ("TX-NEW-8812", "UZUM", 50000.0)
        ]
        results = []
        for tx, prov, amt in samples:
            results.append(check_payment_validity(tx, prov, amt))

        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:
            print("--- Parkly.uz Payment Blacklist Filter Sample Test ---")
            for res in results:
                print(f"[{res['status']}] Tx: {res['transaction_id']} | Provider: {res['provider']} | Reason: {res['reason']}")
        sys.exit(0)

    if not args.tx:
        parser.print_help()
        sys.exit(1)

    res = check_payment_validity(args.tx, args.provider, args.amount)
    if args.output == "json":
        print(json.dumps(res, indent=2))
    else:
        print(f"Status: {res['status']}")
        print(f"Reason: {res['reason']}")
        print(f"Timestamp: {res['timestamp']}")

    if res["status"] != "APPROVED":
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
