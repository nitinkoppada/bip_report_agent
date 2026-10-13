#!/usr/bin/env python3
"""Crawl Oracle Fusion Cloud "Tables and Views for Financials" (oedmf) metadata.

Writes one JSON file per table/view in the same shape as the files in
../tables/ so the two sources can be mixed:

  {"name", "object_type", "owner", "schema", "tablespace", "description",
   "primary_key": {"name", "columns": [...]},
   "columns": [[NAME, DATATYPE, LENGTH, PRECISION, NOT_NULL, COMMENT], ...],
   "flexfield_columns": null,
   "foreign_keys": [[TABLE, FOREIGN_TABLE, COLUMN], ...],
   "indexes": [[NAME, UNIQUE, "COL1,COL2"], ...],
   "view_sql": str | None, "source_url", "prev_url", "next_url"}

Usage:
  (standard library only; uses beautifulsoup4 if it happens to be installed)
  python3 crawl_oedmf.py --release 26d --out ../tables                 # all AR_/RA_ objects
  python3 crawl_oedmf.py --release 26d --prefix AR_ --prefix RA_ --prefix ARB_ --out ../tables
  python3 crawl_oedmf.py --release 26d --names AR_CASH_RECEIPTS_ALL RA_TERMS_B --out ../tables
  python3 crawl_oedmf.py --list-only --release 26d                     # just print the inventory
  python3 crawl_oedmf.py --base-url https://docs.oracle.com/en/cloud/saas/sales/oedms/ \
      --names HZ_LOCATIONS HZ_CUST_ACCT_SITES_ALL --out ../tables         # HZ_ tables live in the Sales guide

Polite by default: one request at a time, --delay seconds between requests
(default 1.5), retries with backoff, and existing files are skipped unless
--force is given, so a rerun resumes where it stopped.

Needs network access to docs.oracle.com.
"""
import argparse
import json
import os
import re
import sys
import time

import urllib.error
import urllib.request
from urllib.parse import urljoin

try:  # optional; the standard-library fallbacks below behave the same for this crawler
    from bs4 import BeautifulSoup
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from minisoup import BeautifulSoup

BASE = "https://docs.oracle.com/en/cloud/saas/financials/{release}/oedmf/"
UA = "bip-report-agent-metadata-crawler/1.0 (+polite; 1 req per {delay}s)"
NAME_RE = re.compile(r"^[A-Z][A-Z0-9_$#]*$")


class Fetcher:
    def __init__(self, delay, retries=4):
        self.delay = delay
        self.retries = retries
        self.last = 0.0
        self.ua = UA.format(delay=delay)

    def get(self, url):
        for attempt in range(self.retries + 1):
            wait = self.delay - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()
            try:
                req = urllib.request.Request(url, headers={"User-Agent": self.ua})
                with urllib.request.urlopen(req, timeout=60) as r:
                    charset = r.headers.get_content_charset() or "utf-8"
                    return r.read().decode(charset, errors="replace")
            except urllib.error.HTTPError as e:
                if e.code in (404, 410):
                    return None
                print(f"  ! {e}", file=sys.stderr)
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                print(f"  ! {e}", file=sys.stderr)
            time.sleep(2 ** (attempt + 1))
        raise RuntimeError(f"giving up on {url}")


