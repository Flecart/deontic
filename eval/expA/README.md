# Experiment A — the predicate generalization curve

Tests the paper's thesis: open-textured (intensional) atom descriptions + LLM
grounding generalize to unforeseen instances; closed (extensional) descriptions
— and a fortiori LLM-free programs — generalize exactly as far as the drafter
foresaw. Design rationale: `docs/RELATED.md` §8 (Experiment A); thesis framing
in the paper draft.

## Pieces

| file | role |
|---|---|
| `statute.ddl` | 8-rule inter-agent data-transfer statute (defaults, exceptions, exception-to-exceptions, one compensation chain). Open descriptions are canonical. |
| `descriptions.py` | The experimental material: per atom, open + closed descriptions and instance banks — `closed_items` (Tier 0, also the program arm's lookup), `tier1` (unlisted near-variants), `tier2` (world-shift instances satisfying the intension outside every listed category), `negative` (hard non-instances). |
| `gen_cases.py` | Backward generation: latent assignment → engine gold (`--why`-able) → bank instantiation → narration (template or `--narrator <model>`); tier-aware leak check (open-description echo always banned; closed-description echo banned at tiers 1–2). |
| `arms.py` | oracle / program / ground_closed / ground_open / holistic. Grounding uses neutral labels C1..C7 so regimes differ only in definition text. |
| `score.py` | verdict acc by arm×tier; atom-level acc by regime×tier (+ per-atom true-recall); violation/remedy acc on acted subset; tokens. |

## Gold semantics

Gold truth of an atom is defined by the **open intension** (the legislator's
contract); the closed list is a best-faith drafting-time operationalization.
Verdict = engine status of `share` ∈ {obligatory, permitted, forbidden}; acted
cases (the hand-off already happened) add gold `violation` and `notify_required`
(only the `r1` chain carries the notify⊗compensate remedy — r3/r6 breaches are
violations *without* a notify duty, a deliberately deontic distinction).

## Validations (must pass before any result is read)

- oracle arm reproduces gold on every case (asserted in `arms.py`);
- program arm = 100% verdict at Tier 0, collapses at Tiers 1–2 (under-inclusion);
- generated cases stratified across verdict classes; leak-flagged cases excluded
  from scoring (`score.py --exclude-leaky`).

Stage 0 (stub, $0): all validations green — oracle 24/24/24, program 100/33/33.

## Reproduce

```bash
python gen_cases.py --out cases.jsonl --n-assignments 24 --seed 1 \
    --narrator openrouter:anthropic/claude-sonnet-4.6   # 3rd family vs grounders
python arms.py --cases cases.jsonl --out results.jsonl \
    --models gpt-4.1,deepseek-v4-flash
python score.py --results results.jsonl --exclude-leaky cases.jsonl
```
