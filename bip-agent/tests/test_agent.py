"""Claude backend + agent loop tests with a scripted fake Anthropic client (no network, no API key)."""
import json
from types import SimpleNamespace as NS

import pytest

from bip_agent.agent import AgentError, ReportAgent
from bip_agent.backends import CLAUDE_MODEL, ClaudeBackend


def tool_use(id_, name, inp):
    return NS(type="tool_use", id=id_, name=name, input=inp)


def text(t):
    return NS(type="text", text=t)


def resp(stop, *blocks):
    return NS(stop_reason=stop, content=list(blocks), usage=NS(input_tokens=100, output_tokens=50))


class FakeStream:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.message


class FakeClient:
    def __init__(self, script):
        self.script = list(script)
        self.calls = []
        self.beta = NS(messages=NS(stream=self._stream))

    def _stream(self, **kwargs):
        # snapshot the message list as it was when this call was made
        self.calls.append({**kwargs, "messages": list(kwargs["messages"])})
        return FakeStream(self.script.pop(0))


def spec_json(sql, cols):
    return json.dumps({
        "report_name": "AR_TEST", "title": "Test", "description": "d", "sql": sql,
        "parameters": [{"name": "P_ORG_ID", "label": "BU", "data_type": "number",
                        "default_value": "", "required": False}],
        "columns": [{"name": c, "label": c, "data_type": "string", "is_break": False, "total": False}
                    for c in cols],
        "tables_used": ["RA_CUSTOMER_TRX_ALL"], "assumptions": [],
    })


GOOD_SQL = ("SELECT rct.TRX_NUMBER AS TRX_NUMBER FROM RA_CUSTOMER_TRX_ALL rct "
            "WHERE (:P_ORG_ID IS NULL OR rct.ORG_ID = :P_ORG_ID)")
BAD_SQL = GOOD_SQL.replace("rct.TRX_NUMBER", "rct.TRX_NUM")


def test_tool_loop_and_repair(catalog):
    client = FakeClient([
        resp("tool_use",
             tool_use("t1", "describe_table", {"name": "RA_CUSTOMER_TRX_ALL"}),
             tool_use("t2", "find_join_path", {"from_table": "RA_CUSTOMER_TRX_ALL", "to_table": "HZ_PARTIES"}),
             tool_use("t3", "validate_sql", {"sql": BAD_SQL, "parameters": ["P_ORG_ID"]}),
             tool_use("t4", "describe_table", {})),  # malformed input -> is_error result
        resp("end_turn", text(spec_json(BAD_SQL, ["TRX_NUMBER"]))),
        resp("end_turn", text(spec_json(GOOD_SQL, ["TRX_NUMBER"]))),
    ])
    agent = ReportAgent(catalog, backend=ClaudeBackend(client=client))
    result = agent.generate("list invoice numbers")
    assert result.ok and result.steps == 3
    assert result.spec.report_name == "AR_TEST"
    assert result.usage == {"input_tokens": 300, "output_tokens": 150}

    first = client.calls[0]
    assert first["model"] == CLAUDE_MODEL
    assert first["tools"][0]["strict"] is True and "input_schema" in first["tools"][0]
    assert first["output_config"]["format"]["type"] == "json_schema"
    assert first["thinking"] == {"type": "adaptive"}
    assert first["fallbacks"] == "default"
    assert "RA_CUSTOMER_TRX_ALL" in first["messages"][0]["content"]

    tool_results = client.calls[1]["messages"][2]["content"]
    assert [r["tool_use_id"] for r in tool_results] == ["t1", "t2", "t3", "t4"]
    assert "TRX_NUMBER" in tool_results[0]["content"]
    assert "HZ_PARTIES" in tool_results[1]["content"]
    assert "TRX_NUM does not exist" in tool_results[2]["content"]
    assert tool_results[3].get("is_error") is True

    repair_msg = client.calls[2]["messages"][-1]["content"]
    assert "TRX_NUM" in repair_msg


def test_gives_up_after_max_repairs(catalog):
    bad = resp("end_turn", text(spec_json(BAD_SQL, ["TRX_NUMBER"])))
    agent = ReportAgent(catalog, backend=ClaudeBackend(client=FakeClient([bad, bad])), max_repairs=1)
    result = agent.generate("list invoice numbers")
    assert not result.ok
    assert result.validation.errors


def test_refusal_raises(catalog):
    agent = ReportAgent(catalog, backend=ClaudeBackend(client=FakeClient([resp("refusal")])))
    with pytest.raises(AgentError):
        agent.generate("anything")


def test_no_fallbacks_option(catalog):
    client = FakeClient([resp("end_turn", text(spec_json(GOOD_SQL, ["TRX_NUMBER"])))])
    ReportAgent(catalog, backend=ClaudeBackend(client=client, use_fallbacks=False)).generate("x")
    assert "fallbacks" not in client.calls[0] and "betas" not in client.calls[0]
