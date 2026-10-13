"""Read-only access to the crawled Receivables metadata catalog.

The catalog lives in receivables-metadata/ (built by crawler/build_catalog.py):
receivables_catalog.json maps object name -> table record, joins.json lists
foreign-key edges. Column rows are [NAME, DATATYPE, LENGTH, PRECISION, NOT_NULL, COMMENT];
views have names only.
"""
from __future__ import annotations

import json
import os
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_DIR = Path(__file__).resolve().parents[2] / "receivables-metadata"

# Columns that are almost never useful in a report and only cost prompt tokens.
WHO_COLUMNS = {
    "LAST_UPDATE_DATE", "LAST_UPDATED_BY", "CREATION_DATE", "CREATED_BY",
    "LAST_UPDATE_LOGIN", "OBJECT_VERSION_NUMBER", "REQUEST_ID", "PROGRAM_ID",
    "PROGRAM_APPLICATION_ID", "PROGRAM_UPDATE_DATE", "JOB_DEFINITION_NAME",
    "JOB_DEFINITION_PACKAGE", "SEED_DATA_SOURCE", "ORA_SEED_SET1", "ORA_SEED_SET2",
}

# Prefixes whose objects should all be in the catalog; a miss there is an error.
IN_SCOPE_PREFIXES = ("AR_", "RA_")
IN_SCOPE_HZ = {
    "HZ_CUST_ACCOUNTS", "HZ_PARTIES", "HZ_CUST_ACCT_SITES_ALL",
    "HZ_CUST_SITE_USES_ALL", "HZ_PARTY_SITES", "HZ_LOCATIONS",
}


@dataclass(frozen=True)
class Column:
    name: str
    datatype: str | None
    length: int | None
    precision: int | None
    not_null: bool | None
    comment: str | None


@dataclass(frozen=True)
class JoinEdge:
    child: str
    child_columns: tuple[str, ...]
    parent: str
    parent_columns: tuple[str, ...]

    def describe(self) -> str:
        pairs = " AND ".join(
            f"{self.child}.{c} = {self.parent}.{p}"
            for c, p in zip(self.child_columns, self.parent_columns)
        )
        return pairs


@dataclass
class TableInfo:
    name: str
    object_type: str
    description: str
    primary_key: tuple[str, ...]
    columns: dict[str, Column]
    flexfield_summary: str | None
    source_url: str | None
    raw: dict = field(repr=False, default_factory=dict)

    @property
    def is_view(self) -> bool:
        return self.object_type == "VIEW"

    def has_column(self, col: str) -> bool:
        col = col.upper()
        if col in self.columns:
            return True
        # Flexfield columns are summarised, not listed.
        return _is_flexfield(col) and bool(self.flexfield_summary)


_PRIORITY_WORDS = ("NUMBER", "NAME", "DATE", "AMOUNT", "STATUS", "CLASS", "TYPE", "CODE", "CURRENCY")


def _column_priority(col: str, table: "TableInfo", keep: set[str] | None,
                     join_columns: set[str] | None) -> int:
    score = 0
    if col in table.primary_key:
        score += 10
    if join_columns and col in join_columns:
        score += 8
    if col == "ORG_ID":
        score += 6
    if keep and set(col.split("_")) & keep:
        score += 5
    if any(w in col for w in _PRIORITY_WORDS):
        score += 4
    if col.endswith("_ID"):
        score += 1
    return score


def _is_flexfield(col: str) -> bool:
    return col.startswith(("ATTRIBUTE", "GLOBAL_ATTRIBUTE", "EXTN_ATTRIBUTE"))


