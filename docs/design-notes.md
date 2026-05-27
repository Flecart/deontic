# Design notes

Context and deferred decisions from the design conversation, so future work can
resume without re-deriving everything.

## Why this exists

A trustworthy, deterministic, **fully traceable** reasoner over norms, so an LLM
does the part it is good at and the engine does the part LLMs are unreliable at.

| Step | Owner |
|---|---|
| Formalise: natural-language norm → formal rule | LLM (high-risk: misformalisation) |
| **Reason: theory + facts → verdicts** | **this engine — deterministic, traceable** |
| Interpret: verdict + trace → explanation | LLM |

The LLM is **not** meant to reason over the `.ddl` text. It emits a theory
(structured JSON is the intended contract; the terse DSL is for humans/tests),
the engine computes the extension, and the verdict + proof trace come back for
the LLM to verbalise. Every rule can carry a `gloss` (its NL source) and the
engine can render a theory back to English (`ddl render`) for an **audit
round-trip**: *"did I formalise this faithfully?"*

## Resolved subtleties (now in code)

- **Superiority direction.** `r < s` means **s is superior** (s defeats r). The
  paper's p.10 prose reads the other way, but every worked example needs this
  reading; pinned by the example tests.
- **Violation.** Advancing an ⊗-chain / triggering `+d⊥` uses
  `violated(c) ⇔ ~c ∈ F` (the opposite was brought about), not the literal
  `c ∉ F` of the paper, which would mark un-actioned prohibitions as violated.
  See `engine.py` header.
- **`r4`/`r4x`** label collision in the §4 listing read as `r4` (publish) /
  `r4x` (use).

## Deferred features (NOT built in v1 — engine-first by decision)

The decision was to make the core engine strong and stable first, treating facts
as trusted inputs. These layers were discussed and intentionally postponed:

### 1. Grounding facts (the oracle problem)
Where does a fact like `published_without_approval` come from — observation,
another agent's assertion, or a proof? Proposed layering:

```
Evidence/Verifier layer   signatures / ZK / observation → admitted brute facts (+provenance)   [crypto lives here, pluggable]
        │
Counts-as layer           constitutive rules: brute fact ⇒C institutional fact                  [in-logic, auditable]
        │
DDL engine                prescriptive rules + superiority → tagged verdicts + trace            [done, this repo]
        │
Ricardian wrapper         content hash binds prose ↔ theory; parties sign the hash              [identity / non-repudiation]
```

- **Verifier layer (outside the logic, pluggable).** Each candidate fact carries
  `{atom, source, evidence}`; a `Verifier` decides admission. The only place
  crypto/observation lives. Verdict traces can then cite provenance.
- **Counts-as bridge (inside the logic).** Evidence verification is just a
  boolean outside; *what the evidence legally means* is a transparent
  constitutive rule (`verified_removal_log ⇒C removed_within_24h`). Reuses the
  engine's existing constitutive rules — already supported.

### 2. Ricardian contract wrapper
Adopt the *idea* now-ish, defer the *crypto*. A `Contract` object would wrap a
`Theory` with: canonical serialisation, a content hash, attached prose, version
identity, and signature *slots*. Value: parties (or two negotiating agents)
converge on a theory and sign its hash → they may later dispute **facts**, not
**terms** (non-repudiation). Cheap/high-value part = canonical hash + prose
binding; expensive/deferred = PKI/signing/ZK.

### 3. Appeal / fact-revision flow
An appeal = admit new (verified) facts and re-run. Because DDL is non-monotonic,
a verdict can legitimately flip (e.g. admitting `approval` flips `F publish` →
`P publish`). A first-class flow would surface a **trace diff**. Today
`Reasoner.with_facts(...)` supports the re-run; the diff/UX is deferred.

### 4. ZK caveat
ZK proves "I hold a valid signature" / range facts, not real-world events. For
normative facts it bottoms out in a *trusted attestor* and mainly adds *privacy*
over a signed attestation. The Verifier interface should fit "signed
attestation" first; ZK is a privacy-preserving variant.

### Also out of scope in v1
- Temporal dimension of norms (the paper lists this as future work).
- Strict rules (the paper's §3.3 formalisation drops them; we follow suit).
- Two-LLM negotiation scaffolding (depends on a solid core, now in place).

## Algorithm note / known limitation
The extension is computed by a monotone fixpoint + a constitutive
well-foundedness closure + a safety net (see `engine.py`). It yields the
standard ambiguity-blocking extension and is **polynomial**, not the linear
bound of Maher (2001) / Prop. 2. Deontic positive cycles (rare; the paper's
examples are stratified) rely on the safety net rather than a dedicated
obligation-support closure — worth revisiting if such theories arise.
