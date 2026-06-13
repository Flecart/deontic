# Why these domains? (statute-selection rationale)

The statutes are not an arbitrary convenience sample. They are chosen on three
crossed axes, so that the generalization result is shown *not* to depend on any
one domain, texture profile, or structural size.

## Axis 1 — the constitutive institutions of an agent economy

A society of autonomous agents that transact needs a small, well-known set of
institutions; political economy and contract theory name roughly these. We
take one statute per institution, so the suite spans *what an agent society
actually has to govern*, not random legal trivia:

| institution | governs | statute |
|---|---|---|
| **Information** | who may disclose what about whom | A — inter-agent data transfer |
| **Resources** | who may draw on the shared commons | B — compute-pool commons (GovSim) |
| **Authority** | who may act on whose behalf | D — agency & delegation |
| **Exchange** | what counts as good performance of a deal | E — sale of goods |
| **Safety** | what an agent may do at all | F — permissible-action / irreversible-action |

C (Hart's "no vehicles in the park") is the canonical illustration and the
difficulty floor, not an institution. This mapping is the headline
justification: these are the five coordination problems an agent economy must
solve, and a normative layer for such a society must handle all of them.

## Axis 2 — the predicate-texture spectrum (the RQ3 control)

The open-vs-closed gap is predicted to scale with how *artifact-like* a
domain's predicates are. To show the effect is a property of texture and not
of one domain, the statutes are chosen to span the spectrum, with the texture
profile **pre-registered per statute** before any run:

| statute | dominant predicate type | predicted Tier-2 gap |
|---|---|---|
| E (sale of goods) | artifact (quality/conformity standards) | **large** |
| A (data transfer) | mixed artifact + scenario | medium–large |
| B (commons) | mixed, some system-state | medium |
| D (agency) | scenario + epistemic-bar | small |
| F (safety) | epistemic-bar (unverifiable guarantees) | small open recall, large closed collapse |

This is a genuine prediction, not a post-hoc reading: D's small gap and E's
large gap were both called in advance (D scored 5/7 on its per-atom profile).
The domains are picked to put points at both ends and the middle.

## Axis 3 — structural size / depth (the size-axis control)

Holding texture aside, the verdict-layer cost of the engine is predicted to
depend on how much *structure* the deduction must resolve. The statutes span
an order of magnitude in rule count:

  C (3) < A (8) ≈ B (8) < E (~10) < D (12) < F (~16)

with A and B sharing one skeleton by construction (the texture-vs-structure
isolation). This lets the paper separate "does texture matter" (axis 2) from
"does the engine earn its keep more as structure deepens" (axis 3, the
size-axis result).

## What this buys the paper

Aggregate results are reported across the suite (the headline), with the
domain/texture/size axes as the *designed* sources of variation rather than
noise. Any single-statute number is then either (a) a point on one of these
axes, or (b) flagged as exploratory. The selection rationale is what lets the
aggregate claim — "open generalizes, closed and programs do not" — be read as
a property of legal texture in general, established across the institutions an
agent society must run, the full texture spectrum, and an order of magnitude
of structural depth.
