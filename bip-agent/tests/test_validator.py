from bip_agent.validator import validate_sql


def test_good_query(catalog):
    sql = """SELECT hp.PARTY_NAME AS CUSTOMER_NAME, ps.AMOUNT_DUE_REMAINING AS BAL
             FROM AR_PAYMENT_SCHEDULES_ALL ps
             JOIN HZ_CUST_ACCOUNTS hca ON hca.CUST_ACCOUNT_ID = ps.CUSTOMER_ID
             JOIN HZ_PARTIES hp ON hp.PARTY_ID = hca.PARTY_ID
             WHERE ps.STATUS = 'OP' AND (:P_ORG_ID IS NULL OR ps.ORG_ID = :P_ORG_ID)"""
    rep = validate_sql(sql, catalog, ["P_ORG_ID"])
    assert rep.ok, rep.summary()
    assert rep.warnings == []
    assert rep.binds == ["P_ORG_ID"]
    assert rep.tables == ["AR_PAYMENT_SCHEDULES_ALL", "HZ_CUST_ACCOUNTS", "HZ_PARTIES"]


def test_unknown_column_with_suggestion(catalog):
    rep = validate_sql("SELECT ps.AMOUNT_REMAINING FROM AR_PAYMENT_SCHEDULES_ALL ps", catalog)
    assert not rep.ok
    assert "AMOUNT_REMAINING" in rep.errors[0]


def test_ebs_style_trx_type_join_is_rejected(catalog):
    sql = """SELECT rct.TRX_NUMBER, ctt.NAME FROM RA_CUSTOMER_TRX_ALL rct, RA_CUST_TRX_TYPES_ALL ctt
             WHERE rct.CUST_TRX_TYPE_ID = ctt.CUST_TRX_TYPE_ID"""
    rep = validate_sql(sql, catalog)
    assert not rep.ok
    assert any("CUST_TRX_TYPE_SEQ_ID" in e for e in rep.errors)


def test_unknown_in_scope_table(catalog):
    rep = validate_sql("SELECT x.A FROM AR_NOT_A_TABLE x", catalog)
    assert any("not in the catalog" in e for e in rep.errors)


def test_out_of_scope_table_is_warning(catalog):
    sql = """SELECT hou.ACTION_TYPE, rct.TRX_NUMBER FROM RA_CUSTOMER_TRX_ALL rct
             JOIN PAY_PAYROLL_ACTIONS hou ON hou.PAYROLL_ACTION_ID = rct.ORG_ID"""
    rep = validate_sql(sql, catalog)
    assert rep.ok, rep.summary()
    assert any("PAY_PAYROLL_ACTIONS" in w for w in rep.warnings)


def test_other_financials_modules_are_verified(catalog):
    sql = """SELECT gcc.SEGMENT1, rct.TRX_NUMBER FROM RA_CUSTOMER_TRX_ALL rct
             JOIN RA_CUST_TRX_LINE_GL_DIST_ALL d ON d.CUSTOMER_TRX_ID = rct.CUSTOMER_TRX_ID
             JOIN GL_CODE_COMBINATIONS gcc ON gcc.CODE_COMBINATION_ID = d.CODE_COMBINATION_ID"""
    assert validate_sql(sql, catalog).ok
    bad = validate_sql("SELECT gcc.NOT_A_COLUMN FROM GL_CODE_COMBINATIONS gcc", catalog)
    assert any("NOT_A_COLUMN" in e for e in bad.errors)


def test_dml_rejected(catalog):
    rep = validate_sql("DELETE FROM AR_ADJUSTMENTS_ALL", catalog)
    assert not rep.ok


def test_multiple_statements_rejected(catalog):
    rep = validate_sql("SELECT 1 FROM DUAL; SELECT 2 FROM DUAL", catalog)
    assert any("multiple statements" in e for e in rep.errors)


def test_unknown_alias(catalog):
    rep = validate_sql("SELECT zz.TRX_NUMBER FROM RA_CUSTOMER_TRX_ALL rct", catalog)
    assert any("unknown table alias ZZ" in e for e in rep.errors)


def test_cartesian_warning(catalog):
    rep = validate_sql("SELECT a.ADJUSTMENT_ID, h.PARTY_NAME FROM AR_ADJUSTMENTS_ALL a, HZ_PARTIES h", catalog)
    assert any("cartesian" in w for w in rep.warnings)


def test_undocumented_join_warning(catalog):
    sql = """SELECT ps.TRX_NUMBER FROM AR_PAYMENT_SCHEDULES_ALL ps
             JOIN HZ_CUST_ACCOUNTS hca ON hca.CUST_ACCOUNT_ID = ps.TERM_ID"""
    rep = validate_sql(sql, catalog)
    assert rep.ok
    assert any("not a documented foreign key" in w for w in rep.warnings)


def test_cte_subquery_literals_and_outer_join(catalog):
    sql = """WITH bal AS (SELECT ps.CUSTOMER_ID, SUM(ps.AMOUNT_DUE_REMAINING) AS BAL
                          FROM AR_PAYMENT_SCHEDULES_ALL ps WHERE ps.STATUS = 'OP' GROUP BY ps.CUSTOMER_ID)
             SELECT hca.ACCOUNT_NUMBER, b.BAL, TO_CHAR(SYSDATE, 'HH24:MI') AS RUN_TIME,
                    EXTRACT(YEAR FROM SYSDATE) AS YR,
                    (SELECT MAX(cr.RECEIPT_DATE) FROM AR_CASH_RECEIPTS_ALL cr
                      WHERE cr.PAY_FROM_CUSTOMER = hca.CUST_ACCOUNT_ID) AS LAST_RECEIPT
             FROM bal b, HZ_CUST_ACCOUNTS hca, HZ_PARTIES hp
             WHERE hca.CUST_ACCOUNT_ID = b.CUSTOMER_ID
             AND   hp.PARTY_ID(+) = hca.PARTY_ID"""
    rep = validate_sql(sql, catalog, [])
    assert rep.ok, rep.summary()
    assert rep.binds == []  # ':MI' inside a string literal is not a bind
    assert not any("cartesian" in w for w in rep.warnings)


def test_bind_without_parameter(catalog):
    rep = validate_sql("SELECT rct.TRX_NUMBER FROM RA_CUSTOMER_TRX_ALL rct WHERE rct.ORG_ID = :P_ORG_ID",
                       catalog, [])
    assert any(":P_ORG_ID" in e for e in rep.errors)


def test_view_columns_checked(catalog):
    rep = validate_sql("SELECT v.RCT_RECEIPT_NUMBER_X FROM AR_CASH_RECEIPTS_H_V v", catalog)
    assert not rep.ok


def test_flexfield_columns_allowed(catalog):
    rep = validate_sql("SELECT rct.ATTRIBUTE1 FROM RA_CUSTOMER_TRX_ALL rct", catalog)
    assert rep.ok, rep.summary()


def test_examples_validate(catalog, example_specs):
    for name, d in example_specs.items():
        rep = validate_sql(d["sql"], catalog, [p["name"] for p in d["parameters"]])
        assert rep.ok, f"{name}: {rep.summary()}"
