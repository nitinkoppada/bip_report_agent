"""Postgres knowledge base tests. They run against the local database and skip when it isn't loaded."""
import pytest

from bip_agent.catalog import Catalog
from bip_agent.knowledge import KnowledgeBase
from bip_agent.pgdb import lit
from bip_agent.retrieval import HybridRetriever


@pytest.fixture(scope="session")
def kb():
    k = KnowledgeBase()
    if not k.ready():
        pytest.skip("Postgres knowledge base not loaded (python3 -m bip_agent kb setup)")
    return k


def test_lit_quotes_safely():
    assert lit("it's $q$ here") == "$qq$it's $q$ here$qq$"
    assert lit(None) == "NULL" and lit(True) == "TRUE" and lit(3) == "3"


def test_postgres_catalog_matches_json(kb, catalog):
    db = kb.catalog()
    assert set(db.tables) == set(catalog.tables)
    t = "AR_PAYMENT_SCHEDULES_ALL"
    assert db.tables[t].columns == catalog.tables[t].columns
    assert db.joins == catalog.joins


def test_every_chunk_is_embedded(kb):
    s = kb.status()
    assert s["objects"] >= 2245 and s["embedded"] == s["chunks"] > 50000


def test_vector_search_finds_paraphrased_table(kb):
    hits = kb.search("bank lockbox setup used to import payments")
    names = [h.name for v in hits.values() for h in v[:10]]
    assert "AR_LOCKBOXES_ALL" in names


def test_hybrid_retriever_keeps_core_tables(kb, catalog):
    res = HybridRetriever(catalog, kb).search("receipts applied to invoices in an apply date range")
    assert {"AR_RECEIVABLE_APPLICATIONS_ALL", "AR_CASH_RECEIPTS_ALL", "RA_CUSTOMER_TRX_ALL"} <= set(res.tables)


def test_example_search_and_holdout(kb):
    assert kb.search_examples("AR aging by customer as of a date", k=1)[0][0] == "ar_aging_by_customer"
    names = [n for n, _ in kb.search_examples("AR aging by customer", k=3, exclude=["ar_aging_by_customer"])]
    assert "ar_aging_by_customer" not in names
