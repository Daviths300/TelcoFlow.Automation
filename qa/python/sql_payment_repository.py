from __future__ import annotations

import os
from typing import Any

import pyodbc
from dotenv import load_dotenv


def build_connection_string() -> str:
    load_dotenv()

    password = os.getenv("MSSQL_SA_PASSWORD")
    port = os.getenv("MSSQL_PORT", "14333")

    if not password:
        raise RuntimeError("MSSQL_SA_PASSWORD is missing from .env")

    return (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER=localhost,{port};"
        "DATABASE=TelcoFlowQA;"
        "UID=sa;"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=10;"
    )


def fetch_payment_state(transaction_id: str) -> dict[str, Any]:
    query = """
        SELECT
            p.transaction_id,
            p.correlation_id,
            p.subscriber_id,
            p.amount,
            p.currency,
            p.bank_status,
            p.payment_service_status,
            CASE
                WHEN b.billing_entry_id IS NULL THEN 0
                ELSE 1
            END AS billing_entry_exists,
            CASE
                WHEN s.balance >= p.amount THEN 1
                ELSE 0
            END AS subscriber_balance_updated
        FROM dbo.payments AS p
        INNER JOIN dbo.subscribers AS s
            ON s.subscriber_id = p.subscriber_id
        LEFT JOIN dbo.billing_entries AS b
            ON b.transaction_id = p.transaction_id
        WHERE p.transaction_id = ?;
    """

    with pyodbc.connect(build_connection_string()) as connection:
        cursor = connection.cursor()
        row = cursor.execute(query, transaction_id).fetchone()

    if row is None:
        raise LookupError(
            f"Transaction was not found: {transaction_id}"
        )

    return {
        "transaction_id": row[0],
        "correlation_id": row[1],
        "subscriber_id": row[2],
        "amount": float(row[3]),
        "currency": row[4],
        "bank_status": row[5],
        "payment_service_status": row[6],
        "billing_entry_exists": bool(row[7]),
        "subscriber_balance_updated": bool(row[8]),
    }
