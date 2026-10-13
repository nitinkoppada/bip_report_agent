"""Checks of a generated spec against the request and Receivables business rules.

The catalog validator proves that tables, columns and joins exist. These checks
catch what it cannot: filters the request asked for that the SQL leaves out,
declared parameters that are never used, and a few AR rules that small models
get wrong (aging arithmetic, what "open" means, transaction classes).

They are heuristics on the request text and the SQL text. Every message says
how to fix the problem, because the messages go back to the model as repair
instructions.
"""
from __future__ import annotations

import re

from .spec import ReportSpec
from .validator import ValidationReport

# Request words -> AR_PAYMENT_SCHEDULES_ALL.CLASS codes
CLASS_WORDS = [
    (r"\binvoices?\b", "INV"),
    (r"\bdebit memos?\b", "DM"),
    (r"\bcredit memos?\b", "CM"),
    (r"\bcharge ?backs?\b", "CB"),
    (r"\bbills? receivables?\b", "BR"),
    (r"\b(?:receipts?|payments?)\b", "PMT"),
]


def _date_params(spec: ReportSpec) -> list[str]:
    return [p.name for p in spec.parameters if p.data_type == "date"]


DATE_STATUS_RE = re.compile(r"^(STATUS|START_DATE|END_DATE|START_DATE_ACTIVE|END_DATE_ACTIVE|"
                            r"EFFECTIVE_START_DATE|EFFECTIVE_END_DATE|EFFECTIVE_FROM|EFFECTIVE_TO|"
                            r"ADDRESS_EFFECTIVE_DATE|ADDRESS_EXPIRATION_DATE|ACCOUNT_TERMINATION_DATE)$")


LOOKUP_COLUMNS = {"NAME", "DESCRIPTION", "MEANING", "LANGUAGE", "TERM_ID", "COLLECTOR_ID", "PROFILE_CLASS_ID"}


def _select_list(sql: str) -> str:
    """Upper-case text of the outermost SELECT list (a WITH clause's CTEs come first)."""
    from .validator import tokenize

    toks = tokenize(sql)
    depth, start = 0, None
    for i, t in enumerate(toks):
        if t.text == "(":
            depth += 1
        elif t.text == ")":
            depth -= 1
        elif depth == 0 and t.up == "SELECT":
            start = i
    if start is None:
        return sql.upper()
    out, depth = [], 0
    for t in toks[start + 1:]:
        if t.text == "(":
            depth += 1
        elif t.text == ")":
            depth -= 1
        if depth == 0 and t.up == "FROM":
            break
        out.append(t.up)
    return " ".join(out).replace(" . ", ".")


def _completeness(spec: ReportSpec, report: ValidationReport, catalog) -> list[str]:
    """Keys and status/date columns of every base table must be selected (master-data requests)."""
    if catalog is None:
        return []
    sql_up = spec.sql.upper()
    selected = _select_list(spec.sql)
    errs = []
    for alias, table in report.aliases.items():
        info = catalog.get(table) if not table.startswith("<") else None
        if info is None or alias == table and any(a != t and t == table for a, t in report.aliases.items()):
            continue
        used = set(re.findall(rf"\b{re.escape(alias)}\.([A-Z0-9_$#]+)", selected))
        if not used:
            continue  # not returned directly (inside a WITH clause, or a filter-only join)
        if used and used <= LOOKUP_COLUMNS | set(info.primary_key):
            continue  # joined only to turn an ID into a name (terms, profile classes, collectors)
        wanted = [c for c in info.primary_key if not c.startswith("EFFECTIVE_") and c not in ("ENTERPRISE_ID", "LANGUAGE")]
        wanted += [c for c in info.columns if DATE_STATUS_RE.match(c)]
        missing = [c for c in dict.fromkeys(wanted) if not re.search(rf"\b{re.escape(alias)}\.{c}\b", selected)]
        if missing:
            errs.append(f"master-data request: {table} ({alias}) must also return {', '.join(missing)} "
                        "(system IDs, status and start/end dates at every level)")
    return errs


