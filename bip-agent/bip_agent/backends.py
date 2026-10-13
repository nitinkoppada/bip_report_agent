"""Model backends behind one small interface.

The agent loop (agent.py) talks to a backend through four calls:

    conv = backend.start(system, user_text)      # new conversation
    turn = backend.step(conv, tools, schema)      # one model call -> Turn
    backend.add_tool_results(conv, results)       # answer the turn's tool calls
    backend.add_user(conv, text)                  # e.g. validation errors to repair

Backends:
* OllamaBackend (default): a local model served by Ollama on this machine.
  Uses native tool calling when the model supports it, and otherwise a
  JSON-only mode where the model answers straight from the retrieved catalog
  context with output constrained to the report-spec schema.
* ClaudeBackend: the Anthropic API (needs an API key).
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

DEFAULT_OLLAMA_MODEL = os.environ.get("BIP_AGENT_LOCAL_MODEL", "qwen2.5-coder:14b")
DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
CLAUDE_MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class BackendError(RuntimeError):
    pass


@dataclass
class ToolCall:
    id: str
    name: str
    args: Any  # dict when well formed; anything else is reported back as an error


@dataclass
class Turn:
    text: str
    tool_calls: list[ToolCall]
    stop: str  # "tool_use" | "end" | "refusal" | "max_tokens"
    usage: dict[str, int] = field(default_factory=dict)


@dataclass
class ToolResult:
    call: ToolCall
    content: str
    is_error: bool = False


def extract_json(text: str) -> dict | None:
    """First JSON object in text, tolerating ```json fences and chatter around it."""
    obj = _extract_json(text)
    if obj is None and "+" in text:
        # Small models sometimes split long strings JavaScript-style: "SELECT ...\n" + "FROM ...".
        obj = _extract_json(re.sub(r'(?<!\\)"\s*\+\s*"', "", text))
    return obj


def _extract_json(text: str) -> dict | None:
    text = text.strip()
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        pass
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    candidates = [fence.group(1)] if fence else []
    start = text.find("{")
    while start != -1:
        candidates.append(text[start:])
        start = text.find("{", start + 1)
        if len(candidates) > 20:
            break
    decoder = json.JSONDecoder()
    for c in candidates:
        try:
            obj, _ = decoder.raw_decode(c)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return None


# ---------------------------------------------------------------------------
# Ollama (local)
# ---------------------------------------------------------------------------
class OllamaBackend:
    """Local model through Ollama's /api/chat.

    mode: "auto" (tools if the model supports them, else json), "tools" or "json".
    num_ctx must hold the retrieved catalog context plus tool results; Ollama's
    own default (2-4k tokens) is far too small and silently truncates the prompt.
    """

    name = "ollama"

    def __init__(self, model: str = DEFAULT_OLLAMA_MODEL, host: str = DEFAULT_OLLAMA_URL,
                 mode: str = "auto", num_ctx: int = 24576, temperature: float = 0.1,
                 timeout: float = 900.0, transport=None, num_predict: int = 4096):
        self.model = model
        self.host = host.rstrip("/")
        if not self.host.startswith("http"):
            self.host = "http://" + self.host
        self.requested_mode = mode
        self._mode: str | None = None if mode == "auto" else mode
        self.num_ctx = num_ctx
        self.temperature = temperature
        # A spec is 1-3k tokens; the cap stops a model that starts repeating itself.
        self.num_predict = num_predict
        self.timeout = timeout
        self._transport = transport or self._http
        self._ids = 0

    # -- http ---------------------------------------------------------------
    def _http(self, path: str, payload: dict | None) -> dict:
        """POST payload as JSON (GET when payload is None) and return the decoded reply."""
        data = None if payload is None else json.dumps(payload).encode()
        req = urllib.request.Request(self.host + path, data=data,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            raise BackendError(f"Ollama {path} returned {exc.code}: {body[:300]}") from exc
        except urllib.error.URLError as exc:
            raise BackendError(
                f"cannot reach Ollama at {self.host} ({exc.reason}). Is `ollama serve` running?") from exc

    # -- capabilities -------------------------------------------------------
    @property
    def mode(self) -> str:
        if self._mode is None:
            info = self._transport("/api/show", {"model": self.model})
            caps = info.get("capabilities")
            # Older Ollama versions do not report capabilities: try tools and
            # fall back to json if the server rejects them (see step()).
            self._mode = "tools" if caps is None or "tools" in caps else "json"
        return self._mode

    @property
    def uses_tools(self) -> bool:
        return self.mode == "tools"

    def check(self) -> list[str]:
        """Human-readable readiness checks; raises BackendError if Ollama is unreachable."""
        tags = self._transport("/api/tags", None)
        names = [m.get("name", "") for m in tags.get("models", [])]
        lines = [f"Ollama reachable at {self.host}; {len(names)} model(s) installed"]
        base = self.model if ":" in self.model else self.model + ":latest"
        if base not in names and self.model not in names:
            lines.append(f"MISSING: model {self.model} is not pulled. Run: ollama pull {self.model}")
            return lines
        lines.append(f"model {self.model} is installed; {self.mode} mode")
        return lines

    def describe(self) -> str:
        return f"ollama:{self.model} ({self.mode} mode, num_ctx={self.num_ctx})"

    # -- conversation -------------------------------------------------------
    def start(self, system: str, user_text: str) -> list:
        return [{"role": "system", "content": system}, {"role": "user", "content": user_text}]

    def add_user(self, conv: list, text: str) -> None:
        conv.append({"role": "user", "content": text})

    def add_tool_results(self, conv: list, results: list[ToolResult]) -> None:
        for r in results:
            content = ("error: " + r.content) if r.is_error else r.content
            conv.append({"role": "tool", "tool_name": r.call.name, "content": content})

    def _next_id(self) -> str:
        self._ids += 1
        return f"call_{self._ids}"

    def step(self, conv: list, tools: list[dict], schema: dict, final: bool = False,
             plain: bool = False) -> Turn:
        """One /api/chat call. final=True drops tools and constrains output to schema;
        plain=True drops both (free text, e.g. to ask for the SQL alone)."""
        payload: dict = {
            "model": self.model,
            "messages": conv,
            "stream": False,
            "options": {"num_ctx": self.num_ctx, "temperature": self.temperature,
                        "num_predict": self.num_predict},
        }
        use_tools = self.uses_tools and not final and not plain
        if plain:
            pass
        elif use_tools:
            payload["tools"] = [{"type": "function", "function": {
                "name": t["name"], "description": t["description"], "parameters": t["parameters"]}}
                for t in tools]
        else:
            payload["format"] = schema
        try:
            resp = self._transport("/api/chat", payload)
        except BackendError as exc:
            if use_tools and "does not support tools" in str(exc):
                self._mode = "json"
                return self.step(conv, tools, schema, final, plain)
            raise
        msg = resp.get("message") or {}
        content = msg.get("content") or ""
        usage = {"input_tokens": resp.get("prompt_eval_count", 0) or 0,
                 "output_tokens": resp.get("eval_count", 0) or 0}
        calls = []
        for tc in msg.get("tool_calls") or []:
            fn = tc.get("function") or {}
            args = fn.get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    pass
            calls.append(ToolCall(tc.get("id") or self._next_id(), fn.get("name", ""), args))
        tool_names = {t["name"] for t in tools}
        if use_tools and not calls:
            # Smaller models often write the call as JSON text instead of a tool call.
            obj = extract_json(content) or {}
            # Seen shapes: {"name": ..., "arguments": {...}}, {"function": ..., "arguments": {...}},
            # and "parameters" in place of "arguments".
            fn = obj.get("name") if isinstance(obj.get("name"), str) else obj.get("function")
            args = obj.get("arguments", obj.get("parameters"))
            if fn in tool_names and isinstance(args, dict):
                calls.append(ToolCall(self._next_id(), fn, args))
                content = ""
        if resp.get("done_reason") == "length" and usage["output_tokens"] >= self.num_predict:
            # Runaway output (the model kept repeating itself). Leave it out of the conversation.
            return Turn(content, [], "max_output", usage)
        assistant = {"role": "assistant", "content": content}
        if msg.get("tool_calls"):
            assistant["tool_calls"] = msg["tool_calls"]
        elif calls:
            assistant["tool_calls"] = [{"function": {"name": c.name, "arguments": c.args}} for c in calls]
        conv.append(assistant)
        if resp.get("done_reason") == "length":
            stop = "max_tokens"
        else:
            stop = "tool_use" if calls else "end"
        return Turn(content, calls, stop, usage)


# ---------------------------------------------------------------------------
# Claude (Anthropic API)
# ---------------------------------------------------------------------------
class ClaudeBackend:
    name = "claude"
    uses_tools = True

    def __init__(self, model: str = CLAUDE_MODEL, effort: str = "high", use_fallbacks: bool = True,
                 client: Any = None):
        self.model = model
        self.effort = effort
        self.use_fallbacks = use_fallbacks
        self._client = client
        self._system = ""

    @property
    def client(self):
        if self._client is None:
            import anthropic  # imported lazily so the local backend needs no SDK

            self._client = anthropic.Anthropic()
        return self._client

    def describe(self) -> str:
        return f"claude:{self.model} (effort {self.effort})"

    def start(self, system: str, user_text: str) -> list:
        self._system = system
        return [{"role": "user", "content": user_text}]

    def add_user(self, conv: list, text: str) -> None:
        conv.append({"role": "user", "content": text})

    def add_tool_results(self, conv: list, results: list[ToolResult]) -> None:
        blocks = []
        for r in results:
            b = {"type": "tool_result", "tool_use_id": r.call.id, "content": r.content}
            if r.is_error:
                b["is_error"] = True
            blocks.append(b)
        conv.append({"role": "user", "content": blocks})

    def step(self, conv: list, tools: list[dict], schema: dict, final: bool = False) -> Turn:
        kwargs = dict(
            model=self.model,
            max_tokens=64000,
            system=self._system,
            messages=conv,
            thinking={"type": "adaptive"},
            # Automatic prompt caching: each loop step resends the same catalog context.
            cache_control={"type": "ephemeral"},
            output_config={"effort": self.effort, "format": {"type": "json_schema", "schema": schema}},
        )
        if not final:
            kwargs["tools"] = [{"name": t["name"], "description": t["description"],
                                "input_schema": t["parameters"], "strict": True,
                                "eager_input_streaming": True} for t in tools]
        if self.use_fallbacks:
            kwargs.update(betas=[FALLBACK_BETA], fallbacks="default")
        with self.client.beta.messages.stream(**kwargs) as stream:
            resp = stream.get_final_message()
        # Append the full content so thinking blocks go back unchanged.
        conv.append({"role": "assistant", "content": resp.content})
        usage = {k: getattr(resp.usage, k, 0) or 0 for k in ("input_tokens", "output_tokens")}
        calls = []
        for b in resp.content:
            if getattr(b, "type", None) == "tool_use":
                args = b.input
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        pass
                calls.append(ToolCall(b.id, b.name, args))
        text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", None) == "text")
        stop = {"tool_use": "tool_use", "refusal": "refusal", "max_tokens": "max_tokens"}.get(resp.stop_reason, "end")
        return Turn(text, calls, stop, usage)


def make_backend(name: str = "ollama", **kw) -> OllamaBackend | ClaudeBackend:
    if name == "ollama":
        return OllamaBackend(**{k: v for k, v in kw.items() if k in
                                ("model", "host", "mode", "num_ctx", "temperature", "timeout")})
    if name == "claude":
        return ClaudeBackend(**{k: v for k, v in kw.items() if k in ("model", "effort", "use_fallbacks")})
    raise ValueError(f"unknown backend {name!r} (use ollama or claude)")
