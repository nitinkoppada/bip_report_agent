import json

from bip_agent.cli import main


def test_render_writes_artifacts(tmp_path):
    from conftest import ROOT

    spec = ROOT / "examples" / "specs" / "ar_aging_by_customer.json"
    assert main(["render", str(spec), "-o", str(tmp_path)]) == 0
    names = {p.name for p in tmp_path.iterdir()}
    assert {"AR_AGING_BY_CUSTOMER.sql", "AR_AGING_BY_CUSTOMER.xdm", "AR_AGING_BY_CUSTOMER.rtf",
            "AR_AGING_BY_CUSTOMER_sample.xml", "spec.json", "validation.json"} <= names
    assert json.loads((tmp_path / "validation.json").read_text())["ok"] is True


def test_validate_command(tmp_path, capsys):
    f = tmp_path / "q.sql"
    f.write_text("SELECT ps.NOPE FROM AR_PAYMENT_SCHEDULES_ALL ps")
    assert main(["validate", str(f)]) == 1
    assert "NOPE" in capsys.readouterr().out
