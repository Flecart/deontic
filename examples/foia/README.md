# FOIA 2000 — pilot formalization

The UK Freedom of Information Act 2000, Parts I–II slice, as DDL: the s1
access duties (`@Authority` bearer), the s2 absolute/qualified exemption layer,
the s17 refusal notice, NCND, and five exemptions (s21, s31, s40, s42, s43).
Scoping rationale: `docs/experiments/foia_corpus/INDEX.md`.

- `foia.ddl` — the theory; encoding choices are documented in its header
  (qualified exemptions carry the `PiMaintainOutweighs` grounding atom in the
  body; s40(2) is absolute via the first condition; one shared PI atom in v1).
- `sources/foia_2000.md` — verbatim statute excerpts (legislation.gov.uk);
  atom provenance points here.
- `tests.sh` — 16 disposition checks (`bash examples/foia/tests.sh`).

The grounding-vs-deduction split is the point: open-textured predicates
("would prejudice", "would contravene the DP principles", the public-interest
balance) are **facts a fact-finder asserts**; the engine owns
exemption-defeats-duty, absolute-vs-qualified, NCND stacking, and the s17
consequence. `deontic abduce examples/foia/foia.ddl 'O@Authority(~Disclose)'
--all` prints the seven minimal withholding configurations — the statute's
structure read back.

Real tribunal cases + the LLM eval pipeline live in
`docs/experiments/foia_corpus/` (`pipeline.py`, `cases/`).
