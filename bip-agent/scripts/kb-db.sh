#!/bin/sh
# Start, stop or check the local Postgres that holds the knowledge base.
# Data lives in ../pgdata next to bip-agent/; the server listens on localhost:5432 only.
set -e
BIN="${PG_BIN:-/Applications/Postgres.app/Contents/Versions/latest/bin}"
DATA="${PG_DATA:-$(cd "$(dirname "$0")/../.." && pwd)/pgdata}"
case "${1:-status}" in
  start)  "$BIN/pg_ctl" -D "$DATA" -l "$DATA/server.log" -o "-p 5432 -c listen_addresses=localhost" start ;;
  stop)   "$BIN/pg_ctl" -D "$DATA" stop ;;
  status) "$BIN/pg_ctl" -D "$DATA" status ;;
  init)   "$BIN/initdb" -D "$DATA" -U postgres --auth=trust --encoding=UTF8 --locale=C &&
          "$0" start && sleep 2 && "$BIN/createdb" -U postgres -h localhost bip_kb ;;
  *) echo "usage: $0 start|stop|status|init" >&2; exit 2 ;;
esac
