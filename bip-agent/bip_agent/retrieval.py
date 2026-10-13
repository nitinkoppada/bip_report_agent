"""Pick the catalog objects relevant to a report request.

Lexical BM25 over each object's name, description and column names/comments,
plus a small Receivables vocabulary that maps business words ("aging",
"receipt", "customer") to the tables that hold them. Only the top objects and
the FK edges among them go into the prompt; the model can ask for more with
the lookup tools.
"""
from __future__ import annotations

import math
import os
import re
from collections import Counter
from dataclasses import dataclass

from .catalog import Catalog, JoinEdge

_TOKEN = re.compile(r"[A-Za-z0-9]+")
_STOP = {
    "the", "a", "an", "of", "and", "or", "for", "to", "in", "by", "with", "on",
    "this", "that", "is", "are", "be", "each", "all", "table", "column", "stores",
    "contains", "row", "rows", "information", "identifier", "id", "report", "show",
    "list", "me", "give", "want", "need", "get", "from", "which", "what", "per",
}

# Business vocabulary -> objects that answer it. Kept short and Receivables-specific.
DOMAIN_HINTS: dict[str, list[str]] = {
    "aging": ["AR_PAYMENT_SCHEDULES_ALL", "AR_AGING_BUCKETS", "AR_AGING_BUCKET_LINES_B"],
    "ageing": ["AR_PAYMENT_SCHEDULES_ALL", "AR_AGING_BUCKETS", "AR_AGING_BUCKET_LINES_B"],
    "overdue": ["AR_PAYMENT_SCHEDULES_ALL"],
    "past": ["AR_PAYMENT_SCHEDULES_ALL"],
    "due": ["AR_PAYMENT_SCHEDULES_ALL"],
    "open": ["AR_PAYMENT_SCHEDULES_ALL"],
    "outstanding": ["AR_PAYMENT_SCHEDULES_ALL"],
    "balance": ["AR_PAYMENT_SCHEDULES_ALL"],
    "invoice": ["RA_CUSTOMER_TRX_ALL", "AR_PAYMENT_SCHEDULES_ALL", "RA_CUST_TRX_TYPES_ALL"],
    "invoices": ["RA_CUSTOMER_TRX_ALL", "AR_PAYMENT_SCHEDULES_ALL", "RA_CUST_TRX_TYPES_ALL"],
    "transaction": ["RA_CUSTOMER_TRX_ALL", "RA_CUST_TRX_TYPES_ALL"],
    "transactions": ["RA_CUSTOMER_TRX_ALL", "RA_CUST_TRX_TYPES_ALL"],
    "line": ["RA_CUSTOMER_TRX_LINES_ALL"],
    "lines": ["RA_CUSTOMER_TRX_LINES_ALL"],
    "revenue": ["RA_CUST_TRX_LINE_GL_DIST_ALL", "RA_CUSTOMER_TRX_LINES_ALL"],
    "distribution": ["RA_CUST_TRX_LINE_GL_DIST_ALL", "AR_DISTRIBUTIONS_ALL"],
    "credit": ["RA_CUSTOMER_TRX_ALL", "RA_CUST_TRX_TYPES_ALL"],
    "memo": ["RA_CUSTOMER_TRX_ALL", "RA_CUST_TRX_TYPES_ALL"],
    "receipt": ["AR_CASH_RECEIPTS_ALL", "AR_RECEIVABLE_APPLICATIONS_ALL", "AR_RECEIPT_METHODS"],
    "receipts": ["AR_CASH_RECEIPTS_ALL", "AR_RECEIVABLE_APPLICATIONS_ALL", "AR_RECEIPT_METHODS"],
    "cash": ["AR_CASH_RECEIPTS_ALL", "AR_RECEIVABLE_APPLICATIONS_ALL"],
    "payment": ["AR_CASH_RECEIPTS_ALL", "AR_PAYMENT_SCHEDULES_ALL"],
    "payments": ["AR_CASH_RECEIPTS_ALL", "AR_PAYMENT_SCHEDULES_ALL"],
    "applied": ["AR_RECEIVABLE_APPLICATIONS_ALL"],
    "application": ["AR_RECEIVABLE_APPLICATIONS_ALL"],
    "applications": ["AR_RECEIVABLE_APPLICATIONS_ALL"],
    "unapplied": ["AR_RECEIVABLE_APPLICATIONS_ALL", "AR_CASH_RECEIPTS_ALL"],
    "adjustment": ["AR_ADJUSTMENTS_ALL", "AR_RECEIVABLES_TRX_ALL"],
    "adjustments": ["AR_ADJUSTMENTS_ALL", "AR_RECEIVABLES_TRX_ALL"],
    "writeoff": ["AR_ADJUSTMENTS_ALL", "AR_RECEIVABLES_TRX_ALL"],
    "customer": ["HZ_CUST_ACCOUNTS", "HZ_PARTIES"],
    "customers": ["HZ_CUST_ACCOUNTS", "HZ_PARTIES"],
    "site": ["HZ_CUST_SITE_USES_ALL", "HZ_CUST_ACCT_SITES_ALL", "HZ_PARTY_SITES"],
    "address": ["HZ_LOCATIONS", "HZ_PARTY_SITES", "HZ_CUST_ACCT_SITES_ALL"],
    "collector": ["AR_COLLECTORS"],
    "terms": ["RA_TERMS_B", "RA_TERMS_TL"],
    "batch": ["AR_BATCHES_ALL", "RA_BATCH_SOURCES_ALL"],
    "source": ["RA_BATCH_SOURCES_ALL"],
    "type": ["RA_CUST_TRX_TYPES_ALL"],
    "dispute": ["AR_PAYMENT_SCHEDULES_ALL", "AR_DISPUTE_HISTORY"],
    "accounting": ["AR_DISTRIBUTIONS_ALL", "RA_CUST_TRX_LINE_GL_DIST_ALL"],
    "bu": ["HR_ORGANIZATION_UNITS_F_TL", "HR_ALL_ORGANIZATION_UNITS_F", "FND_SETID_ASSIGNMENTS"],
    "business": ["HR_ORGANIZATION_UNITS_F_TL", "HR_ALL_ORGANIZATION_UNITS_F", "FND_SETID_ASSIGNMENTS"],
    "lookup": ["FND_LOOKUP_VALUES_TL", "FND_LOOKUP_VALUES_B"],
    "meaning": ["FND_LOOKUP_VALUES_TL"],
}

