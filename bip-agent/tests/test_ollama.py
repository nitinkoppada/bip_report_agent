"""Ollama backend tests against a stub Ollama HTTP server (no model, no network)."""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from bip_agent.agent import AgentError, ReportAgent
from bip_agent.backends import OllamaBackend, extract_json

GOOD_SQL = ("SELECT rct.TRX_NUMBER AS TRX_NUMBER FROM RA_CUSTOMER_TRX_ALL rct "
            "WHERE (:P_ORG_ID IS NULL OR rct.ORG_ID = :P_ORG_ID)")
BAD_SQL = GOOD_SQL.replace("rct.TRX_NUMBER", "rct.TRX_NUM")


def spec(sql):
    return {
        "report_name": "AR_TEST", "title": "Test", "description": "d", "sql": sql,
        "parameters": [{"name": "P_ORG_ID", "label": "BU", "data_type": "number",
                        "default_value": "", "required": False}],
        "columns": [{"name": "TRX_NUMBER", "label": "Trx", "data_type": "string",
                     "is_break": False, "total": False}],
        "tables_used": ["RA_CUSTOMER_TRX_ALL"], "assumptions": [],
    }


def chat(content="", tool_calls=None, done_reason="stop", prompt_tokens=1000):
    msg = {"role": "assistant", "content": content}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return {"message": msg, "done_reason": done_reason, "prompt_eval_count": prompt_tokens, "eval_count": 200}


class StubOllama:
    """Serves /api/show, /api/tags and a scripted sequence of /api/chat replies."""

    def __init__(self, chats, capabilities=("completion", "tools"), models=("qwen2.5-coder:14b",)):
        self.chats = list(chats)
        self.capabilities = capabilities
        self.models = models
        self.requests = []
        stub = self

        class H(BaseHTTPRequestHandler):
            def _send(self, code, obj):
                body = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                stub.requests.append((self.path, None))
                self._send(200, {"models": [{"name": m} for m in stub.models]})

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                stub.requests.append((self.path, body))
                if self.path == "/api/show":
                    out = {} if stub.capabilities is None else {"capabilities": list(stub.capabilities)}
                    return self._send(200, out)
                item = stub.chats.pop(0)
                if isinstance(item, tuple):  # (status, body) error reply
                    return self._send(*item)
                self._send(200, item)

            def log_message(self, *a):
                pass

        self.server = HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def chat_payloads(self):
        return [b for p, b in self.requests if p == "/api/chat"]

    def close(self):
        self.server.shutdown()


@pytest.fixture
def stub_factory():
    stubs = []

    def make(*a, **kw):
        s = StubOllama(*a, **kw)
        stubs.append(s)
        return s

    yield make
    for s in stubs:
        s.close()


def test_tools_mode_with_repair(catalog, stub_factory):
    stub = stub_factory([
        chat(tool_calls=[{"function": {"name": "describe_table", "arguments": {"name": "RA_CUSTOMER_TRX_ALL"}}},
                         {"function": {"name": "validate_sql",
                                       "arguments": json.dumps({"sql": BAD_SQL, "parameters": ["P_ORG_ID"]})}}]),
        chat("Here is the spec:\n```json\n" + json.dumps(spec(BAD_SQL)) + "\n```"),
        chat(json.dumps(spec(GOOD_SQL))),
    ])
    agent = ReportAgent(catalog, backend=OllamaBackend(host=stub.url))
    result = agent.generate("list invoice numbers")
    assert result.ok and result.steps == 3
    assert result.usage == {"input_tokens": 3000, "output_tokens": 600}

    first, second, third = stub.chat_payloads()
    assert first["model"] == "qwen2.5-coder:14b"
    assert first["options"]["num_ctx"] == 24576 and first["stream"] is False
    assert [t["function"]["name"] for t in first["tools"]] == [
        "search_catalog", "describe_table", "find_join_path", "validate_sql"]
    assert "format" not in first
    tool_msgs = [m for m in second["messages"] if m["role"] == "tool"]
    assert [m["tool_name"] for m in tool_msgs] == ["describe_table", "validate_sql"]
    assert "TRX_NUMBER" in tool_msgs[0]["content"]
    assert "TRX_NUM does not exist" in tool_msgs[1]["content"]
    assert "failed validation" in third["messages"][-1]["content"]


