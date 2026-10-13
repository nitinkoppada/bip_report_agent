"""Minimal Postgres access through the psql client (no Python driver needed).

Queries return rows as dicts: the SQL is wrapped in json_agg so psql prints one
JSON document. The connection string comes from BIP_AGENT_DB_URL (default
postgresql://postgres@localhost:5432/bip_kb); the psql binary from
BIP_AGENT_PSQL, the PATH, or Postgres.app.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

DEFAULT_DB_URL = "postgresql://postgres@localhost:5432/bip_kb"
_POSTGRES_APP = Path("/Applications/Postgres.app/Contents/Versions/latest/bin/psql")


class DBError(RuntimeError):
    pass


def db_url() -> str:
    return os.environ.get("BIP_AGENT_DB_URL", DEFAULT_DB_URL)


def psql_path() -> str:
    for cand in (os.environ.get("BIP_AGENT_PSQL"), shutil.which("psql"), str(_POSTGRES_APP)):
        if cand and Path(cand).exists():
            return cand
    raise DBError("psql not found; install Postgres (e.g. Postgres.app) or set BIP_AGENT_PSQL")


class PG:
    def __init__(self, url: str | None = None, timeout: float = 600.0):
        self.url = url or db_url()
        self.timeout = timeout

    def _run(self, args: list[str], stdin: str | None = None) -> str:
        cmd = [psql_path(), "-X", "-q", "-v", "ON_ERROR_STOP=1", "-At", "-d", self.url] + args
        try:
            p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=self.timeout)
        except subprocess.TimeoutExpired as exc:
            raise DBError(f"psql timed out after {self.timeout:.0f}s") from exc
        if p.returncode != 0:
            raise DBError(p.stderr.strip()[:2000] or f"psql exited with {p.returncode}")
        return p.stdout

    def execute(self, sql: str) -> None:
        """Run one or more statements (a script) in a single transaction."""
        self._run(["-1", "-f", "-"], stdin=sql)

    def query(self, sql: str) -> list[dict]:
        """Rows of one SELECT as dicts."""
        out = self._run(["-f", "-"], stdin=f"SELECT coalesce(json_agg(q), '[]'::json) FROM ({sql}) q;")
        return json.loads(out.strip() or "[]")

    def scalar(self, sql: str):
        rows = self.query(sql)
        return next(iter(rows[0].values())) if rows else None

    def available(self) -> bool:
        try:
            return self.scalar("SELECT 1 AS ok") == 1
        except DBError:
            return False


def lit(value) -> str:
    """SQL literal for a Python value (strings are dollar-quoted safely)."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return repr(value)
    s = str(value)
    tag = "q"
    while f"${tag}$" in s:
        tag += "q"
    return f"${tag}${s}${tag}$"
