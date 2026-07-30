import pytest

from qa.python.payment_reconciliation import analyze_payment
from qa.python.sql_payment_repository import fetch_payment_state


def test_detects_billing_mismatch_from_sql_server() -> None:
    payment_state = fetch_payment_state("TXN-2026-DB-0001")

    result = analyze_payment(payment_state)

    assert payment_state["bank_status"] == "SUCCESS"
    assert payment_state["payment_service_status"] == "SUCCESS"
    assert payment_state["billing_entry_exists"] is False
    assert payment_state["subscriber_balance_updated"] is False

    assert result.anomaly_detected is True
    assert result.anomaly_code == "BILLING_ENTRY_MISSING"
    assert result.severity == "HIGH"
    assert result.priority == "P0"


def test_unknown_transaction_raises_lookup_error() -> None:
    with pytest.raises(
        LookupError,
        match="Transaction was not found",
    ):
        fetch_payment_state("TXN-DOES-NOT-EXIST")
