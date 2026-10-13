"""Reviewed reference reports used as worked examples in the prompt.

examples/specs/ holds hand-written specs whose SQL and business rules have been
checked. The agent shows the model the one or two closest to the request, so it
copies Fusion conventions (payment schedules for balances, days-past-due
arithmetic, null-tolerant parameters) instead of inventing them.

Hold examples out with exclude=[...] or BIP_AGENT_HOLDOUT=name1,name2, e.g. to
test a request that an example answers word for word.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples" / "specs"

_STOP = {"THE", "AND", "FOR", "WITH", "BY", "OF", "TO", "IN", "AN", "A", "ON", "AS", "OR",
         "SHOWING", "REPORT", "OPTIONAL", "FILTER", "FILTERS", "ALL", "EACH", "PER"}


@dataclass
class Example:
    name: str
    spec: dict

    def words(self) -> set[str]:
        return _words(" ".join([self.name, self.spec.get("title", ""), self.spec.get("description", "")]))

    def render(self) -> str:
        s = self.spec
        params = ", ".join(
            f"{p['name']} ({p['data_type']}{', required' if p.get('required') else ', optional'})"
            for p in s.get("parameters", []))
        lines = [f"### Example: {s.get('title', self.name)}",
                 f"Request: {s.get('description', '')}",
                 "SQL:", s["sql"].strip(),
                 f"Parameters: {params or 'none'}",
                 "Business rules:"]
        lines += [f"- {a}" for a in s.get("assumptions", [])]
        return "\n".join(lines)


def _words(text: str) -> set[str]:
    out = set()
    for w in re.findall(r"[A-Za-z]+", text.upper()):
        if len(w) > 1 and w not in _STOP:
            out.add(w[:-1] if w.endswith("S") and len(w) > 4 else w)
    return out


def load_examples(directory: Path | None = None) -> list[Example]:
    d = Path(directory) if directory else EXAMPLES_DIR
    if not d.is_dir():
        return []
    return [Example(p.stem, json.loads(p.read_text())) for p in sorted(d.glob("*.json"))]


def pick_examples(request: str, examples: list[Example], k: int = 1,
                  exclude: list[str] | None = None) -> list[Example]:
    """The k examples sharing the most words with the request (ties keep file order)."""
    held = {x.strip().lower() for x in (exclude or []) if x.strip()}
    held |= {x.strip().lower() for x in os.environ.get("BIP_AGENT_HOLDOUT", "").split(",") if x.strip()}
    req = _words(request)
    pool = [e for e in examples if e.name.lower() not in held]
    scored = sorted(pool, key=lambda e: -len(req & e.words()))
    return scored[:k]
