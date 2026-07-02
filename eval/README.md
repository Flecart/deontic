# Experiment suite: open-texture generalization

Six synthetic statutes (`expA` … `expF`) measuring how the same norm generalizes
to unforeseen cases under three bindings — drafting-time program (no LLM),
closed enumerated descriptions + LLM grounder, open intensional descriptions +
LLM grounder — against a holistic LLM judge and an oracle ceiling. Gold labels
are correct by construction: cases are backward-generated from latent atom
assignments through the `deontic` engine, then narrated into prose; novelty is
a controlled variable (Tier 0 listed / Tier 1 unlisted variant / Tier 2
world-shift instance).

| Statute | Domain |
|---|---|
| `expA` | inter-agent data transfer (the original, deepest ablations) |
| `expB` | shared-resource commons (+ persuasion probe `sway.py`) |
| `expC` | Hart's "no vehicles in the park" (concept-figure floor) |
| `expD` | agency & delegation (12 rules, multi-bearer) |
| `expE` | sale of goods (pre-registered prediction failed — reported) |
| `expF` | agent-safety constitution (12-model panel; open over-generalizes) |

## Method & provenance

- `QA_PROTOCOL.md` — validation gates (oracle exactness, program Tier-0
  exactness, leak checks, dual-family bank validation, description freeze).
- `DOMAIN_RATIONALE.md` — why these six domains (institution, texture, size axes).
- Per statute: `statute.ddl`, `descriptions.py` (open + closed contracts per
  atom), `gen_cases.py`, `arms.py`, `score.py`, `validate_banks.py`, results in
  `results_*.jsonl`, findings in `RESULTS.md` / `RESULTS_tables.md`.

## Reproducing numbers

Every headline number is a plain count over the committed JSONL logs:

```bash
cd eval
python3 reproduce_results.py   # per-statute + pooled tables from logs (no API)
python3 aggregate.py           # cross-statute pooled + bootstrap CIs (run from eval/)
python3 token_cost.py          # token totals and $ estimates per model/arm
python3 error_analysis.py      # classify every wrong atom decision -> ERROR_ANATOMY.md
```

`error_analysis.py` separates model misreads from unclear cases using three
log-native signals (the model's true/false/**unknown** raw answer, all-models-
wrong consensus, and annotator disagreement in `bank_validation.jsonl`); the
`case_unclear` / `gold_disputed` rows it lists are the ones to eyeball in the
Data QA viewer (`python3 docs/experiments/app.py`, then http://localhost:8051).

Re-running arms needs the engine binary and an API key:

```bash
pip install -r eval/requirements.txt                       # just `openai`
export PATH="$HOME/.elan/bin:$PATH" && lake build deontic  # the engine binary
export OPENROUTER_API_KEY=sk-or-...   # or OPENAI_API_KEY for provider openai
python3 expA/arms.py --help
```

## Shared infrastructure

- `models.py` — model registry + one OpenAI-compatible client for OpenAI and
  OpenRouter (`CHEAP_PANEL`: 12 validated OpenRouter models; `COSTLY_PANEL`:
  frontier models, run manually).
- `agents.py` — the model-call chokepoint used by every `arms.py`/`gen_cases.py`.
- `deontic_tool.py` / `deontic_skill.md` — scoped CLI/function-tool surface for
  agentic conditions.

The earlier LegalBench three-condition harness (baseline / cli / tool on real
legal NLI tasks) was removed from the tree along with `examples/legalbench/`;
both are preserved at git tag `real-law-final`
(`git checkout real-law-final -- eval/run.py` etc.).
