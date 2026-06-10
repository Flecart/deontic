# Skill: the `deontic` reasoner (CLI)

`deontic` is a defeasible deontic logic reasoner. You write a small **DDL
theory** (a `.ddl` file) formalizing the relevant clause/rule, then run the CLI
to decide obligations, prohibitions, and permissions. Use a shell to create the
file and run commands; iterate for a few rounds, then answer.

## Commands

```
deontic check  <file.ddl>                      # per-atom per-bearer summary
deontic query  <file.ddl> <atom> ...           # normative status by bearer
deontic query  <file.ddl> X --bearer Customer  # one party only
deontic abduce <file.ddl> '<goal>' --all       # fact configs that make the goal hold
deontic atoms  <file.ddl>                      # list atoms + descriptions
```

Typical workflow:
```bash
cat > /tmp/t.ddl <<'EOF'
atom Disclose: discloses confidential information to a third party
atom Employee: the recipient is an employee of the receiving party
no_disc:  =>O ~Disclose
perm:     Employee ~>O Disclose
superiority: perm > no_disc
EOF
deontic query  /tmp/t.ddl Disclose          # -> F(Disclose)  (forbidden by default)
deontic abduce /tmp/t.ddl 'P(Disclose)' --all  # -> { Employee }  (permitted iff Employee)
```

## DDL syntax

- `# ...` comment; `facts: a, b` ground facts.
- `atom NAME: description` — **mandatory** for every atom used.
- `label: ant1, ant2 =>O conc` — defeasible obligation (prescriptive).
- `label: =>O ~x` — prohibition `O(~x)` (empty antecedent = unconditional default).
- `label: cond ~>O x` — defeater that *permits* x (pair with `superiority`).
- `label: cond => y` — defeasible constitutive rule (classification).
- `superiority: rA > rB` — rA defeats rB when both apply.

## Writing atom descriptions

The description is the atom's **entire test** — it is what a fact-finder
(human or LLM) uses to decide whether the atom holds, possibly seeing nothing
else at all. Make it self-contained:

- **No references.** Never point at a statute section, article, case name, or
  any other document ("the s40(3A) first condition", "the Art 6(1)(f) test",
  "(Three Rivers)") — the reader has none of those in front of them. Say
  verbatim what the test is; inline the content the reference stands for.
- State **when the atom is TRUE and when it is FALSE**, including the easy
  confusions to exclude (e.g. "accessibility of a DIFFERENT document does not
  count").
- Another atom may be mentioned BY NAME to mark a boundary ("ordinary
  commercial sensitivity belongs to PrejudiceCommercialInterests"), but this
  atom's own test must never require reading that one — descriptions are also
  consumed one atom at a time.

## Reading output

`query X` prints per-bearer status when several parties have rules on `X`
(`Customer: F(X)` / `Vendor: F(X)`), or a single line when only one party does.
Values: `O(X)` obligated · `F(X)` forbidden · `Ps(X)`/`P(X)` permitted ·
`fact(X)` constitutively holds · `unknown` not addressed.
`abduce 'P(X)' --all` — aggregate permission; `abduce 'P@Customer(X)' --all` —
directed to Customer only.

## The four patterns

| To model | Write | Decide with |
|----------|-------|-------------|
| prohibition ("shall not X") | `=>O ~X` | `query X` → `F(X)` |
| conditional duty ("if C, must X") | `C =>O X` + `facts: C` | `query X` → `O(X)` |
| permission ("may X if C") | `=>O ~X` + `C ~>O X` + `superiority` | `abduce 'P(X)' --all` → `{C}` |
| classification ("C counts as Y") | `C => Y` | `abduce 'C(Y)' --all` → `{C}` |

Worked theories: `examples/legalbench/` (one folder per task family).
