# Agentic eval harness

Compares a model on LegalBench-style legal tasks under three conditions:

- **baseline** — prompt the model directly for a label.
- **cli** *(default agentic)* — give the model a `bash` tool (the `deontic`
  binary is on PATH) plus [`deontic_skill.md`](deontic_skill.md) in the system
  prompt. It writes `.ddl` files and runs `deontic query/abduce/...` itself for
  up to N rounds — closest to a real agent with a terminal.
- **tool** — a structured `run_deontic(ddl, command, args)` function tool instead
  of raw shell (no arbitrary commands; handy to compare against `cli`).

The full tool/CLI transcript is logged (the auditability win). The `cli` shell
is scoped (runs in the repo, 30s timeout, refuses destructive/networked
commands) — it is **not a sandbox**; use only for trusted research evals.

Model-swappable: one OpenAI-compatible client drives both OpenAI and OpenRouter.

## Setup

```bash
.venv/bin/python -m pip install -r eval/requirements.txt   # just `openai`
export PATH="$HOME/.elan/bin:$PATH" && lake build deontic   # the tool binary
ln -sf "$PWD/.lake/build/bin/deontic" ~/.local/bin/deontic   # put `deontic` on PATH
export OPENAI_API_KEY=sk-...          # for provider openai
export OPENROUTER_API_KEY=sk-or-...   # for provider openrouter
```

(The `cli` condition also injects the build dir onto PATH for its shell, so the
symlink is mainly for your own interactive use. Override the binary location
with `DEONTIC_BIN`.)

Run from the **project root** (so `./.lake/build/bin/deontic` resolves; override
with `DEONTIC_BIN`).

## Usage

```bash
# Offline smoke test (no network/spend): the `stub` model always answers "Yes".
python eval/run.py --model stub                      # default: baseline,cli

# Real run on the built-in sample (6 contract_nli items), baseline vs cli, logged.
python eval/run.py --model gpt-4o-mini --out runs/gpt4omini.jsonl

# Pick conditions explicitly (baseline | cli | tool; 'all' = all three):
python eval/run.py --model gpt-4.1 --condition baseline,cli,tool

# Any OpenRouter model ad-hoc (no registry entry needed):
python eval/run.py --model openrouter:deepseek/deepseek-chat --condition cli

# Your own data (LegalBench task TSV with a fixed hypothesis, or a JSONL):
python eval/run.py --model gpt-4.1 --data path/to/test.tsv \
    --text-col text --answer-col answer --hypothesis "Receiving Party may share ... employees."
```

Models live in [`models.py`](models.py) `REGISTRY` — add a line to register one,
or pass `provider:model_id`. Tasks live in [`data.py`](data.py) `TASKS`.

## Output

Per example it prints `pred` vs `gold` and (for `tool`) the number of reasoner
calls, then an accuracy summary per condition. With `--out` it writes a JSONL
log with the full transcript — including every DDL theory the model wrote and
the reasoner's reply — so you can audit *why* the tool condition answered as it did.

## Getting real LegalBench data

The built-in `sample/contract_nli.jsonl` is for smoke-testing. For the real
benchmark use the `nguha/legalbench` HuggingFace dataset, e.g.

```python
from datasets import load_dataset
ds = load_dataset("nguha/legalbench", "contract_nli_sharing_with_employees")
```

then export `text`/`answer` columns to a TSV/JSONL and point `--data` at it
(each `contract_nli_*` task has a fixed hypothesis — pass it via `--hypothesis`).
See [`../examples/legalbench/COMPARISON.md`](../examples/legalbench/COMPARISON.md)
for the with/without-reasoner protocol this harness implements.

## Notes

- Reasoning models (e.g. `o4-mini`) omit `temperature` automatically.
- Errors (bad key, rate limit, no tool support) are caught per example, logged,
  and the sweep continues; they show as `ERR` and count as incorrect.
