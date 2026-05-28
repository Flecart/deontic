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

## Examples

| File | Scenario |
|------|----------|
| `examples/ex1_license.ddl` | License contract (Governatori §4): commission, use, publish |
| `examples/ex1b_noremoval.ddl` | Publish without removal — non-compensable violation |
| `examples/ex3_tcpc.ddl` | TCPC 2012 complaint classification |

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
