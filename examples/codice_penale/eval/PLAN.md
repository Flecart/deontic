# Plan — Evaluation dataset for "deontic tool vs LLM-only"

> Deliverable: scaffold the `eval/` tree below. (Written in plan mode; on approval, copy this
> file to that path and create the scaffold + v0 pilot.)

## Context

We claim an LLM + the deontic reasoner reaches more correct/consistent normative
verdicts than the same LLM alone, and that the gap widens with norm complexity
(`docs/evaluation.md`). To measure it we need a labelled dataset of penal-law
scenarios. The methodology (user's): **work backwards** — start from a
ground-truth verdict produced by the engine over the encoded `codice_penale`,
dress it as a plausible real-world story, and build **minimal pairs** that force
a system to *discriminate* on the one decisive legal element. The engine is the
gold-label oracle (labels come from the calculus, not annotator opinion); the
dataset doubles as a regression suite for the theory itself.

## Where it lives

```
examples/codice_penale/eval/
  PLAN.md            # this file
  README.md          # how to run, schema, metrics (short)
  schema.json        # JSON Schema for one item (validated in CI)
  dataset/
    v0_pilot.jsonl   # ~40 items, ~15 minimal pairs, hand-authored
    v1.jsonl         # later
  tools/
    offences.py      # parse element atoms + penalty atom per offence from specs.txt/.ddl
    backward_gen.py  # config -> engine verdict (oracle); emits item stubs
    validate.py      # schema + leakage + engine-gold consistency checks
    harness.py       # runs the 3 arms over dataset, writes predictions.jsonl
    metrics.py       # scores predictions vs gold; per-tier + pair-accuracy
    llm.py           # thin pluggable LLM adapter (env-keyed; Anthropic default)
  prompts/
    arm_llm_only.md  # narrative + statute text -> verdict
    arm_rag.md       # + retrieval
    arm_ground.md    # narrative -> atom assignments (for the deontic arm)
  results/           # gitignored run outputs
```

## Data model (one item, JSONL)

| field | type | notes |
|---|---|---|
| `id` | str | `furto-001` (offence-seq) |
| `tier` | int 1–4 | difficulty (see Tiers) |
| `source` | str | `synthetic` \| `real:Cass.<n>` \| `news:<ref>` |
| `theory` | str | path, e.g. `examples/codice_penale/furto.ddl` |
| `narrative` | str | Italian story the model sees — **no element phrasing, no legal conclusion** |
| `question` | str | e.g. "È punibile X, e per quale reato?" |
| `atoms_gold` | obj | `{AtomName: 0/1}` — the grounding gold = the engine `--assume` config |
| `gold` | obj | `{verdict: "offence"\|"no-offence"\|"unresolved", offence: "<art>"\|null, penalty_status: "O(...)"\|"P(...)"\|"F(...)", decisive: "<short legal reason>"}` |
| `minimal_pair` | str\|null | id of the twin differing by one decisive atom |
| `distractor` | bool | story carries lurid-but-irrelevant facts |
| `prior_divergent` | bool | codified answer ≠ lay intuition |

`gold` is computed by the engine; everything else is authored/validated.

## Components to implement

### 1. `tools/offences.py` — offence catalogue
- Parse `tools/specs.txt` and the hand-written `.ddl` (omicidio/furto/lesioni/…)
  to build, per offence: `{art, file, element_atoms[], mens, penalty_atom,
  procedibilita?, aggravanti?}`. Reuse the rule shapes already there
  (`pena_<art>` conclusion = penalty atom; precondition-block head + `oneof` =
  elements). This is the source of truth for what atoms to set.

### 2. `tools/backward_gen.py` — the oracle (engine-as-gold)
- Input: an offence + a chosen config (which elements/scriminanti present).
- Build the `--assume` token list from the config (present atoms only; e.g.
  `Impossessamento,CosaMobileAltrui,Sottrazione,FineDiProfitto,Dolo,Querela`).
- Call: `./.lake/build/bin/deontic query <file> <penalty_atom> Sanziona --assume <tokens> --json`.
- Parse JSON (shape confirmed in `Deontic/Pretty.lean`): per-atom
  `{"<atom>":{"status":"O(x)|F(x)|P(x)|Ps(x)|Pw(x)|fact(x)|unresolved|unknown","tags":[…]}}`,
  plus top-level `hasViolation`, `hasUnresolvedConflicts`.
- Derive `gold`: offence-committed ⇔ `penalty_atom.status` starts `"O("`;
  not-punishable ⇔ `Sanziona.status` is `"F("` or not `"O("`; deadlock ⇔
  `hasUnresolvedConflicts`. Set `atoms_gold` = the config.
- Output: item **stubs** (everything but `narrative`/`question`, which are
  authored). Deterministic, scriptable — this generates labels at scale.

### 3. Scenario authoring (manual, optionally LLM-drafted then human-verified)
- For each stub, write an Italian `narrative` that **entails exactly** the
  config, with **no leakage**: never name an element atom or its rubric, never
  state the verdict; the decisive element must be *inferable* from facts.
- Minimal pairs: take a base config, flip **one decisive atom**, re-narrate only
  the sentence that changes, regenerate gold via `backward_gen.py`, link
  `minimal_pair` both ways.

### 4. `tools/validate.py` — QA gate
- JSON-Schema validate each item (`schema.json`).
- **Engine-gold consistency:** re-run `backward_gen.py` on `atoms_gold` and
  assert it reproduces `gold` (catches stale labels).
- **Leakage heuristic:** flag narratives containing any element-atom rubric
  token or verdict words (punibile/reato/assolto/scriminante…); human resolves.
- **Pair integrity:** twins share `theory`, differ in exactly one `atoms_gold`
  key, and have different `gold.verdict` (or penalty tier).

### 5. `tools/harness.py` — the three arms
Reads dataset, for each item runs each arm via `llm.py`, writes
`results/predictions.jsonl` (`{id, arm, raw, pred_verdict, pred_offence,
pred_atoms?}`). Arms (same base model, same statute text in-context — don't
starve LLM-only):
- **llm_only** (`prompts/arm_llm_only.md`): narrative + relevant statute text →
  structured verdict.
- **rag**: same + retrieval over `sources/codice_penale_full.md` (simple BM25/
  embedding top-k; reuse the article index logic in `tools/gen.py`).
- **deontic** (`prompts/arm_ground.md`): narrative → atom assignments over the
  offence's element atoms; then call the engine (reuse `backward_gen.py`) to get
  the verdict. Record `pred_atoms` so grounding is scored separately.

### 6. `tools/metrics.py`
- **Verdict accuracy / F1** vs `gold.verdict` (and offence-id when applicable).
- **Pair-accuracy:** fraction of minimal pairs where *both* twins are correct —
  the headline discrimination metric.
- **Per-tier curve:** accuracy by `tier` per arm (the scaling-curve plot).
- **Grounding accuracy** (deontic arm only): `pred_atoms` vs `atoms_gold`,
  reported separately from verdict — isolates grounding error from deduction.
- **Calibrated abstention:** on `hasUnresolvedConflicts` items, did the arm
  abstain/flag vs confabulate.
- **Cost:** tokens + latency per arm (denominator).

### 7. `tools/llm.py` + `prompts/*`
- Thin adapter: `complete(system, user) -> text`, provider via env
  (`OPENAI_API_KEY` default; pluggable). Prompts request **strict JSON**
  output (verdict / offence / atom-assignments) for deterministic parsing.

## Difficulty tiers (tie to real atoms)

| Tier | What | Example decisive flip |
|---|---|---|
| 1 | single constitutive element | furto `FineDiProfitto` 0↔1; lesione vs percosse `MalattiaCorpoMente` |
| 2 | one scriminante / excuse | killing + `PericoloAttuale,DifesaProporzionata` (52); `MinoreAnni14` (97) |
| 3 | exception-to-exception | `VizioTotaleMente` + `Preordinato` (87 restores); `StatoNecessita` + `DovereEsporsi` (54 c.2) |
| 4 | concorso / lex specialis | furto-elements + `Violenza` ⇒ rapina not furto; `Premeditazione` ⇒ ergastolo overrides base |

## v0 pilot (~40 items, hand-authored, all verified)
Minimal pairs across, at least: furto vs furto-d'uso (T1), lesione/percosse/
lesione-grave gradation (T1), omicidio doloso vs colposo (T1), legittima difesa
proporzionata vs no (T2), vizio totale vs +preordinato (T3), rapina vs furto
(T4), premeditazione→ergastolo (T4); plus 4 prior-divergent (minore-che-uccide,
furto-improcedibile-senza-querela) and 4 distractor variants. Goal: stand up the
harness and confirm the LLM-only↔deontic gap *appears* before scaling to v1.

## Verification (end-to-end)
1. `python tools/backward_gen.py --selftest` reproduces known labels (e.g. furto
   full config ⇒ `O(ReclusioneFurto)`; drop `FineDiProfitto` ⇒ not `O`).
2. `python tools/validate.py dataset/v0_pilot.jsonl` → 0 schema/leakage/pair/
   consistency errors.
3. `python tools/harness.py --dataset v0_pilot --arms llm_only,rag,deontic`
   (needs API key) → `results/predictions.jsonl`.
4. `python tools/metrics.py results/predictions.jsonl` → table: per-arm accuracy,
   pair-accuracy, per-tier curve, grounding accuracy, cost. Expect
   deontic ≥ rag ≥ llm_only, gap widening T1→T4, pair-accuracy gap largest.

## Open decisions (defaults chosen; change on request)
- **Language:** narratives in Italian (matches the code); questions Italian. EN
  glosses optional.
- **LLM provider:** pluggable adapter, Anthropic default.
- **v0 authoring:** hand-written (max control); LLM-drafting deferred to v1.
- **RAG arm:** simple article-index retrieval reusing `tools/gen.py`'s indexer;
  could be dropped if only the 2-arm (llm_only vs deontic) contrast is wanted.
