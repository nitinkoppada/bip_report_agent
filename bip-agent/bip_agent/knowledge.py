"""Postgres knowledge base for the crawled metadata, with vector search (RAG).

Schema `kb` (see SCHEMA below):
  objects    one row per table/view: description, primary key, source URL, raw crawl record
  columns    one row per column: datatype, length, comment
  joins      documented foreign-key edges (child columns -> parent columns)
  examples   reviewed report specs used as worked examples; approved reports are added here
  chunks     text chunks with nomic-embed-text embeddings (vector(768), HNSW index) and a
             full-text tsvector: one per object, one per non-who/non-flexfield column,
             one per example

Load and index:   python3 -m bip_agent kb init && kb load && kb embed
Search:           python3 -m bip_agent kb search "cash we have not matched to invoices"

Embeddings come from a local Ollama model, so nothing leaves the machine.
"""
from __future__ import annotations

import json
import os
import re
import tempfile
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .backends import DEFAULT_OLLAMA_URL
from .catalog import WHO_COLUMNS, Catalog
from .pgdb import PG, DBError, lit

EMBED_MODEL = os.environ.get("BIP_AGENT_EMBED_MODEL", "nomic-embed-text")
EMBED_DIM = 768

SCHEMA = f"""
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE SCHEMA IF NOT EXISTS kb;

CREATE TABLE IF NOT EXISTS kb.objects (
    name              text PRIMARY KEY,
    object_type       text NOT NULL,
    owner             text,
    module            text NOT NULL DEFAULT 'AR',
    description       text NOT NULL DEFAULT '',
    primary_key       text[] NOT NULL DEFAULT '{{}}',
    flexfield_summary text,
    source_url        text,
    view_sql          text,
    raw               jsonb NOT NULL,
    loaded_at         timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kb.columns (
    object_name  text NOT NULL REFERENCES kb.objects(name) ON DELETE CASCADE,
    column_name  text NOT NULL,
    position     int  NOT NULL,
    datatype     text,
    length       int,
    precision    int,
    not_null     boolean,
    comment      text,
    PRIMARY KEY (object_name, column_name)
);

CREATE TABLE IF NOT EXISTS kb.joins (
    id              serial PRIMARY KEY,
    child           text NOT NULL,
    child_columns   text[] NOT NULL,
    parent          text NOT NULL,
    parent_columns  text[] NOT NULL,
    both_in_catalog boolean,
    raw             jsonb NOT NULL
);
CREATE INDEX IF NOT EXISTS joins_child_idx ON kb.joins (child);
CREATE INDEX IF NOT EXISTS joins_parent_idx ON kb.joins (parent);

CREATE TABLE IF NOT EXISTS kb.examples (
    name        text PRIMARY KEY,
    title       text NOT NULL,
    description text NOT NULL DEFAULT '',
    request     text,
    spec        jsonb NOT NULL,
    source      text NOT NULL DEFAULT 'reviewed',
    added_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kb.chunks (
    id           bigserial PRIMARY KEY,
    kind         text NOT NULL CHECK (kind IN ('object', 'column', 'example')),
    object_name  text,
    column_name  text,
    example_name text,
    content      text NOT NULL,
    embedding    vector({EMBED_DIM}),
    tsv          tsvector GENERATED ALWAYS AS (to_tsvector('english', replace(content, '_', ' '))) STORED
);
CREATE INDEX IF NOT EXISTS chunks_kind_idx ON kb.chunks (kind);
CREATE INDEX IF NOT EXISTS chunks_object_idx ON kb.chunks (object_name);
CREATE INDEX IF NOT EXISTS chunks_tsv_idx ON kb.chunks USING gin (tsv);
CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON kb.chunks USING hnsw (embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS kb.meta (key text PRIMARY KEY, value text NOT NULL);
"""


def _module(name: str) -> str:
    return "HZ" if name.startswith("HZ_") else name.split("_", 1)[0]