def text(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip() if el else ""


# ---------------------------------------------------------------- inventory

def inventory(fetcher, base, prefixes, chapter, include_audit=False):
    """Return {NAME: url} for every TOC link whose text looks like an object name."""
    html = fetcher.get(base + "toc.htm")
    if not html:
        raise SystemExit(f"no toc.htm at {base}")
    soup = BeautifulSoup(html, "html.parser")
    scope = soup
    if chapter:
        # Chapter headings are list items like "12 Receivables" with a nested list of links.
        pat = re.compile(r"^\d+\s+" + re.escape(chapter) + r"$", re.I)
        for li in soup.find_all("li"):
            head = li.find(["a", "span", "p", "div"], recursive=False)
            label = text(head) if head else (li.find(string=True, recursive=False) or "").strip()
            if pat.match(label):
                scope = li
                break
        else:
            print(f"! chapter '{chapter}' not found in TOC; using whole TOC", file=sys.stderr)
    out = {}
    for a in scope.find_all("a", href=True):
        name = text(a)
        if not NAME_RE.match(name):
            continue
        if prefixes and not any(name.startswith(p) for p in prefixes):
            continue
        if name.endswith("_") and not include_audit:
            continue  # NAME_ pages are audit copies of NAME (AUDIT_* columns)
        url = urljoin(base, a["href"].split("#")[0])
        out.setdefault(name, url)
    return out


# ---------------------------------------------------------------- page parse

def table_rows(tbl):
    rows = []
    for tr in tbl.find_all("tr"):
        cells = [text(c) for c in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    return rows


def section_label(tbl):
    """Find the heading / caption that names a table on the page."""
    cap = tbl.find("caption")
    if cap and text(cap):
        return text(cap)
    for prev in tbl.find_all_previous(["h1", "h2", "h3", "h4", "h5", "p", "div"], limit=6):
        t = text(prev)
        if t and len(t) < 60:
            return t
    return ""


def as_int(v):
    return int(v) if v and v.isdigit() else None


FLEX_RE = re.compile(r"^(GLOBAL_|EXTN_)?ATTRIBUTE(_CATEGORY|\d+|_(NUMBER|DATE|TIMESTAMP|CHAR|CLOB)\d+)$")


def summarize_flexfields(rec):
    """Move ATTRIBUTE*/GLOBAL_ATTRIBUTE* columns out of `columns` into a one-line summary,
    matching the hand-extracted files (keeps the catalog readable for SQL generation)."""
    flex = [c for c in rec["columns"] if FLEX_RE.match(c[0] or "")]
    if not flex:
        return
    rec["columns"] = [c for c in rec["columns"] if not FLEX_RE.match(c[0] or "")]
    groups = {}
    for c in flex:
        m = re.match(r"^(.*?)(\d+)$", c[0])
        key, num = (m.group(1), int(m.group(2))) if m else (c[0], None)
        groups.setdefault(key, []).append(num)
    parts = []
    for key, nums in groups.items():
        nums = sorted(n for n in nums if n is not None)
        if not nums:
            parts.append(key)
        elif len(nums) == 1:
            parts.append(f"{key}{nums[0]}")
        else:
            parts.append(f"{key}{nums[0]}-{key}{nums[-1]}")
    rec["flexfield_columns"] = ("Skipped flexfield columns (" + str(len(flex)) + "): " + ", ".join(parts)
                                + ". Their datatypes and comments are on the source page.")


DTYPES = ("VARCHAR2|NVARCHAR2|NUMBER|DATE|TIMESTAMP\\(\\d\\) WITH LOCAL TIME ZONE|TIMESTAMP\\(\\d\\) WITH TIME ZONE|"
          "TIMESTAMP\\(\\d\\)|TIMESTAMP|CLOB|NCLOB|BLOB|CHAR|NCHAR|RAW|LONG|FLOAT|INTEGER|ROWID|XMLTYPE|BINARY_DOUBLE")
SQUASHED_RE = re.compile(r"^([A-Z][A-Z0-9_$#]*)(" + DTYPES + r")(\d*)(.*)$")


def squashed_column(p):
    """Columns on some pages (mostly *_GT temporary tables) come as one string per column,
    e.g. 'EXCHANGE_DATE_OLDDATEOracle internal use only'. The greedy name match takes the
    last datatype keyword, which is right for names ending in _DATE etc."""
    m = SQUASHED_RE.match(p)
    if not m:
        return [p, None, None, None, None, None]
    name, dtype, num, comment = m.groups()
    if dtype == "CHAR" and name.endswith("VAR") and num.startswith("2"):
        # greedy name swallowed VAR of VARCHAR2: 'X_TYPEVARCHAR230' -> X_TYPE VARCHAR2(30)
        dtype, name, num = ("NVARCHAR2", name[:-4], num[1:]) if name.endswith("NVAR") else ("VARCHAR2", name[:-3], num[1:])
    n = as_int(num)
    is_char = dtype in ("VARCHAR2", "NVARCHAR2", "CHAR", "NCHAR", "RAW")
    return [name, dtype, n if is_char else None, None if is_char else n, None, comment.strip() or None]


def split_top_level(s, sep=","):
    out, depth, cur, quote = [], 0, [], False
    for ch in s:
        if ch == "'":
            quote = not quote
        elif not quote and ch == "(":
            depth += 1
        elif not quote and ch == ")":
            depth -= 1
        if ch == sep and depth == 0 and not quote:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out


def view_columns(sql):
    """Column names of a view, read from its outermost SELECT list (aliases win)."""
    flat = re.sub(r"\s+", " ", sql).strip()
    m = re.match(r"(?is)^\s*(?:WITH\b.*?\)\s*)?SELECT\s+(?:DISTINCT\s+)?(.*)$", flat)
    if not m:
        return []
    body, depth, quote, end = m.group(1), 0, False, None
    for i, ch in enumerate(body):
        if ch == "'":
            quote = not quote
        elif not quote and ch == "(":
            depth += 1
        elif not quote and ch == ")":
            depth -= 1
        elif not quote and depth == 0 and re.match(r"(?i)\bFROM\b", body[i:i + 5]) and (i == 0 or not body[i - 1].isalnum() and body[i - 1] != "_"):
            end = i
            break
    cols = []
    for item in split_top_level(body[:end] if end else body):
        tok = re.findall(r'[A-Za-z_][A-Za-z0-9_$#]*|"[^"]+"', item.strip())
        if tok:
            cols.append(tok[-1].strip('"').upper())
    return cols


def parse_page(html, url):
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup.find("article") or soup.body or soup
    h1 = main.find(["h1", "h2"])
    rec = {
        "name": text(h1), "object_type": None, "owner": None, "schema": None, "tablespace": None,
        "description": "", "primary_key": None, "columns": [], "flexfield_columns": None,
        "foreign_keys": [], "indexes": [], "view_sql": None, "source_url": url,
        "prev_url": None, "next_url": None,
    }
    # description: paragraphs after the title, before the first section heading
    desc = []
    for el in (h1.find_all_next(["p", "h2", "h3", "table"]) if h1 else []):
        if el.name != "p":
            break
        t = text(el)
        if t.lower().startswith("details"):
            break
        desc.append(t)
    rec["description"] = "\n".join(d for d in desc if d)

    # details: "Schema: FUSION", "Object owner: AR", ...
    full = text(main)
    for key, label in (("schema", "Schema"), ("owner", "Object owner"),
                       ("object_type", "Object type"), ("tablespace", "Tablespace")):
        m = re.search(label + r"\s*:\s*([A-Za-z0-9_ ]+?)(?=\s+(?:Schema|Object|Tablespace|Primary|Columns|Query)\b|$)", full)
        if m:
            rec[key] = m.group(1).strip()

    for tbl in main.find_all("table"):
        rows = table_rows(tbl)
        if len(rows) < 2:
            continue
        header = [h.lower() for h in rows[0]]
        body = rows[1:]
        label = section_label(tbl).lower()
        if header == ["name"] and (tbl.get("summary") or "").lower() == "columns":
            # single-column layout: one <p> per column, either a bare name (views)
            # or name+datatype+length+comment run together (temporary tables)
            cell = tbl.find("td")
            for p in (cell.find_all("p") if cell else []):
                t = text(p)
                if t:
                    rec["columns"].append([t, None, None, None, None, None] if NAME_RE.match(t) else squashed_column(t))
        elif header == ["sql_statement"] or "sql_statement" in header:
            cell = tbl.find("td")
            if cell:
                rec["view_sql"] = "\n".join(p.get_text(" ", strip=True) for p in cell.find_all("p")) or cell.get_text(" ", strip=True)
        elif "datatype" in header or "data type" in header:
            ix = {h: i for i, h in enumerate(header)}
            g = lambda r, k: r[ix[k]] if k in ix and ix[k] < len(r) else ""
            for r in body:
                rec["columns"].append([
                    g(r, "name"), g(r, "datatype") or g(r, "data type"),
                    as_int(g(r, "length")), as_int(g(r, "precision")),
                    g(r, "not-null").lower() in ("yes", "y", "true") or g(r, "not null").lower() in ("yes", "y"),
                    g(r, "comments"),
                ])
        elif "foreign table" in header:
            for r in body:
                if len(r) >= 3:
                    rec["foreign_keys"].append(r[:3])
        elif "uniqueness" in header or "index" in header:
            ix = {h: i for i, h in enumerate(header)}
            for r in body:
                cols = r[ix["columns"]] if "columns" in ix and ix["columns"] < len(r) else r[-1]
                uniq = r[ix["uniqueness"]] if "uniqueness" in ix else ""
                rec["indexes"].append([r[0], uniq.lower() == "unique", re.sub(r"\s*,\s*", ",", cols)])
        elif "primary key" in label or (header[:2] == ["name", "columns"] and rec["primary_key"] is None):
            r = body[0]
            rec["primary_key"] = {"name": r[0], "columns": [c.strip() for c in r[-1].split(",")]}

    pre = main.find("pre")
    if pre and not rec["view_sql"]:
        rec["view_sql"] = pre.get_text()
    if rec["view_sql"] and not rec["columns"]:
        # view pages list no column table; take names from the SELECT list, datatypes unknown
        rec["columns"] = [[c, None, None, None, None, None] for c in view_columns(rec["view_sql"])]
    summarize_flexfields(rec)

    for a in soup.find_all("a", href=True):
        t = text(a).lower()
        if t in ("previous", "prev") and not rec["prev_url"]:
            rec["prev_url"] = urljoin(url, a["href"])
        elif t == "next" and not rec["next_url"]:
            rec["next_url"] = urljoin(url, a["href"])
    return rec


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--release", default="26d")
    ap.add_argument("--base-url", help="guide root instead of the Financials guide for --release, "
                                       "e.g. https://docs.oracle.com/en/cloud/saas/sales/oedms/")
    ap.add_argument("--prefix", action="append", help="object name prefix (repeatable); default AR_ and RA_")
    ap.add_argument("--chapter", default=None, help="limit to a TOC chapter, e.g. Receivables")
    ap.add_argument("--names", nargs="*", help="only these object names")
    ap.add_argument("--names-file", help="file with one object name per line (added to --names)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "tables"))
    ap.add_argument("--delay", type=float, default=1.5, help="seconds between requests")
    ap.add_argument("--force", action="store_true", help="re-fetch files that already exist")
    ap.add_argument("--list-only", action="store_true")
    ap.add_argument("--include-audit", action="store_true", help="also crawl NAME_ audit tables")
    ap.add_argument("--dump-html", help="save raw HTML here too, for debugging the parser")
    a = ap.parse_args()

    if a.names_file:
        with open(a.names_file) as fh:
            a.names = (a.names or []) + [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
    prefixes = a.prefix or ["AR_", "RA_"]
    f = Fetcher(a.delay)
    base = a.base_url or BASE.format(release=a.release)
    if not base.endswith("/"):
        base += "/"
    inv = inventory(f, base, None if a.names else prefixes, a.chapter, a.include_audit)
    if a.names:
        missing = [n for n in a.names if n not in inv]
        if missing:
            print(f"! not in TOC: {', '.join(missing)}", file=sys.stderr)
        inv = {n: inv[n] for n in a.names if n in inv}
    print(f"{len(inv)} objects in scope", file=sys.stderr)

    os.makedirs(a.out, exist_ok=True)
    tag = a.release if not a.base_url else re.sub(r"\W+", "_", base.split("/saas/")[-1]).strip("_")
    inv_path = os.path.join(a.out, "..", f"inventory_{tag}.json")
    with open(inv_path, "w") as fh:
        json.dump(inv, fh, indent=1, sort_keys=True)
    if a.list_only:
        for n, u in sorted(inv.items()):
            print(n, u)
        return

    done = failed = 0
    for i, (name, url) in enumerate(sorted(inv.items()), 1):
        path = os.path.join(a.out, f"{name}.json")
        if os.path.exists(path) and not a.force:
            continue
        print(f"[{i}/{len(inv)}] {name}", file=sys.stderr)
        try:
            html = f.get(url)
            if html is None:
                raise RuntimeError("404")
            if a.dump_html:
                os.makedirs(a.dump_html, exist_ok=True)
                open(os.path.join(a.dump_html, name + ".html"), "w").write(html)
            rec = parse_page(html, url)
            rec["name"] = rec["name"] or name
            if not rec["columns"]:
                print(f"  ! no columns parsed for {name}; check with --dump-html", file=sys.stderr)
            with open(path + ".tmp", "w") as fh:
                json.dump(rec, fh, indent=1)
            os.replace(path + ".tmp", path)
            done += 1
        except Exception as e:  # keep going; rerun picks up failures
            print(f"  ! {name}: {e}", file=sys.stderr)
            failed += 1
    print(f"written {done}, failed {failed}, skipped {len(inv) - done - failed}", file=sys.stderr)


if __name__ == "__main__":
    main()
