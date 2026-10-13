"""The report agent: plain-English request -> validated ReportSpec.

Flow
1. Retrieve the catalog objects relevant to the request (retrieval.py) and put
   their columns and the FK edges among them in the first user message.
2. Let the model (a local Ollama model by default, or Claude) work with four
   catalog tools (search, describe, join path, validate) and answer with JSON
   matching REPORT_SPEC_SCHEMA. Models without tool calling answer straight
   from the retrieved context with schema-constrained JSON.
3. Validate the answer locally (spec.check + validator.validate_sql). If there
   are errors, send them back and let the model repair, up to max_repairs times.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from .backends import BackendError, OllamaBackend, ToolResult, extract_json
from .catalog import Catalog
from .examples import load_examples, pick_examples
from .retrieval import Retriever
from .rules import check_request
from .spec import REPORT_SPEC_SCHEMA, ReportSpec
from .validator import ValidationReport, validate_sql

SYSTEM_PROMPT = """\
You are an Oracle Fusion Cloud ERP BI Publisher report developer specialising in Receivables (AR).
You turn a business request into one SQL data set for a BI Publisher data model that runs against
the ApplicationDB_FSCM data source, plus the output columns and parameters that describe it.

Ground every table, column and join in the metadata catalog you are given (crawled from Oracle's
"Tables and Views" guides, Fusion Cloud release 26d: every Financials table, the HZ_ customer tables,
the FND_ common tables (lookups, currencies, flexfields) and the HR_/PER_ tables for business units,
organizations and people; views, import/interface and temporary tables are excluded). Use the tools to look up tables that are
not in the context, to find join paths, and to validate your SQL before you answer. Use base tables
only. If the report truly needs an object from outside the catalog (FND_, HR_, PER_ ...), you may
use it, but say so in assumptions. This is Oracle Fusion Cloud, not E-Business Suite: do not use
EBS-only tables or columns.

SQL rules
- One read-only SELECT (a WITH clause is fine). No semicolon, no DML, no PL/SQL.
- Give every table an alias and qualify every column with it (ps.AMOUNT_DUE_REMAINING).
- Alias every output column in UPPER_SNAKE_CASE, at most 30 characters. The spec's columns list
  must use exactly these aliases, in SELECT order. Break (group header) columns come first.
- Parameters are bind variables named :P_<NAME>. Make optional filters null-tolerant:
  (:P_CUSTOMER_NUMBER IS NULL OR hca.ACCOUNT_NUMBER = :P_CUSTOMER_NUMBER).
- Prefer base tables (*_ALL, *_B) over UI views (*_V, *_VL) and never use *_GT temp tables.
  For translated *_TL tables filter LANGUAGE = USERENV('LANG').
- Fusion joins to RA_CUST_TRX_TYPES_ALL and RA_BATCH_SOURCES_ALL use the *_SEQ_ID columns
  (e.g. rct.CUST_TRX_TYPE_SEQ_ID = ctt.CUST_TRX_TYPE_SEQ_ID), not EBS-style *_ID columns.
- Customer name and number: HZ_CUST_ACCOUNTS (ACCOUNT_NUMBER) joined to HZ_PARTIES (PARTY_NAME)
  on PARTY_ID.
- Open balances live in AR_PAYMENT_SCHEDULES_ALL (AMOUNT_DUE_REMAINING, STATUS 'OP'/'CL',
  CLASS INV/DM/CM/CB/BR/PMT). Receipt and credit memo applications live in
  AR_RECEIVABLE_APPLICATIONS_ALL (APPLICATION_TYPE 'CASH'/'CM', STATUS 'APP' for applied,
  DISPLAY = 'Y' for the current row).
- Filter by business unit with ORG_ID when the request implies it, via an optional :P_ORG_ID.
  The business unit name is HR_ORGANIZATION_UNITS_F_TL.NAME (ORGANIZATION_ID = x.ORG_ID,
  LANGUAGE = USERENV('LANG'), TRUNC(SYSDATE) BETWEEN EFFECTIVE_START_DATE AND EFFECTIVE_END_DATE).
