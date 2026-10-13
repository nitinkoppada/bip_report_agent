"""Command line entry point.

  python -m bip_agent check                                                 (is the local model ready?)
  python -m bip_agent generate "AR aging by customer as of a date" -o out/aging   (local Ollama model)
  python -m bip_agent generate "..." -o out/x --backend claude                     (Anthropic API)
  python -m bip_agent render examples/specs/ar_aging.json -o out/aging     (offline)
  python -m bip_agent validate query.sql [-p P_AS_OF_DATE ...]              (offline)
  python -m bip_agent retrieve "receipts applied to invoices"              (offline)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .backends import (CLAUDE_MODEL, DEFAULT_OLLAMA_MODEL, DEFAULT_OLLAMA_URL, BackendError,
                       make_backend)
from .catalog import Catalog
from .datamodel import build_datamodel, build_sample_xml
from .rtf_layout import build_rtf
from .rules import check_request
from .spec import ReportSpec
from .validator import validate_sql


def write_outputs(spec: ReportSpec, catalog: Catalog, outdir: Path, request: str | None = None) -> dict:
    """Validate a spec and write the SQL, data model, RTF layout and sample data."""
    outdir.mkdir(parents=True, exist_ok=True)
    report = validate_sql(spec.sql, catalog, [p.name for p in spec.parameters])
    spec_errors = spec.check()
    request_errors = check_request(request, spec, report, catalog) if request else []
    name = spec.report_name
    files = {
        f"{name}.sql": spec.sql + "\n",
        f"{name}.xdm": build_datamodel(spec),
        f"{name}.rtf": build_rtf(spec),
        f"{name}_sample.xml": build_sample_xml(spec),
        "spec.json": json.dumps(spec.to_dict(), indent=2) + "\n",
    }
    validation = {**report.to_dict(), "spec_errors": spec_errors, "request_errors": request_errors,
                  "ok": report.ok and not spec_errors and not request_errors}
    files["validation.json"] = json.dumps(validation, indent=2) + "\n"
    for fname, content in files.items():
        (outdir / fname).write_text(content)
    return validation


def _backend(args):
    if args.backend == "claude":
        return make_backend("claude", model=args.model or CLAUDE_MODEL, effort=args.effort,
                            use_fallbacks=not args.no_fallbacks)
    return make_backend("ollama", model=args.model or DEFAULT_OLLAMA_MODEL, host=args.ollama_host,
                        mode=args.mode, num_ctx=args.num_ctx)


def _print_validation(v: dict) -> None:
    print(f"validation: {'OK' if v['ok'] else 'FAILED'}")
    for e in v.get("spec_errors", []) + v["errors"] + v.get("request_errors", []):
        print(f"  ERROR   {e}")
    for w in v["warnings"]:
        print(f"  WARNING {w}")


class Knowledge:
    """Where the agent reads metadata from: the Postgres knowledge base (hybrid search) or JSON files."""

    def __init__(self, catalog: Catalog, kb=None):
        self.catalog = catalog
        self.kb = kb

    @property
    def source(self) -> str:
        return "postgres (hybrid keyword + vector search)" if self.kb else "json files (keyword search)"

    def retriever(self):
        from .retrieval import HybridRetriever, Retriever

        return HybridRetriever(self.catalog, self.kb) if self.kb else Retriever(self.catalog)

    def examples(self):
        from .examples import Example, load_examples

        if self.kb:
            return [Example(r["name"], r["spec"]) for r in self.kb.examples()]
        return load_examples()

    def example_picker(self):
        if not self.kb:
            return None
        kb = self.kb

        def pick(request, examples, k, exclude):
            by_name = {e.name: e for e in examples}
            return [by_name[n] for n, _ in kb.search_examples(request, k=k, exclude=exclude) if n in by_name]
        return pick


def load_knowledge(mode: str, catalog_dir: str | None, log=lambda m: None) -> Knowledge:
    """mode: auto (Postgres when it is loaded and embedded, else JSON), postgres, or files."""
    if mode != "files":
        from .knowledge import KnowledgeBase

        kb = KnowledgeBase()
        if kb.ready():
            return Knowledge(kb.catalog(), kb)
        if mode == "postgres":
            raise SystemExit("error: the Postgres knowledge base is not reachable or not loaded; "
                             "run `python3 -m bip_agent kb setup`")
        log("knowledge base not ready; using the JSON catalog files")
    return Knowledge(Catalog.load(catalog_dir))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bip_agent", description="Generate Oracle Fusion BI Publisher reports")
    ap.add_argument("--catalog", help="metadata directory (default: ../receivables-metadata)")
    ap.add_argument("--kb", default=os.environ.get("BIP_AGENT_KB", "auto"), choices=["auto", "postgres", "files"],
                    help="metadata source: Postgres knowledge base, JSON files, or auto (Postgres if ready)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def backend_args(p):
        p.add_argument("--backend", default=os.environ.get("BIP_AGENT_BACKEND", "ollama"),
                       choices=["ollama", "claude"], help="ollama = local model (default), claude = Anthropic API")
        p.add_argument("--model", default=None,
                       help=f"model name (default {DEFAULT_OLLAMA_MODEL} for ollama, {CLAUDE_MODEL} for claude)")
        p.add_argument("--ollama-host", default=DEFAULT_OLLAMA_URL)
        p.add_argument("--mode", default="auto", choices=["auto", "tools", "json"],
                       help="ollama only: tool calling, JSON-only answers, or detect from the model")
        p.add_argument("--num-ctx", type=int, default=24576, help="ollama only: context window in tokens")
        p.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"],
                       help="claude only")
        p.add_argument("--no-fallbacks", action="store_true", help="claude only: disable refusal fallbacks")

    g = sub.add_parser("generate", help="plain-English request -> SQL, data model, layout")
    g.add_argument("request")
    g.add_argument("-o", "--out", required=True)
    g.add_argument("--holdout", action="append", default=[],
                   help="leave this reference example out of the prompt (e.g. ar_aging_by_customer)")
    g.add_argument("--examples", type=int, default=None,
                   help="number of reference examples in the prompt (default 1 local, 2 claude; 0 for none)")
    backend_args(g)

    c = sub.add_parser("check", help="check that the model backend is reachable and the model is installed")
    backend_args(c)

    r = sub.add_parser("render", help="spec JSON -> artifacts, no API call")
    r.add_argument("spec")
    r.add_argument("-o", "--out", required=True)

    v = sub.add_parser("validate", help="check a SQL file against the catalog")
    v.add_argument("sql_file")
    v.add_argument("-p", "--param", action="append", default=None, help="declared parameter name")

    q = sub.add_parser("retrieve", help="show which catalog objects a request would pull in")
    q.add_argument("request")

    k = sub.add_parser("kb", help="Postgres knowledge base: setup, load, embed, status, search, eval, add-example")
    k.add_argument("action", choices=["setup", "init", "load", "embed", "status", "search", "eval", "add-example"])
    k.add_argument("text", nargs="?", help="search: request text; add-example: path to a spec.json")
    k.add_argument("--name", help="add-example: example name (default: the spec's report_name, lower case)")
    k.add_argument("--request", help="add-example: the request the report answers")
    k.add_argument("--pause-every", type=int, default=2048, help="embed: rest after this many chunks (0 = never)")
    k.add_argument("--pause-seconds", type=float, default=30.0, help="embed: seconds to rest each time")

    args = ap.parse_args(argv)
    if args.cmd == "kb":
        return kb_command(args)
    log = lambda m: print(f"[agent] {m}", file=sys.stderr)  # noqa: E731
    knowledge = None if args.cmd == "check" else load_knowledge(args.kb, args.catalog, log)
    catalog = knowledge.catalog if knowledge else None

    if args.cmd == "check":
        backend = _backend(args)
        if args.backend == "claude":
            print("claude backend: needs ANTHROPIC_API_KEY (or an `ant auth login` profile); not checked offline")
            return 0
        try:
            lines = backend.check()
        except BackendError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print("\n".join(lines))
        return 1 if any(line.startswith("MISSING") for line in lines) else 0

    if args.cmd == "generate":
        from .agent import AgentError, ReportAgent

        log(f"knowledge: {knowledge.source}")
        agent = ReportAgent(catalog, backend=_backend(args), n_examples=args.examples,
                            exclude_examples=args.holdout, retriever=knowledge.retriever(),
                            examples=knowledge.examples(), example_picker=knowledge.example_picker(),
                            log=log)
        try:
            result = agent.generate(args.request)
        except AgentError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        out = Path(args.out)
        val = write_outputs(result.spec, catalog, out, request=args.request)
        (out / "request.txt").write_text(args.request + "\n")
        print(f"wrote {out}/ ({agent.backend.describe()}, {result.steps} model calls, {result.repairs} repairs, "
              f"{result.usage.get('input_tokens', 0)} in / {result.usage.get('output_tokens', 0)} out tokens)")
        _print_validation(val)
        return 0 if val["ok"] else 1

    if args.cmd == "render":
        spec = ReportSpec.from_dict(json.loads(Path(args.spec).read_text()))
        val = write_outputs(spec, catalog, Path(args.out))
        print(f"wrote {args.out}/")
        _print_validation(val)
        return 0 if val["ok"] else 1

    if args.cmd == "validate":
        rep = validate_sql(Path(args.sql_file).read_text(), catalog, args.param)
        print(rep.summary())
        return 0 if rep.ok else 1

    if args.cmd == "retrieve":
        print(f"knowledge: {knowledge.source}")
        res = knowledge.retriever().search(args.request)
        for n in res.tables:
            print(f"{res.scores[n]:6.2f}  {n}")
        print("\njoins:")
        for e in res.edges:
            print(f"  {e.describe()}")
        return 0
    return 1


def kb_command(args) -> int:
    from .knowledge import KnowledgeBase
    from .pgdb import DBError, db_url

    kb = KnowledgeBase(log=lambda m: print(m, file=sys.stderr))
    try:
        if args.action in ("setup", "init"):
            kb.init()
            print(f"schema kb ready in {db_url()}")
        if args.action in ("setup", "load"):
            print(json.dumps(kb.load(args.catalog)))
        if args.action in ("setup", "embed"):
            print(f"embedded {kb.embed_missing(pause_every=args.pause_every, pause_seconds=args.pause_seconds)} chunks")
        if args.action in ("setup", "status", "load", "embed"):
            print(json.dumps(kb.status(), indent=2))
        if args.action == "search":
            for via, hits in kb.search(args.text or "").items():
                print(f"{via}:")
                for h in hits[:10]:
                    print(f"  {h.score:6.3f}  {h.name}")
        if args.action == "eval":
            return kb_eval(kb, args.catalog)
        if args.action == "add-example":
            spec = json.loads(Path(args.text).read_text())
            name = args.name or spec.get("report_name", Path(args.text).stem).lower()
            kb.add_example(name, spec, request=args.request)
            print(f"added example {name}; it will be offered for similar requests")
    except DBError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


def kb_eval(kb, catalog_dir) -> int:
    """Table recall of keyword vs hybrid retrieval on examples/retrieval_eval.json."""
    from .retrieval import HybridRetriever, Retriever

    cases = json.loads((Path(__file__).resolve().parents[1] / "examples" / "retrieval_eval.json").read_text())
    catalog = kb.catalog()
    for label, r in (("keyword", Retriever(catalog)), ("hybrid", HybridRetriever(catalog, kb))):
        totals: dict[str, list[int]] = {}
        for c in cases:
            got = set(r.search(c["q"]).tables)
            t = totals.setdefault(c.get("set", "core"), [0, 0])
            t[0] += len(set(c["expect"]) & got)
            t[1] += len(c["expect"])
        print(f"{label:8s} " + "  ".join(f"{s}: {h}/{n} tables ({h / n:.0%})" for s, (h, n) in totals.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
