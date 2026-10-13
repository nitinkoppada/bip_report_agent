# BIP report agent (prototype, Receivables)

Turns a plain-English request into Oracle Fusion Cloud BI Publisher artifacts:

| File | What it is |
|---|---|
| `<NAME>.sql` | The data set query (Oracle SQL against `ApplicationDB_FSCM`) |
| `<NAME>.xdm` | BI Publisher data model XML: one SQL data set, parameters, `G_HEADER` / `G_LINES` groups |
| `<NAME>.rtf` | RTF layout with BIP tags: title, parameters, group header, detail table, subtotals, grand total |
| `<NAME>_sample.xml` | Dummy data shaped like the data model output, for previewing the RTF in Word's Template Builder |
| `spec.json` | The structured report spec the model produced (columns, parameters, assumptions) |
| `validation.json` | Catalog validation result (errors, warnings, tables, bind variables) |

## How it works

1. **Retrieval** (`retrieval.py`): BM25 over the 454 objects in `../receivables-metadata/` plus a small
   Receivables vocabulary ("aging" -> `AR_PAYMENT_SCHEDULES_ALL`, "receipt" -> `AR_CASH_RECEIPTS_ALL`, ...).
   The top objects, their joined lookup tables and the documented FK edges among them go into the prompt
   (who-columns dropped).
2. **The model** (`agent.py`, `backends.py`) works with four tools: `search_catalog`, `describe_table`,
   `find_join_path`, `validate_sql`, and answers with JSON matching `REPORT_SPEC_SCHEMA`.
   The default backend is a **local model through Ollama** (`qwen2.5-coder:14b`, 24k-token window); nothing leaves your machine.
   If the local model has no tool calling, the agent switches to JSON mode: the model answers straight from
   the retrieved catalog context, its output is constrained to the spec schema, and repair rounds include the
   catalog entries of the tables the errors mention. The Claude API (`claude-opus-5-5`) is an optional second
   backend (`--backend claude`). The system prompt carries the Fusion conventions
   (`*_SEQ_ID` joins to transaction types and batch sources, `HZ_CUST_ACCOUNTS` -> `HZ_PARTIES` for names,
   null-tolerant optional parameters, `_TL` language filter, no `_GT` tables) and a short list of
   Receivables business rules (open = `STATUS = 'OP'`, amounts from payment schedules, aging in days past
   due, date ranges as two date parameters). The closest reviewed example report from `examples/specs/`
   (`examples.py`; one for a local model, two for Claude) follows the catalog context as a worked example.
3. **Validation** (`validator.py`): read-only single SELECT; every AR_/RA_/HZ_ table exists; every
   `alias.COLUMN` exists on its table; joins between catalog tables match a documented FK (warning if not);
   no table left unjoined; every `:P_X` bind has a parameter; the SQL is complete (has a FROM) and has no
   backticks. **Request checks** (`rules.py`) compare the spec with the request: every declared parameter is
   used, requested filters are present (date range, as-of date, business unit, customer), aging buckets
   use days past due, open items are `STATUS = 'OP'`, and `CLASS IN` lists only the classes the request
   names. Errors from all three go back to the model for up to two repair rounds and land in
   `validation.json` (`spec_errors`, `errors`, `request_errors`).
4. **Generators** (`datamodel.py`, `rtf_layout.py`) write the data model, layout and sample XML from the spec.

## Run it on your machine with a local model

1. **Install Ollama** from https://ollama.com/download (macOS, Windows, Linux; on Linux
   `curl -fsSL https://ollama.com/install.sh | sh`). Use version 0.5 or newer, which has tool calling and
   JSON-schema output. It runs as a background service on `http://localhost:11434`.
2. **Pull the model**: `ollama pull qwen2.5-coder:14b` (about 9 GB download).
3. **Get the code**: copy `bip-agent/` and `receivables-metadata/` from the project files into the same parent
   folder (the agent looks for `../receivables-metadata`; or pass `--catalog PATH`). Needs Python 3.10+;
   no packages are required to run, `pip install pytest` to run the tests.
