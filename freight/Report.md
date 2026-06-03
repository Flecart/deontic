# Emergent contract case law for an LLM agent society

*A repeated freight/sales game where an LLM judge builds, and is bound by, its
own evolving body of precedent. Four "legal regimes" (arms) are compared on
welfare, predictability, and selection.*

This is the executable pilot of the spec in the kickoff brief. It lives in
`freight/` and reuses this repo's `deontic` DDL engine for one specific job (the
overruling / closure-stability metric); everything else is new.

> **Scope honesty.** The brief's full pilot is T=400, 16 agents, 3×4 = 12 runs
> with an Opus-class judge. What ran here is a **de-risked, cost-bounded pilot**:
> T=200, 2 seeds × 4 arms = 8 runs, `gpt-4o-mini` as both agent-prior source and
> judge, `text-embedding-3-small` for retrieval. The code takes the full scale
> via CLI flags (`--rounds`, `--seeds`, `--judge-model`); only compute/$$ stands
> between this and the headline configuration. Read the numbers below as a
> *machinery-works + directional-signal* result, not a powered experiment.

---

## 1. The game

A buyer **B** and seller **S** contract over a shipment spec **x** with crisp
fields (quantity, deadline, price *p*) and fuzzy ones (quality tier, packaging,
substitution clause, force-majeure clause). After contracting:

1. S draws a private cost shock **θ** and chooses a delivery **x′** that may
   deviate on the fuzzy dimensions; it incurs cost *c*(x′, θ).
2. B draws private valuation noise **η** and realises value *v*(x′, η).
3. **Settlement**: B demands compensation *r* ∈ [0, p]; S accepts or rejects.
4. If no deal, B decides whether to **file** (cost *c_f*). If filed, the judge
   **𝒥**(x, x′, 𝒞) returns a ruling ∈ {compliant, breach} and damages *d*.

Payoffs (transfers cancel in *total* welfare):
`π_B = v − p + r` (settle) or `v − p + d − c_f` (file & win);
`π_S = p − c − r` or `p − c − d`.

The spec space (`env.py`): 7 goods × {standard, premium} × 3 windows × 3
packaging × 4 substitution templates × 4 force-majeure templates ≈ 2k discrete
contract shells, plus continuous quantity/price.

## 2. The Priest–Rubin selection engine (`agents.py`)

The brief's central primitive: **both parties act on a *prior* over how 𝒥 will
rule, and litigate only when those priors diverge enough to burn the settlement
surplus.** We make that prior *faithful and cheap* by grounding it in the same
object 𝒥 itself consults — the **breach rate among the precedents retrieved for
this case** — then adding each side's self-serving optimism and a sliver of
private information (S leans on θ via a force-majeure story; B leans on its
valuation shortfall).

With similarity-weighted retrieved-breach-rate `base`, damage estimate `d̂`:

```
p_B = base + optimism + b_info ;   p_S = base − optimism + s_info
settlement zone exists  ⟺  (p_B − p_S)·d̂·p ≤ c_f
buyer files (no zone)   ⟺  p_B·d̂·p − c_f > 0       (case not hopeless)
```

So **filings select for high prior-divergence** — the ambiguity frontier — and
as 𝒞 matures and precedent becomes consistent, divergence shrinks and filing
decays. Crucially **only 𝒥 (and the one-off Civ/RR setup) spend LLM calls**; the
priors are read off retrieval. That is what makes the closed loop affordable.

A `StubAgents` mode files *every* transaction — used to de-risk the corpus
machinery in isolation from strategy (the brief's recommended first build).

## 3. The judge 𝒥 (`judge.py`)

`gpt-4o-mini` (configurable; Opus-class in the full run). For each filed case it
retrieves the **top-5 precedents by cosine similarity** on the facts text,
prompts with the thin seed law **Ω₀** + those precedents, and returns strict
JSON `{ruling, damage, rationale}`. Ω₀ is deliberately thin: *S must deliver per
spec*; *deviations within commercial reasonableness are permitted*; *price &
quantity are crisp*. Self-consistency (the predictability metric) resamples the
ruling at temperature and reports modal agreement.

## 4. The corpus 𝒞 and the four arms (`corpus.py`)

`Corpus` is a list of decided cases with cached embeddings and cosine top-k
retrieval. The arms differ **only** in what enters 𝒞:

| Arm | Accretion rule |
|-----|----------------|
| **CL** (common law) | only cases that survived settlement and were **filed** — endogenous to strategy |
| **Civ** (civil law) | one comprehensive code generated at t=0 by Constitutional-AI-style self-critique, then **frozen** |
| **US** (uniform sampling) | every round, with prob *q*, a **random** transaction is submitted to 𝒥 and accreted |
| **RR** (random rule) | at CL's rate, a plausible-but-uncorrelated rule is injected from an LLM rule bank |

*q* is **calibrated per seed to CL's realised filing rate** (CL is run first;
its filing rate sets *q* for US and RR), so the arms accrete at matched volume
and differ only in *what* they select.

