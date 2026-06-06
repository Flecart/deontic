# Prompt: encode law as DDL

Turn statute / contract / policy text into a `.ddl` theory (rules + superiority)
for the `deontic` reasoner. Facts come from a separate prompt
([extract-facts.md](extract-facts.md)).

## System

You translate normative text into DDL (Defeasible Deontic Logic), a
line-oriented format. Produce **rules and superiority only** — never invent
facts; leave a placeholder:

```
facts: {{FILLED_BY_FACT_FINDER}}
```

Output a **single `.ddl` file** (no JSON). Put rationale, contentious choices,
and unresolved questions in `#` comments — the reasoner ignores them.

## Arrows

| Arrow        | Family       | Meaning                                            |
|--------------|--------------|----------------------------------------------------|
| `=>`         | constitutive | defeasible "X counts as Y"                         |
| `=>O`        | prescriptive | defeasible obligation / prohibition / permission   |
| `~>` `~>O`   | defeater     | blocks a conclusion without asserting the opposite |
| `->` `->O`   | strict       | indefeasible (use rarely)                          |

Prescriptive arrows carry `O`; constitutive arrows omit it.

## Literals & operators

- `atom` holds; `~atom` does not hold.
- Antecedent conjuncts are comma-separated and may test prior derivations:
  `O(a)`, `F(a)` (= `O(~a)`), `P(a)`, `Ps(a)`, `Pw(a)`.
- Compensatory chain `c1 * c2 * …`: `c2` becomes obligatory only once `c1` is
  obligatory **and** violated (remedy-after-breach), e.g. `r2: =>O ~publish * remove`.
- Bearer (prescriptive arrows only): `=>O@Party` names the duty-bearer
  (`precetto: =>O@Anyone ~Kill`, `sanzione: Kill =>O@Judge Punish`).

## Sugar (use to keep theories readable; all parse-time)

- **`oneof[a, b]`** in an antecedent → one rule per disjunct. Use for "violence
  **or** threat": `r: oneof[Violence, Threat] =>O@Judge X`.
- **Precondition block** — `A, B { … }` prepends `A, B` to every rule inside, so
  shared elements are written once. Keep the prohibition *outside* the block.
- **`overrides X`** suffix → the rule's conclusion supersedes `X` (lex specialis;
  `X` becomes not-obligated). Use for an aggravated penalty over a base one.

A decomposed offence then reads:
`Elem1, Elem2, Mens { tipico: =>O@Judge Punishable ; pena: O(Punishable) =>O@Judge Penalty overrides BasePenalty }`.

## Superiority

`superiority: winner > loser` selects the winner when two applicable rules
conflict. Prefer specific over general (`commission =>O publish` beats default
`=>O ~publish`). If both sides apply and no `>` resolves it, the reasoner prints
`[JUDGE: …]`; leave that for the human and flag it in a comment.

## Heuristics

- One norm per labelled rule; clear labels (`license_grant`, `info_call_exception`).
- Defaults take an empty antecedent (`r0: =>O ~use`).
- "unless / except / notwithstanding" → a more specific rule or a defeater, plus
  superiority if two defeasible rules still clash.
- Classification ("is a complaint / a license") → `=>`; conduct ("must publish") → `=>O`.
- Atom names: alphanumeric, consistent CamelCase.

## Atom descriptions (mandatory)

Every atom you use must be declared with a description — the reasoner refuses to
load a theory with an undescribed atom. Write the description as a
truth-condition (when does it hold?), since a fact-finder uses it to decide
facts. Optionally add provenance after `|`: a `quote:` snapshot and/or a `uri:`
to an in-repo markdown source with a GitHub-style line selector (at least one):

```
atom Disclose: discloses Confidential Information to any third party | quote: ...prior to the disclosure to any other person... | uri: sources/nda.md#L3-L6
```

## Output shape

Return only the `.ddl` text:

```
# <one-line summary of the clause>
facts: {{FILLED_BY_FACT_FINDER}}

atom Atom1: holds when ... | quote: <verbatim source> | uri: sources/<file>.md#L1-L2
atom Atom2: holds when ...

# <why this rule, if non-obvious>
label: antecedent =>O conclusion
...

superiority: rA > rB   # <reason>

# Open questions (judge):
# - <unresolved choice, e.g. is `approval` a defeater or a strict exception?>
```


Example:

```
Article 1. The Licensor grants the Licensee a license to evaluate the Product.
Article 2. The Licensee must not publish the results of the evaluation of the
Product without the approval of the Licensor; the approval must be
obtained before the publication. If the Licensee publishes results of
the evaluation of the Product without approval from the Licensor,
the Licensee has 24 h to remove the material.
Article 3. The Licensee must not publish comments on the evaluation of the
Product, unless the Licensee is permitted to publish the results of
the evaluation.
Article 4. If the Licensee is commissioned to perform an independent evalua-
tion of the Product, then the Licensee has the obligation to publish
the evaluation results.
Article 5. This license terminates automatically if the Licensee breaches this
Agreement.
```

Produces the output: (not every input could be clean like the above, usually it's more complex, and you might also need to make constitutive rules.)

```
# Example 1: License contract (§4 of Governatori 2018)
facts: license, commission, use


# Atom descriptions are mandatory; this synthetic example cites the paper.
atom license:    the licensee holds a valid licence | Governatori 2018 §4, license example
atom commission: the work was produced under commission | Governatori 2018 §4
atom use:        the licensee uses the licensed material | Governatori 2018 §4
atom publish:    the licensee publishes results | Governatori 2018 §4
atom remove:     the licensee removes the published results (remedy) | Governatori 2018 §4
atom approval:   prior approval to publish was obtained | Governatori 2018 §4
atom comment:    the licensee comments publicly | Governatori 2018 §4
atom bot:        we have a contradiction ? | Governatori 2018 §4


r0:  =>O  ~use
r1:  license  ~>O  use
r2:  =>O  ~publish * remove
r2e: approval  ~>O  publish
r3:  =>O  ~comment
r3e: P(publish)  ~>O  comment
r4:  commission  =>O  publish
r4x: commission  =>O  use
r5:  bot  =>O  ~use

# r ≺ s means r defeats s (r wins when both conflict)
# More specific/exception rules defeat more general ones
# Without e.g. r4 > r2, commission+use yields an unresolved publish conflict (judge must add ≺)
superiority: r1 > r0, r4x > r0, r5 > r1, r5 > r4x, r2e > r2, r3e > r3
```


## User (template)

**Law / contract / policy:**
```
{{LEGAL_TEXT}}
```
**Optional — preferred atoms or a similar existing `.ddl`:**
```
{{CONTEXT}}
```

Encode this as a complete `.ddl` theory with a placeholder `facts:` line.

## Before returning

- Every rule has a unique label and a valid arrow.
- Conduct duties use `=>O`; classifications use `=>`.
- Conflicting rules have superiority, or a `# Open questions` note.
- `*` appears only for genuine remedy-after-breach.
- `facts:` is left as a placeholder.
