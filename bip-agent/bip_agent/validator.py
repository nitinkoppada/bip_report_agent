"""Static checks of generated SQL against the metadata catalog.

This is not a full Oracle SQL parser. It tokenizes the query, resolves table
aliases in FROM/JOIN clauses (including CTEs and inline views), and checks:

* the statement is a read-only SELECT / WITH query;
* every in-scope table (AR_, RA_, the six HZ_ tables) exists in the catalog;
* every alias.COLUMN reference exists on the aliased catalog table;
* equality joins between catalog tables match a documented FK edge (warning
  otherwise) and no table is left without a join (cartesian product);
* bind variables (:P_X) are collected so they can be matched to parameters.

The agent tells the model to qualify every column with its table alias, which
is what makes the column check possible.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .catalog import Catalog

KEYWORDS = {
    "SELECT", "FROM", "WHERE", "AND", "OR", "NOT", "IN", "IS", "NULL", "AS", "ON",
    "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "OUTER", "CROSS", "NATURAL", "USING",
    "GROUP", "BY", "ORDER", "HAVING", "UNION", "ALL", "INTERSECT", "MINUS", "EXCEPT",
    "DISTINCT", "CASE", "WHEN", "THEN", "ELSE", "END", "BETWEEN", "LIKE", "EXISTS",
    "WITH", "ASC", "DESC", "NULLS", "FIRST", "LAST", "FETCH", "NEXT", "ROWS", "ONLY",
    "OFFSET", "OVER", "PARTITION", "CONNECT", "START", "PRIOR", "LATERAL", "APPLY",
    "PIVOT", "UNPIVOT", "FOR", "ROW", "ROWNUM", "SYSDATE", "TRUNC", "ESCAPE",
    "MODEL", "SAMPLE", "WINDOW", "QUALIFY", "LIMIT",
}
FORBIDDEN = {"INSERT", "UPDATE", "DELETE", "MERGE", "DROP", "CREATE", "ALTER",
             "TRUNCATE", "GRANT", "REVOKE", "EXECUTE", "BEGIN", "DECLARE", "COMMIT",
             "ROLLBACK", "CALL", "LOCK"}
TABLE_LIST_END = {"WHERE", "GROUP", "ORDER", "HAVING", "UNION", "INTERSECT", "MINUS",
                  "EXCEPT", "CONNECT", "START", "FETCH", "OFFSET", "FOR", "MODEL",
                  "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "CROSS", "NATURAL", "ON",
                  "USING", "PIVOT", "UNPIVOT", "WINDOW"}
PSEUDO_TABLES = {"DUAL"}

# Fusion-specific mistakes worth a pointed message.
SEQ_ID_HINTS = {
    ("RA_CUST_TRX_TYPES_ALL", "CUST_TRX_TYPE_ID"): "join RA_CUST_TRX_TYPES_ALL on CUST_TRX_TYPE_SEQ_ID, not CUST_TRX_TYPE_ID",
    ("RA_BATCH_SOURCES_ALL", "BATCH_SOURCE_ID"): "join RA_BATCH_SOURCES_ALL on BATCH_SOURCE_SEQ_ID, not BATCH_SOURCE_ID",
}

_TOKEN_RE = re.compile(
    r"""
    (?P<str>'(?:[^']|'')*')
  | (?P<qid>"[^"]+")
  | (?P<bind>:[A-Za-z_][A-Za-z0-9_]*)
  | (?P<num>\d+(?:\.\d+)?)
  | (?P<id>[A-Za-z_][A-Za-z0-9_$#]*)
  | (?P<op><>|!=|<=|>=|\|\||[=<>(),.;*+\-/])
  | (?P<ws>\s+)
  | (?P<other>.)
    """,
    re.VERBOSE,
)


@dataclass
class Tok:
    kind: str
    text: str

    @property
    def up(self) -> str:
        return self.text.upper()


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    aliases: dict[str, str] = field(default_factory=dict)  # alias -> table / <cte>/<subquery>
    tables: list[str] = field(default_factory=list)
    binds: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict:
        return {"ok": self.ok, "errors": self.errors, "warnings": self.warnings,
                "tables": self.tables, "aliases": self.aliases, "binds": self.binds}

    def summary(self) -> str:
        lines = [f"Validation: {'OK' if self.ok else 'FAILED'} "
                 f"({len(self.errors)} errors, {len(self.warnings)} warnings)"]
        lines += [f"ERROR: {e}" for e in self.errors]
        lines += [f"WARNING: {w}" for w in self.warnings]
        return "\n".join(lines)


def tokenize(sql: str) -> list[Tok]:
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"\(\s*\+\s*\)", " ", sql)  # Oracle outer-join marker
    toks = []
    for m in _TOKEN_RE.finditer(sql):
        kind = m.lastgroup
        if kind == "ws":
            continue
        text = m.group()
        if kind == "qid":
            kind, text = "id", text.strip('"')
        toks.append(Tok(kind, text))
    return toks


def _match_parens(toks: list[Tok]) -> dict[int, int]:
    stack, match = [], {}
    for i, t in enumerate(toks):
        if t.text == "(":
            stack.append(i)
        elif t.text == ")" and stack:
            j = stack.pop()
            match[j] = i
            match[i] = j
    return match


def _is_ident(t: Tok | None) -> bool:
    return t is not None and t.kind == "id" and t.up not in KEYWORDS


def validate_sql(sql: str, catalog: Catalog, parameters: list[str] | None = None) -> ValidationReport:
    rep = ValidationReport()
    toks = tokenize(sql)
    if not toks:
        rep.errors.append("empty SQL")
        return rep
    while toks and toks[-1].text == ";":
        toks.pop()
    if any(t.text == ";" for t in toks):
        rep.errors.append("multiple statements are not allowed in a BIP data set")
    if toks[0].up not in ("SELECT", "WITH") and toks[0].text != "(":
        rep.errors.append(f"query must start with SELECT or WITH, found {toks[0].text!r}")
    if not any(t.up == "FROM" for t in toks):
        rep.errors.append("the SQL is incomplete (no FROM clause); write the whole query as one JSON string, "
                          "with \\n for line breaks and no + concatenation")
    n_case = sum(1 for t in toks if t.kind == "id" and t.up == "CASE")
    n_end = sum(1 for t in toks if t.kind == "id" and t.up == "END")
    if n_case != n_end:
        rep.errors.append(f"{n_case} CASE but {n_end} END: every CASE expression needs its END")
    if any(t.text == "`" for t in toks):
        rep.errors.append("backticks are MySQL syntax; Oracle aliases are plain identifiers such as DAYS_1_30")
    for t in toks:
        if t.kind == "id" and t.up in FORBIDDEN:
            rep.errors.append(f"forbidden keyword {t.up}: data sets must be read-only queries")
    parens = _match_parens(toks)
    # scope[i] = index of the innermost "(" enclosing token i (-1 at top level),
    # so table references can be grouped per query block.
    scope, stack = [], []
    for idx, t in enumerate(toks):
        if t.text == ")" and stack:
            stack.pop()
        scope.append(stack[-1] if stack else -1)
        if t.text == "(":
            stack.append(idx)

    # --- CTE names --------------------------------------------------------
    ctes: set[str] = set()
    for i, t in enumerate(toks):
        if t.kind == "id" and _is_ident(t) and i + 2 < len(toks) and toks[i + 1].up == "AS" and toks[i + 2].text == "(":
            prev = toks[i - 1] if i else None
            if prev is not None and (prev.up == "WITH" or prev.text == ","):
                ctes.add(t.up)

    # --- table references -------------------------------------------------
    aliases: dict[str, str] = {}
    primary: list[tuple[str, int]] = []  # (alias or name, query-block scope) per table reference
    i = 0
    n = len(toks)
    while i < n:
        t = toks[i]
        if t.kind == "id" and t.up in ("FROM", "JOIN"):
            # Skip "FROM" inside EXTRACT(x FROM y) / TRIM(... FROM ...)
            j = i + 1
            while j < n:
                if toks[j].text == "(":
                    close = parens.get(j, j)
                    alias_tok = toks[close + 1] if close + 1 < n else None
                    if alias_tok is not None and alias_tok.up == "AS":
                        alias_tok = toks[close + 2] if close + 2 < n else None
                    if _is_ident(alias_tok):
                        aliases[alias_tok.up] = "<subquery>"
                    # tokens inside the parens are scanned by the outer loop
                    break
                if toks[j].kind != "id" or toks[j].up in KEYWORDS:
                    break
                name = toks[j].up
                k = j + 1
                while k + 1 < n and toks[k].text == "." and toks[k + 1].kind == "id":
                    name = toks[k + 1].up  # FUSION.AR_X -> AR_X
                    k += 2
                if k < n and toks[k].text == "(":  # TABLE(fn(...))
                    break
                alias = None
                if k < n and toks[k].up == "AS":
                    k += 1
                if k < n and _is_ident(toks[k]):
                    alias = toks[k].up
                    k += 1
                target = name if name not in ctes else f"<cte:{name}>"
                aliases[alias or name] = target
                primary.append((alias or name, scope[j]))
                if name not in aliases:
                    aliases.setdefault(name, target)
                if name not in ctes and name not in rep.tables:
                    rep.tables.append(name)
                if k < n and toks[k].text == "," and t.up == "FROM":
                    j = k + 1
                    continue
                break
        i += 1
    rep.aliases = aliases

    for name in rep.tables:
        if name in PSEUDO_TABLES:
            continue
        if name not in catalog:
            if catalog.in_scope(name):
                rep.errors.append(f"table {name} is not in the catalog (views, import/interface and temporary "
                                  "tables are excluded; use the base tables)")
            else:
                rep.warnings.append(f"table {name} is outside the crawled catalog; columns and joins not verified")

    # --- alias.column references -----------------------------------------
    seen_refs: set[tuple[str, str]] = set()
    for i in range(n - 2):
        a, dot, c = toks[i], toks[i + 1], toks[i + 2]
        if a.kind != "id" or dot.text != "." or c.kind != "id":
            continue
        if i + 3 < n and toks[i + 3].text in ("(", "."):
            continue  # package.function( or schema.table.column
        if i > 0 and toks[i - 1].text == ".":
            continue
        qual, col = a.up, c.up
        if (qual, col) in seen_refs:
            continue
        seen_refs.add((qual, col))
        target = aliases.get(qual)
        if target is None:
            if qual in catalog.tables and qual in rep.tables:
                target = qual
            else:
                rep.errors.append(f"{qual}.{col}: unknown table alias {qual}")
                continue
        if target.startswith("<") or target not in catalog:
            continue
        info = catalog.get(target)
        if not info.has_column(col):
            hint = SEQ_ID_HINTS.get((target, col))
            msg = f"{qual}.{col}: column {col} does not exist on {target}"
            if hint:
                msg += f" ({hint})"
            else:
                close = [x for x in info.columns if col in x or x in col][:5]
                if close:
                    msg += f"; similar columns: {', '.join(close)}"
            rep.errors.append(msg)

    # --- joins ------------------------------------------------------------
    parent: dict[str, str] = {a: a for a in aliases}

    def find(x: str) -> str:
        while parent.get(x, x) != x:
            x = parent[x]
        return x

    for i in range(n - 6):
        w = toks[i:i + 7]
        if not (w[0].kind == "id" and w[1].text == "." and w[2].kind == "id" and w[3].text == "="
                and w[4].kind == "id" and w[5].text == "." and w[6].kind == "id"):
            continue
        a1, c1, a2, c2 = w[0].up, w[2].up, w[4].up, w[6].up
        t1, t2 = aliases.get(a1), aliases.get(a2)
        if not t1 or not t2 or a1 == a2:
            continue
        parent[find(a1)] = find(a2)
        for t, c in ((t1, c1), (t2, c2)):
            if (t, c) in SEQ_ID_HINTS:
                rep.errors.append(f"{t}.{c}: {SEQ_ID_HINTS[(t, c)]}")
        if t1 in catalog and t2 in catalog and t1 != t2:
            ok1 = catalog.get(t1).has_column(c1)
            ok2 = catalog.get(t2).has_column(c2)
            if ok1 and ok2 and not catalog.is_known_join(t1, c1, t2, c2):
                rep.warnings.append(
                    f"join {a1}.{c1} = {a2}.{c2} ({t1} to {t2}) is not a documented foreign key; check it")
    # Flag base-table references with no equality join to anything else
    # (scalar subqueries and IN filters are fine, so this is only a warning).
    blocks: dict[int, list[str]] = {}
    for a, sc in primary:
        if not aliases[a].startswith("<") and aliases[a] not in PSEUDO_TABLES:
            blocks.setdefault(sc, []).append(a)
    lonely: list[str] = []
    for refs in blocks.values():
        if len(refs) < 2:
            continue
        groups: dict[str, list[str]] = {}
        for a in refs:
            groups.setdefault(find(a), []).append(a)
        if len(groups) > 1:
            lonely += [g[0] for g in groups.values() if len(g) == 1]
    if lonely:
        rep.warnings.append(
            f"no equality join found for {', '.join(sorted(lonely))}; check for a cartesian product "
            "(fine if it is joined through a subquery)")

    # --- binds -------------------------------------------------------------
    for t in toks:
        if t.kind == "bind":
            b = t.text[1:].upper()
            if b not in rep.binds:
                rep.binds.append(b)
    if parameters is not None:
        params = {p.upper() for p in parameters}
        for b in rep.binds:
            if b not in params:
                rep.errors.append(f"bind variable :{b} has no matching data model parameter")
        for p in params - set(rep.binds):
            rep.warnings.append(f"parameter {p} is declared but not used in the SQL")
    return rep
