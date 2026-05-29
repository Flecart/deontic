# deontic

A **defeasible deontic logic** reasoner for normative rules: obligations, permissions, compensatory remedies, superiority between rules, and violations.

We are building this as a **formal reasoning layer for legal AI**: large language models are strong at language and retrieval, but weak at consistent deontic consequence. This tool gives LLM-assisted legal workflows a small, auditable kernel—rules in `.ddl`, answers as tagged derivations (`+∂_O`, `+∂_⊥`, and explicit **judge** prompts when conflicts are unresolved).

The calculus follows Governatori (2018), *Defeasible Deontic Logic: An Argumentation-based Approach*. See [docs/architecture.md](docs/architecture.md) for how the pieces fit together.

## Quick start

Requires [Lean 4](https://lean-lang.org/) (see `lean-toolchain`).

```bash
lake build deontic

# Full extension for a theory
./.lake/build/bin/deontic check examples/ex1_license.ddl

# Status of specific atoms
./.lake/build/bin/deontic query examples/ex1_license.ddl publish use comment

# Which fact configurations ALLOW disclosure? (abduction / "what-if")
./.lake/build/bin/deontic abduce examples/clauses/disclosure_awareness.ddl 'P(Disclose)' --all

# What does each atom mean? (descriptions + provenance, for humans/LLMs)
./.lake/build/bin/deontic atoms examples/clauses/disclosure_awareness.ddl

# Machine-readable output for pipelines
./.lake/build/bin/deontic query examples/ex1_license.ddl publish --json
```

## What it does

| Capability | Example |
|------------|---------|
| Defeasible obligations & permissions | `commission =>O publish` vs default `=>O ~publish` |
| Compensatory chains | `=>O ~publish * remove` (remedy after breach) |
| Defeaters | `license ~>O use` |
| Superiority | `r4 > r2` — which rule wins when both apply |
| Violations | Obligation derived but fact situation does not comply (`+∂_⊥`) |
| Unresolved conflicts | Neither `O(a)` nor `O(~a)` provable; `[…]` asks for `≺` |
| Abduction ("what-if") | Which **fact configurations** make a goal hold — `abduce 'P(Disclose)'` |

## Abduction: which facts make a goal hold?

`check`/`query` run *forward* (facts → status). `abduce` runs *backward*: given a
**goal** it searches for the fact configurations that entail it.

```bash
# All minimal fact sets under which Disclose becomes permitted
deontic abduce examples/clauses/disclosure_awareness.ddl 'P(Disclose)' --all
#  → { EmployeeRecipient, AwareOfTerms, AwareOfLiability }

# Configurations that REQUIRE use, pinning/narrowing with assumptions
deontic abduce examples/ex1_license.ddl 'O(use)'

# Conjunctive / negative conditions: Disclose allowed while a condition stays absent
deontic abduce examples/clauses/disclosure_awareness.ddl 'P(Disclose)' --assume -AwareOfLiability
```

- **Goal tokens** (prefix `!` = must *not* hold): `O(a)`, `F(a)`, `P(a)`, `Ps(a)`,
  `Pw(a)`, `C(a)`, or a bare `a` / `~a`. "Allow" ≈ `P(...)`, "require" ≈ `O(...)`.
- **`--all`** lists every subset-minimal configuration; default shows the first few.
- **`--assume a,~b,-c`** pins facts (`a` true, `b` false, `c` must stay absent),
  both narrowing the search and shrinking it.
- Search space is the **abducible** atoms (those appearing in rule antecedents),
  so it stays small; `--json` emits the minimal configs for pipelines.

## Atom descriptions & provenance

Atom names (`Disclose`, `EmployeeRecipient`) are opaque on their own. Declare
what each means so a fact-finder — human or LLM — knows what asserting it
commits to, and where it came from:

```ddl
atom Disclose: disclose Confidential Information to any other person | quote: ...prior to the disclosure to any other person... | uri: examples/clauses/sources/nda_confidentiality.md#L3-L6
```

Descriptions are **mandatory** — `check`/`query`/`abduce` refuse to load a
theory with an undescribed atom. After `|` is optional **provenance**: a
`quote:` snapshot and/or a `uri:` pointing to an in-repo markdown source with a
GitHub-style line selector (`#L3-L6`); at least one must be present. `deontic
atoms <file>` prints the dictionary (`--json` for tools; `--resolve` inlines the
lines the uri points at).

## Imports & namespacing

Reuse a shared module (e.g. a definitions library) across theories:

```ddl
import definitions.ddl as roles   # imported atoms/labels become roles.*
from definitions.ddl import *      # or merge into this namespace
```

Paths are relative to the importing file. Merging is **description-guarded**:
two declarations of the same atom must agree on their description, or the load
fails — the same name must mean the same thing. Rule-label collisions and import
cycles are errors too. (Selective `from … import a, b` isn't implemented yet.)

## Examples

| Path | Scenario |
|------|----------|
| `examples/ex1_license.ddl` | License contract (Governatori §4): commission, use, publish |
| `examples/clauses/` | Single contract clauses, exercised via the `abduce` reverse search |
| `examples/imports/` | Reusing a shared definitions module (`import` / `from … import *`) |
| `examples/deprecated/` | Pre-description examples kept for reference (won't load) |

## Vision: legal LLMs with formal grounding

Typical legal LLM stacks retrieve text and generate prose. They rarely expose:

- which rule instances fired,
- whether an obligation or permission actually follows,
- or when two rules conflict and **no** priority is stated in the theory.

**deontic** is meant to sit in the loop:

1. **Extract or draft** a theory (facts + rules + superiority) from a contract, statute, or case—human- or LLM-assisted.
2. **Run** `check` / `query` on a fact pattern.
3. **Consume** JSON: normative status per atom, violation flags, judge prompts for missing `>`.
4. **Iterate**: refine `.ddl`, add superiority, or adjust facts until the formal extension matches the intended legal analysis.

The reasoner is deliberately not a black box: output is proof-theoretic tags, not a single yes/no from an opaque model. That supports audit, teaching, and hybrid systems where the LLM explains *in language* what the kernel already proved or flagged.

## Documentation

- [Architecture](docs/architecture.md) — modules, fixed-point engine, violations vs judge conflicts, JSON API
- [LLM prompts](prompts/README.md) — fact extraction from evidence; encoding law as `.ddl`

## License

See repository license file when present.