4. **Check and run**:

```bash
cd bip-agent
python3 -m bip_agent check            # Ollama reachable? model pulled? tools or JSON mode?
python3 -m bip_agent generate "AR aging by customer as of a date, 30/60/90 buckets" -o out/aging
```

### Hardware for the default model

These are estimates for 4-bit models at the context window the agent sets for each.

| Model | Download | Memory needed | Runs well on |
|---|---|---|---|
| **`qwen2.5-coder:14b`** (default) | ~9 GB | ~14 GB | 16 GB GPU, Apple Silicon with 24-32 GB |
| `qwen2.5-coder:7b` | ~4.7 GB | ~6-8 GB | 8 GB GPU or 16 GB Mac; add `--num-ctx 16384`. Not recommended: in testing it wrote SQL that passed every check but was wrong |
| `qwen2.5-coder:32b` | ~20 GB | ~26 GB | 32 GB+ GPU, Apple Silicon with 48 GB+; add `--num-ctx 32768` |

On an Apple M5 Pro the 14b model takes about 100-200 s per report (2-4 model calls); nearly all of it is the model writing the SQL, and the data model and layout are generated in well under a second.

**How the agent fits a small local model.** Local runs are tuned for a 16-24k-token window:
the prompt carries at most 8 catalog objects (about 3-6k tokens); only the top two keep column comments,
and the rest list their 35 likeliest report columns (keys, join columns, names, numbers, dates, amounts,
statuses, words from the request), with `describe_table` available for the full list. The model gets at
most 5 tool rounds, and the loop also stops early when the window is three-quarters full, because Ollama
silently truncates prompts that outgrow it. After that the model must answer in schema-constrained JSON,
and the catalog validator plus up to two repair rounds catch wrong tables, columns and joins. Expect a local
model to need repairs more often than Claude, and review its business rules (statuses, date logic)
carefully. Switch models with `--model` or the `BIP_AGENT_LOCAL_MODEL` environment variable; any Ollama
model works, and the agent detects whether it supports tool calling.

### Commands

```bash
python3 -m bip_agent generate "<request>" -o out/x                  # local model (default)
python3 -m bip_agent generate "<request>" -o out/x --model qwen2.5-coder:14b --num-ctx 24576
python3 -m bip_agent generate "<request>" -o out/x --mode json      # skip tool calling
python3 -m bip_agent generate "<request>" -o out/x --backend claude # Anthropic API, needs ANTHROPIC_API_KEY
                                                                     # and `pip install anthropic`

# Offline, no model needed
python3 -m bip_agent render examples/specs/ar_aging_by_customer.json -o out/aging
python3 -m bip_agent validate my_query.sql -p P_AS_OF_DATE -p P_ORG_ID
python3 -m bip_agent retrieve "receipts applied to invoices"
python3 -m pytest -q
```

Other options: `--ollama-host` (or `OLLAMA_HOST`) for Ollama on another machine, `BIP_AGENT_BACKEND=claude`
to change the default backend, `--effort` and `--no-fallbacks` for Claude, `--catalog DIR` (before the
subcommand) for another metadata folder. If a local run fails with a context-window error, raise `--num-ctx`.

## Knowledge base (Postgres + vector search)

The crawled metadata can live in a local Postgres database with pgvector, and the agent then retrieves
from it with hybrid search: the keyword ranking (BM25 plus Receivables vocabulary) fused with vector
search over table descriptions and column comments, embedded by a local model (`nomic-embed-text`
through Ollama). Nothing leaves the machine.

| Table | Holds |
|---|---|
| `kb.objects` | 2,245 tables (every Financials table plus 116 HZ_ customer tables; no views, import/interface or _GT tables) |
| `kb.columns` | 64,596 columns with datatype and comment |
| `kb.joins` | 3,540 documented foreign-key edges; indexes are in each table's raw record |
| `kb.examples` | reviewed and approved report specs, offered as worked examples |
| `kb.chunks` | 50,905 text chunks with 768-dim embeddings (HNSW index) and full-text vectors |