# Lookup tables worth pulling in whenever a fact table they describe is selected.
DIMENSIONS = {
    "HZ_CUST_ACCOUNTS", "HZ_PARTIES", "RA_CUST_TRX_TYPES_ALL", "RA_TERMS_B",
    "AR_RECEIPT_METHODS", "RA_BATCH_SOURCES_ALL", "AR_RECEIVABLES_TRX_ALL",
}

# Translation tables that carry the display names of a chosen base table (X_B -> X_TL is automatic).
COMPANIONS = {
    "HR_ALL_ORGANIZATION_UNITS_F": ["HR_ORGANIZATION_UNITS_F_TL"],
    "FND_LOOKUP_VALUES_B": ["FND_LOOKUP_VALUES_TL"],
}

# Central transaction tables, pulled in when one of the top hits joins to them.
CORE = {"RA_CUSTOMER_TRX_ALL", "AR_PAYMENT_SCHEDULES_ALL", "AR_CASH_RECEIPTS_ALL"}


def tokenize(text: str) -> list[str]:
    out = []
    for tok in _TOKEN.findall(text.replace("_", " ").lower()):
        if tok in _STOP or len(tok) < 2:
            continue
        # crude singularisation so "receipts" meets "receipt"
        if len(tok) > 4 and tok.endswith("s") and not tok.endswith("ss"):
            tok = tok[:-1]
        out.append(tok)
    return out


def _type_weight(name: str, object_type: str) -> float:
    """Prefer base tables over temp, interface and UI helper views."""
    if name.endswith("_GT") or "_INTERFACE" in name or name.endswith("_INT"):
        return 0.3
    if name.endswith(("_TL", "_VL")):
        return 0.5
    if object_type == "VIEW":
        return 0.6
    if name.endswith("_ALL") or name.startswith("HZ_"):
        return 1.2
    return 1.0


@dataclass
class RetrievalResult:
    tables: list[str]
    scores: dict[str, float]
    edges: list[JoinEdge]


