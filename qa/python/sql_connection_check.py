from __future__ import annotations

import os
import sys

import pyodbc
from dotenv import load_dotenv


def main() -> int:
    load_dotenv()

    password = os.getenv("MSSQL_SA_PASSWORD")
    port = os.getenv("MSSQL_PORT", "14333")

    if not password:
        print(
            "MSSQL_SA_PASSWORD is missing from .env",
            file=sys.stderr,
        )
        return 2

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER=localhost,{port};"
        "DATABASE=TelcoFlowQA;"
        "UID=sa;"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=10;"
    )

    try:
        with pyodbc.connect(connection_string) as connection:
            cursor = connection.cursor()

            database_name = cursor.execute(
                "SELECT DB_NAME();"
            ).fetchval()

            payment_count = cursor.execute(
                "SELECT COUNT(*) FROM dbo.payments;"
            ).fetchval()

            transaction = cursor.execute(
                """
                SELECT
                    transaction_id,
                    bank_status,
                    payment_service_status
                FROM dbo.payments
                WHERE transaction_id = 'TXN-2026-DB-0001';
                """
            ).fetchone()

            print(f"Database: {database_name}")
            print(f"Payment rows: {payment_count}")

            if transaction is None:
                print(
                    "Target transaction was not found.",
                    file=sys.stderr,
                )
                return 1

            print(f"Transaction: {transaction[0]}")
            print(f"Bank status: {transaction[1]}")
            print(f"Payment service status: {transaction[2]}")

        print("SQL connection check: PASS")
        return 0

    except pyodbc.Error as error:
        print(
            f"SQL connection check: FAIL\n{error}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