**Keeping the DDL engine in the loop.** The overruling / entailment-closure
metric compiles every holding into a defeasible deontic rule
(`sit_<severity>_<clause>_<fm> ⇒O breach` / `⇒O ~breach`) and asks the `deontic`
binary which fact-situations are now **unresolved** — i.e. carry contradictory
holdings with no superiority to break the tie. A jump in unresolved situations
is the formal signature of a fresh case overturning settled law. `stability =
1 − conflicted/situations`.

## 5. Metrics (`run.py`)

- **Welfare** — stake-weighted, on a frozen held-out set. The seller
  re-optimises its deviation against each arm's terminal 𝒞 (anticipated
  liability `P(breach|x′)·d̂·p`); realised welfare = Σ(v − c) − wasteful dispute
  costs. Transfers cancel, so the welfare channel is *deterrence quality*: an
  accurate corpus suppresses value-destroying deviation and pointless filing.
- **Selection bias** — KL(accreted ‖ all) along a 5-bin ambiguity axis
  (Laplace-smoothed).
- **Predictability** — 𝒥's self-consistency on resampled rulings under terminal 𝒞.
- **Corpus growth & closure stability** — |𝒞_t| and the DDL unresolved-conflict
  proxy above.
- **Win-rate trajectory** — P(rule for plaintiff | filed) over windows of t.
- **Accuracy vs oracle** — stake-weighted agreement of 𝒥 (under terminal 𝒞) with
  a UCC-grounded oracle ruling, on a 30 % labelled subset of held-out.

## 6. Predictions under test

1. **Priest–Rubin ~50 %** — CL plaintiff win-rate → ~0.5 as 𝒞 matures; US tracks
   the population breach base-rate instead.
2. **Invocation decay** — CL filing rate falls in *t* after a transient.
3. **Welfare ordering** — CL > US > RR; CL vs Civ ambiguous.
4. **Selection-induced coverage** — CL's 𝒞 concentrates on the ambiguity frontier
   (high KL, high mean accreted ambiguity); US spreads ~uniformly (low KL).

---

## 7. Results

Pilot: **T = 200, 2 seeds × 4 arms = 8 runs**, `gpt-4o-mini` judge, top-5
retrieval, filing cost = 6 % of price. Merged metrics in
`freight/results_summary.json`; full per-round replay in `freight/runs/`.

| arm | seed | \|𝒞\| | filing (early→late) | win-rate (all / late) | KL | **closure** | acc vs oracle | welfare (within-seed rank) |
|----|----|----|----|----|----|----|----|----|
| CL  | 0 | 42 | 0.35 → **0.15** | 0.88 / 0.86 | 0.069 | 0.80 | 0.97 | 456.8k (1st) |
| Civ | 0 | 1  | 0.83 → 0.85     | 0.90 / 0.88 | 0.00  | **1.00** | 0.97 | 436.8k (4th) |
| US  | 0 | 45 | 0.30 → **0.14** | 0.96 / 1.00 | 0.061 | 0.88 | 0.97 | 453.5k (3rd) |
| RR  | 0 | 41 | 0.09 → 0.00     | 0.50 / 0.67 | 0.00  | **0.27** | 0.97 | 456.5k (2nd) |
| CL  | 1 | 66 | 0.46 → **0.20** | 0.88 / 0.82 | 0.035 | 0.91 | **0.77** | 172.6k (4th) |
| Civ | 1 | 1  | 0.89 → 0.91     | 0.90 / 0.91 | 0.00  | **1.00** | 0.74 | 176.0k (3rd) |
| US  | 1 | 72 | 0.58 → **0.17** | 0.95 / 0.97 | 0.013 | 1.00 | 0.75 | 185.0k (2nd) |
| RR  | 1 | 74 | 0.08 → 0.00     | 1.00 / 1.00 | 0.00  | **0.08** | 0.55 | 187.1k (1st) |

Self-consistency was **1.00 in every run** (see below). Welfare is per-seed (the
held-out set differs by seed), so it is ranked within seed, not averaged.

### Verdict on each prediction

**(2) Invocation decay — SUPPORTED.** CL filing falls sharply after a transient:
0.35→0.15 (s0), 0.46→0.20 (s1); the round-window trajectory is
`[0.6, 0.25, 0.2, 0.2, 0.15, 0.15, 0.15, 0.05, 0.25, 0.1]` (s0). US decays too
(its accreted cases also let agents learn); **Civ does not decay at all**
(0.83→0.85) — a frozen code gives agents no *distribution of outcomes* to learn
from, so their priors never converge and they keep litigating. That last point
is itself a finding: in a case-driven world, predictability for agents comes
from observed holdings, not from a statute's existence.