class Catalog:
    def __init__(self, tables: dict[str, TableInfo], joins: list[JoinEdge]):
        self.tables = tables
        self.joins = joins
        self._edges_by_table: dict[str, list[JoinEdge]] = defaultdict(list)
        for e in joins:
            self._edges_by_table[e.child].append(e)
            if e.parent != e.child:
                self._edges_by_table[e.parent].append(e)

    # ---- loading -------------------------------------------------------
    @classmethod
    def load(cls, directory: str | os.PathLike | None = None) -> "Catalog":
        d = Path(directory or os.environ.get("BIP_AGENT_CATALOG_DIR") or DEFAULT_DIR)
        cat_file = d / "catalog.json" if (d / "catalog.json").exists() else d / "receivables_catalog.json"
        raw_catalog = json.loads(cat_file.read_text())
        raw_joins = json.loads((d / "joins.json").read_text())
        return cls.from_raw(raw_catalog, raw_joins)

    @classmethod
    def from_raw(cls, raw_catalog: dict, raw_joins: list) -> "Catalog":
        tables = {}
        for name, t in raw_catalog.items():
            cols = {}
            for row in t.get("columns") or []:
                row = list(row) + [None] * (6 - len(row))
                cols[row[0].upper()] = Column(row[0].upper(), *row[1:6])
            pk = t.get("primary_key") or {}
            tables[name.upper()] = TableInfo(
                name=name.upper(),
                object_type=t.get("object_type") or "TABLE",
                description=t.get("description") or "",
                primary_key=tuple(pk.get("columns") or ()),
                columns=cols,
                flexfield_summary=t.get("flexfield_columns"),
                source_url=t.get("source_url"),
                raw=t,
            )
        joins = []
        for e in raw_joins:
            child_cols = tuple(c.strip().upper() for c in str(e["child_column"]).split(","))
            parent_cols = (
                tuple(c.strip().upper() for c in str(e["parent_column"]).split(","))
                if e.get("parent_column")
                else tuple(e.get("parent_pk") or ())
            )
            if not parent_cols:
                # e.g. "RECEIVABLES_TRX_ID, ORG_ID -> AR_RECEIVABLES_TRX_ALL": same names on both sides.
                parent_cols = child_cols
            joins.append(JoinEdge(e["child"].upper(), child_cols, e["parent"].upper(), parent_cols))
        return cls(tables, joins)

    # ---- lookups -------------------------------------------------------
    def get(self, name: str) -> TableInfo | None:
        return self.tables.get(name.upper())

    def __contains__(self, name: str) -> bool:
        return name.upper() in self.tables

    def edges_for(self, table: str) -> list[JoinEdge]:
        return self._edges_by_table.get(table.upper(), [])

    def edges_between(self, a: str, b: str) -> list[JoinEdge]:
        a, b = a.upper(), b.upper()
        return [e for e in self.edges_for(a) if {e.child, e.parent} == {a, b} or (a == b == e.child == e.parent)]

    def is_known_join(self, t1: str, c1: str, t2: str, c2: str) -> bool:
        """True if t1.c1 = t2.c2 matches (one column pair of) a documented FK edge."""
        t1, c1, t2, c2 = t1.upper(), c1.upper(), t2.upper(), c2.upper()
        for e in self.edges_for(t1):
            pairs = set(zip(e.child_columns, e.parent_columns))
            if e.child == t1 and e.parent == t2 and (c1, c2) in pairs:
                return True
            if e.parent == t1 and e.child == t2 and (c2, c1) in pairs:
                return True
        return False

    def join_path(self, start: str, goal: str, max_hops: int = 3) -> list[JoinEdge] | None:
        """Shortest FK path between two catalog objects (BFS, both directions)."""
        start, goal = start.upper(), goal.upper()
        if start == goal:
            return []
        frontier = [(start, [])]
        seen = {start}
        for _ in range(max_hops):
            nxt = []
            for node, path in frontier:
                for e in self.edges_for(node):
                    other = e.parent if e.child == node else e.child
                    if other in seen or other not in self.tables:
                        continue
                    if other == goal:
                        return path + [e]
                    seen.add(other)
                    nxt.append((other, path + [e]))
            frontier = nxt
        return None

    def in_scope(self, name: str) -> bool:
        """Objects the catalog is meant to cover completely: AR_/RA_, the core HZ_ tables, and
        every other product prefix (AP, GL, XLA, ...) that has tables in the catalog."""
        name = name.upper()
        if name.startswith(IN_SCOPE_PREFIXES) or name in IN_SCOPE_HZ:
            return True
        if not hasattr(self, "_prefixes"):
            self._prefixes = {n.split("_", 1)[0] + "_" for n in self.tables}
        return name.split("_", 1)[0] + "_" in self._prefixes

    # ---- prompt rendering ---------------------------------------------
    def describe_table(self, name: str, include_who: bool = False, max_desc: int = 400,
                       comments: bool = True, max_columns: int | None = None,
                       keep: set[str] | None = None, join_columns: set[str] | None = None) -> str:
        """Prompt text for one object. max_columns keeps the columns most likely to
        matter in a report (keys, names, numbers, dates, amounts, statuses, and
        any whose name shares a word with keep) and notes how many were left out."""
        t = self.get(name)
        if t is None:
            return f"{name}: not in catalog"
        lines = [f"### {t.name} ({t.object_type})"]
        if t.description:
            desc = t.description if len(t.description) <= max_desc else t.description[:max_desc] + "..."
            lines.append(desc)
        if t.primary_key:
            lines.append(f"PK: {', '.join(t.primary_key)}")
        cols = []
        candidates = [c for c in t.columns.values() if include_who or c.name not in WHO_COLUMNS]
        hidden = 0
        if max_columns is not None and len(candidates) > max_columns:
            chosen = {c.name for c in sorted(candidates, key=lambda c: -_column_priority(c.name, t, keep, join_columns))[:max_columns]}
            hidden = len(candidates) - len(chosen)
            candidates = [c for c in candidates if c.name in chosen]
        for c in candidates:
            if t.is_view:
                cols.append(c.name)
                continue
            dt = c.datatype or "?"
            if c.length:
                dt += f"({c.length})"
            comment = (c.comment or "").strip() if comments else ""
            if len(comment) > 90:
                comment = comment[:90] + "..."
            cols.append(f"{c.name} {dt}" + (f" -- {comment}" if comment else ""))
        if hidden:
            cols.append(f"... {hidden} more columns (describe_table {t.name} lists all)")
        lines.append("Columns:\n  " + "\n  ".join(cols))
        if t.flexfield_summary:
            lines.append(f"Flexfields: {t.flexfield_summary[:200]}")
        return "\n".join(lines)
