*** Settings ***
Library    OperatingSystem
Library    Process

*** Variables ***
${PROJECT_ROOT}    ${CURDIR}/../../..
${INPUT_FILE}      ${PROJECT_ROOT}/qa/python/testdata/payment_success_billing_missing.json
${OUTPUT_FILE}     ${PROJECT_ROOT}/qa/reports/payment-reconciliation.json

*** Test Cases ***
Successful Payment Missing From Billing Should Be Detected
    ${result}=    Run Process
    ...    ${PROJECT_ROOT}/.venv/bin/python
    ...    ${PROJECT_ROOT}/qa/python/payment_reconciliation.py
    ...    --input
    ...    ${INPUT_FILE}
    ...    --output
    ...    ${OUTPUT_FILE}
    ...    cwd=${PROJECT_ROOT}

    Should Be Equal As Integers    ${result.rc}    0
    File Should Exist    ${OUTPUT_FILE}

    ${report}=    Get File    ${OUTPUT_FILE}
    Should Contain    ${report}    "anomaly_code": "BILLING_ENTRY_MISSING"
    Should Contain    ${report}    "severity": "HIGH"
    Should Contain    ${report}    "priority": "P0"