**(1) Priest–Rubin ~50 % — NOT supported (at this scale).** CL plaintiff
win-rate stays high (~0.86 even late). The population breach base-rate is high
(sellers deviate under cost pressure), and T=200 with this filing-cost
calibration does not concentrate filings tightly enough on the 50-50 frontier to
pull the win-rate to 0.5. The *mechanism* is in place (filing decays because
clear cases settle out), but the selection is too weak to surface the 50 % law.
Honest negative — needs the full T=400 and likely a higher filing cost.

**(3) Welfare CL > US > RR — NOT supported / the metric is gameable.** The
within-seed ranking is inconsistent (s0: CL>RR>US>Civ; s1: RR>US>Civ>CL).
Crucially, **RR scores high on welfare precisely because it barely litigates**
(filing → 0): under-enforcement avoids dispute costs. But RR's law is
*incoherent* — see closure below. So raw welfare rewards a regime that simply
fails to enforce; it must be read together with enforcement coherence, not
alone. This is a methodological result about the metric itself.

**(4) Selection on the ambiguity frontier — NOT supported.** CL's KL ≈ US's
(~0.06 s0, and CL only marginally above US in s1). Filing selects on *precedent
unsettledness* `u`, which correlates only weakly with the static structural
ambiguity axis the KL is measured on. Measuring KL on the `u` axis (or running
to scale) is the fix.

**(BONUS) Entailment-closure stability cleanly separates the regimes — the
standout positive, and the one the DDL engine delivers.** Compiling holdings to
defeasible deontic rules and asking the `deontic` binary for unresolved
conflicts yields: **Civ 1.00, US 0.88–1.00, CL 0.80–0.91, RR 0.27 / 0.08.** The
engine sharply flags RR's injected contradictory rules as an incoherent body of
law, and ranks the endogenous common-law corpus as mostly-but-not-perfectly
coherent (real overrulings happen) — exactly the overruling-dataset proxy the
brief asked for. This is what reframes prediction (3): RR's "good" welfare is the
hollow welfare of a law that contradicts itself and so never binds.

### Takeaways

- The corpus-dynamics machinery works end-to-end with a real LLM judge in the
  loop, and the **DDL closure metric is the sharpest instrument** — it is the
  one result that is clean, monotone, and theory-aligned across both seeds.
- **One prediction (decay) replicates; one (Priest–Rubin 50 %) needs scale; two
  (welfare ordering, ambiguity-KL) did not hold as stated** and surfaced two
  genuine refinements: welfare must be coupled to coherence, and selection should
  be measured on the unsettledness axis the agents actually act on.
- **Self-consistency saturated at 1.00** — `gpt-4o-mini` at temperature is too
  decisive on these facts for the predictability metric to bite; it needs a
  harder model gradient or genuinely borderline held-out facts to be informative.

---

## 8. How to reproduce

```bash
export PATH="$HOME/.elan/bin:$PATH" && lake build deontic   # the DDL engine
export OPENAI_API_KEY=...                                   # chat + embeddings

# de-risk the corpus loop alone (stub agents file everything):
python -m freight.run --arms CL --rounds 60 --agents stub --seeds 0

# the pilot (what this report ran), per seed in parallel:
python -m freight.run --arms CL,Civ,US,RR --rounds 200 --seeds 0 \
    --judge-model gpt-4o-mini --heldout 40 --c-f 0.06 --out freight/runs/s0
#   (--c-f is the filing cost as a FRACTION of contract price; stake-scaled)

# the brief's headline scale (costs real money):
python -m freight.run --arms CL,Civ,US,RR --rounds 400 --seeds 0,1,2 \
    --judge-model gpt-4o
```

Each run writes a per-arm JSONL replay log and a `*_summary.json` with every
metric. `freight/runs/` is git-ignored at the repo level; the summary used for
this report is committed under `freight/runs/`.

## 9. Honest limitations

- **Stateless agents.** Agents have no persistent identity; "re-pairing 16
  agents" reduces to fresh seeded draws. Reputation effects are out of scope.
- **Priors are retrieval-grounded, not separately elicited.** This is a faithful
  and cheap proxy for "prior over 𝒥" (𝒞 *is* 𝒥's output), but it bakes in that
  agents read precedent the way 𝒥 does. Eliciting per-agent LLM priors is a flag
  away but multiplies cost.
- **Small N.** 2 seeds × 200 rounds is under-powered for the convergence claims;
  trajectories are indicative, not significant. The clearest casualty is the
  Priest–Rubin 50 % prediction, which plausibly needs the full T=400 and a
  higher filing cost to surface. Scale via flags.
- **Oracle is a simplified UCC stylisation**, not real doctrine — it grounds
  *relative* accuracy across arms, not legal correctness.
