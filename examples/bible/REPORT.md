# Love fulfils the law: the Gospel moral order as defeasible deontic logic

*Companion study to `caselaw/REPORT.md`. It takes that report's central
architectural finding — a fixed inviolable constitution is brittle; the best
institution is an **overridable** constitution plus a small set of supreme
invariants — and asks whether a 2000-year-old moral-legal system is a worked
instance of it. Code & data: `caselaw/bible_*.py`; artifacts: `examples/bible/`;
raw results: `caselaw/runs/bible*.json`.*

## Abstract

We formalise a nucleus of New-Testament moral teaching as a defeasible deontic
theory and adjudicate Jesus's recorded verdicts with the `deontic` engine. The
encoding makes one architectural claim testable: the Gospels run the exact design
`caselaw/REPORT.md` argued is best — the **two great commandments as a supreme,
load-bearing invariant**, with the **written Decalogue kept as an overridable
default** ("I came not to destroy the law but to fulfil it", Matt 5:17). On a
corpus of 25 episodes we find: (1) the literal written law alone reproduces only
**0.50** of Jesus's held-out verdicts — right on the explicit prohibitions, wrong
on every mercy/positive-duty case; (2) love-of-neighbour alone does better
(**0.78**) but misses the vertical (love-of-God) axis and *over-permits* (it
licenses sabbath profit-work the Gospels still forbid); (3) the **hybrid** —
love supreme over a defeasible Decalogue — reaches **0.94**, its only misses being
genuine hard cases of moral philosophy (supererogation, a minor-need exception);
(4) an **ablation** confirms the supreme principle is load-bearing: removing the
single love-grounded superiority turns the Sabbath healing from a derived
obligation into an unresolved `[JUDGE]` deadlock; and (5) in a live commons of
selfish agents, the **letter of the law collapses the resource exactly like no
institution at all** — depleting a commons violates no enumerated commandment
because it has no owner — whereas every **generative principle** (love,
utility, universalisability) reaches the diffuse harm and sustains it 18/18. The
through-line: *the letter enumerates, the principle generates*; "love is the
fulfilling of the law" (Rom 13:10) is, formally, the statement that a supreme
generative invariant covers the cases an enumeration cannot.

## Design: an auditable moral constitution

A moral judgment is only science if its *reasons* are recorded and its *verdicts*
are checkable. We borrow case law's discipline — every ruling carries its *ratio
decidendi* — and realise it with the engine's grounding machinery:

- **Grounded atoms (provenance).** Every atom is a mandatory truth-condition with
  a `quote:`/`uri:` into `sources/gospels.md` (line-addressable). `deontic atoms`
  prints and `--resolve`s the dictionary, so each term is bound to its text.
- **Ratio as superiority.** Each `superiority:` line is annotated with the
  commandment that licenses it. In `constitution.ddl` the Sabbath resolution reads
  `mercy > keepSabbath` with the ratio *love thy neighbour (Matt 22:39) + "the
  sabbath was made for man" (Mark 2:27) + "I will have mercy and not sacrifice"
  (Matt 9:13)*. The verdict is thus traceable to the principle that grounded it.
- **The deadlock as the audit gap.** Where no principle resolves a clash the
  engine prints `[JUDGE: …]`. `legalism.ddl` is exactly `constitution.ddl` minus
  the love-grounded superiority: on identical Sabbath facts it returns
  `unresolved`, while `constitution.ddl` returns `O(heal)`. An un-adjudicated
  conflict is precisely an un-auditable verdict; we measure it as **coherence**
  (residual `[JUDGE]` deadlocks).

The worked artifacts:

| file | shows |
|---|---|
| `constitution.ddl` | hybrid: love supreme + Decalogue default → Sabbath healing yields `O(heal)` |
| `legalism.ddl` | same minus the ratio → `[JUDGE]` deadlock (the Pharisaic gap) |
| `zacchaeus.ddl` | restitution as a compensatory chain `=>O ~defraud * restoreFourfold` (Luke 19:8) |

