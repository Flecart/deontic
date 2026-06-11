# EIR 2004 — formalization (domain #2)

The Environmental Information Regulations 2004 as DDL: the reg 5(1) duty,
all reg 12(4)/(5) exceptions (every one qualified by the reg 12(1)(b) public
interest test, with the reg 12(2) presumption in favour of disclosure baked
into the PI atom's truth conditions), and reg 13 personal data. The reg 12(5)
"would adversely affect" bar (more probable than not) is in each atom's
contract. `bash examples/eir/tests.sh` — 13 checks.

Seed eval corpus: ~15 FTT decisions already fetched and cached during the
FOIA campaign (the `skip:eir-only` entries in
docs/experiments/foia_corpus/candidates.txt). Labelling starts once the
pipeline is domain-parametrized (see docs/experiments/DOMAINS.md).