class Retriever:
    def __init__(self, catalog: Catalog, k1: float = 1.4, b: float = 0.6):
        self.catalog = catalog
        self.k1, self.b = k1, b
        self.docs: dict[str, Counter] = {}
        for name, t in catalog.tables.items():
            parts = [name, name, name, t.description]  # name weighted 3x
            for c in t.columns.values():
                parts.append(c.name)
                if c.comment:
                    parts.append(c.comment)
            self.docs[name] = Counter(tokenize(" ".join(parts)))
        self.doc_len = {n: sum(c.values()) for n, c in self.docs.items()}
        self.avg_len = sum(self.doc_len.values()) / max(1, len(self.doc_len))
        df: Counter = Counter()
        for c in self.docs.values():
            df.update(c.keys())
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def bm25(self, query_tokens: list[str]) -> dict[str, float]:
        scores: dict[str, float] = {}
        for name, tf in self.docs.items():
            s = 0.0
            dl = self.doc_len[name]
            for q in query_tokens:
                f = tf.get(q)
                if not f:
                    continue
                s += self.idf.get(q, 0) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avg_len))
            if s:
                scores[name] = s
        return scores

    def rank(self, request: str) -> dict[str, float]:
        """Relevance score per catalog object (higher is better)."""
        raw_tokens = [t.lower() for t in _TOKEN.findall(request)]
        q = tokenize(request)
        scores = self.bm25(q)
        if scores:
            top = max(scores.values())
            scores = {n: s / top for n, s in scores.items()}
        for name in list(scores):
            scores[name] *= _type_weight(name, self.catalog.tables[name].object_type)
        # Explicitly named objects and domain hints get a strong boost.
        for tok in raw_tokens + q:
            for name in DOMAIN_HINTS.get(tok, []):
                if name in self.catalog:
                    scores[name] = scores.get(name, 0) + 1.0
        for m in re.findall(r"\b(?:AR|RA|HZ)_[A-Z0-9_]+\b", request.upper()):
            if m in self.catalog:
                scores[m] = scores.get(m, 0) + 3.0
        return scores

    def search(self, request: str, top_k: int = 8) -> RetrievalResult:
        scores = self.rank(request)
        ranked = sorted(scores, key=lambda n: (-scores[n], n))
        chosen = ranked[:top_k]
        # Pull in the lookup tables joined to what we chose, and the core
        # transaction tables joined to the top three hits.
        for rank, name in enumerate(list(chosen)):
            for e in self.catalog.edges_for(name):
                other = e.parent if e.child == name else e.child
                wanted = other in DIMENSIONS or (rank < 3 and other in CORE)
                if wanted and other not in chosen and other in self.catalog:
                    chosen.append(other)
        # Names live in translation tables: add the _TL companion of each chosen base table.
        for name in list(chosen):
            tl = COMPANIONS.get(name, []) + ([name[:-2] + "_TL"] if name.endswith("_B") else [])
            chosen += [t for t in tl if t in self.catalog and t not in chosen]
        # HZ_CUST_ACCOUNTS without HZ_PARTIES gives no customer name.
        if "HZ_CUST_ACCOUNTS" in chosen and "HZ_PARTIES" not in chosen:
            chosen.append("HZ_PARTIES")
        chosen_set = set(chosen)
        edges = [
            e for e in self.catalog.joins
            if e.child in chosen_set and e.parent in chosen_set and e.child != e.parent
        ]
        return RetrievalResult(chosen, {n: scores.get(n, 0.0) for n in chosen}, edges)

    def search_names(self, query: str, limit: int = 15) -> list[tuple[str, float, str]]:
        """Ranked (name, score, short description) for the search_catalog tool."""
        q = tokenize(query)
        scores = self.bm25(q)
        for name in list(scores):
            scores[name] *= _type_weight(name, self.catalog.tables[name].object_type)
        ranked = sorted(scores, key=lambda n: -scores[n])[:limit]
        return [(n, round(scores[n], 2), self.catalog.tables[n].description[:120]) for n in ranked]


