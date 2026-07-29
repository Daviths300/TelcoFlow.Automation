from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import pyodbc

from qa.python.payment_reconciliation import analyze_payment
from qa.python.sql_payment_repository import fetch_payment_state


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconcile payment state from SQL Server."
    )
    parser.add_argument(
        "--transaction-id",
        required=True,
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
    )
    args = parser.parse_args()

    try:
        payment_state = fetch_payment_state(args.transaction_id)
        result = analyze_payment(payment_state)

        report = {
            "source": "sql-server",
            "payment_state": payment_state,
            "reconciliation": asdict(result),
        }

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

        print(json.dumps(report, indent=2))
        print(f"\nReport: {args.output}")
        return 0

    except (RuntimeError, LookupError, pyodbc.Error) as error:
        print(
            f"Database reconciliation failed: {error}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
