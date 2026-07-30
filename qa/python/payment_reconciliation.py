from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReconciliationResult:
    transaction_id: str
    correlation_id: str
    anomaly_detected: bool
    anomaly_code: str | None
    severity: str
    priority: str
    summary: str
    evidence: dict[str, Any]
    recommended_action: str


def analyze_payment(payload: dict[str, Any]) -> ReconciliationResult:
    required_fields = {
        "transaction_id",
        "correlation_id",
        "bank_status",
        "payment_service_status",
        "billing_entry_exists",
        "subscriber_balance_updated",
    }

    missing_fields = sorted(required_fields - payload.keys())
    if missing_fields:
        raise ValueError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )

    bank_success = payload["bank_status"].upper() == "SUCCESS"
    payment_success = (
        payload["payment_service_status"].upper() == "SUCCESS"
    )
    billing_missing = not payload["billing_entry_exists"]
    balance_not_updated = not payload["subscriber_balance_updated"]

    evidence = {
        "bank_status": payload["bank_status"],
        "payment_service_status": payload["payment_service_status"],
        "billing_entry_exists": payload["billing_entry_exists"],
        "subscriber_balance_updated": payload[
            "subscriber_balance_updated"
        ],
    }

    if (
        bank_success
        and payment_success
        and billing_missing
        and balance_not_updated
    ):
        return ReconciliationResult(
            transaction_id=payload["transaction_id"],
            correlation_id=payload["correlation_id"],
            anomaly_detected=True,
            anomaly_code="BILLING_ENTRY_MISSING",
            severity="HIGH",
            priority="P0",
            summary=(
                "Payment succeeded externally, but no billing entry "
                "or subscriber balance update was found."
            ),
            evidence=evidence,
            recommended_action=(
                "Block duplicate payment attempts, begin reconciliation, "
                "and trace the transaction using the correlation ID."
            ),
        )

    return ReconciliationResult(
        transaction_id=payload["transaction_id"],
        correlation_id=payload["correlation_id"],
        anomaly_detected=False,
        anomaly_code=None,
        severity="NONE",
        priority="NONE",
        summary="Payment and billing states are consistent.",
        evidence=evidence,
        recommended_action="No reconciliation action is required.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze payment and billing consistency."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = analyze_payment(payload)

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(asdict(result), indent=2),
            encoding="utf-8",
        )

        print(json.dumps(asdict(result), indent=2))
        print(f"\nReport: {args.output}")
        return 0

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Reconciliation failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
