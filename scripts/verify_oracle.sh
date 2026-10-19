#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export ORACLE_PASSWORD="${ORACLE_PASSWORD:-synthetic_dev_only}"
export ORACLE_USER="${ORACLE_USER:-aceu}"
export ORACLE_APP_PASSWORD="${ORACLE_APP_PASSWORD:-synthetic_dev_only}"
export ORACLE_APP_PASSWORD="${ORACLE_APP_PASSWORD:-$ORACLE_PASSWORD}"
export ORACLE_ADMIN_PASSWORD="${ORACLE_ADMIN_PASSWORD:-$ORACLE_PASSWORD}"
export ORACLE_DSN="${ORACLE_DSN:-localhost:1521/FREEPDB1}"
PYTHON_BIN="${PYTHON:-python3}"
WAIT_SECONDS="${ORACLE_WAIT_SECONDS:-300}"

# Start the repository's Oracle Free service and wait for its container health check.
docker compose up -d oracle
container_id="$(docker compose ps -q oracle)"
if [[ -z "$container_id" ]]; then
  echo "Oracle container was not created" >&2
  exit 1
fi
for ((elapsed=0; elapsed<WAIT_SECONDS; elapsed+=2)); do
  state="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$container_id")"
  if [[ "$state" == healthy ]]; then break; fi
  if [[ "$state" == unhealthy || "$state" == exited || "$state" == dead ]]; then
    docker compose logs --tail=80 oracle >&2
    echo "Oracle container entered state: $state" >&2
    exit 1
  fi
  sleep 2
done
if [[ "${state:-}" != healthy ]]; then
  docker compose logs --tail=80 oracle >&2
  echo "Oracle container did not become healthy within ${WAIT_SECONDS}s (state: ${state:-unknown})" >&2
  exit 1
fi

"$PYTHON_BIN" db/apply_schema.py
"$PYTHON_BIN" - <<'PY'
import os
import oracledb

connection = oracledb.connect(
    user=os.environ["ORACLE_USER"],
    password=os.environ["ORACLE_APP_PASSWORD"],
    dsn=os.environ["ORACLE_DSN"],
)
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM scores")
    print(f"Oracle smoke query passed; score rows: {cursor.fetchone()[0]}")
connection.close()
PY
