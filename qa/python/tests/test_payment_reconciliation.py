from qa.python.payment_reconciliation import analyze_payment


def test_detects_successful_payment_missing_from_billing() -> None:
    payload = {
        "transaction_id": "TXN-001",
        "correlation_id": "CORR-001",
        "bank_status": "SUCCESS",
        "payment_service_status": "SUCCESS",
        "billing_entry_exists": False,
        "subscriber_balance_updated": False,
    }

    result = analyze_payment(payload)

    assert result.anomaly_detected is True
    assert result.anomaly_code == "BILLING_ENTRY_MISSING"
    assert result.severity == "HIGH"
    assert result.priority == "P0"


def test_accepts_consistent_payment_and_billing_state() -> None:
    payload = {
        "transaction_id": "TXN-002",
        "correlation_id": "CORR-002",
        "bank_status": "SUCCESS",
        "payment_service_status": "SUCCESS",
        "billing_entry_exists": True,
        "subscriber_balance_updated": True,
    }

    result = analyze_payment(payload)

    assert result.anomaly_detected is False
    assert result.anomaly_code is None
    assert result.severity == "NONE"
