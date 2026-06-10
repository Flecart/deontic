# deontic_py

A typed, JSON-backed Python client for the `deontic` reasoner. It is the
supported way to drive the engine from Python — it shells out to the CLI with
`--json` and parses the structured output into dataclasses, so callers never
scrape human text.

Prerequisite: the binary must be built.

```bash
export PATH="$HOME/.elan/bin:$PATH" && lake build deontic
```

## Quick start

```python
from deontic_py import Deontic

d = Deontic()                                 # finds .lake/build/bin/deontic

ext = d.check("examples/ex1_license.ddl")     # Extension over the whole base
ext.verdict("use")                            # "obligatory"
ext.verdict("publish")                        # "dilemma"  (unresolved conflict)
ext.has_violation                             # False
[c.atom for c in ext.unresolved_conflicts]    # ["publish"]

# theory can be a path OR a raw .ddl string
ddl = "facts: rain\natom rain: it rains\natom umbrella: bring one\nr: rain =>O umbrella\n"
d.query(ddl, ["umbrella"])["umbrella"].status # "O(umbrella)"
d.verdict(ddl, "umbrella")                     # "obligatory"

# backward search: which facts make a goal hold?
d.abduce("examples/ex1_license.ddl", ["P(publish)"], all=True).minimal_configs
# -> [["approval"], ["commission"]]

# overlay facts without editing the file
d.check("examples/ex1_license.ddl", assume=["~use"]).has_violation

# atom dictionary (descriptions + provenance)
for e in d.atoms("examples/ex1_license.ddl"):
    print(e.atom, e.description)

# proof certificate: which applicable rules decided an atom, and what they defeated
rep = d.why("examples/ex1_license.ddl", ["publish"])["publish"]["Licensee"]
rep.status          # "O(publish)"
rep.winning_rules   # ["r4"]
[(r.rule, r.defeated_by) for r in rep.against_o]  # [("r2", ["r4"])]
```

### Binary resolution

`Deontic(binary=...)` is authoritative (errors if missing). Otherwise:
`$DEONTIC_BIN` → `<repo>/.lake/build/bin/deontic`. A missing binary raises
`DeonticNotBuilt`; a `.ddl` parse error or an undescribed atom raises
`DeonticParseError`; a slow run raises `DeonticTimeout`. Pass `cache=True` to
memoise repeated calls (handy for large fact sweeps).

## Result types (`deontic_py.results`)

Each mirrors a renderer in `Deontic/Pretty.lean`:

- `Extension` / `QueryResult` — `atoms: dict[str, AtomStatus]`, `has_violation`,
  `violating_rules`, `has_unresolved_conflicts`, `unresolved_conflicts:
  list[Conflict]`. Helpers: `.status(a)`, `.code(a)`, `.verdict(a)`, `ext[a]`.
- `AtomStatus` — `.status` (raw, e.g. `"O(use)"`), `.code` (`"O"`), `.verdict`
  (`"obligatory"`), `.tags: list[Tag]`.
- `Conflict` — `atom`, `for_o`, `against_o`, `unresolved_pairs`.
- `AbduceResult` — `minimal_configs`, `minimal_count`, `satisfying`,
  `evaluated`, `truncated`.
- `AtomEntry` — `atom`, `description`, `provenance`, `resolved`.
- `WhyReport` — proof certificate per atom/bearer (`why()`): `status`,
  `for_o` / `against_o` (each a `WhyRule` with `rule`, `text`, `defeated_by`),
  `.winning_rules` helper.

Status → verdict map (4-class): `O→obligatory`, `F→forbidden`,
`Ps/P/Pw→allowed`, `unresolved→dilemma`, anything else → `allowed`.

## LLM tool surface (`deontic_py.llm`)

Hand an agent a single `run_deontic` tool and route its calls through
`dispatch`, which returns the reasoner's **human-readable** prose (better for the
model than JSON):

```python
from deontic_py import TOOL_SCHEMA, dispatch          # Anthropic tools format
# (TOOL_SCHEMA_OPENAI is the OpenAI function-calling variant)

text = dispatch(ddl, "query", args=["umbrella"])      # never raises; errors -> string
```

`TOOL_SCHEMA["description"]` embeds a DDL cheat-sheet (`DDL_SYNTAX`) so the model
can write valid theories. For Anthropic tool-use, `call_tool(tool_use.input)`
takes the input dict directly.

## Verify

```bash
python -m deontic_py.selftest    # drives the real binary; asserts vs CLI --json
```
