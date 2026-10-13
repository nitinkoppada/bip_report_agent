#!/usr/bin/env python3
"""Combine ../tables/*.json into one catalog plus a join map and a Markdown summary.

Scope: when ../scope_*.txt files exist (one table name per line), only those tables go into
the catalog; views, import/interface and temporary (_GT) tables are left out that way.

Outputs (next to the tables/ folder):
  catalog.json              every in-scope table, keyed by name
  joins.json                FK edges: child.column -> parent (parent key from its PK when known)
  SUMMARY.md                human-readable overview
"""
import glob
import json
import os
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
GROUPS = [
    ("Transactions", ["RA_CUSTOMER_TRX_ALL", "RA_CUSTOMER_TRX_LINES_ALL", "RA_CUST_TRX_LINE_GL_DIST_ALL",
                      "RA_CUST_TRX_LINE_SALESREPS_ALL", "RA_INTERFACE_LINES_ALL", "AR_DEFERRED_LINES_ALL"]),
    ("Receipts and applications", ["AR_CASH_RECEIPTS_ALL", "AR_CASH_RECEIPT_HISTORY_ALL",
                                   "AR_RECEIVABLE_APPLICATIONS_ALL", "AR_BATCHES_ALL"]),
    ("Balances, adjustments and accounting", ["AR_PAYMENT_SCHEDULES_ALL", "AR_ADJUSTMENTS_ALL",
                                              "AR_DISTRIBUTIONS_ALL", "AR_CONS_INV_ALL", "AR_DISPUTE_HISTORY"]),
    ("Setups", ["RA_CUST_TRX_TYPES_ALL", "RA_BATCH_SOURCES_ALL", "RA_TERMS_B", "RA_TERMS_LINES",
                "AR_RECEIPT_METHODS", "AR_RECEIPT_CLASSES", "AR_RECEIPT_METHOD_ACCOUNTS_ALL",
                "AR_BATCH_SOURCES_ALL", "AR_RECEIVABLES_TRX_ALL", "AR_MEMO_LINES_ALL_B",
                "AR_SYSTEM_PARAMETERS_ALL", "AR_AGING_BUCKETS", "AR_AGING_BUCKET_LINES_B",
                "AR_COLLECTORS", "AR_LOOKUPS"]),
    ("Customers (TCA)", ["HZ_CUST_ACCOUNTS", "HZ_PARTIES", "HZ_CUST_ACCT_SITES_ALL",
                         "HZ_CUST_SITE_USES_ALL", "HZ_PARTY_SITES", "HZ_LOCATIONS"]),
]


def main():
    objs = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "tables", "*.json"))):
        with open(p) as fh:
            o = json.load(fh)
        objs[o["name"].upper()] = o
    scope_files = sorted(glob.glob(os.path.join(ROOT, "scope_*.txt")))
    if scope_files:
        scope = set()
        for f in scope_files:
            with open(f) as fh:
                scope |= {ln.strip().upper() for ln in fh if ln.strip() and not ln.startswith("#")}
        missing = sorted(scope - set(objs))
        if missing:
            print(f"! {len(missing)} in-scope tables have no crawled file: {', '.join(missing[:20])}")
        objs = {n: o for n, o in objs.items() if n in scope}

    pk = {n: (o.get("primary_key") or {}).get("columns") or [] for n, o in objs.items()}
    edges, seen = [], set()
    for n, o in objs.items():
        for fk in o.get("foreign_keys") or []:
            if len(fk) < 3:
                continue
            child, parent, col = fk[0].upper(), fk[1].upper(), fk[2].upper()
            key = (child, col, parent)
            if key in seen:
                continue
            seen.add(key)
            pcols = pk.get(parent, [])
            edges.append({
                "child": child, "child_column": col, "parent": parent,
                "parent_column": pcols[0] if len(pcols) == 1 else None,
                "parent_pk": pcols, "both_in_catalog": child in objs and parent in objs,
            })

    with open(os.path.join(ROOT, "catalog.json"), "w") as fh:
        json.dump(objs, fh, indent=1, sort_keys=True)
    with open(os.path.join(ROOT, "joins.json"), "w") as fh:
        json.dump(sorted(edges, key=lambda e: (e["child"], e["child_column"])), fh, indent=1)

    out = ["# Oracle Fusion Financials table metadata", "",
           f"{len(objs)} objects, {sum(len(o.get('columns') or []) for o in objs.values())} columns, "
           f"{len(edges)} foreign key edges ({sum(e['both_in_catalog'] for e in edges)} between objects in this catalog).",
           "", "Source: Oracle Fusion Cloud *Tables and Views for Financials* (all tables) and *Tables and Views for Sales* "
           "(HZ_ customer tables) on docs.oracle.com, crawled with `crawler/crawl_oedmf.py`. Views, import/interface "
           "and temporary (_GT) tables are excluded. "
           "Each table file records its `source_url`, which names the release.",
           "", "Flexfield columns (ATTRIBUTE*, GLOBAL_ATTRIBUTE*) are summarised per table in `flexfield_columns` rather than listed.", ""]
    listed = set()
    for title, names in GROUPS:
        out += [f"## {title}", "", "| Object | Type | Cols | Primary key | Description |", "|---|---|---|---|---|"]
        for n in names:
            o = objs.get(n)
            listed.add(n)
            if not o:
                out.append(f"| {n} | missing | | | |")
                continue
            d = (o.get("description") or "").replace("\n", " ").replace("|", "/")
            d = d[:160] + ("..." if len(d) > 160 else "")
            out.append(f"| {n} | {o.get('object_type') or ''} | {len(o.get('columns') or [])} | "
                       f"{', '.join(pk.get(n) or [])} | {d} |")
        out.append("")
    extra = sorted(set(objs) - listed)
    if extra:
        out += [f"## Other objects ({len(extra)})", "", "| Object | Type | Cols | Description |", "|---|---|---|---|"]
        for n in extra:
            o = objs[n]
            d = (o.get("description") or "").replace("\n", " ").replace("|", "/")
            d = d[:100] + ("..." if len(d) > 100 else "")
            out.append(f"| {n} | {o.get('object_type') or ''} | {len(o.get('columns') or [])} | {d} |")
        out.append("")

    core = defaultdict(list)
    for e in edges:
        if e["child"] in listed and e["parent"] in listed and e["child"] != e["parent"]:
            core[e["child"]].append(e)
    out += ["## Key joins between core objects", "",
            "Child column -> parent key between the grouped objects above, taken from each page's Foreign Keys table. "
            "`joins.json` has every edge.", ""]
    for child in sorted(core):
        for e in sorted(core[child], key=lambda e: e["child_column"]):
            pc = e["parent_column"] or "/".join(e["parent_pk"]) or "?"
            out.append(f"- `{child}.{e['child_column']}` -> `{e['parent']}.{pc}`")
    gaps = os.path.join(ROOT, "KNOWN_GAPS.md")
    if os.path.exists(gaps):
        out += ["", open(gaps).read().strip()]
    with open(os.path.join(ROOT, "SUMMARY.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"{len(objs)} objects, {len(edges)} edges")


if __name__ == "__main__":
    main()