- Customer account sites (HZ_CUST_ACCT_SITES_ALL) carry SET_ID, a reference data set, not ORG_ID.
  To filter customers by business unit, map the BU to its set through FND_SETID_ASSIGNMENTS
  (DETERMINANT_TYPE = 'BU', DETERMINANT_VALUE = the BU's ORGANIZATION_ID) and say which reference
  group you assumed, or filter through the BU's transactions (ORG_ID) if that is what the request means.
- Lookup meanings come from FND_LOOKUP_VALUES_TL (LOOKUP_TYPE, LOOKUP_CODE, LANGUAGE = USERENV('LANG')).
- Write SQL a BI Publisher developer would accept: readable, no SELECT *, ORDER BY the break
  columns then the natural detail order.

Receivables business rules
- Open items are AR_PAYMENT_SCHEDULES_ALL rows with STATUS = 'OP'. Original, applied, credited,
  adjusted and remaining amounts are columns of AR_PAYMENT_SCHEDULES_ALL (AMOUNT_DUE_ORIGINAL,
  AMOUNT_APPLIED, AMOUNT_CREDITED, AMOUNT_ADJUSTED, AMOUNT_DUE_REMAINING); do not join
  applications to get them.
- Include only the transaction classes the request names (invoice INV, debit memo DM, credit memo CM,
  chargeback CB, bills receivable BR, receipt PMT).
- Aging: days past due = TRUNC(:P_AS_OF_DATE) - TRUNC(ps.DUE_DATE). Current is <= 0, then
  BETWEEN 1 AND 30, 31 AND 60, 61 AND 90, and > 90 days. Count days, not months.
- A date range is two date parameters (e.g. :P_FROM_DATE, :P_TO_DATE) applied with
  TRUNC(x.SOME_DATE) BETWEEN TRUNC(:P_FROM_DATE) AND TRUNC(:P_TO_DATE).
- Every parameter you declare must be used in the WHERE clause, and every filter the request asks
  for needs a parameter.
- Reviewed example reports come after the catalog objects. Reuse their conventions; build the columns and
  filters from this request, not the example's.

Completeness (master data, "all attributes", extracts, setups)
- Cover every level of the entity, not just the top one. For a customer that means party, party-level
  tax profile, account, account profile, party site, location, account site, each site use
  (Bill-To and Ship-To side by side), site profile, site tax profile and registrations, and contacts.
- At every level return the system identifiers (primary and foreign key IDs, e.g. PARTY_ID,
  CUST_ACCOUNT_ID, PARTY_SITE_ID, LOCATION_ID, SITE_USE_ID), ORIG_SYSTEM_REFERENCE, the business
  numbers and names, STATUS, the start and end dates (START_DATE/END_DATE, *_ACTIVE, EFFECTIVE_*),
  CREATION_DATE, LAST_UPDATE_DATE and a derived <LEVEL>_ACTIVE flag (status active and today inside
  the dates). Return inactive and end-dated rows too, unless the request asks for active only.
- Turn every ID that has a name (payment terms, profile classes, collectors, business units) into the
  name, but keep the ID column as well.
- For date-effective child rows (profiles, registrations, contact points) take the row effective today,
  else the latest, so one parent row does not repeat.

Answer
- Call tools with real tool calls, not JSON written in your reply.
- When the SQL validates, reply with the JSON report spec only. The sql value is one JSON string:
  use \\n for line breaks and never join strings with +. Mark numeric columns that should be
  summed with total=true. Data types are string, number or date.
- In assumptions, list every business-rule choice you made (statuses and classes included,
  how dates are compared, what "open" means) and anything you could not verify in the catalog.
"""

TOOLS = [
    {
        "name": "search_catalog",
        "description": "Search the Receivables metadata catalog by keywords. Returns ranked object names "
                       "with a short description. Use it to find tables not already in the context.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Keywords, e.g. 'adjustment activity'"}},
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "describe_table",
        "description": "Full column list (datatype, comment), primary key and documented foreign keys "
                       "of one catalog table or view.",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Exact object name, e.g. AR_ADJUSTMENTS_ALL"}},
            "required": ["name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "find_join_path",
        "description": "Shortest chain of documented foreign-key joins between two catalog objects "
                       "(up to 3 hops).",
        "parameters": {
            "type": "object",
            "properties": {"from_table": {"type": "string"}, "to_table": {"type": "string"}},
            "required": ["from_table", "to_table"],
            "additionalProperties": False,
        },
    },
    {
        "name": "validate_sql",
        "description": "Check SQL against the catalog: tables exist, alias.column references exist, joins "
                       "match documented foreign keys, bind variables match the parameter names. "
                       "Call it before giving the final answer.",
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {"type": "string"},
                "parameters": {"type": "array", "items": {"type": "string"},
                               "description": "Parameter names without colon, e.g. ['P_AS_OF_DATE']"},
            },
            "required": ["sql", "parameters"],
            "additionalProperties": False,
        },
    },
]

JSON_MODE_NOTE = """
No tools are available in this session. Use only the catalog objects listed in the request, and answer
with the JSON report spec only. If validation errors come back, fix them and answer with the full spec again.
"""


class AgentError(RuntimeError):
    pass


def _complete_sql(sql) -> str:
    """sql stripped, if it looks like a whole query (SELECT/WITH ... FROM ...); else ""."""
    if not isinstance(sql, str):
        return ""
    sql = sql.strip().rstrip(";").strip()
    return sql if re.match(r"(?is)\s*(SELECT|WITH)\b.*\bFROM\b", sql) else ""


def _fenced_sql(text: str) -> str:
    m = re.search(r"```sql\s*(.*?)```", text or "", re.S | re.I)
    return _complete_sql(m.group(1)) if m else ""


@dataclass
class AgentResult:
    spec: ReportSpec
    validation: ValidationReport
    spec_errors: list[str]
    retrieved_tables: list[str]
    steps: int
    usage: dict[str, int] = field(default_factory=dict)
    request_errors: list[str] = field(default_factory=list)
    repairs: int = 0

    @property
    def ok(self) -> bool:
        return self.validation.ok and not self.spec_errors and not self.request_errors


class ReportAgent:
    def __init__(self, catalog: Catalog, backend: Any = None, max_steps: int = 16,
                 max_repairs: int = 2, top_k: int | None = None, max_tool_rounds: int | None = None,
                 log=None, examples: list | None = None, n_examples: int | None = None,
                 exclude_examples: list[str] | None = None, retriever: Retriever | None = None,
                 example_picker=None):
        self.catalog = catalog
        self.retriever = retriever or Retriever(catalog)
        # example_picker(request, examples, k, exclude) -> list[Example]; default is word overlap.
        self.example_picker = example_picker or pick_examples
        self.backend = backend if backend is not None else OllamaBackend()
        self.max_steps = max_steps
        self.max_repairs = max_repairs
        # Local models (default qwen2.5-coder:14b, 24k window) get a smaller, compact
        # context and fewer tool rounds: small models tend to loop on tools.
        self.local = getattr(self.backend, "name", "") == "ollama"
        self.top_k = top_k if top_k is not None else (5 if self.local else 8)
        self.max_tool_rounds = max_tool_rounds if max_tool_rounds is not None else (5 if self.local else 12)
        self.log = log or (lambda msg: None)
        # Reviewed reference reports shown as worked examples (examples.py).
        self.examples = load_examples() if examples is None else examples
        self.n_examples = n_examples if n_examples is not None else (1 if self.local else 2)
        self.exclude_examples = exclude_examples or []
        self.picked_examples: list[str] = []

    # ---- context ---------------------------------------------------------
    def build_context(self, request: str) -> tuple[str, list[str]]:
        r = self.retriever.search(request, top_k=self.top_k)
        if self.local:
            r.tables = r.tables[:8]
            kept = set(r.tables)
            r.edges = [e for e in r.edges if e.child in kept and e.parent in kept]
        keep = set()
        for w in re.findall(r"[A-Za-z]+", request.upper()):
            if len(w) > 2:
                keep.add(w)
                if w.endswith("S") and len(w) > 4:
                    keep.add(w[:-1])  # RECEIPTS -> RECEIPT
        join_cols: dict[str, set[str]] = {}
        for e in r.edges:
            join_cols.setdefault(e.child, set()).update(e.child_columns)
            join_cols.setdefault(e.parent, set()).update(e.parent_columns)
        parts = [f"Report request:\n{request.strip()}\n",
                 "Relevant catalog objects (who-columns omitted):\n"]
        for i, n in enumerate(r.tables):
            # Local models: only the top two hits keep comments; the rest are trimmed
            # to their likeliest report columns (describe_table shows the full list).
            compact = self.local and i >= 2
            parts.append(self.catalog.describe_table(
                n, comments=not compact, max_desc=200 if compact else 400,
                max_columns=(35 if compact else 60) if self.local else None, keep=keep,
                join_columns=join_cols.get(n)) + "\n")
        if r.edges:
            parts.append("Documented foreign keys among these objects:")
            parts += [f"- {e.describe()}" for e in r.edges]
        picked = self.example_picker(request, self.examples, self.n_examples, self.exclude_examples)
        self.picked_examples = [e.name for e in picked]
        if picked:
            parts.append("\nReviewed example reports (follow their conventions; answer this request, "
                         "not theirs):\n")
            parts += [e.render() + "\n" for e in picked]
        return "\n".join(parts), r.tables

    # ---- tools -----------------------------------------------------------
    def run_tool(self, name: str, args: dict) -> str:
        if not isinstance(args, dict):
            raise ValueError("tool input must be an object")
        if name == "search_catalog":
            hits = self.retriever.search_names(str(args["query"]))
            return "\n".join(f"{n} (score {s}): {d}" for n, s, d in hits) or "no matches"
        if name == "describe_table":
            t = self.catalog.get(str(args["name"]))
            if t is None:
                hits = self.retriever.search_names(str(args["name"]), limit=5)
                return f"{args['name']} is not in the catalog. Closest: " + ", ".join(h[0] for h in hits)
            text = self.catalog.describe_table(t.name, include_who=not self.local, comments=not self.local,
                                               max_desc=400 if self.local else 2000)
            fks = [e.describe() for e in self.catalog.edges_for(t.name)]
            if fks:
                text += "\nForeign keys:\n" + "\n".join(f"- {f}" for f in fks[:25 if self.local else 60])
            return text
        if name == "find_join_path":
            path = self.catalog.join_path(str(args["from_table"]), str(args["to_table"]))
            if path is None:
                return "no documented join path within 3 hops"
            return "\n".join(e.describe() for e in path) or "same table"
        if name == "validate_sql":
            params = args.get("parameters")
            if not isinstance(params, list):
                raise ValueError("parameters must be a list of names")
            return validate_sql(str(args["sql"]), self.catalog, [str(p).lstrip(":") for p in params]).summary()
        raise ValueError(f"unknown tool {name}")

    # ---- loop ------------------------------------------------------------
    def _tables_in(self, problems: list[str]) -> list[str]:
        names = []
        for p in problems:
            for m in re.findall(r"\b(?:AR|RA|HZ)_[A-Z0-9_]+\b", p):
                if m in self.catalog and m not in names:
                    names.append(m)
        return names

    def generate(self, request: str) -> AgentResult:
        context, retrieved = self.build_context(request)
        try:
            self.log(f"backend: {self.backend.describe()}")
            uses_tools = self.backend.uses_tools  # may ask Ollama what the model supports
        except BackendError as exc:
            raise AgentError(str(exc)) from exc
        self.log(f"retrieved: {', '.join(retrieved)}")
        if self.picked_examples:
            self.log(f"example: {', '.join(self.picked_examples)}")
        system = SYSTEM_PROMPT if uses_tools else SYSTEM_PROMPT + JSON_MODE_NOTE
        conv = self.backend.start(system, context)
        usage = {"input_tokens": 0, "output_tokens": 0}
        repairs = 0
        finalized = False
        tool_rounds = 0
        last_sql = ""  # latest complete SQL the model wrote (tool call or free-form answer)
        for step in range(1, self.max_steps + 1):
            try:
                turn = self.backend.step(conv, TOOLS, REPORT_SPEC_SCHEMA, final=finalized)
            except BackendError as exc:
                raise AgentError(str(exc)) from exc
            for k in usage:
                usage[k] += turn.usage.get(k, 0)
            if turn.stop == "refusal":
                raise AgentError("the model declined the request")
            if turn.stop == "max_output":
                if finalized:
                    raise AgentError("the model kept generating without finishing the spec "
                                     f"({getattr(self.backend, 'num_predict', '?')} tokens)")
                finalized = True
                self.log("answer ran past the output limit; asking for schema-constrained JSON")
                self.backend.add_user(conv, "Answer with the final report spec as JSON only.")
                continue
            if turn.stop == "max_tokens":
                raise AgentError("the model ran out of output tokens or context window "
                                 "(for a local model, raise --num-ctx)")

            if turn.tool_calls:
                results = []
                for call in turn.tool_calls:
                    if call.name == "validate_sql" and isinstance(call.args, dict):
                        last_sql = _complete_sql(call.args.get("sql")) or last_sql
                    try:
                        out = self.run_tool(call.name, call.args)
                        self.log(f"tool {call.name}: ok")
                        results.append(ToolResult(call, out))
                    except (KeyError, TypeError, ValueError) as exc:
                        self.log(f"tool {call.name}: error {exc}")
                        results.append(ToolResult(call, str(exc), is_error=True))
                self.backend.add_tool_results(conv, results)
                tool_rounds += 1
                # Ollama truncates prompts that outgrow num_ctx without an error, so stop
                # the tool loop early when the window is three-quarters full.
                ctx_full = turn.usage.get("input_tokens", 0) > 0.75 * getattr(self.backend, "num_ctx", 1e9)
                if self.local and (tool_rounds >= self.max_tool_rounds or ctx_full) and not finalized:
                    # Stop the tool loop: the next call is constrained to the spec schema.
                    finalized = True
                    self.log(f"{tool_rounds} tool rounds; asking for the final spec")
                    self.backend.add_user(conv, "Stop using tools now. Answer with the final report spec as JSON only.")
                continue

            data = extract_json(turn.text)
            last_sql = _complete_sql((data or {}).get("sql")) or _fenced_sql(turn.text) or last_sql
            spec = None
            if data is not None and "sql" in data:
                try:
                    spec = ReportSpec.from_dict(data)
                except (KeyError, TypeError, AttributeError) as exc:
                    if finalized or getattr(self.backend, "name", "") != "ollama":
                        raise AgentError(f"could not parse the report spec: {exc}") from exc
            if spec is None:
                if not finalized and getattr(self.backend, "name", "") == "ollama":
                    # Ask once more with output constrained to the spec schema.
                    finalized = True
                    self.log("answer was not a spec; asking for schema-constrained JSON")
                    self.backend.add_user(conv, "Now answer with the final report spec as JSON only, with every "
                                                "field of the schema. Write the sql value as one JSON string "
                                                "(\\n for line breaks, no + concatenation).")
                    continue
                raise AgentError("the model's answer is not a report spec JSON object")
            if not _complete_sql(spec.sql) and not last_sql and getattr(self.backend, "name", "") == "ollama":
                # Constrained decoding sometimes cuts the SQL string short (just "SELECT") when the
                # model tries to continue it with +. Ask for the query alone, as free text.
                self.log("spec SQL was cut short; asking for the SQL alone")
                self.backend.add_user(conv, "The sql value in your spec was cut off. Write the complete SQL "
                                            "query only, in a ```sql block, with the same column aliases.")
                try:
                    sql_turn = self.backend.step(conv, TOOLS, REPORT_SPEC_SCHEMA, final=True, plain=True)
                except BackendError as exc:
                    raise AgentError(str(exc)) from exc
                for k in usage:
                    usage[k] += sql_turn.usage.get(k, 0)
                last_sql = _fenced_sql(sql_turn.text) or _complete_sql(sql_turn.text)
            if not _complete_sql(spec.sql) and last_sql:
                # Keep the complete query the model wrote elsewhere (tool call, free text).
                self.log("spec SQL was cut short; using the model's complete SQL")
                spec.sql = last_sql
            spec_errors = spec.check()
            report = validate_sql(spec.sql, self.catalog, [p.name for p in spec.parameters])
            request_errors = check_request(request, spec, report, self.catalog)
            problems = spec_errors + report.errors + request_errors
            if not problems or repairs >= self.max_repairs:
                return AgentResult(spec, report, spec_errors, retrieved, step, usage, request_errors, repairs)
            repairs += 1
            self.log(f"repair {repairs}: {len(problems)} problem(s)")
            msg = ("The spec failed validation. Fix these problems and answer with the full corrected spec:\n"
                   + "\n".join(f"- {p}" for p in problems))
            if not uses_tools:
                # No describe_table tool: show the tables the errors mention.
                extra = [self.catalog.describe_table(n) for n in self._tables_in(problems)[:3]]
                if extra:
                    msg += "\n\nCatalog entries for the tables involved:\n" + "\n\n".join(extra)
            self.backend.add_user(conv, msg)
        raise AgentError(f"no answer after {self.max_steps} model calls")
