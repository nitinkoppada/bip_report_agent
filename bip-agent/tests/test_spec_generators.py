import xml.etree.ElementTree as ET

from bip_agent.datamodel import build_datamodel, build_sample_xml
from bip_agent.rtf_layout import build_rtf
from bip_agent.spec import ReportSpec, select_aliases

NS = {"x": "http://xmlns.oracle.com/oxp/xmlp"}


def test_select_aliases():
    sql = """WITH a AS (SELECT 1 AS Z FROM DUAL)
             SELECT t.X AS FOO, NVL(t.Y, 0) BAR, t.BAZ, (SELECT 1 FROM DUAL) AS QUX FROM T t"""
    assert select_aliases(sql) == {"FOO", "BAR", "BAZ", "QUX"}


def test_spec_check_catches_mismatch():
    spec = ReportSpec.from_dict({
        "report_name": "x", "title": "X", "description": "", "sql": "SELECT t.A AS COL_A FROM T t",
        "parameters": [], "tables_used": [], "assumptions": [],
        "columns": [{"name": "COL_B", "label": "B", "data_type": "string", "is_break": False, "total": True}],
    })
    errs = spec.check()
    assert any("COL_B" in e and "SELECT aliases" in e for e in errs)
    assert any("not numeric" in e for e in errs)


def test_examples_spec_check(example_specs):
    for name, d in example_specs.items():
        assert ReportSpec.from_dict(d).check() == [], name


def test_datamodel_xml(example_specs):
    spec = ReportSpec.from_dict(example_specs["ar_aging_by_customer"])
    root = ET.fromstring(build_datamodel(spec).encode())
    assert root.tag == "{http://xmlns.oracle.com/oxp/xmlp}dataModel"
    sql = root.find("x:dataSets/x:dataSet/x:sql", NS).text
    assert "AR_PAYMENT_SCHEDULES_ALL" in sql
    header = root.find(".//x:group[@name='G_HEADER']", NS)
    lines = header.find("x:group[@name='G_LINES']", NS)
    assert [e.get("name") for e in header.findall("x:element", NS)] == ["CUSTOMER_NAME", "ACCOUNT_NUMBER"]
    assert len(lines.findall("x:element", NS)) == len(spec.detail_columns)
    params = root.findall("x:parameters/x:parameter", NS)
    assert [p.get("name") for p in params] == ["P_AS_OF_DATE", "P_ORG_ID", "P_CUSTOMER_NUMBER"]
    assert params[0].find("x:date", NS) is not None


def test_datamodel_without_breaks():
    spec = ReportSpec.from_dict({
        "report_name": "flat", "title": "Flat", "description": "d",
        "sql": "SELECT rct.TRX_NUMBER AS TRX_NUMBER FROM RA_CUSTOMER_TRX_ALL rct",
        "parameters": [], "tables_used": [], "assumptions": [],
        "columns": [{"name": "TRX_NUMBER", "label": "Trx", "data_type": "string", "is_break": False, "total": False}],
    })
    root = ET.fromstring(build_datamodel(spec).encode())
    assert root.find(".//x:group[@name='G_HEADER']", NS) is None
    assert root.find(".//x:group[@name='G_LINES']", NS) is not None
    sample = ET.fromstring(build_sample_xml(spec).encode())
    assert len(sample.findall("G_LINES")) == 6
    assert "<?for-each:G_LINES?>" in build_rtf(spec)


def test_sample_xml_shape(example_specs):
    spec = ReportSpec.from_dict(example_specs["ar_receipts_applied"])
    root = ET.fromstring(build_sample_xml(spec).encode())
    headers = root.findall("G_HEADER")
    assert len(headers) == 2
    assert headers[0].find("RECEIPT_NUMBER") is not None
    assert headers[0].find("G_LINES/AMOUNT_APPLIED") is not None


def test_rtf_tags_and_braces(example_specs):
    for d in example_specs.values():
        spec = ReportSpec.from_dict(d)
        rtf = build_rtf(spec)
        assert rtf.startswith("{\\rtf1")
        depth = 0
        prev = ""
        for ch in rtf:
            if prev != "\\":
                depth += ch == "{"
                depth -= ch == "}"
            prev = ch if prev != "\\" else ""
            assert depth >= 0
        assert depth == 0
        assert rtf.count("<?for-each:") == rtf.count("<?end for-each?>")
        for c in spec.columns:
            assert c.name in rtf
