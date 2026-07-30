#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

source .venv/bin/activate

echo "== 1/6 Docker + SQL Server =="
docker compose up -d

for attempt in {1..18}; do
  STATUS="$(docker inspect \
    --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}unknown{{end}}' \
    telcoflow-sqlserver 2>/dev/null || true)"

  if [[ "$STATUS" == "healthy" ]]; then
    echo "SQL Server: healthy"
    break
  fi

  if [[ "$attempt" == "18" ]]; then
    echo "SQL Server did not become healthy."
    exit 1
  fi

  sleep 5
done

echo "== 2/6 SQL connection =="
python qa/python/sql_connection_check.py

echo "== 3/6 Pytest =="
pytest -q

echo "== 4/6 Robot Framework =="
mkdir -p qa/reports/robot
robot \
  --outputdir qa/reports/robot \
  qa/robot/tests

echo "== 5/6 FastAPI health =="

API_STARTED=0
API_PID=""

cleanup() {
  if [[ "$API_STARTED" == "1" ]] && [[ -n "$API_PID" ]]; then
    kill "$API_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

if ! curl -fsS http://127.0.0.1:8000/health >/dev/null; then
  fastapi dev qa/api/app.py >/tmp/telcoflow-api.log 2>&1 &
  API_PID=$!
  API_STARTED=1

  for attempt in {1..20}; do
    if curl -fsS http://127.0.0.1:8000/health >/dev/null; then
      break
    fi

    if [[ "$attempt" == "20" ]]; then
      cat /tmp/telcoflow-api.log
      exit 1
    fi

    sleep 1
  done
fi

curl -fsS \
  http://127.0.0.1:8000/health \
  | python -m json.tool

echo "== 6/6 Postman/Newman =="
mkdir -p qa/reports/postman

npx --yes newman run \
  "qa/postman/TelcoFlow Reconciliation API.postman_collection.json" \
  -e "qa/postman/TelcoFlow Local.postman_environment.json" \
  --env-var "baseUrl=http://127.0.0.1:8000" \
  --reporters cli,junit \
  --reporter-junit-export qa/reports/postman/newman.xml

echo
echo "================================="
echo "TELCOFLOW QUALITY GATE: PASSED"
echo "================================="
