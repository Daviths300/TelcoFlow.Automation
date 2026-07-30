SET NOCOUNT ON;

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

WHERE p.transaction_id = 'TXN-2026-DB-0001';
