# Import examples

Demonstrates reusing a shared module across theories. Paths are relative to the
importing file; descriptions are checked on the *merged* theory.

| File | Shows |
|------|-------|
| `definitions.ddl` | A reusable definitions module (roles → `Representative`), no facts |
| `nda_glob.ddl` | `from definitions.ddl import *` — merge into this namespace |
| `nda_namespaced.ddl` | `import definitions.ddl as roles` — atoms become `roles.*` |

Two import forms:

- `import <path> [as <alias>]` — imported atoms and rule labels are prefixed
  `alias.` (the file stem is the default alias); reference them qualified
  (`roles.Representative`).
- `from <path> import *` — merged unprefixed into the current namespace.

**Merging is description-guarded.** Two declarations of the same atom must agree
on their description, otherwise the load fails with a conflict — the same atom
name must mean the same thing. Rule-label collisions and import cycles are also
errors. (Selective `from <path> import a, b` is not implemented yet.)

```bash
deontic atoms  examples/imports/nda_namespaced.ddl
deontic abduce examples/imports/nda_glob.ddl 'P(Disclose)' --all
#  → { Representative, NeedToKnow }
```
