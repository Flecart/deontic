# LLM prompts for deontic workflows

These prompts support a **two-stage** pipeline in front of the Lean reasoner:

1. **[extract-facts.md](extract-facts.md)** — From evidence and a narrative, decide which **ground facts** hold (input to `facts:` in a `.ddl` file).
2. **[law-to-ddl.md](law-to-ddl.md)** — From law or contract text in natural language, draft **rules, operators, and superiority** (the normative theory).

Run the formal reasoner only after both stages:

```bash
lake build deontic
./.lake/build/bin/deontic query my_theory.ddl publish --json
```

The reasoner computes obligations, permissions, violations (`+∂_⊥`), and unresolved conflicts (`[JUDGE: …]`). It does **not** read free text; the LLM’s job is to produce accurate `.ddl` fragments.

## Suggested usage

| Step | Prompt | Human review |
|------|--------|----------------|
| Encode law | `law-to-ddl.md` | Check arrows, compensatory chains, superiority |
| Establish scenario | `extract-facts.md` | Verify each atom against source documents |
| Reason | `deontic query` / `check` | Resolve `[JUDGE: …]` by adding `r > s` if needed |

Copy the **System** block into your agent’s system message and the **User** block as the task template, filling in the placeholders.
