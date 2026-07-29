from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from qa.api.app import app


client = TestClient(app)


def payment_state() -> dict[str, Any]:
    return {
        "transaction_id": "TXN-2026-DB-0001",
        "correlation_id": "CORR-2026-DB-0001",
        "subscriber_id": "SUB-DB-10001",
        "amount": 25.0,
        "currency": "GEL",
        "bank_status": "SUCCESS",
        "payment_service_status": "SUCCESS",
        "billing_entry_exists": False,
        "subscriber_balance_updated": False,
    }


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "telcoflow-reconciliation-api",
    }


def test_payment_endpoint_returns_payment_state(monkeypatch) -> None:
    monkeypatch.setattr(
        "qa.api.app.fetch_payment_state",
        lambda transaction_id: payment_state(),
    )

    response = client.get(
        "/api/payments/TXN-2026-DB-0001"
    )

    assert response.status_code == 200
    assert response.json()["transaction_id"] == "TXN-2026-DB-0001"
    assert response.json()["billing_entry_exists"] is False


def test_reconciliation_endpoint_detects_anomaly(monkeypatch) -> None:
    monkeypatch.setattr(
        "qa.api.app.fetch_payment_state",
        lambda transaction_id: payment_state(),
    )

    response = client.post(
        "/api/reconciliation/payments/TXN-2026-DB-0001"
    )

    body = response.json()

    assert response.status_code == 200
    assert body["source"] == "sql-server"
    assert body["reconciliation"]["anomaly_detected"] is True
    assert (
        body["reconciliation"]["anomaly_code"]
        == "BILLING_ENTRY_MISSING"
    )
    assert body["reconciliation"]["severity"] == "HIGH"
    assert body["reconciliation"]["priority"] == "P0"


def test_missing_transaction_returns_404(monkeypatch) -> None:
    def raise_not_found(transaction_id: str) -> dict:
        raise LookupError(
            f"Transaction was not found: {transaction_id}"
        )

    monkeypatch.setattr(
        "qa.api.app.fetch_payment_state",
        raise_not_found,
    )

    response = client.get(
        "/api/payments/TXN-DOES-NOT-EXIST"
    )

    assert response.status_code == 404
    assert "Transaction was not found" in response.json()["detail"]


def test_database_failure_returns_503(monkeypatch) -> None:
    def raise_database_error(transaction_id: str) -> dict:
        raise RuntimeError("Database configuration unavailable")

    monkeypatch.setattr(
        "qa.api.app.fetch_payment_state",
        raise_database_error,
    )

    response = client.post(
        "/api/reconciliation/payments/TXN-2026-DB-0001"
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "The reconciliation database is unavailable."
    )
