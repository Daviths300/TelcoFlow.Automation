from __future__ import annotations

from dataclasses import asdict

import pyodbc
from fastapi import FastAPI, HTTPException, status

from qa.python.payment_reconciliation import analyze_payment
from qa.python.sql_payment_repository import fetch_payment_state


app = FastAPI(
    title="TelcoFlow Reconciliation API",
    version="0.1.0",
    description=(
        "Detects payment and billing inconsistencies "
        "from the TelcoFlowQA SQL Server database."
    ),
)


def database_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="The reconciliation database is unavailable.",
    )


@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "telcoflow-reconciliation-api",
    }


@app.get("/api/payments/{transaction_id}", tags=["Payments"])
def get_payment(transaction_id: str) -> dict:
    try:
        return fetch_payment_state(transaction_id)

    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except (RuntimeError, pyodbc.Error) as error:
        raise database_error() from error


@app.post(
    "/api/reconciliation/payments/{transaction_id}",
    tags=["Reconciliation"],
)
def reconcile_payment(transaction_id: str) -> dict:
    try:
        payment_state = fetch_payment_state(transaction_id)
        result = analyze_payment(payment_state)

        return {
            "source": "sql-server",
            "payment_state": payment_state,
            "reconciliation": asdict(result),
        }

    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except (RuntimeError, pyodbc.Error) as error:
        raise database_error() from error