*Design note.* We do **not** make superiority itself a derivable conclusion of a
meta-rule (the engine's superiority is static label-pairs). Grounding the ratio in
comments + provenance + the `--trace` certificate is auditable without a
proof-engine rewrite; derived superiority is logged as future work.

## The experiment

**Corpus (`bible_dataset.py`).** 25 Gospel episodes, each normalised to a verdict
on a shared target `act` ("is *this* contemplated act forbidden/obligatory/
permitted, given the situation?"). The **verdict is the label** and is largely
uncontested (the text says what he did); the **ratio is the interpretive layer**
we make auditable but do not score as truth. Feature vectors are unique (no
identical situation with two verdicts). Two morally-irrelevant distractors
(`crowdPresent`, `daytime`) separate structural generalisation from memorisation.

**Arms (`bible_theories.py`), written from a *principle*, not fitted to labels —**
so fidelity is an honest out-of-sample measurement:

- `decalogue` — the written law: prohibitions of both tables + sabbath rest, no
  positive duty, no override (legalism).
- `love` — love-of-**neighbour** only: relieve need, do no harm, forgive; silent
  on the love-of-God axis (morality reduced to interpersonal niceness).
- `hybrid` — love (both commandments) **supreme** over a defeasible Decalogue.
- `caselaw` — a defeasible theory **synthesised** from Jesus's rulings on the
  train split (Jesus as judge), tested on held-out episodes.

**Leakage control.** Episode-level 60/40 train/test split, theory frozen before
the test episodes are seen, 8 seeds. The fixed arms never see labels at all (they
are principled encodings); the `caselaw` arm learns only on train.

### Held-out verdict fidelity

| arm | held-out | full corpus | coherence (deadlocks) | rules |
|---|---|---|---|---|
| decalogue (legalism) | **0.50** | 0.48 | 0 | 3 |
| love (neighbour only) | **0.78** | 0.80 | 0 | 4 |
| **hybrid** (Gospel design) | **0.94** | 0.92 | 0 | 8 |
| caselaw (evolved from rulings) | 0.71 | 0.89 | 0 | 6.4 |

- **The literal law alone is right only half the time (0.50)** — it forbids murder,
  theft, idolatry, sabbath-breaking, but cannot mandate the Samaritan's mercy,
  cannot reach the Sermon's intensifications (anger, lust, retaliation), and
  *forbids* the Sabbath healing. This mirrors `caselaw/REPORT.md`'s fixed
  constitution (0.52): an enumeration is right only where reality matches its
  framers' list.
- **Love-of-neighbour alone (0.78)** recovers all the horizontal cases but (a)
  misses the vertical axis — it is silent on idolatry, blasphemy, and the duty of
  worship — and (b) **over-permits**: with no sabbath default it licenses ordinary
  profit-work on the sabbath, which the Gospels still forbid. "Just be loving to
  people" is not the whole law.
- **The hybrid (0.94) is strictly best**, exactly as `caselaw/REPORT.md` predicted
  for "constitution-as-overridable-default + supreme invariants" (0.90 there).
  Its **only two misses are genuine hard cases**: the rich young ruler (is selling
  all a universal duty or a counsel of perfection?) and the ox in the pit (a
  minor-need sabbath exception the formal theory lacks). These are honest ceilings,
  not encoding bugs — we leave them as open `[JUDGE]`-style questions.
- **The law can be *evolved* (0.71 held-out, 0.89 full).** A defeasible theory
  synthesised from Jesus's rulings recovers most of the structure, but cold-starts
  on a 15-episode train split — the sparse-data regime where `caselaw/REPORT.md`
  also found evolved law trails a well-specified hybrid.

### The supreme principle is load-bearing (ablation)

Remove the one love-grounded superiority from the hybrid:

| | full_acc | deadlocks |
|---|---|---|
| hybrid | 0.92 | 0 |
| hybrid − supreme principle | 0.88 | 1 → `SabbathHeal` |

Without the supreme commandment the head-to-head duty collision (mercy vs rest)
has no resolution: the engine reports `[JUDGE]` and the verdict is lost. This is
the formal signature of legalism — the law underdetermines, and only a principle
*above* the rules can re-order them. In our corpus this structural collision
appears once (Sabbath healing); in the Gospels it recurs across the Sabbath
controversies (Mark 3, Luke 13, Luke 14), each an instance of the same clash the
principle resolves.

### The ambitious arm: which moral nucleus sustains a commons?

A live GovSim-style commons (5 selfish agents, regenerating pool, 18 rounds),
each nucleus enforced by the engine (confiscate the unlawful surplus when
over-extraction is forbidden):

| moral nucleus | sustained | trajectory |
|---|---|---|
| none | **collapse** | 100 → 40 → 10 → 0 |
| **legalism** (literal Decalogue) | **collapse** | 100 → 40 → 10 → 0 |
| love (neighbour) | **survives 18/18** | 100, 100, …, 100 |
| utilitarian | survives 18/18 | 100, …, 100 |
| kantian | survives 18/18 | 100, …, 100 |

**Legalism collapses the commons identically to having no institution at all.**
Depleting a commons is not theft of any *owner's* property — there is no
identifiable victim — so no enumerated commandment is triggered and the law is
silent. Every **generative principle** reaches the diffuse harm: love-of-neighbour
sees that over-extraction harms one's fellow commoners (present and future);
utility sees the lowered long-run yield; universalisability sees the maxim destroy
the resource. Each forbids it and sustains the commons. This is the live
counterpart of the fidelity result and of `caselaw/REPORT.md`'s **F6
(no-plaintiff externality)**: an enumeration cannot reach a harm with no standing
plaintiff; a principle can. *"Love is the fulfilling of the law" (Rom 13:10)* is,
formally, the claim that a supreme generative invariant covers what the letter
enumerates and more.

## Discussion

The Gospels' own polemic against legalism is, on this formalisation, a correct
result in institutional design. Treating the written law as an **inviolable
floor** (the Pharisaic reading `caselaw/REPORT.md` modelled as the harmful
"supreme constitution", 0.76 < pure case law) is brittle: it forbids the merciful
act and cannot reach the un-named harm. Treating it as an **overridable default
under a supreme principle of love** (Matt 5:17; Mark 2:27) is the adaptive,
auditable design that tops every metric here — the same recipe the controlled
experiment reached from synthetic theories. Two independent routes, one
architecture: *a small set of supreme invariants, everything else defeasible.*

## Threats to validity / honesty

- **Verdicts vs ratios.** We score only the verdict (defensible from the text).
  The ratios are interpretive; a different tradition would phrase them differently,
  though the *verdicts* are largely shared.
- **Feature assignment.** Reading anger/lust as "harming the neighbour", or
  stoning as harming a neighbour rather than executing a penalty, are faithful but
  contestable readings (the Sermon's own logic; mercy over the judicial penalty).
  We assign features blind to which arm benefits, but a hostile re-reading could
  shift a few cases.
- **Single hand-encoder.** This is one careful encoding with a frozen episode
  split, not the inter-encoder-agreement or LLM-judge-induction protocol we
  flagged as stronger leakage controls. Those are the obvious next step.
- **Normalisation to one `act`.** Collapsing each episode to a single contested
  act loses richness (compensatory chains, two-jurisdiction cases) that the
  qualitative `.ddl` artifacts keep but the quantitative corpus does not.
- **The GovSim legalism result hinges on the fact-finder lens** — legalism
  genuinely *cannot see* the diffuse harm (its categories of owner/theft don't
  apply), which is the philosophical content, not a trick; but it is a modelling
  choice, stated plainly.
- **Soteriology is bracketed.** We encode interpersonal/vertical *conduct*, not
  faith, grace, or salvation; the engine reasons about acts.
- **Small corpus.** 25 episodes, 8 seeds. Trends are large and consistent but not
  error-barred at scale. Formal logic measures coherence + fidelity-to-recorded-
  verdicts + commons outcomes — it does **not** adjudicate which morality is true.

## Methods / reproduce

```
caselaw/bible_theories.py     # decalogue / love / hybrid arms + the ablation theory
caselaw/bible_dataset.py      # 25 Gospel episodes (facts, verdict, ratio, cite)
caselaw/bible_experiment.py   # held-out fidelity + coherence + supreme-principle ablation
caselaw/bible_govsim.py       # the commons arm (which nucleus sustains it)
examples/bible/*.ddl          # auditable artifacts (constitution / legalism / zacchaeus)
examples/bible/sources/gospels.md   # line-addressable provenance

python3 -m caselaw.bible_dataset       # corpus stats + consistency check
python3 -m caselaw.bible_experiment    # -> runs/bible.json
python3 -m caselaw.bible_govsim        # -> runs/bible_govsim.json
./.lake/build/bin/deontic query  <(sed 's/{{FILLED_BY_FACT_FINDER}}/sabbath, neighborInNeed/' examples/bible/constitution.ddl) heal
./.lake/build/bin/deontic atoms  examples/bible/constitution.ddl --resolve
```

## Conclusion

Encoding a nucleus of Gospel ethics as defeasible deontic logic turns a
theological intuition into a measurable institutional-design result. The letter of
the law, alone, is half-right and collapses a commons; love-as-supreme over a
defeasible law is auditable, coherent, predicts the recorded verdicts best, and
sustains cooperation. The Gospels' "fulfil, not abolish" is the same architecture
the controlled case-law study reached independently — **a few supreme invariants,
everything else defeasible** — and "love is the fulfilling of the law" is its
one-line statement: a generative principle reaches what an enumeration cannot.