# ---------------------------------------------------------------------------
# Embeddings (Ollama)
# ---------------------------------------------------------------------------
def embed(texts: list[str], host: str = DEFAULT_OLLAMA_URL, model: str = EMBED_MODEL,
          timeout: float = 300.0) -> list[list[float]]:
    host = host.rstrip("/")
    if not host.startswith("http"):
        host = "http://" + host
    req = urllib.request.Request(host + "/api/embed", data=json.dumps({"model": model, "input": texts}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        out = json.loads(r.read())["embeddings"]
    if len(out) != len(texts):
        raise RuntimeError(f"embedding model returned {len(out)} vectors for {len(texts)} texts")
    return out


def _vec(v: list[float]) -> str:
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"


# ---------------------------------------------------------------------------
# Knowledge base
# ---------------------------------------------------------------------------
@dataclass
class Hit:
    name: str
    score: float
    via: str


class KnowledgeBase:
    def __init__(self, pg: PG | None = None, ollama_host: str = DEFAULT_OLLAMA_URL, log=None):
        self.pg = pg or PG()
        self.ollama_host = ollama_host
        self.log = log or (lambda m: None)

    # ---- setup -----------------------------------------------------------
    def init(self) -> None:
        self.pg.execute(SCHEMA)

    def _load_json_file(self, obj) -> str:
        """Write obj to a temp file readable by the local server (pg_read_file)."""
        fd, path = tempfile.mkstemp(prefix="bip_kb_", suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(obj, f)
        os.chmod(path, 0o644)
        return path

    def load(self, catalog_dir: str | os.PathLike | None = None, examples_dir: str | os.PathLike | None = None) -> dict:
        """(Re)load objects, columns, joins and examples from the crawl JSON files."""
        from .catalog import DEFAULT_DIR
        from .examples import EXAMPLES_DIR

        d = Path(catalog_dir or os.environ.get("BIP_AGENT_CATALOG_DIR") or DEFAULT_DIR)
        cat_file = d / "catalog.json" if (d / "catalog.json").exists() else d / "receivables_catalog.json"
        raw_catalog = json.loads(cat_file.read_text())
        raw_joins = json.loads((d / "joins.json").read_text())
        cat = Catalog.from_raw(raw_catalog, raw_joins)  # same parsing as the JSON loader

        objects = []
        for name, t in cat.tables.items():
            objects.append({
                "name": name, "object_type": t.object_type, "owner": t.raw.get("owner"),
                "module": _module(name), "description": t.description,
                "primary_key": list(t.primary_key), "flexfield_summary": t.flexfield_summary,
                "source_url": t.source_url,
                "view_sql": t.raw.get("view_sql") if t.raw.get("view_sql") not in (None, "None") else None,
                "raw": t.raw,
                "columns": [{"column_name": c.name, "position": i + 1, "datatype": c.datatype,
                             "length": c.length, "precision": c.precision, "not_null": c.not_null,
                             "comment": c.comment} for i, c in enumerate(t.columns.values())],
            })
        joins = [{"child": e.child, "child_columns": list(e.child_columns), "parent": e.parent,
                  "parent_columns": list(e.parent_columns), "both_in_catalog": raw.get("both_in_catalog"),
                  "raw": raw} for e, raw in zip(cat.joins, raw_joins)]
        ex_dir = Path(examples_dir) if examples_dir else EXAMPLES_DIR
        examples = [json.loads(p.read_text()) | {"_name": p.stem} for p in sorted(ex_dir.glob("*.json"))] \
            if ex_dir.is_dir() else []

        files = [self._load_json_file(objects), self._load_json_file(joins), self._load_json_file(examples)]
        try:
            self.pg.execute(f"""
TRUNCATE kb.columns, kb.joins RESTART IDENTITY;
DELETE FROM kb.objects;
DELETE FROM kb.examples WHERE source = 'reviewed';
WITH src AS (SELECT jsonb_array_elements(pg_read_file({lit(files[0])})::jsonb) AS o)
INSERT INTO kb.objects (name, object_type, owner, module, description, primary_key, flexfield_summary,
                        source_url, view_sql, raw)
SELECT o->>'name', o->>'object_type', o->>'owner', o->>'module', coalesce(o->>'description', ''),
       ARRAY(SELECT jsonb_array_elements_text(o->'primary_key')), o->>'flexfield_summary',
       o->>'source_url', o->>'view_sql', o->'raw'
FROM src;
WITH src AS (SELECT jsonb_array_elements(pg_read_file({lit(files[0])})::jsonb) AS o),
     c AS (SELECT o->>'name' AS object_name, jsonb_array_elements(o->'columns') AS c FROM src)
INSERT INTO kb.columns (object_name, column_name, position, datatype, length, precision, not_null, comment)
SELECT object_name, c->>'column_name', (c->>'position')::int, c->>'datatype', (c->>'length')::int,
       (c->>'precision')::int, (c->>'not_null')::boolean, c->>'comment'
FROM c;
WITH src AS (SELECT jsonb_array_elements(pg_read_file({lit(files[1])})::jsonb) AS j)
INSERT INTO kb.joins (child, child_columns, parent, parent_columns, both_in_catalog, raw)
SELECT j->>'child', ARRAY(SELECT jsonb_array_elements_text(j->'child_columns')), j->>'parent',
       ARRAY(SELECT jsonb_array_elements_text(j->'parent_columns')), (j->>'both_in_catalog')::boolean, j->'raw'
FROM src;
WITH src AS (SELECT jsonb_array_elements(pg_read_file({lit(files[2])})::jsonb) AS e)
INSERT INTO kb.examples (name, title, description, request, spec, source)
SELECT e->>'_name', coalesce(e->>'title', e->>'_name'), coalesce(e->>'description', ''), e->>'description',
       e - '_name', 'reviewed'
FROM src
ON CONFLICT (name) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description,
       request = EXCLUDED.request, spec = EXCLUDED.spec, source = EXCLUDED.source, added_at = now();
INSERT INTO kb.meta VALUES ('loaded_from', {lit(str(d.resolve()))}), ('loaded_at', now()::text)
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
""")
        finally:
            for f in files:
                os.unlink(f)
        self._build_chunks()
        return self.status()

    def _build_chunks(self) -> None:
        """Rebuild chunks from the loaded tables. Embeddings of chunks whose text is unchanged are
        kept, so a reload after adding tables only embeds the new ones."""
        who = ", ".join(lit(c) for c in sorted(WHO_COLUMNS))
        self.pg.execute(f"""
CREATE TEMP TABLE prev_emb ON COMMIT DROP AS
  SELECT DISTINCT ON (content) content, embedding FROM kb.chunks WHERE embedding IS NOT NULL;
DELETE FROM kb.chunks;
INSERT INTO kb.chunks (kind, object_name, content)
SELECT 'object', o.name,
       lower(o.object_type) || ' ' || o.name || ': ' || o.description || ' Columns: ' ||
       coalesce((SELECT string_agg(c.column_name, ', ' ORDER BY c.position)
                 FROM (SELECT * FROM kb.columns c WHERE c.object_name = o.name
                       AND c.column_name NOT IN ({who}) ORDER BY c.position LIMIT 40) c), '')
FROM kb.objects o;
INSERT INTO kb.chunks (kind, object_name, column_name, content)
SELECT 'column', c.object_name, c.column_name,
       'column ' || c.object_name || '.' || c.column_name || ' (' || coalesce(c.datatype, 'unknown') || '): ' ||
       coalesce(c.comment, '')
FROM kb.columns c
WHERE c.column_name NOT IN ({who})
  AND c.column_name !~ '^(ATTRIBUTE|GLOBAL_ATTRIBUTE|EXTN_ATTRIBUTE)';
INSERT INTO kb.chunks (kind, example_name, content)
SELECT 'example', e.name, 'example report ' || e.title || ': ' || e.description FROM kb.examples e;
UPDATE kb.chunks c SET embedding = p.embedding FROM prev_emb p WHERE c.content = p.content;
""")

    def embed_missing(self, batch: int = 64, pause_every: int = 0, pause_seconds: float = 0.0) -> int:
        """Embed every chunk without an embedding. Returns the number embedded.

        pause_every/pause_seconds rest the GPU between rounds (e.g. 2000 chunks, then 30 s) so a
        long run doesn't overheat a laptop."""
        done = 0
        t0 = time.time()
        while True:
            rows = self.pg.query(f"SELECT id, content FROM kb.chunks WHERE embedding IS NULL ORDER BY id LIMIT {batch * 16}")
            if not rows:
                break
            updates = []
            for i in range(0, len(rows), batch):
                part = rows[i:i + batch]
                vecs = embed(["search_document: " + r["content"][:2000] for r in part], self.ollama_host)
                updates += [(r["id"], v) for r, v in zip(part, vecs)]
            values = ",\n".join(f"({rid}, {lit(_vec(v))}::vector)" for rid, v in updates)
            self.pg.execute(f"UPDATE kb.chunks c SET embedding = u.e FROM (VALUES {values}) AS u(id, e) WHERE c.id = u.id;")
            done += len(updates)
            self.log(f"embedded {done} chunks ({done / max(time.time() - t0, 1e-6):.0f}/s)")
            if pause_every and pause_seconds and done % pause_every < len(updates):
                self.log(f"cooling down for {pause_seconds:.0f}s")
                time.sleep(pause_seconds)
        self.pg.execute(f"INSERT INTO kb.meta VALUES ('embed_model', {lit(EMBED_MODEL)}) "
                        "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;")
        return done

    def status(self) -> dict:
        return self.pg.query("""
SELECT (SELECT count(*) FROM kb.objects) AS objects,
       (SELECT count(*) FROM kb.columns) AS columns,
       (SELECT count(*) FROM kb.joins) AS joins,
       (SELECT count(*) FROM kb.examples) AS examples,
       (SELECT count(*) FROM kb.chunks) AS chunks,
       (SELECT count(*) FROM kb.chunks WHERE embedding IS NOT NULL) AS embedded,
       (SELECT value FROM kb.meta WHERE key = 'embed_model') AS embed_model,
       (SELECT value FROM kb.meta WHERE key = 'loaded_at') AS loaded_at""")[0]

    def ready(self) -> bool:
        try:
            s = self.status()
        except DBError:
            return False
        return s["objects"] > 0 and s["embedded"] == s["chunks"] > 0

    # ---- reading ---------------------------------------------------------
    def catalog(self) -> Catalog:
        """Build the in-memory Catalog from Postgres (same shape as the JSON loader)."""
        objs = self.pg.query("SELECT name, raw FROM kb.objects ORDER BY name")
        joins = self.pg.query("SELECT raw FROM kb.joins ORDER BY id")
        return Catalog.from_raw({o["name"]: o["raw"] for o in objs}, [j["raw"] for j in joins])

    def examples(self) -> list[dict]:
        return self.pg.query("SELECT name, spec FROM kb.examples ORDER BY name")

    def add_example(self, name: str, spec: dict, request: str | None = None, source: str = "approved") -> None:
        """Store an approved report as a worked example and index it."""
        self.pg.execute(f"""
INSERT INTO kb.examples (name, title, description, request, spec, source)
VALUES ({lit(name)}, {lit(spec.get('title') or name)}, {lit(spec.get('description') or '')}, {lit(request)},
        {lit(json.dumps(spec))}::jsonb, {lit(source)})
ON CONFLICT (name) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description,
    request = EXCLUDED.request, spec = EXCLUDED.spec, source = EXCLUDED.source, added_at = now();
DELETE FROM kb.chunks WHERE kind = 'example' AND example_name = {lit(name)};
INSERT INTO kb.chunks (kind, example_name, content)
SELECT 'example', e.name, 'example report ' || e.title || ': ' || e.description FROM kb.examples e
WHERE e.name = {lit(name)};
""")
        self.embed_missing()

    # ---- search ----------------------------------------------------------
    def search(self, request: str, k_objects: int = 40, k_columns: int = 150) -> dict[str, list[Hit]]:
        """Ranked object hits from three signals: object vectors, column vectors, full text."""
        q = _vec(embed(["search_query: " + request], self.ollama_host)[0])
        words = [w for w in re.findall(r"[a-z0-9]+", request.lower()) if len(w) > 2]
        tsq = " | ".join(sorted(set(words))) or "x"
        rows = self.pg.query(f"""
WITH q AS (SELECT {lit(q)}::vector AS v),
obj AS (
  SELECT c.object_name AS name, 1 - (c.embedding <=> q.v) AS score, 'object_vector' AS via
  FROM kb.chunks c, q WHERE c.kind = 'object'
  ORDER BY c.embedding <=> q.v LIMIT {k_objects}),
col AS (
  SELECT name, max(score) AS score, 'column_vector' AS via FROM (
    SELECT c.object_name AS name, 1 - (c.embedding <=> q.v) AS score
    FROM kb.chunks c, q WHERE c.kind = 'column'
    ORDER BY c.embedding <=> q.v LIMIT {k_columns}) x GROUP BY name),
fts AS (
  SELECT c.object_name AS name, max(ts_rank_cd(c.tsv, to_tsquery('english', {lit(tsq)}))) AS score,
         'full_text' AS via
  FROM kb.chunks c WHERE c.kind IN ('object', 'column') AND c.tsv @@ to_tsquery('english', {lit(tsq)})
  GROUP BY c.object_name ORDER BY 2 DESC LIMIT {k_objects})
SELECT * FROM obj UNION ALL SELECT * FROM col UNION ALL SELECT * FROM fts""")
        out: dict[str, list[Hit]] = {"object_vector": [], "column_vector": [], "full_text": []}
        for r in rows:
            out[r["via"]].append(Hit(r["name"], float(r["score"]), r["via"]))
        for v in out.values():
            v.sort(key=lambda h: -h.score)
        return out

    def search_examples(self, request: str, k: int = 3, exclude: list[str] | None = None) -> list[tuple[str, float]]:
        q = _vec(embed(["search_query: " + request], self.ollama_host)[0])
        held = {x.lower() for x in (exclude or [])}
        rows = self.pg.query(f"""
SELECT c.example_name AS name, 1 - (c.embedding <=> {lit(q)}::vector) AS score
FROM kb.chunks c WHERE c.kind = 'example' ORDER BY 2 DESC""")
        return [(r["name"], float(r["score"])) for r in rows if r["name"].lower() not in held][:k]
