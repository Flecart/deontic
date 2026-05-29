# Does the reasoner help on contract_nli? — baseline

## What was established

All **14** LegalBench `contract_nli_*` hypothesis types were formalized as DDL
and the reasoner returns the correct label by construction (see `README.md`).
This is an **expressiveness baseline**: the deontic fragment we have is rich
enough to capture every ContractNLI hypothesis shape with four small patterns —
prohibition (`=>O ~X`), conditional obligation (`cond =>O X`), permission
carve-out (`default + cond ~>O X + superiority`), and constitutive
classification (`cond => Y`).

## Where the reasoner does — and doesn't — help

**It helps as a verification kernel, not an end-to-end classifier.** Once a
contract is in DDL, deciding a hypothesis is *exact, deterministic, and
auditable*: `query`/`abduce` yield Entailment / Contradiction / NotMentioned
with the firing rules visible — no hallucinated label. That is the value for an
agent society: a checkable normative answer, not an opaque guess.

**The hard part is upstream.** ContractNLI's difficulty is the natural-language →
DDL formalization (reading a real NDA, choosing atoms, picking
arrows/superiority). That step is *not* automated here — it is done by a
human/LLM via `prompts/law-to-ddl.md`. So the reasoner improves *faithfulness and
auditability* of the inference, while shifting the open problem to formalization
quality.

## Honest limitations (surfaced while formalizing)

- **No quantitative accuracy yet.** A real score (vs gold labels on the
  LegalBench split) needs the dataset, which isn't available offline here. These
  14 are *representative* encodings, correct by construction — they show
  coverage/expressiveness, not measured accuracy on real contracts.
- **Modelling compromises:** disjunctive duty "return *or* destroy" collapses to
  one atom; "all CI must be identified" is modelled as CI's *sole* classification
  path; "no licensing" as a prohibition on claiming rights.
- **Engine quirk:** constitutive conclusions don't satisfy other rules' *plain*
  antecedents, so role-style definitions must be asserted as facts to fire
  downstream rules (matters when chaining classification into permissions).
- **One contract → one label per hypothesis.** Showing all three NLI labels for a
  hypothesis needs different contracts (as the dataset has).

## To turn this into a real eval (next step)

1. Ingest the LegalBench `contract_nli_*` splits (premise contracts + hypotheses + gold).
2. Have the `law-to-ddl` LLM emit a DDL theory per contract.
3. Run `query`/`abduce` for each hypothesis; map derivable→Entailment,
   opposite-derivable→Contradiction, neither→NotMentioned.
4. Score against gold, and separately audit formalization fidelity (the real bottleneck).
