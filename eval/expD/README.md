# Experiment D — agency & delegation (S4, the multi-bearer / large-statute rung)

Fourth statute of the suite (size ladder in `../expA/SCENARIOS.md`). Two
roles it plays that the earlier statutes can't:

1. **Multi-bearer.** The binding question lands on `@Principal` (must the
   company honor the deal its sub-agent concluded?); conduct duties land on
   `@SubAgent` (a disclose⊗disgorge chain for conflicted dealing). Gold is
   therefore *per bearer*: the honor verdict **and**, separately, whether the
   sub-agent breached its conduct duties (engine `violatingRules` ∩ {r9,r10}).
   This exercises the engine's directed-obligation machinery, flagged
   unexercised in the expA/expB write-up.
2. **Large statute (~12 rules, exception depth 5).** The honor question has a
   five-deep exception chain — scope (r1) < revocation (r2) < apparent
   authority (r3) < published revocation (r4) < ratification (r5) — plus a
   conflict prohibition (r6, cured by ratification r5) and agency-of-necessity
   (r8). This is the size-axis test: holistic verdict accuracy is predicted to
   degrade with rule count while grounded+engine stays flat (the verdict tax
   should *invert* relative to the 8-rule statutes).

Narrator: **claude-sonnet-4.6** (suite-wide, per the 2026-06-12 quality
decision). Pipeline mirrors `../expB/` (`gen_cases.py` async narration,
`arms.py`, `score.py`); engine binary is the shared `../../.lake/.../deontic`.

## Texture profile (pre-registered, in `descriptions.py`)

- artifact: `within_scope`, `revocation_published`, `authority_manifested`
- scenario: `mandate_revoked`, `ratified`, `self_dealing`
- epistemic-bar: `counterparty_good_faith` (prove subjective ignorance),
  `urgent_necessity` (necessity + unreachability)

## Domain-specific generation rules (`gen_cases.py`)

- `within_scope` and `counterparty_good_faith` are **always instantiated** —
  the deal itself realises `within_scope` (out-of-brief negative when false),
  and good faith is a negative existential (false needs affirmative knowledge
  evidence, true needs affirmative ignorance evidence).
- World coherence: `revocation_published ⇒ mandate_revoked`;
  `¬good_faith ⇒ mandate_revoked`; `urgent_necessity ⇒ within_scope`;
  `urgent_necessity ⇒ ¬self_dealing`. 100 coherent worlds.
- The deal is **concluded in every case**; `acted` means the company has
  already *refused* to perform (activates the refusal-notice gold).

## Verdict space is (almost) binary — by design, not accident

Over the 100 coherent worlds the honor verdict splits 65 obligatory / 34
forbidden / **1 permitted**: "permitted to refuse" is a vanishing residual
because agency duties fire in nearly every fact pattern. This is a faithful
structural property of agency law and a *third* kind of structural variation
in the suite (A/B had three substantive classes; C was tiny; D is near-binary
with a deep exception chain). Honor-verdict tables carry the majority-class
baseline (~65%); the headline stays at the atom level, which is unaffected by
verdict priors.

## Validation gates (green on the $0 template dry run)

oracle = gold on all 288 cases; program 100% honor at Tier 0, true-atom
recall exactly 100/0/0 (honor collapses to ~2% at Tiers 1–2 — under-inclusion
is even more punishing here than in A/B because the verdict is near-binary).

## Reproduce

```bash
python gen_cases.py --out cases_memo.jsonl --n-assignments 48 --seed 4 \
    --variants 2 --narrator openrouter:anthropic/claude-sonnet-4.6
python arms.py --cases cases_memo.jsonl --out results_main.jsonl \
    --models gpt-4.1,gpt-5.4,deepseek-v4-flash,qwen3.6-plus
python score.py --results results_main.jsonl --exclude-leaky cases_memo.jsonl
```