def test_tool_call_written_as_text(catalog, stub_factory):
    stub = stub_factory([
        chat('{"name": "find_join_path", "arguments": {"from_table": "AR_CASH_RECEIPTS_ALL", "to_table": "HZ_PARTIES"}}'),
        chat(json.dumps(spec(GOOD_SQL))),
    ])
    result = ReportAgent(catalog, backend=OllamaBackend(host=stub.url)).generate("x")
    assert result.ok
    tool_msg = [m for m in stub.chat_payloads()[1]["messages"] if m["role"] == "tool"][0]
    assert "HZ_PARTIES" in tool_msg["content"]


def test_json_mode_when_model_has_no_tools(catalog, stub_factory):
    stub = stub_factory([chat(json.dumps(spec(BAD_SQL))), chat(json.dumps(spec(GOOD_SQL)))],
                        capabilities=("completion",))
    backend = OllamaBackend(host=stub.url)
    result = ReportAgent(catalog, backend=backend).generate("list invoice numbers")
    assert result.ok and backend.mode == "json"
    first, second = stub.chat_payloads()
    assert "tools" not in first and first["format"]["required"][0] == "report_name"
    assert "No tools are available" in first["messages"][0]["content"]
    repair = second["messages"][-1]["content"]
    assert "TRX_NUM" in repair and "### RA_CUSTOMER_TRX_ALL" in repair  # catalog entry attached


def test_falls_back_to_json_when_server_rejects_tools(catalog, stub_factory):
    stub = stub_factory([(400, {"error": "registry.ollama.ai/library/x does not support tools"}),
                         chat(json.dumps(spec(GOOD_SQL)))], capabilities=None)
    backend = OllamaBackend(host=stub.url)
    assert ReportAgent(catalog, backend=backend).generate("x").ok
    assert backend.mode == "json"
    assert "format" in stub.chat_payloads()[1]


def test_non_spec_answer_gets_schema_constrained_retry(catalog, stub_factory):
    stub = stub_factory([chat("I would join the payment schedules to customers."),
                         chat(json.dumps(spec(GOOD_SQL)))])
    assert ReportAgent(catalog, backend=OllamaBackend(host=stub.url)).generate("x").ok
    retry = stub.chat_payloads()[1]
    assert "format" in retry and "tools" not in retry


def test_context_overflow_is_reported(catalog, stub_factory):
    stub = stub_factory([chat("{", done_reason="length")])
    with pytest.raises(AgentError, match="num-ctx"):
        ReportAgent(catalog, backend=OllamaBackend(host=stub.url)).generate("x")


def test_unreachable_server(catalog):
    backend = OllamaBackend(host="http://127.0.0.1:9", mode="tools", timeout=2)
    with pytest.raises(AgentError, match="ollama serve"):
        ReportAgent(catalog, backend=backend).generate("x")


def test_check_reports_missing_model(stub_factory):
    stub = stub_factory([], models=("llama3:8b",))
    lines = OllamaBackend(host=stub.url).check()
    assert any("ollama pull qwen2.5-coder:14b" in line for line in lines)
    ok = OllamaBackend(host=stub.url, model="llama3:8b").check()
    assert not any(line.startswith("MISSING") for line in ok)


def test_local_context_fits_7b_window(catalog):
    local = ReportAgent(catalog, backend=OllamaBackend(mode="json"))
    for request in ["AR aging by customer as of a date with 30/60/90 buckets",
                    "receipts applied to invoices in a date range",
                    "adjustments approved last month"]:
        ctx, tables = local.build_context(request)
        assert len(ctx) / 4 < 6500, request  # ~tokens; leaves room in a 16k window
        assert len(tables) <= 8
    ctx, tables = local.build_context("receipts applied to invoices in a date range")
    assert "AR_RECEIVABLE_APPLICATIONS_ALL" in tables
    receipts = ctx[ctx.index("### AR_CASH_RECEIPTS_ALL"):]
    receipts = receipts[:receipts.index("\n### ")]
    for col in ("RECEIPT_NUMBER", "AMOUNT", "CURRENCY_CODE", "PAY_FROM_CUSTOMER", "ORG_ID"):
        assert f"  {col} " in receipts, col
    assert "more columns (describe_table AR_CASH_RECEIPTS_ALL lists all)" in receipts


