import json

import pytest

from bip_agent.examples import load_examples, pick_examples
from bip_agent.rules import check_request
from bip_agent.spec import ReportSpec
from bip_agent.validator import validate_sql

AGING = "AR aging by customer as of a date, with 1-30, 31-60, 61-90 and 90+ day buckets, optional business unit filter"
OPEN = ("Open invoices by customer: open invoice, debit memo and chargeback installments, "
        "optional customer and business unit filters")
RECEIPTS = "Receipts applied: cash receipt applications to invoices within an apply-date range, grouped by receipt"


def problems(catalog, request, d):
    s = ReportSpec.from_dict(d)
    r = validate_sql(s.sql, catalog, [p.name for p in s.parameters])
    return check_request(request, s, r)


def test_reference_specs_pass(catalog, example_specs):
    assert problems(catalog, AGING, example_specs["ar_aging_by_customer"]) == []
    assert problems(catalog, OPEN, example_specs["ar_open_invoices_by_customer"]) == []
    assert problems(catalog, RECEIPTS, example_specs["ar_receipts_applied"]) == []


def test_forward_looking_aging_is_caught(catalog, example_specs):
    d = json.loads(json.dumps(example_specs["ar_aging_by_customer"]))
    d["sql"] = d["sql"].replace("TRUNC(:P_AS_OF_DATE) - TRUNC(ps.DUE_DATE)",
                                "TRUNC(ps.DUE_DATE) - TRUNC(:P_AS_OF_DATE)")
    assert any("days past due" in p for p in problems(catalog, AGING, d))


def test_closed_items_and_extra_classes_are_caught(catalog, example_specs):
    d = json.loads(json.dumps(example_specs["ar_open_invoices_by_customer"]))
    d["sql"] = (d["sql"].replace("ps.STATUS = 'OP'", "ps.STATUS IN ('OP', 'CL')")
                .replace("('INV', 'DM', 'CB')", "('INV', 'DM', 'CB', 'PMT')"))
    out = problems(catalog, OPEN, d)
    assert any("STATUS = 'OP'" in p for p in out)
    assert any("PMT" in p for p in out)


def test_missing_date_range_and_unused_parameter_are_caught(catalog, example_specs):
    d = json.loads(json.dumps(example_specs["ar_receipts_applied"]))
    d["sql"] = d["sql"].replace("AND    TRUNC(ara.APPLY_DATE) BETWEEN TRUNC(:P_FROM_DATE) AND TRUNC(:P_TO_DATE)\n", "")
    out = problems(catalog, RECEIPTS, d)
    assert any("date range" in p for p in out)
    assert any("declared but not used" in p for p in out)


def test_incomplete_sql_and_backticks(catalog):
    assert any("incomplete" in e for e in validate_sql("SELECT \n", catalog).errors)
    bad = "SELECT ps.TRX_NUMBER AS `1_30` FROM AR_PAYMENT_SCHEDULES_ALL ps"
    assert any("backticks" in e for e in validate_sql(bad, catalog).errors)


def test_examples_pick_closest_and_holdout():
    ex = load_examples()
    assert [e.name for e in pick_examples("AR aging by customer as of a date", ex)] == ["ar_aging_by_customer"]
    held = pick_examples("AR aging by customer as of a date", ex, exclude=["ar_aging_by_customer"])
    assert held and held[0].name != "ar_aging_by_customer"
    assert "SQL:" in ex[0].render()


def test_case_without_end(catalog):
    sql = ("SELECT CASE WHEN ps.DUE_DATE IS NULL THEN 'X' ELSE 'Y' AS B "
           "FROM AR_PAYMENT_SCHEDULES_ALL ps")
    assert any("END" in e for e in validate_sql(sql, catalog).errors)


def test_master_data_request_needs_ids_status_and_dates(catalog):
    sql = ("SELECT hca.ACCOUNT_NUMBER AS ACCOUNT_NUMBER, hp.PARTY_NAME AS PARTY_NAME, rtt.NAME AS TERM "
           "FROM HZ_CUST_ACCOUNTS hca JOIN HZ_PARTIES hp ON hp.PARTY_ID = hca.PARTY_ID "
           "LEFT JOIN RA_TERMS_TL rtt ON rtt.TERM_ID = hca.CUST_ACCOUNT_ID")
    s = ReportSpec("X", "x", "", sql)
    out = check_request("all customer attributes for MDM", s, validate_sql(sql, catalog), catalog)
    acct = [p for p in out if "HZ_CUST_ACCOUNTS" in p]
    assert acct and "CUST_ACCOUNT_ID" in acct[0] and "STATUS" in acct[0]
    assert not [p for p in out if "RA_TERMS_TL" in p]  # name lookups are exempt
    assert not [p for p in check_request("open invoices by customer", s, validate_sql(sql, catalog), catalog)
                if p.startswith("master-data")]
