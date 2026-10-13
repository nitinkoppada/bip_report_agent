from bip_agent.retrieval import Retriever


def test_catalog_loads(catalog):
    assert len(catalog.tables) >= 450
    ps = catalog.get("AR_PAYMENT_SCHEDULES_ALL")
    assert ps.primary_key == ("PAYMENT_SCHEDULE_ID",)
    assert ps.has_column("amount_due_remaining")
    assert not ps.has_column("NOT_A_COLUMN")


def test_known_join_both_directions(catalog):
    assert catalog.is_known_join("AR_PAYMENT_SCHEDULES_ALL", "CUSTOMER_ID", "HZ_CUST_ACCOUNTS", "CUST_ACCOUNT_ID")
    assert catalog.is_known_join("HZ_CUST_ACCOUNTS", "CUST_ACCOUNT_ID", "AR_PAYMENT_SCHEDULES_ALL", "CUSTOMER_ID")
    assert not catalog.is_known_join("AR_PAYMENT_SCHEDULES_ALL", "TERM_ID", "HZ_CUST_ACCOUNTS", "CUST_ACCOUNT_ID")


def test_trx_types_join_uses_seq_id(catalog):
    assert catalog.is_known_join("RA_CUSTOMER_TRX_ALL", "CUST_TRX_TYPE_SEQ_ID",
                                 "RA_CUST_TRX_TYPES_ALL", "CUST_TRX_TYPE_SEQ_ID")


def test_join_path(catalog):
    path = catalog.join_path("AR_RECEIVABLE_APPLICATIONS_ALL", "HZ_PARTIES")
    assert path is not None and 1 <= len(path) <= 3
    assert path[-1].parent == "HZ_PARTIES" or path[-1].child == "HZ_PARTIES"


def test_describe_table_skips_who_columns(catalog):
    text = catalog.describe_table("AR_CASH_RECEIPTS_ALL")
    assert "RECEIPT_NUMBER" in text and "LAST_UPDATE_LOGIN" not in text


def test_retrieval_aging(catalog):
    r = Retriever(catalog).search("AR aging by customer with 30/60/90 day buckets")
    assert "AR_PAYMENT_SCHEDULES_ALL" in r.tables[:5]
    assert {"HZ_CUST_ACCOUNTS", "HZ_PARTIES"} <= set(r.tables)


def test_retrieval_receipts_applied(catalog):
    r = Retriever(catalog).search("receipts applied to invoices last month")
    assert {"AR_RECEIVABLE_APPLICATIONS_ALL", "AR_CASH_RECEIPTS_ALL", "RA_CUSTOMER_TRX_ALL"} <= set(r.tables)
    assert any(e.child == "AR_RECEIVABLE_APPLICATIONS_ALL" for e in r.edges)


def test_retrieval_prefers_base_tables(catalog):
    r = Retriever(catalog).search("open invoices by customer")
    assert r.tables[0] in {"AR_PAYMENT_SCHEDULES_ALL", "RA_CUSTOMER_TRX_ALL"}
    assert not any(t.endswith("_GT") for t in r.tables[:5])


def test_explicit_table_name_is_retrieved(catalog):
    r = Retriever(catalog).search("list rows of AR_DISPUTE_HISTORY")
    assert r.tables[0] == "AR_DISPUTE_HISTORY"


def test_catalog_is_tables_only_and_covers_other_modules(catalog):
    assert not [n for n, t in catalog.tables.items() if t.is_view]
    assert not [n for n in catalog.tables if n.endswith("_GT") or "INTERFACE" in n or n.startswith("HZ_IMP_")]
    for name in ("GL_CODE_COMBINATIONS", "AP_INVOICES_ALL", "XLA_AE_LINES", "ZX_LINES", "HZ_CONTACT_POINTS"):
        assert name in catalog, name
    assert catalog.in_scope("GL_NOT_A_TABLE") and not catalog.in_scope("PAY_PAYROLL_ACTIONS")