Setup on a Mac: install [Postgres.app](https://postgresapp.com) (it includes pgvector), then

```bash
scripts/kb-db.sh init                    # data folder ../pgdata, database bip_kb on localhost:5432
ollama pull nomic-embed-text             # ~270 MB embedding model
python3 -m bip_agent kb setup            # schema, load JSON, embed (about 2 minutes)
python3 -m bip_agent kb status
python3 -m bip_agent kb search "cash we have not matched to invoices"
python3 -m bip_agent kb eval             # keyword vs hybrid recall on examples/retrieval_eval.json
python3 -m bip_agent kb add-example out/x/spec.json --request "..."   # grow the example library
```

After a reboot, start the database with `scripts/kb-db.sh start`. `generate` and `retrieve` use the
knowledge base automatically when it is loaded (`--kb auto`, the default) and fall back to the JSON files
otherwise; force either with `--kb postgres` or `--kb files`. The connection string is
`BIP_AGENT_DB_URL` (default `postgresql://postgres@localhost:5432/bip_kb`). Re-run `kb load` and
`kb embed` after a new crawl.

With the full Financials catalog loaded, on the 30 Receivables requests in `examples/retrieval_eval.json`
hybrid search finds 95% of expected tables for requests in Receivables wording and 64% for paraphrased ones
(73% with `BIP_AGENT_MODULES=AR,RA,HZ,ARB,IEX`, which pins retrieval to Receivables). Requests that name a
module ("customer", "supplier", "journal", "tax") down-weight tables from other modules automatically. The
fusion weights were tuned on this set, so treat the numbers as optimistic.

The crawl scope lives in `../receivables-metadata/scope_*.txt` (one table per line); rerun the crawler with
`--names-file` and then `crawler/build_catalog.py`, `kb load` and `kb embed` to refresh.

## Examples

`examples/specs/` holds three reference specs written by hand (not model output) and `examples/out/`
their rendered artifacts. They double as test fixtures, show the spec format, and are the worked examples
the agent puts in the prompt. To test a request that an example answers directly, hold that example out:
`generate "..." -o out/x --holdout ar_aging_by_customer` (or `BIP_AGENT_HOLDOUT=name1,name2`);
`--examples 0` turns them off.

- `ar_aging_by_customer`: open items bucketed current / 1-30 / 31-60 / 61-90 / 90+ as of a date, grouped by customer.
- `ar_open_invoices_by_customer`: open invoice, debit memo and chargeback installments with applied/credited/adjusted/remaining.
- `ar_receipts_applied`: cash applications in an apply-date range, grouped by receipt.

Each spec lists its business-rule assumptions (for example, the aging uses today's open balance, not a
historical as-of balance).

## Loading into BI Publisher

- **Data model**: create a data model with an SQL data set on `ApplicationDB_FSCM` and paste the `.sql`,
  then add the parameters from `spec.json`; or use the `.xdm` as the reference for the structure. The `.xdm`
  follows BIP's data model XML but has not yet been imported into a live instance.
- **Layout**: upload the `.rtf` as an RTF template on a report that uses the data model. To preview it
  offline, load `<NAME>_sample.xml` in Word's Template Builder. Tags are plain text, so they look long in
  Word but render normally.

## Limits

- The validator is a tokenizer, not a full Oracle parser. It relies on every column being qualified with
  its alias (the prompt asks for this); unqualified columns are not checked.
- Only AR_, RA_ and six HZ_ tables are verifiable. GL_, XLA_, ZX_, FND_, IBY_ and other objects are allowed
  with a warning; crawl them into the catalog to check them.
- Views in the catalog have column names but no datatypes.
- The SQL has not been run against a Fusion instance; check it there before production use.
- The local backend is tested against a stub Ollama server, not a real model yet; answer quality from a
  local model is unmeasured until it runs on your machine.
