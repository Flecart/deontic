# CLAUDE.md

Cold-start orientation. This file is the **map**: read it, then jump straight to
the file you need (tables below) — don't sweep the repo. Skim
`docs/architecture.md` for design depth.

## What this is

A **defeasible deontic logic** reasoner in **Lean 4** (Governatori 2018 proof
theory). It turns normative text — contracts, statutes, clauses — into `.ddl`
theories and computes obligations, permissions, prohibitions, compensatory
remedies, violations, and unresolved conflicts.

**The real target is norms for LLM agent societies, not real legal practice.**
That reframes design calls: *you* are effectively the legislator and own the
vocabulary, so shared/standardized definitions are viable (they fragment in real
law). Keep that lens.

## Build & run

`lake` is **not on PATH** — prefix it: `export PATH="$HOME/.elan/bin:$PATH"`.

```bash
lake build deontic                 # build the CLI
lake build Deontic.Examples        # elaborates the #guard tests + #eval demos
./.lake/build/bin/deontic check  <file.ddl> [--json|--assume t,...]
./.lake/build/bin/deontic query  <file.ddl> <atom>... [--trace|--json|--assume t,...]
./.lake/build/bin/deontic abduce <file.ddl> <goal>... [--all|--assume t,...|--json]
./.lake/build/bin/deontic atoms  <file.ddl> [--json|--resolve]
```

Tests: `#guard`/`#eval` in `Deontic/Examples.lean` (no framework) — run when that
module builds; force a re-check with `rm -rf .lake/build/lib/lean/Deontic/Examples.*`.

## Where to look (jump here, don't grep)

| To understand / change… | Read |
|---|---|
| The proof calculus (`canDerive_*` per modality) | `Deontic/ProofConditions.lean` |
| When a rule body is satisfied (applicability) | `Deontic/Applicability.lean` |
| The per-bearer fixed-point loop | `Deontic/Extension.lean` |
| `.ddl` grammar + **sugar** (`oneof`, `{…}` blocks, `overrides`) | `Deontic/Parser.lean`; design in `docs/architecture.md` §Parser |
| Directed obligations `@Bearer` (scoping, conflicts) | `docs/architecture.md` §Hohfeldian bearers; `Theory.scopedForBearer` |
| `[JUDGE]` unresolved conflicts vs `+∂_⊥` violations | `Deontic/Conflict.lean`; `docs/architecture.md` |
| CLI commands, JSON shape | `Main.lean`; `docs/architecture.md` §CLI |
| Worked theory + the methodology | `examples/codice_penale/` (`README.md`, `PRINCIPLES.md`, `coverage.md`) |
| LLM workflows (text→`.ddl`, fact extraction) | `prompts/` |
| How to evaluate "tool vs LLM-only" | `docs/evaluation.md` |

**Flagship example — `examples/codice_penale/`**: the Italian penal code as DDL.
~395 offence articles are element-decomposed (precetto @Chiunque / sanzione
@Giudice / pena; scriminanti + imputabilità in `parte_generale.ddl`, shared
vocabulary in `definizioni.ddl`); Libro I is grounded as described atoms. Authored
via the **spec-driven generator** `tools/gen.py` + `tools/specs.txt` (NOT the
rejected coarse generator — decomposition is hand-written; the script fills
provenance + scaffolding). Run `bash examples/codice_penale/tests.sh` (uses
`check`, the enforcing load — `atoms` is non-enforcing and hides missing descriptions).

**Two engine gotchas that bite when authoring `.ddl`** (verified, easy to miss):
plain (non-deontic) body literals must be **facts** — a constitutive `=>`
conclusion does *not* chain into another rule's body; route intermediates through
a deontic `O(…)` literal. And the fixed point is a **frozen-snapshot (Jacobi)**
pass, so a rule meant to defeat another must depend on conditions available no
later than its target (this is why `overrides` gates on plain facts).

## How to work here (the spirit, not just the rules)

- **Understand before touching.** Read the existing code and match its idiom
  (naming, comment density, `private` helpers) before adding. `ProofConditions`
  faithfully implements a published calculus — don't rewrite it for new features;
  the sugar and bearers are deliberately *parse-time / scoping* layers around it.
- **Small, verified increments.** Build after each meaningful change; verify with
  a real CLI run *and* a `#guard`/`tests.sh`, not just "it compiles." When you
  claim something works, you've run it.
- **Be a thought-partner, not a cowboy.** Several features (modularity,
  provenance, bearers, the three sugars) were shaped by brainstorming first. For
  a large/architecture-touching change, lay out options and get a steer; then
  execute the confirmed design fully.
- **Surface the choices, don't bury them.** When a clause has more than one
  faithful encoding, pick one and *say so* (`#` comments in the `.ddl`, and to
  the user). The engine deliberately doesn't guess the law: unresolved conflicts
  print `[JUDGE: …]`. Report violations and deadlocks plainly.

## Conventions that matter

- **Docs are the cold-start budget.** Keep this file and `docs/architecture.md`
  high-signal so an agent starting from empty context can act without sweeping
  the repo: state *where* things live, not every symbol (names rot). Prefer a
  pointer to `examples/`/a file over inlining; cut prose that re-derives what the
  code or a one-line pointer already says. Update these maps when layout changes.
- **Commits:** Karma / "gitkarma" conventional style (`feat(scope): …`,
  `fix(parser): …`, `test(examples): …`, `docs: …`). Branch is the user's
  choice; remote `github.com:Flecart/deontic`. Push when work is done and green.
  **Never commit `guido.pdf`** (untracked source PDF — don't `git add -A` without
  unstaging it).
- **Atom grounding (core philosophy):** atom names are opaque, so every used atom
  needs a description — **mandatory** (`loadTheory` refuses undescribed atoms).
  Provenance is `{quote?, uri?}` (≥1 set); a `uri` is a relative path to an
  in-repo `.md` with a GitHub-style line selector. The unifying rule (also for
  imports/namespacing): **description = an atom's contract, namespace = its
  identity, a merge is legal only when contracts match** (else error).

## Layout

`Deontic/` — the library (`Basic` → `Theory` → `Applicability`/`ProofConditions`
→ `Extension`/`Conflict` → `Query`/`Abduce` → `Pretty`; `Parser` standalone;
`Examples` holds tests). `Main.lean` — the CLI. `examples/` — `.ddl` theories
(`codice_penale/` = the big one; `clauses/` = single contract clauses with
sources; `imports/` = shared-module reuse; `deprecated/` = pre-grounding, won't
load). `prompts/` — LLM workflow prompts. `docs/architecture.md` — design depth.

A persistent memory dir (project goals, design decisions, user preferences) loads
via `MEMORY.md` each session — trust it but verify any symbol it names still exists.
