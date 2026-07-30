#!/usr/bin/env bash

set -Eeuo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_PYTHON="${PROJECT_ROOT}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Python virtual environment was not found." >&2
  echo "Expected: ${VENV_PYTHON}" >&2
  exit 2
fi

echo "Project root: ${PROJECT_ROOT}"
"${VENV_PYTHON}" "${PROJECT_ROOT}/qa/python/environment_check.py"
