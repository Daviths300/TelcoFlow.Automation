# TelcoFlow.Automation

![TelcoFlow Quality Gate](https://github.com/Daviths300/TelcoFlow.Automation/actions/workflows/quality-gate.yml/badge.svg)

TelcoFlow.Automation is a telecom-focused QA automation project for detecting payment and billing inconsistencies in a SQL Server-backed system.

## Core Scenario

The system detects cases where:

- the bank reports a successful payment;
- the payment service reports SUCCESS;
- the billing entry is missing;
- the subscriber balance was not updated.

The API returns the anomaly code, evidence, severity, priority, correlation data, and a recommended action.

## Main Anomaly

- Code: BILLING_ENTRY_MISSING
- Severity: HIGH
- Priority: P0

## Technology Stack

- Python 3.12
- FastAPI
- Microsoft SQL Server 2022
- Docker Compose
- Pytest
- Robot Framework
- Postman and Newman
- Swagger / OpenAPI
- GitHub Actions

## API Endpoints

- GET /health
- GET /api/payments/{transaction_id}
- POST /api/reconciliation/payments/{transaction_id}

## Automated Coverage

- Python unit and integration tests
- SQL-backed reconciliation tests
- Robot Framework acceptance tests
- FastAPI endpoint tests
- Negative 404 transaction scenario
- Postman/Newman API regression suite
- Response schema and response-time assertions

Latest Postman/Newman result:

- 4 requests
- 20 assertions passed
- 0 failures
- Average response time: 35 ms

## Run Locally

1. Create and activate the Python virtual environment.
2. Install dependencies from requirements-dev.txt.
3. Start Docker Desktop.
4. Run docker compose up -d.
5. Execute the complete quality gate:

    ./qa/bash/run_quality_gate.sh

Expected final result:

    TELCOFLOW QUALITY GATE: PASSED

Swagger documentation:

    http://127.0.0.1:8000/docs

## Project Structure

- qa/api — FastAPI application
- qa/bash — unified quality gate
- qa/postman — Collection, Environment and OpenAPI files
- qa/python — Python and database tests
- qa/robot — Robot Framework tests
- qa/sql — schema, seed and reconciliation queries
- .github/workflows — GitHub Actions CI

## Quality Status

- SQL Server integration: Passed
- Pytest: Passed
- Robot Framework: Passed
- FastAPI: Passed
- Postman/Newman: 20/20 Passed
- Local Quality Gate: Passed
- GitHub Actions CI: Passed
