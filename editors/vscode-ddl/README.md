# DDL syntax highlighting for VS Code

Syntax highlighting for `.ddl` files — the **Defeasible Deontic Logic** theories
consumed by the [`deontic`](../../README.md) reasoner.

Highlights comments, the `facts:` / `superiority:` sections, `atom`
declarations with `quote:` / `uri:` provenance (and `#Lx-Ly` line selectors),
module `import` / `from … import *`, rule labels, the arrows
(`->`, `->O`, `=>`, `=>O`, `~>`, `~>O`), deontic operators (`O() F() P() Pw()
Ps() C()`), and the `~` `*` `>` operators.

It is **grammar-only** (a TextMate grammar): no build step, no runtime, nothing
to keep alive. That is deliberate — see *Maintaining the grammar* below.

## Install

Pick whichever fits. The extension is `editors/vscode-ddl/` in the repo.

**1 — Local install (no tooling).** Copy or symlink the folder into your
editor's extensions directory, then reload the window
(`Ctrl+Shift+P → Developer: Reload Window`):

```bash
# VS Code
ln -s "$PWD/editors/vscode-ddl" ~/.vscode/extensions/ddl-syntax-0.1.0
# VSCodium:        ~/.vscode-oss/extensions/...
# Cursor/Windsurf: ~/.cursor/extensions/...  (same layout)
```

**2 — Build a `.vsix` and install it** (shareable single file):

```bash
cd editors/vscode-ddl
npx @vscode/vsce package           # -> ddl-syntax-0.1.0.vsix
code --install-extension ddl-syntax-0.1.0.vsix
```

(`code` → `codium` / `cursor` for those editors.)

**3 — Hack on it.** Open `editors/vscode-ddl/` in VS Code and press `F5` to
launch an Extension Development Host with the grammar loaded; open any `.ddl`
file there.

Verify it works by opening [`samples/showcase.ddl`](samples/showcase.ddl) — it
exercises every token.

## Should you publish it to a marketplace?

For a project-internal DSL, **probably not yet** — publishing adds an account,
a release cadence, and public-support expectations for a niche grammar. Recommended order:

1. **Now:** keep it in-repo; collaborators install via method 1 or 2 above (the
   `.vsix` is a clean single-file handoff). Zero overhead.
2. **If VSCodium/Cursor users want it discoverable:** publish to
   [Open VSX](https://open-vsx.org) — `npx ovsx publish` with a free token.
   Lighter-weight than the MS Marketplace.
3. **If you want public visibility on the VS Code Marketplace:** create a
   publisher at <https://marketplace.visualstudio.com/manage>, get an Azure
   DevOps Personal Access Token, set `"publisher"` in `package.json`, add an
   `icon`, then `npx @vscode/vsce publish`.

Either way the grammar files don't change — publishing is just distribution.

## Maintaining the grammar

The whole language lives in
[`syntaxes/ddl.tmLanguage.json`](syntaxes/ddl.tmLanguage.json). Design for
maintenance:

- Every construct is its own **named rule** in `repository`, each with a
  `comment` explaining it. The top-level `patterns` list sets the **try order**
  (first match wins at each position) — the order is load-bearing, so the
  comments call out the cases that depend on it (line selector before comment;
  longest arrows first; sections/atoms before the generic rule-label).
- Token → scope map:

  | Construct | Example | Scope |
  |-----------|---------|-------|
  | comment | `# note` | `comment.line.number-sign` |
  | line selector | `#L3-L6` | `constant.numeric.line-selector` |
  | import keywords | `import` `from` `as` | `keyword.control.import` |
  | sections | `facts` `superiority` | `keyword.control.section` |
  | atom keyword / name | `atom Disclose` | `keyword.control.atom` / `entity.name.type.atom` |
  | rule label | `r1:` | `entity.name.function.label` |
  | provenance keys | `uri` `quote` | `keyword.other.provenance` |
  | arrows | `=>O` `~>` … | `keyword.operator.arrow` |
  | deontic ops | `O(` `F(` `P(` … | `support.function.deontic` |
  | operators | `~` `*` `>` | `keyword.operator` |
  | provenance separator | `\|` | `punctuation.separator.provenance` |

- **To add a token:** add a named rule to `repository`, then add an `include`
  to `patterns` at the right priority. Keep one concern per rule and one regex
  per rule.
- **To verify a change:** open `samples/showcase.ddl` and eyeball it, or use
  `Ctrl+Shift+P → Developer: Inspect Editor Tokens and Scopes` to see the scope
  under the cursor.
- **Keep in sync** with `Deontic/Parser.lean` — if the `.ddl` syntax changes
  there (new arrow, new section, new provenance field), update the matching
  rule here and add a line to the showcase.
