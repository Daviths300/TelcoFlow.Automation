*** Settings ***
Library    OperatingSystem
Library    Process

*** Variables ***
${PROJECT_ROOT}      ${CURDIR}/../../..
${PYTHON}            ${PROJECT_ROOT}/.venv/bin/python
${TRANSACTION_ID}    TXN-2026-DB-0001
${OUTPUT_FILE}       ${PROJECT_ROOT}/qa/reports/db-payment-reconciliation.json

*** Test Cases ***
SQL Payment Missing From Billing Should Be Detected
    ${result}=    Run Process
    ...    ${PYTHON}
    ...    -m
    ...    qa.python.db_payment_reconciliation
    ...    --transaction-id
    ...    ${TRANSACTION_ID}
    ...    --output
    ...    ${OUTPUT_FILE}
    ...    cwd=${PROJECT_ROOT}

    Should Be Equal As Integers    ${result.rc}    0
    File Should Exist    ${OUTPUT_FILE}

    ${report}=    Get File    ${OUTPUT_FILE}

    Should Contain    ${report}    "source": "sql-server"
    Should Contain    ${report}    "anomaly_detected": true
    Should Contain    ${report}    "anomaly_code": "BILLING_ENTRY_MISSING"
    Should Contain    ${report}    "severity": "HIGH"
    Should Contain    ${report}    "priority": "P0"
