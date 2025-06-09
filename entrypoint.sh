#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Function to check if Postgres is ready
postgres_ready() {
    python << END
import sys
import psycopg2
from urllib.parse import urlparse
try:
    result = urlparse("${DATABASE_URL}")
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

# Wait for PostgreSQL to become available
until postgres_ready; do
  echo >&2 "Waiting for PostgreSQL to become available..."
  sleep 1
done
echo >&2 "PostgreSQL is available"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start Uvicorn
echo "Starting Uvicorn..."

PORT=9000
HOST=0.0.0.0
WORKERS=3
TIMEOUT=60

exec uvicorn app:app \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    --timeout-keep-alive $TIMEOUT \
    --log-level info
