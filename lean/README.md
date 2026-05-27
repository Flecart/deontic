# ddl (Lean 4) — Defeasible Deontic Logic inference engine

A **Lean 4 port** of the Python reference implementation in `../src/ddl`, of the
logic in Governatori (2018), *"Practical Normative Reasoning with Defeasible
Deontic Logic"* (`../guido.pdf`). It reasons about **norms** — obligations,
prohibitions, permissions, contrary-to-duty compensation chains — with a
**constructive, fully traceable** proof theory: every verdict comes with a
justification.

The port is method-for-method faithful to the Python engine: on every worked
example its computed extension is **byte-identical** to the Python engine's, and
the CLI output matches the Python CLI's.

## Build & test

```bash
cd lean
lake build          # builds the library, the test runner, and the CLI
lake test           # runs the acceptance suite (reproduces the paper's examples)
```

`lake test` reports each check and exits non-zero on any failure. Coverage
mirrors the Python `tests/`: basic defeasible logic, the licence (Ex.1/§4),
premium customer (Ex.2), TCPC complaint (Ex.3/4), U-turn (Ex.5), ⊗ compensation
chains, the Proposition 1 invariants, the high-level API, and JSON round-trips.

## CLI

```bash
lake exe ddl run    ../examples/license.ddl --facts "license. publish. remove. comment."
lake exe ddl query  ../examples/license.ddl "F use" --facts "license. publish. remove. comment."
lake exe ddl query  ../examples/uturn.ddl   "Ps Uturn" --facts "AtTrafficLights. UturnPermittedSign."
lake exe ddl render ../examples/complaint.ddl          # the theory back in plain English
lake exe ddl run    ../examples/license.json           # the structured-JSON front end
```

Queries accept the tag form (`+dO remove`, `-dC publish`), the friendly form
(`O remove`, `F publish`, `P use`, `Ps use`), `noncompliant`/`compliant`, or a
bare literal (`publish` = `+dC publish`). `run --all` shows every conclusion.

## Library use

```lean
import Ddl
open Ddl

def r : Reasoner := Reasoner.ofTheory (parse! (
  "r0: =>O -use\n r1: license ~>O use\n r0 < r1\n license."))

#eval (r.queryStr "P use").holds      -- true
#eval IO.println (r.report)           -- all active normative effects
```

The same theory can be built from the LLM-facing JSON (`theoryFromJsonStr`) or
the DSL (`parse`); both compile to the same `Theory`.

## Module map (parallels `../src/ddl`)

| Lean module        | Python file   | Contents |
|--------------------|---------------|----------|
| `Ddl/Syntax.lean`  | `syntax.py`   | `Literal`, `ModalLiteral`, `Rule`, `Theory`, ⊗-chain normalisation |
| `Ddl/Proof.lean`   | `proof.py`    | `Conclusion` (tagged literal), `Justification` |
| `Ddl/Engine.lean`  | `engine.py`   | `Extension` + all ± proof conditions, support closure, the fixpoint |
| `Ddl/Parser.lean`  | `parser.py`   | the `.ddl` surface syntax |
| `Ddl/Render.lean`  | `render.py`   | natural-language rendering (the audit round-trip) |
| `Ddl/Api.lean`     | `api.py`      | `Reasoner`, `Verdict`, query parsing + proof traces |
| `Ddl/JsonIo.lean`  | `json_io.py`  | the structured-JSON theory interface |
| `Tests.lean`       | `tests/`      | the acceptance suite |
| `Main.lean`        | `cli.py`      | the command-line interface |

## Notes on the port

* The fixpoint loops use `partial def` (mirroring the Python `while`-loops); the
  computation is monotone over a finite modal Herbrand base, so it converges.
* Faithful-but-pragmatic choices from the Python engine are preserved: violation
  is `~c ∈ F`; plain-literal body conditions use `±dC` (which subsume facts) so
  constitutive rules chain; the superiority reading is `r < s` ⇒ *s defeats r*.
* Lean 4.30 migrated several `String` methods to return `String.Slice`; the
  parser keeps small `String`-valued helpers (`trim`/`stake`/`sdrop`/`sfront`)
  to avoid threading slices throughout.