def test_tool_loop_is_capped_for_local_models(catalog, stub_factory):
    lookup = chat(tool_calls=[{"function": {"name": "search_catalog", "arguments": {"query": "receipt"}}}])
    stub = stub_factory([lookup, lookup, chat(json.dumps(spec(GOOD_SQL)))])
    agent = ReportAgent(catalog, backend=OllamaBackend(host=stub.url), max_tool_rounds=2)
    assert agent.generate("x").ok
    last = stub.chat_payloads()[2]
    assert "format" in last and "tools" not in last
    assert "Stop using tools" in last["messages"][-1]["content"]


def test_tool_loop_stops_when_context_fills(catalog, stub_factory):
    big = chat(tool_calls=[{"function": {"name": "search_catalog", "arguments": {"query": "receipt"}}}],
               prompt_tokens=19000)
    stub = stub_factory([big, chat(json.dumps(spec(GOOD_SQL)))])
    assert ReportAgent(catalog, backend=OllamaBackend(host=stub.url)).generate("x").ok
    assert "format" in stub.chat_payloads()[1]


def test_extract_json():
    assert extract_json('noise ```json\n{"a": 1}\n``` more') == {"a": 1}
    assert extract_json('Answer: {"sql": "x", "n": {"b": 2}} done') == {"sql": "x", "n": {"b": 2}}
    assert extract_json("no json here") is None


def test_extract_json_joins_plus_concatenated_strings():
    text = '```json\n{"sql": "SELECT a\\n" +\n  "FROM b", "n": 1}\n```'
    assert extract_json(text) == {"sql": "SELECT a\nFROM b", "n": 1}


def test_tool_call_written_as_text_with_function_key(catalog, stub_factory):
    text_call = json.dumps({"function": "validate_sql",
                            "arguments": {"sql": GOOD_SQL, "parameters": ["P_ORG_ID"]}})
    stub = stub_factory([chat(text_call), chat(json.dumps(spec(GOOD_SQL)))])
    assert ReportAgent(catalog, backend=OllamaBackend(host=stub.url)).generate("x").ok
    assert stub.chat_payloads()[1]["messages"][-1]["role"] == "tool"


def test_partial_free_form_spec_gets_constrained_retry(catalog, stub_factory):
    partial = json.dumps({"sql": GOOD_SQL, "parameters": ["P_ORG_ID"]})
    stub = stub_factory([chat(partial), chat(json.dumps(spec(GOOD_SQL)))])
    assert ReportAgent(catalog, backend=OllamaBackend(host=stub.url)).generate("x").ok
    assert "format" in stub.chat_payloads()[1]


def test_cut_short_sql_is_replaced_by_earlier_complete_sql(catalog, stub_factory):
    call = chat(tool_calls=[{"function": {"name": "validate_sql",
                                          "arguments": {"sql": GOOD_SQL, "parameters": ["P_ORG_ID"]}}}])
    stub = stub_factory([call, chat("Done."), chat(json.dumps(spec("SELECT \n")))])
    result = ReportAgent(catalog, backend=OllamaBackend(host=stub.url)).generate("x")
    assert result.ok and result.spec.sql == GOOD_SQL


def test_cut_short_sql_without_earlier_sql_asks_for_sql_alone(catalog, stub_factory):
    stub = stub_factory([chat(json.dumps(spec("SELECT \n"))), chat(f"```sql\n{GOOD_SQL}\n```")])
    result = ReportAgent(catalog, backend=OllamaBackend(host=stub.url, mode="json")).generate("x")
    assert result.ok and result.spec.sql == GOOD_SQL
    plain = stub.chat_payloads()[1]
    assert "format" not in plain and "tools" not in plain


def test_runaway_output_gets_constrained_retry(catalog, stub_factory):
    runaway = chat("SELECT SELECT SELECT", done_reason="length")
    runaway["eval_count"] = 4096
    stub = stub_factory([runaway, chat(json.dumps(spec(GOOD_SQL)))])
    assert ReportAgent(catalog, backend=OllamaBackend(host=stub.url)).generate("x").ok
    retry = stub.chat_payloads()[1]
    assert "format" in retry
    assert all("SELECT SELECT" not in m["content"] for m in retry["messages"])
