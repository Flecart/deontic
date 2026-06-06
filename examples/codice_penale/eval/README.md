# Eval — does the deontic tool beat the LLM alone?

A labelled dataset of penal-law scenarios + a 3-arm harness, to measure whether
an LLM **+ the deontic engine** reaches more correct/consistent verdicts than the
same LLM alone, and whether the gap **widens with norm complexity**. Design and
rationale: [`PLAN.md`](PLAN.md); the claim: [`../../../docs/evaluation.md`](../../../docs/evaluation.md).

**Methodology — work backwards.** The engine over the encoded `codice_penale` is
the gold oracle: we pick an atom config, ask the engine for the verdict, and
that verdict *is* the label (the calculus decides, not an annotator). Then we
dress the config as an Italian story with **no leakage** and build **minimal
pairs** that flip one decisive legal element. The dataset doubles as a
regression suite for the theory itself.

## Layout

```
schema.json            JSON Schema for one item (validate.py enforces it)
dataset/v0_pilot.jsonl 28 items, 11 minimal pairs, all engine-verified
prompts/               the three arms' system prompts (Italian)
tools/                 offences · backward_gen · build_v0 · validate · harness · metrics · llm · retrieval
results/               run outputs (gitignored)
```

## Data model (one JSONL item)

`id`, `tier` (1–4), `source`, `theory` (path to the `.ddl`), `narrative` (the
Italian story the model sees — no element phrasing, no verdict), `question`,
`atoms_gold` (`{Atom: 0|1}`, the engine `--assume` config), `gold`
(`{verdict, offence, penalty_status, decisive}` — **computed by the engine**),
`minimal_pair`, `distractor`, `prior_divergent`. Full field notes in `PLAN.md`.

## Run it

Build the engine first (`lake build deontic` from the repo root). Run tools from
`tools/`:

```bash
# 1. The oracle reproduces known labels
python3 backward_gen.py --selftest

# 2. (Re)build the pilot from authored specs + engine gold, then QA-gate it
python3 build_v0.py
python3 validate.py ../dataset/v0_pilot.jsonl       # schema · gold · leakage · pairs

# 3. Run the three arms (needs an LLM API key — see below) and score
python3 harness.py --dataset v0_pilot --arms llm_only,rag,deontic
python3 metrics.py ../results/predictions.jsonl
```

`metrics.py` reports per-arm verdict accuracy, offence-id accuracy, **pair-accuracy**
(both twins correct — the headline discrimination metric), the **per-tier curve**,
**grounding accuracy** (deontic arm, atom-level, reported separately from the
verdict), abstention on unresolved items, and cost (tokens + latency). Expect
**deontic ≥ rag ≥ llm_only**, the gap widening T1→T4, pair-accuracy gap largest.

## The three arms (same base model, same encoded norms in context)

- **llm_only** — narrative + the offence's atom glosses → verdict JSON.
- **rag** — same + top-k articles retrieved from `sources/codice_penale_full.md`
  (BM25, `retrieval.py`).
- **deontic** — narrative → atom assignments (`arm_ground.md`); the **engine**
  computes the verdict from those atoms (`backward_gen.verdict_auto`). The
  grounding (`pred_atoms`) is scored separately, isolating grounding error from
  deduction.

## LLM config

`llm.py` is a thin pluggable adapter. Default provider **anthropic**, model
`claude-opus-4-8`, adaptive thinking. Override via env:
`DEONTIC_LLM_PROVIDER`, `DEONTIC_LLM_MODEL`, `DEONTIC_LLM_EFFORT`
(`low|medium|high|max`); set `ANTHROPIC_API_KEY`. To add another provider, add a
branch to `complete()` returning the same `Completion` shape.

## Difficulty tiers

| Tier | What | Pilot example |
|---|---|---|
| 1 | single constitutive element | furto vs furto-d'uso (`FineDiProfitto`); percosse vs lesione |
| 2 | one scriminante / excuse | legittima difesa proporzionata vs no; minore di 14 |
| 3 | exception-to-exception | vizio totale vs +actio libera; necessità vs +dovere di esporsi |
| 4 | concorso / lex specialis | rapina vs niente (`Violenza`); premeditazione → ergastolo |

## Extending the dataset

Add a spec to `build_v0.py` (config + Italian narrative + tier + pair link),
rerun `build_v0.py` (engine fills `gold`), then `validate.py`. Authoring rules
(no leakage, minimal pairs flip one decisive atom) are in `PLAN.md` §3 and
enforced/flagged by `validate.py`. The lone standing `validate.py` warning — the
percosse↔lesione pair differing in >1 atom — is expected: the decisive concept
("did an illness result") maps to different element atoms in the encoding.
