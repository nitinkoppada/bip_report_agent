# BIP Report Agent

An AI agent that turns a plain-English requirement into Oracle Fusion Cloud ERP BI Publisher artifacts:
the SQL data set, the data model (`.xdm`), an RTF layout and sample XML.

- `bip-agent/` - the agent (local model through Ollama by default, Claude API optional), the catalog
  validator and request checks, the Postgres knowledge base with hybrid keyword + vector search, tests.
  See [bip-agent/README.md](bip-agent/README.md).
- `receivables-metadata/` - table metadata crawled from Oracle's Fusion Cloud *Tables and Views* guides
  (release 26d): 3,240 tables (Financials, HZ customer tables, FND common tables, HR/PER) with columns,
  keys, indexes and 3,833 joins, plus the crawler that produced it.
- `bip-agent/out_customer/` - the reviewed TCA customer master extract by business unit.

Quick start on a Mac: install Ollama and Postgres.app, then

```bash
ollama pull qwen2.5-coder:14b && ollama pull nomic-embed-text
bip-agent/scripts/kb-db.sh init
cd bip-agent && python3 -m bip_agent kb setup
python3 -m bip_agent generate "AR aging by customer as of a date" -o out/aging
```
