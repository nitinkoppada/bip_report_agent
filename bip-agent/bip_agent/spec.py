"""The report specification the model returns, and its JSON schema."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

DATA_TYPES = ("string", "number", "date")

REPORT_SPEC_SCHEMA = {
    "type": "object",
    "properties": {
        "report_name": {"type": "string", "description": "UPPER_SNAKE_CASE name, e.g. AR_AGING_BY_CUSTOMER"},
        "title": {"type": "string", "description": "Human title printed on the layout"},
        "description": {"type": "string"},
        "sql": {"type": "string", "description": "One Oracle SELECT statement; every column qualified with its table alias"},
        "parameters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Bind name without colon, e.g. P_AS_OF_DATE"},
                    "label": {"type": "string"},
                    "data_type": {"type": "string", "enum": list(DATA_TYPES)},
                    "default_value": {"type": "string", "description": "Empty string for none"},
                    "required": {"type": "boolean"},
                },
                "required": ["name", "label", "data_type", "default_value", "required"],
                "additionalProperties": False,
            },
        },
        "columns": {
            "type": "array",
            "description": "Output columns in SELECT order; names equal the SELECT aliases",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "label": {"type": "string"},
                    "data_type": {"type": "string", "enum": list(DATA_TYPES)},
                    "is_break": {"type": "boolean", "description": "true for group-header columns (e.g. customer)"},
                    "total": {"type": "boolean", "description": "true to sum this numeric column in the layout"},
                },
                "required": ["name", "label", "data_type", "is_break", "total"],
                "additionalProperties": False,
            },
        },
        "tables_used": {"type": "array", "items": {"type": "string"}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["report_name", "title", "description", "sql", "parameters", "columns",
                 "tables_used", "assumptions"],
    "additionalProperties": False,
}


@dataclass
class Parameter:
    name: str
    label: str
    data_type: str = "string"
    default_value: str = ""
    required: bool = False


@dataclass
class OutputColumn:
    name: str
    label: str
    data_type: str = "string"
    is_break: bool = False
    total: bool = False


@dataclass
class ReportSpec:
    report_name: str
    title: str
    description: str
    sql: str
    parameters: list[Parameter] = field(default_factory=list)
    columns: list[OutputColumn] = field(default_factory=list)
    tables_used: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "ReportSpec":
        return cls(
            report_name=_safe_name(d["report_name"]),
            title=d.get("title") or d["report_name"],
            description=d.get("description", ""),
            sql=d["sql"].strip().rstrip(";").strip(),
            parameters=[Parameter(**{**p, "name": p["name"].lstrip(":").upper()}) for p in d.get("parameters", [])],
            columns=[OutputColumn(**{**c, "name": c["name"].upper()}) for c in d.get("columns", [])],
            tables_used=[t.upper() for t in d.get("tables_used", [])],
            assumptions=list(d.get("assumptions", [])),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def break_columns(self) -> list[OutputColumn]:
        return [c for c in self.columns if c.is_break]

    @property
    def detail_columns(self) -> list[OutputColumn]:
        return [c for c in self.columns if not c.is_break]

    def check(self) -> list[str]:
        """Spec-level problems (the SQL itself is checked by validator.validate_sql)."""
        errs = []
        if not self.columns:
            errs.append("spec has no output columns")
        if self.columns and not self.detail_columns:
            errs.append("every column is a break column; at least one detail column is needed")
        names = [c.name for c in self.columns]
        dup = {n for n in names if names.count(n) > 1}
        if dup:
            errs.append(f"duplicate column names: {', '.join(sorted(dup))}")
        for c in self.columns:
            if not re.fullmatch(r"[A-Z][A-Z0-9_]{0,29}", c.name):
                errs.append(f"column name {c.name!r} must be an Oracle identifier (starts with a letter; A-Z, 0-9, _; "
                            "max 30 chars), e.g. DAYS_1_30 instead of 1_30_DAYS; rename it in the SQL and the columns")
            if c.total and c.data_type != "number":
                errs.append(f"column {c.name} is marked total but is not numeric")
        aliases = select_aliases(self.sql)
        if aliases is not None:
            missing = [n for n in names if n not in aliases]
            if missing:
                errs.append(f"columns not found as SELECT aliases in the SQL: {', '.join(missing)}")
        return errs


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Z0-9_]+", "_", name.upper()).strip("_") or "REPORT"


def select_aliases(sql: str) -> set[str] | None:
    """Output column names of the outermost SELECT list (None if it can't be found)."""
    from .validator import tokenize

    toks = tokenize(sql)
    depth = 0
    start = None
    # Outermost SELECT: the last SELECT at depth 0 (a WITH clause puts CTEs first).
    for i, t in enumerate(toks):
        if t.text == "(":
            depth += 1
        elif t.text == ")":
            depth -= 1
        elif depth == 0 and t.up == "SELECT":
            start = i
    if start is None:
        return None
    items, cur, depth = [], [], 0
    for t in toks[start + 1:]:
        if t.text == "(":
            depth += 1
        elif t.text == ")":
            depth -= 1
        if depth == 0 and t.up == "FROM":
            break
        if depth == 0 and t.text == ",":
            items.append(cur)
            cur = []
            continue
        cur.append(t)
    items.append(cur)
    out = set()
    for it in items:
        it = [t for t in it if t.up != "DISTINCT"]
        if not it:
            continue
        last = it[-1]
        if last.kind == "id":
            out.add(last.up)
    return out
