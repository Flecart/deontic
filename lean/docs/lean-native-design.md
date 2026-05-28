# Design question: how "Lean-native" should the DDL reimplementation be?

Context brief for a subagent picking up this question cold. Read this top to
bottom; it assumes no prior knowledge of the conversation, only the repo.

## What exists today

- `../../src/ddl/` — the **Python reference**: a Defeasible Deontic Logic
  inference engine (Governatori 2018, `../../guido.pdf`). Computes the extension
  `E(D)` of a theory `D = (F, R^C, R^O, <)` and returns tagged conclusions
  (`±dC/±dO/±dPs/±dPw/±dP/±d⊥`) with justification traces.
- `..` (this `lean/` project) — a **faithful Lean 4 port** of that engine,
  module-for-module (`Ddl/Syntax`, `Proof`, `Engine`, `Parser`, `Render`, `Api`,
  `JsonIo`; `Main.lean` is the CLI; `Tests.lean` is the suite). Verified:
  - the computed extension is **byte-identical** to Python on all 7 example
    theories (337 conclusions each), and the CLI output matches the Python CLI;
  - `lake test` passes 44/44 checks (every Python test reproduced).
- The engine fixpoint is implemented with **`partial def`** (mirrors the Python
  `while` loops). It executes correctly but **cannot be reasoned about in Lean**
  — `partial def` produces no equational lemmas. This is the single most
  important fact for any verification work below.
- The project is **Mathlib-free**; it depends only on Lean core (+ `Lean.Data.Json`
  in `JsonIo`). Toolchain: Lean 4.30.0 (note: 4.30 moved `String.trim/take/drop`
  to return `String.Slice`; `Parser.lean` keeps `String`-valued helpers
  `trim/stake/sdrop/sfront` to cope).

## The question

The user asked: instead of the custom `.ddl` language (+ a runtime parser),
would it be better to have "everything in Lean"? The phrase is ambiguous and
splits into independent decisions. Do not collapse them.

### Key reframe
The parser/JSON reader serve **one boundary**: ingesting a theory produced
*elsewhere at runtime* (the design notes say: by an LLM that formalises NL norms;
see `../../docs/design-notes.md` and `../../README.md`). If that boundary is
real, a runtime parser is required regardless — you can't compile LLM-emitted
Lean source per request (arbitrary code execution, slow, unsafe). So "everything
in Lean" pays off in a *different layer* than the parser. The real fork is:
**(a) for whom are theories authored?** and **(b) do you want machine-checked
guarantees?**

## Three largely-independent moves

### Move 1 — `ddl%` macro / theories as Lean terms (ergonomics; small effort)
Use Lean's `syntax`/`macro`/`elab` to embed the surface syntax so in-repo
theories are parsed by Lean's own parser at compile time:
```lean
def license := ddl% { r0: =>O -use ; r1: license ~>O use ; r0 < r1 }
```
- Wins: compile-time validation (undefined superiority label ⇒ elaboration
  error, not runtime), editor hover/jump, no runtime parse failures for static
  theories.
- Costs: macro authoring; macro error messages can be cryptic; theories become
  Lean-version-locked (non-Lean tools can't read them).
- Does **not** replace the runtime parser; complements it for human/test-authored
  theories.

### Move 2 — Decidability + per-theory machine-checked verdicts (scoped; high value)
The Herbrand base is finite, so each `±d□q` is decidable. Add `Decidable`
instances (or just expose the boolean `Extension.has` and a wrapper) so concrete
verdicts can be *proved*, not merely tested:
```lean
example : license ⊢ F use := by native_decide
```
- This is the cheapest thing that makes the Lean version *better than* the Python
  one (Python can only test). No Mathlib needed.
- `native_decide` compiles and runs; `decide` would need the fixpoint to reduce
  in the kernel (the `partial def` blocks that — see Move 3).

### Move 3 — Verified engine + metatheory (large; the real prize)
Define the declarative proof conditions as Lean predicates and prove:
- **Proposition 1** (coherence: never both `+d□q` and `−d□q`; consistency;
  operator interactions) for *all* theories — currently only spot-checked on 6.
- **Soundness & completeness**: `extension D` agrees with the declarative spec,
  so the justification trace becomes a *certificate* (proof-carrying verdicts —
  the strongest version of "a reasoner an LLM can trust").

Hard parts a subagent must plan for:
1. **`partial def` is unprovable.** A verified engine needs a *total*
   reformulation of the fixpoint: either fuel-indexed with a proven-sufficient
   bound (the base is finite and the operator is monotone, so a bound exists), or
   a Knaster–Tarski least fixpoint via `OrderHom.lfp`. This is effectively a
   second implementation kept in sync with the executable one (or: make the total
   one canonical and derive execution from it).
2. **Mathlib.** `lfp`, fixpoint induction, order theory, and ergonomic
   `Decidable`/`Finset` machinery realistically mean adding a Mathlib dependency
   — a build-time and dependency cost the project currently avoids. Weigh
   explicitly.
3. **`−∂` is not a clean monotone inductive.** Constructive refutation plus
   team-defeat are handled in the paper via the *Principle of Strong Negation*
   (`−∂` is the strong negation of `+∂`). A naive `inductive` captures `+∂` but
   not `−∂`. Expect to define both mutually over a stratified / fixpoint
   semantics. There is published metatheory for defeasible logic to lean on, but
   this is a research-grade subproject, not an afternoon.
4. **Suggested ordering:** prove Proposition 1 on the *total* fixpoint first
   (a preserved invariant + fixpoint induction) before attempting full
   soundness/completeness against the declarative relation.

## Product constraint (do not regress)
The stated purpose (README + design-notes): LLM *formalises* NL norms → engine
*reasons deterministically + traceably* → LLM *interprets*. The JSON form is the
intended machine contract; the DSL is for humans/tests. Any redesign that drops
runtime ingestion breaks the intended integration. Keep at least one runtime
front-end (JSON and/or DSL).

## Current recommendation (subject to user intent)
Keep the runtime parser. Do **Move 1 + Move 2** now (small, no Mathlib, makes the
Lean port strictly better than Python). Treat **Move 3** as a separate, scoped
effort starting from Proposition 1 on a total fixpoint. The open question to
confirm with the user before Move 3: *is the goal machine-checked correctness
(then Move 3 is the point and Mathlib is justified), or just nicer authoring
(then Moves 1–2 suffice and Mathlib is avoidable)?*
```text
authoring ergonomics only ........→ Moves 1–2, no Mathlib
+ per-theory checked verdicts ....→ Move 2 (native_decide)
+ universal guarantees / certs ...→ Move 3 (total fixpoint + Mathlib)
must ingest external/LLM theories → keep the runtime parser in all cases
```
