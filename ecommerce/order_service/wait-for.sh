#!/bin/sh

set -e

host="$1"
shift
cmd="$@"

# Wait for host to be resolvable
until nslookup "$host" >/dev/null 2>&1; do
  >&2 echo "Waiting for $host to be resolvable - sleeping"
  sleep 2
done

# Wait for PostgreSQL to be ready
until PGPASSWORD=postgres psql -h "$host" -U "postgres" -c '\q' >/dev/null 2>&1; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

>&2 echo "Postgres is up - executing command"
exec $cmd