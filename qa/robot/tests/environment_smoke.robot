*** Settings ***
Library    OperatingSystem
Library    Process

*** Variables ***
${PROJECT_ROOT}    ${CURDIR}/../../..

*** Test Cases ***
QA Project Structure Should Exist
    Directory Should Exist    ${PROJECT_ROOT}/qa/python
    Directory Should Exist    ${PROJECT_ROOT}/qa/bash
    Directory Should Exist    ${PROJECT_ROOT}/qa/robot
    Directory Should Exist    ${PROJECT_ROOT}/qa/sql
    Directory Should Exist    ${PROJECT_ROOT}/infrastructure

Python Environment Check Should Pass
    ${result}=    Run Process
    ...    ${PROJECT_ROOT}/.venv/bin/python
    ...    ${PROJECT_ROOT}/qa/python/environment_check.py
    ...    cwd=${PROJECT_ROOT}
    Should Be Equal As Integers    ${result.rc}    0
