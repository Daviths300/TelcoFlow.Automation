USE TelcoFlowQA;
GO

IF OBJECT_ID(N'dbo.subscribers', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.subscribers
    (
        subscriber_id VARCHAR(50) NOT NULL
            CONSTRAINT PK_subscribers PRIMARY KEY,
        msisdn VARCHAR(20) NOT NULL
            CONSTRAINT UQ_subscribers_msisdn UNIQUE,
        balance DECIMAL(18, 2) NOT NULL
            CONSTRAINT DF_subscribers_balance DEFAULT 0,
        status VARCHAR(20) NOT NULL,
        created_at DATETIME2 NOT NULL
            CONSTRAINT DF_subscribers_created_at
            DEFAULT SYSUTCDATETIME()
    );
END;
GO

IF OBJECT_ID(N'dbo.payments', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.payments
    (
        payment_id INT IDENTITY(1, 1) NOT NULL
            CONSTRAINT PK_payments PRIMARY KEY,
        transaction_id VARCHAR(64) NOT NULL
            CONSTRAINT UQ_payments_transaction_id UNIQUE,
        correlation_id VARCHAR(64) NOT NULL,
        subscriber_id VARCHAR(50) NOT NULL,
        amount DECIMAL(18, 2) NOT NULL,
        currency CHAR(3) NOT NULL,
        bank_status VARCHAR(20) NOT NULL,
        payment_service_status VARCHAR(20) NOT NULL,
        created_at DATETIME2 NOT NULL
            CONSTRAINT DF_payments_created_at
            DEFAULT SYSUTCDATETIME(),

        CONSTRAINT FK_payments_subscribers
            FOREIGN KEY (subscriber_id)
            REFERENCES dbo.subscribers(subscriber_id)
    );
END;
GO

IF OBJECT_ID(N'dbo.billing_entries', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.billing_entries
    (
        billing_entry_id INT IDENTITY(1, 1) NOT NULL
            CONSTRAINT PK_billing_entries PRIMARY KEY,
        transaction_id VARCHAR(64) NOT NULL
            CONSTRAINT UQ_billing_entries_transaction_id UNIQUE,
        subscriber_id VARCHAR(50) NOT NULL,
        amount DECIMAL(18, 2) NOT NULL,
        entry_type VARCHAR(30) NOT NULL,
        created_at DATETIME2 NOT NULL
            CONSTRAINT DF_billing_entries_created_at
            DEFAULT SYSUTCDATETIME(),

        CONSTRAINT FK_billing_entries_subscribers
            FOREIGN KEY (subscriber_id)
            REFERENCES dbo.subscribers(subscriber_id)
    );
END;
GO

IF OBJECT_ID(N'dbo.audit_events', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.audit_events
    (
        audit_event_id BIGINT IDENTITY(1, 1) NOT NULL
            CONSTRAINT PK_audit_events PRIMARY KEY,
        correlation_id VARCHAR(64) NOT NULL,
        event_type VARCHAR(50) NOT NULL,
        details NVARCHAR(500) NULL,
        created_at DATETIME2 NOT NULL
            CONSTRAINT DF_audit_events_created_at
            DEFAULT SYSUTCDATETIME()
    );
END;
GO
