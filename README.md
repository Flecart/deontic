# ddl — Defeasible Deontic Logic inference engine

A reference implementation of the logic in Governatori (2018), *"Practical
Normative Reasoning with Defeasible Deontic Logic"* (`guido.pdf`). It reasons
about **norms** — obligations, prohibitions, permissions, contrary-to-duty
compensation chains — with a **constructive, fully traceable** proof theory:
every verdict comes with a justification.

The intent is to be the deterministic reasoner an LLM can lean on: the model
*formalises* natural-language norms into a theory and *interprets* results; the
engine does the multi-step defeasible reasoning the model is unreliable at
(which rule defeats which, propagating violations through compensation chains,
weak vs. strong permission). See [`docs/design-notes.md`](docs/design-notes.md).

## Install

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .            # or: pip install -e ".[dev]" for tests
```

## Concepts (the formal model)

A theory is `D = (F, R^C, R^O, <)`:

- **Facts `F`** — plain literals taken as given.
- **Constitutive rules `R^C`** (`=>C`, "counts-as") — derive institutional facts.
- **Prescriptive rules `R^O`** (`=>O`) — derive obligations; their head is an
  ⊗-chain `a₁ ⊗ … ⊗ aₙ` where `O a₁` is primary and later elements are
  contrary-to-duty compensations.
- **Superiority `<`** — `r < s` means **s overrides r**.

Rules are **defeasible** (`=>`) or **defeaters** (`~>`, block-only). Conclusions
are tagged literals: `+dC`/`-dC` (constitutive), `+dO` (obligation; `F l` is
`+dO -l`), `+dP`/`+dPs`/`+dPw` (generic/strong/weak permission), and `+d⊥`
(a non-compensable violation — the situation is non-compliant).

## The `.ddl` surface syntax

```
license. publish. remove. comment.      # facts (one or many, '.'-separated)

r0:  =>O -use                # obligation rule (=>O); F use
r1:  license ~>O use         # defeater (~>); a licence permits use
r2:  =>O -publish (x) remove # ⊗-chain: F publish, compensated by remove
r3e: P publish ~>O comment   # modal body literal: "P publish"
c31: highSpend => premium    # constitutive rule (=> defaults to =>C)

r0 < r1                      # superiority: r1 overrides r0
```

Modes attach to the arrow (`=>O`, `=>C`, `~>O`); bare `=>`/`~>` are
constitutive. `(x)` is ⊗. `bottom` is the non-compliance literal `⊥`.

## CLI

```bash
ddl run    examples/license.ddl --facts "license. publish. remove. comment."
ddl query  examples/license.ddl "F use" --facts "license. publish. remove. comment."
ddl query  examples/uturn.ddl   "Ps Uturn" --facts "AtTrafficLights. UturnPermittedSign."
ddl render examples/complaint.ddl          # the theory back in plain English
```

Queries accept the tag form (`+dO remove`, `-dC publish`), the friendly form
(`O remove`, `F publish`, `P use`, `Ps use`), `noncompliant`, or a bare literal
(`publish` = `+dC publish`). `ddl run --all` shows every conclusion.

## Library / LLM use

```python
from ddl import Reasoner, parse, lit

# DSL or the structured (LLM-facing) JSON form both compile to the same engine.
r = Reasoner.from_ddl(open("examples/license.ddl").read()).with_facts(
    {lit("license"), lit("publish"), lit("remove"), lit("comment")}
)
v = r.query("F use")
print(v.holds)      # True
print(v)            # verdict + natural-language proof trace
print(r.report())   # all active normative effects
```

The JSON theory format (self-documenting, schema-validated, with `gloss`
fields) is in [`ddl/json_io.py`](src/ddl/json_io.py); see
[`examples/license.json`](examples/license.json).

## Tests

```bash
pytest        # reproduces the paper's worked examples as acceptance criteria
```

Coverage: basic defeasible logic, the licence (Ex. 1/§4), premium customer
(Ex. 2), TCPC complaint (Ex. 3/4), U-turn (Ex. 5), ⊗ compensation chains, and
the Proposition 1 coherence/consistency invariants.

## Status & scope

v1 is the core engine + library + CLI, with facts treated as trusted inputs.
Evidence/provenance verification, a Ricardian-contract wrapper, an appeal/diff
flow, and the temporal dimension of norms are deliberately deferred — see
[`docs/design-notes.md`](docs/design-notes.md).