# Request words -> product prefixes. When a request names a module ("customer", "supplier",
# "journal"), tables from other modules are down-weighted, which matters once the catalog holds
# all of Financials instead of Receivables alone. BIP_AGENT_MODULES=AR,GL pins the modules instead.
MODULE_WORDS: list[tuple[str, tuple[str, ...]]] = [
    (r"\b(receivables?|customers?|receipts?|collectors?|aging|ageing|dunning|ar|debit memos?|credit memos?|"
     r"chargebacks?|bill-to|ship-to|remit)\b", ("AR_", "RA_", "HZ_", "ARB_", "IEX_")),
    (r"\b(payables?|suppliers?|vendors?|ap)\b", ("AP_", "IBY_", "HZ_")),
    (r"\b(general ledger|ledgers?|journals?|gl|trial balance|chart of accounts|code combinations?)\b", ("GL_",)),
    (r"\b(subledger|accounting entr(?:y|ies)|accounting lines|xla)\b", ("XLA_",)),
    (r"\b(tax|taxes|withholding)\b", ("ZX_",)),
    (r"\b(bank statements?|cash management|bank accounts?)\b", ("CE_",)),
    (r"\b(fixed assets?|assets?|depreciation)\b", ("FA_",)),
    (r"\b(revenue contracts?|performance obligations?|revenue management)\b", ("VRM_",)),
    (r"\b(expenses?|expense reports?)\b", ("EXM_",)),
    (r"\b(intercompany)\b", ("FUN_",)),
]


# Shared setup tables (lookups, business units) belong to every module; never down-weighted.
SHARED_PREFIXES = ("FND_", "HR_")


def request_modules(request: str) -> tuple[str, ...]:
    pinned = os.environ.get("BIP_AGENT_MODULES", "").strip()
    if pinned:
        return tuple(p.strip().upper().rstrip("_") + "_" for p in pinned.split(",") if p.strip())
    text = request.lower()
    out: list[str] = []
    for pat, prefixes in MODULE_WORDS:
        if re.search(pat, text):
            out += [p for p in prefixes if p not in out]
    return tuple(out)


class HybridRetriever(Retriever):
    """BM25 + domain hints fused with pgvector search over the Postgres knowledge base.

    Four ranked lists go into reciprocal rank fusion: the lexical ranking above,
    object-description vectors, column-comment vectors (best column per object)
    and Postgres full text. Fusion is by rank, so the different score scales don't
    matter; explicit table names in the request still win outright.
    """

    # Tuned on examples/retrieval_eval.json (30 requests): lexical keeps its lead on
    # requests in Receivables vocabulary; vectors add the paraphrased ones.
    WEIGHTS = {"lexical": 2.0, "object_vector": 1.0, "column_vector": 0.7, "full_text": 0.5}
    RRF_K = 10
    OTHER_MODULE_WEIGHT = 0.6
    HINT_BOOST = 0.5

    def __init__(self, catalog: Catalog, kb, **kw):
        super().__init__(catalog, **kw)
        self.kb = kb
        self.last_signals: dict[str, list[str]] = {}

    def rank(self, request: str) -> dict[str, float]:
        lexical = super().rank(request)
        lists = {"lexical": sorted(lexical, key=lambda n: -lexical[n])[:40]}
        for via, hits in self.kb.search(request).items():
            lists[via] = [h.name for h in hits if h.name in self.catalog]
        self.last_signals = {k: v[:8] for k, v in lists.items()}
        fused: dict[str, float] = {}
        for via, names in lists.items():
            w = self.WEIGHTS[via]
            for r, name in enumerate(names):
                fused[name] = fused.get(name, 0.0) + w / (self.RRF_K + r + 1)
        top = max(fused.values()) if fused else 1.0
        modules = request_modules(request)
        for name in fused:
            fused[name] = fused[name] / top * _type_weight(name, self.catalog.tables[name].object_type)
            if modules and not name.startswith(modules) and not name.startswith(SHARED_PREFIXES):
                fused[name] *= self.OTHER_MODULE_WEIGHT
        # Vocabulary hits ("bu", "lookup", "aging") keep their tables in the top results even
        # when vectors favour others; type weighting would otherwise bury e.g. a _TL name table.
        words = {t.lower() for t in _TOKEN.findall(request)} | set(tokenize(request))
        for name in {n for w in words for n in DOMAIN_HINTS.get(w, []) if n in self.catalog}:
            fused[name] = fused.get(name, 0) + self.HINT_BOOST
        for m in re.findall(r"\b(?:AR|RA|HZ)_[A-Z0-9_]+\b", request.upper()):
            if m in self.catalog:
                fused[m] = fused.get(m, 0) + 3.0
        return fused

    def search_names(self, query: str, limit: int = 15) -> list[tuple[str, float, str]]:
        scores = self.rank(query)
        ranked = sorted(scores, key=lambda n: -scores[n])[:limit]
        return [(n, round(scores[n], 3), self.catalog.tables[n].description[:120]) for n in ranked]
