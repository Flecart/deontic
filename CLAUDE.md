# CLAUDE.md

Orientation for an agent starting cold on this repo. Read this, skim
`docs/architecture.md`, then work.

## What this is

A **defeasible deontic logic** reasoner in **Lean 4** (Governatori 2018 proof
theory). It turns normative text — contracts, statutes, clauses — into `.ddl`
theories and computes obligations, permissions, prohibitions, compensatory
remedies, violations, and unresolved conflicts.

**The real target is norms for LLM agent societies, not real legal practice.**
That reframes design calls: *you* are effectively the legislator and own the
vocabulary, so shared/standardized definitions are viable (they fragment in
real law). Keep that lens.

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

Tests are `#guard`/`#eval` in `Deontic/Examples.lean` (no separate framework) —
they run when that module is built. Force a re-check by deleting its build
artifact first: `rm -rf .lake/build/lib/lean/Deontic/Examples.*`.

## How to work here (the spirit, not just the rules)

- **Understand before touching.** The proof conditions in `ProofConditions.lean`
  faithfully implement a published calculus. Read the existing code and match
  its idiom (naming, comment density, `private` helpers) before adding to it.
- **Small, verified increments.** Build after each meaningful change; verify
  behaviour with a real CLI run *and* a `#guard`, not just "it compiles." When
  you claim something works, you've run it.
- **Be a thought-partner on design, not a cowboy.** Several features here were
  shaped by brainstorming first (modularity, provenance, namespacing). For a
  large or architecture-touching change, lay out options and trade-offs and get
  a steer before building. Execute confirmed designs fully; don't silently
  invent big ambiguous ones.
- **Surface the choices, don't bury them.** When a legal clause has more than
  one faithful encoding, pick one and *say so* (in `#` comments in the `.ddl`,
  and to the user). The engine deliberately doesn't guess the law: when rules
  conflict with no superiority it prints `[JUDGE: …]` for a human. Honour that —
  report violations and unresolved conflicts plainly.
- **Concise, maintainable docs.** Keep prose short; reference `examples/`
  instead of inlining; put design-level (not symbol-level) detail in
  `docs/architecture.md` — symbol names rot. Generation prompts emit plain
  `.ddl` (rationale as `#` comments), never JSON.

## Conventions that matter

- **Commits:** Karma / "gitkarma" conventional style (`feat(scope): …`,
  `fix(parser): …`, `test(examples): …`, `docs: …`).  Branch is the current one that the user chooses.
  remote `github.com:Flecart/deontic`. Push when work is done and green.
  **Never commit `guido.pdf`** (untracked source PDF — leave it alone; don't
  `git add -A` without unstaging it).
- **Atom grounding (core philosophy):** atom names are opaque, so every used
  atom needs a description — it's **mandatory** (`loadTheory` refuses
  undescribed atoms). Provenance is structured `{quote?, uri?}` (≥1 set); a
  `uri` is a relative path to an in-repo `.md` source with a GitHub-style line
  selector. The unifying rule for the (in-progress) namespacing:
  **description = an atom's contract, namespace = its identity, a merge is legal
  only when the contracts match** (else error on conflict).

## Layout

`Deontic/` — the library (`Basic` → `Theory` → `Applicability`/`ProofConditions`
→ `Extension`/`Conflict` → `Query`/`Abduce` → `Pretty`; `Parser` is standalone;
`Examples` holds tests). `Main.lean` — the CLI. `examples/` — `.ddl` theories
(`clauses/` = single contract clauses with sources; `deprecated/` = pre-grounding
examples that no longer load). `prompts/` — LLM workflow prompts. `docs/` —
architecture.

There is a persistent memory dir (project goals, design decisions, the user's
preferences) loaded via `MEMORY.md` each session — trust it but verify any
symbol it names still exists.