def check_request(request: str, spec: ReportSpec, report: ValidationReport, catalog=None) -> list[str]:
    """Problems with how the spec answers the request (empty list when none apply)."""
    req = request.lower()
    sql = spec.sql
    sql_up = sql.upper()
    binds = set(report.binds)
    errs: list[str] = []

    # Every declared parameter must filter something.
    unused = [p.name for p in spec.parameters if p.name not in binds]
    if unused:
        errs.append(f"parameters {', '.join(unused)} are declared but not used in the SQL; "
                    "use each one in a WHERE condition or remove it")

    dates_used = [p for p in _date_params(spec) if p in binds]
    if re.search(r"date[- ]range|between .* and|from[- ]date|\brange\b|\bperiod\b", req):
        if len(dates_used) < 2:
            errs.append("the request asks for a date range, but the SQL does not filter on two date "
                        "parameters; add e.g. :P_FROM_DATE and :P_TO_DATE (data_type date) and a condition "
                        "like TRUNC(x.SOME_DATE) BETWEEN TRUNC(:P_FROM_DATE) AND TRUNC(:P_TO_DATE)")
    if re.search(r"\bas of\b|\bas-of\b", req) and not dates_used:
        errs.append("the request asks for an as-of date, but no date parameter is used in the SQL; "
                    "add :P_AS_OF_DATE (data_type date, required)")
    if re.search(r"business unit|\bbu\b|operating unit|\borg\b", req) and "ORG_ID" not in sql_up:
        errs.append("the request asks for a business unit filter; add an optional :P_ORG_ID and "
                    "(:P_ORG_ID IS NULL OR x.ORG_ID = :P_ORG_ID)")
    if re.search(r"customer (?:number )?filter|optional customer|customer and business unit filter|for a customer", req):
        if not any("CUSTOMER" in b or "ACCOUNT" in b for b in binds):
            errs.append("the request asks for a customer filter; add an optional :P_CUSTOMER_NUMBER and "
                        "(:P_CUSTOMER_NUMBER IS NULL OR hca.ACCOUNT_NUMBER = :P_CUSTOMER_NUMBER)")

    # Aging: buckets are days past due = as-of date minus due date, in days.
    if re.search(r"\baging\b|\bageing\b|past due|overdue|buckets?", req) and "DUE_DATE" in sql_up:
        past_due = re.search(r"(?::P_\w+|SYSDATE)\s*\)?\s*-\s*(?:TRUNC\s*\(\s*)?\w+\.DUE_DATE", sql, re.I)
        if not past_due:
            errs.append("aging buckets must be based on days past due = TRUNC(:P_AS_OF_DATE) - TRUNC(ps.DUE_DATE) "
                        "(positive when overdue): current is <= 0, then BETWEEN 1 AND 30, 31 AND 60, 61 AND 90, "
                        "and > 90. Do not compare DUE_DATE to dates after the as-of date")
        if re.search(r"ADD_MONTHS|INTERVAL\s+'\d+'\s+MONTH", sql, re.I):
            errs.append("aging buckets are counted in days, not months; remove ADD_MONTHS / month intervals")

    # "Open" items: STATUS = 'OP' only.
    if re.search(r"\bopen\b|\boutstanding\b|\baging\b|\bageing\b", req) and "AR_PAYMENT_SCHEDULES_ALL" in report.tables:
        if re.search(r"STATUS\s+IN\s*\([^)]*'CL'", sql, re.I) or not re.search(r"STATUS\s*=\s*'OP'", sql, re.I):
            errs.append("open items are payment schedules with STATUS = 'OP'; filter ps.STATUS = 'OP' "
                        "and do not include closed ('CL') rows")

    # Amount columns the request names ("original, applied, ... and remaining amounts").
    if re.search(r"\bamounts?\b", req):
        cols = " ".join(c.name for c in spec.columns)
        missing = [w for w, stem in (("original", "ORIG"), ("applied", "APPLIED"), ("credited", "CREDIT"),
                                     ("adjusted", "ADJUST"), ("remaining", "REMAINING"), ("discount", "DISCOUNT"))
                   if re.search(rf"\b{w}\b", req) and stem not in cols]
        if missing:
            errs.append(f"the request asks for {', '.join(missing)} amounts, but no output column has them; "
                        "add them (for transactions they are AR_PAYMENT_SCHEDULES_ALL columns such as "
                        "AMOUNT_DUE_ORIGINAL, AMOUNT_APPLIED, AMOUNT_CREDITED, AMOUNT_ADJUSTED, AMOUNT_DUE_REMAINING)")

    # Master-data extracts: every table used must contribute its key and its status/date columns.
    if re.search(r"\b(mdm|master data|all (?:the )?(?:\w+ )?(?:attributes|details|information|columns)|"
                 r"every attribute|extract)\b", req):
        errs += _completeness(spec, report, catalog)

    # Transaction classes: if the request names classes and the SQL filters CLASS, don't add others.
    named = {code for pat, code in CLASS_WORDS if re.search(pat, req)}
    m = re.search(r"\bCLASS\s+IN\s*\(([^)]*)\)", sql, re.I)
    if m and named and not re.search(r"\baging\b|\bageing\b", req):
        listed = set(re.findall(r"'([A-Z]+)'", m.group(1).upper()))
        extra = sorted(listed - named)
        if extra:
            errs.append(f"CLASS IN includes {', '.join(extra)}, which the request did not ask for; "
                        f"keep only {', '.join(sorted(named & listed)) or ', '.join(sorted(named))}")
    return errs
