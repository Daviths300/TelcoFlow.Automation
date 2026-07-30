USE TelcoFlowQA;
GO

IF NOT EXISTS
(
    SELECT 1
    FROM dbo.subscribers
    WHERE subscriber_id = 'SUB-DB-10001'
)
BEGIN
    INSERT INTO dbo.subscribers
    (
        subscriber_id,
        msisdn,
        balance,
        status
    )
    VALUES
    (
        'SUB-DB-10001',
        '995555100001',
        0.00,
        'ACTIVE'
    );
END
ELSE
BEGIN
    UPDATE dbo.subscribers
    SET balance = 0.00,
        status = 'ACTIVE'
    WHERE subscriber_id = 'SUB-DB-10001';
END;
GO

IF NOT EXISTS
(
    SELECT 1
    FROM dbo.payments
    WHERE transaction_id = 'TXN-2026-DB-0001'
)
BEGIN
    INSERT INTO dbo.payments
    (
        transaction_id,
        correlation_id,
        subscriber_id,
        amount,
        currency,
        bank_status,
        payment_service_status
    )
    VALUES
    (
        'TXN-2026-DB-0001',
        'CORR-2026-DB-0001',
        'SUB-DB-10001',
        25.00,
        'GEL',
        'SUCCESS',
        'SUCCESS'
    );
END
ELSE
BEGIN
    UPDATE dbo.payments
    SET bank_status = 'SUCCESS',
        payment_service_status = 'SUCCESS',
        amount = 25.00
    WHERE transaction_id = 'TXN-2026-DB-0001';
END;
GO

-- Billing entry deliberately removed to reproduce the defect.
DELETE FROM dbo.billing_entries
WHERE transaction_id = 'TXN-2026-DB-0001';
GO

IF NOT EXISTS
(
    SELECT 1
    FROM dbo.audit_events
    WHERE correlation_id = 'CORR-2026-DB-0001'
      AND event_type = 'PAYMENT_CONFIRMED'
)
BEGIN
    INSERT INTO dbo.audit_events
    (
        correlation_id,
        event_type,
        details
    )
    VALUES
    (
        'CORR-2026-DB-0001',
        'PAYMENT_CONFIRMED',
        N'Bank and payment service reported success.'
    );
END;
GO
