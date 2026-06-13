# Experiment F results — agent safety (REBUILT v2, classificatory atoms)

## Why rebuilt (the classify-vs-balance discipline)

F v1 atomized **balancing standards** — `irreversible` ("cannot be undone by
any reasonable means"), `averting_harm` ("necessary to prevent imminent
harm"), `consequential` ("significant"), `contained` (as a guarantee). Those
are not classificatory predicates; grounding them *is* the adjudication, which
violates the paper's premise (the LLM classifies, never weighs/judges). The
LLM correctly refused to ground them (v1 open recall ~10–40%), which we now
read as the architecture's **type-check**, not an "epistemic-bar texture"
finding. (Same trap as a FOIA "public interest" clause.)

v2 uses only **classificatory atoms** — action-type classifications
(`external_effect`, `destructive`, `financial`, `affects_third_parties`) and
concrete safeguard facts (`confirmed`, `sandboxed`, `reversible_window`,
`runtime_certified`, `emergency_declared`). The balancing the legislator wants
(which action types are high-stakes, which safeguards lift the prohibition,
emergency override) is encoded in the **rules**, exactly how real AI
constitutions are written — broad but *categorized* principles, not open-ended
reasonableness tests. v1 archived as `*_v1.jsonl`.

## Gates + grounding strength (the 12-model panel)

Gates green: oracle = gold on all 432; program 100% Tier-0, recall 100/0/0;
balanced 3-class verdict (144/144/144), 0 leak-flagged. Narration quality
spot-checked (faithful, hard negatives subtle, no leakage).

**12-model cheap panel** (June-2026 OpenRouter slugs) — atom accuracy by
regime × tier; the rebuild made every atom groundable, and grounding is strong
across all providers (no model swapped for JSON misbehaviour; all-false rate
0–7%):

| model | closed T0/T1/T2 | open T0/T1/T2 |
|---|---|---|
| gpt-4.1 | 96/86/86 | 87/89/84 |
| deepseek-v4-flash | 91/84/85 | 81/84/80 |
| deepseek-v4-pro | 94/84/86 | 80/84/79 |
| qwen3.6-plus | 97/84/88 | 86/86/84 |
| kimi-k2.5 | 94/89/87 | 85/87/82 |
| glm-4.7 | 96/83/81 | 86/87/83 |
| glm-4.7-flash | 92/84/86 | 83/86/81 |
| mistral-small | 93/86/87 | 86/87/84 |
| mimo-flash | 96/86/87 | 87/88/84 |
| grok-4.3 | 93/88/88 | 85/87/85 |
| gemini-flash | 97/75/76 | 79/83/81 |
| llama-3.3-70b | 93/86/87 | 86/86/82 |

Costly/frontier models (gpt-5.4, claude-opus, claude-sonnet, grok-4.20) are
registered in `models.py` (`COSTLY_PANEL`) for the **human** to run now that
the cheap-panel grounding is validated strong.

## Honest finding: the epistemic drop fixed groundability, not the verdict gap

The rebuild **succeeded** at its stated job: open atom recall is up (84% Tier-2
vs v1's 77%), no atom is ungroundable. But at the *verdict* layer closed still
beats open on F (≈90 vs ≈60, 3 families). The diagnosis is **not** epistemic-bar
anymore — it is **open over-generalization**, diagnosed per-atom (Tier-2
recall/false-positive, closed | open):

| atom | closed | open | issue |
|---|---|---|---|
| external_effect | 70/35 | 99/66 | open over-includes |
| destructive | 72/0 | 97/33 | open over-includes |
| affects_third_parties | 100/52 | 100/73 | open over-includes |
| confirmed | 80/7 | 31/2 | open under-recalls |
| emergency_declared | 99/0 | 46/0 | open under-recalls |

Open's broad purpose-stated intensions **over-fire the prohibition atoms** and
**under-fire the safeguards/override**, so open over-predicts `forbidden`
(verdict errors permitted→forbidden 62, obligatory→forbidden 44). This is the
flip side of generalization: an intension generalizes *and* over-reaches, and
the verdict layer punishes over-firing a prohibition asymmetrically.

**Caveat (disclosed):** this is partly sensitive to open-vs-closed description
calibration — our open `external_effect` is genuinely broader than its closed
enumeration; `confirmed`'s open clause is stricter. We deliberately do **not**
re-tune the descriptions until open wins (the circularity trap). F is therefore
reported as the *open-over-generalization* case (a real limitation), not as an
open-advantage statute. It is also an *easy* statute (verdict ~90 for the
winning regime) and contributes methodologically — the classify-vs-balance
demonstration — rather than to the discriminative difficulty (which A/B/C/D at
~60 verdict carry).

## Artifacts

`cases_memo.jsonl` (432, 0 flagged; v1 at `cases_memo_v1.jsonl`),
`results_main.jsonl` (12-model panel), `statute.ddl` (engine-verified),
`descriptions.py` (classificatory atoms). Holistic arm pending.
