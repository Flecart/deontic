# First real results

Task: **`contract_nli_sharing_with_employees`** (LegalBench, real `nguha/legalbench`
test split). 60 examples, **shuffled** (seed 0) so the slice is label-balanced
(the split is otherwise label-sorted — see below). Conditions: `baseline`
(direct prompt) vs `cli` (model drives the `deontic` reasoner via a shell).

```
model               baseline        cli
gpt-5.4-mini        97% (58/60)     85% (51/60)     avg 1.6 reasoner calls
deepseek-v4-flash   97% (58/60)     88% (53/60)     avg 3.0 reasoner calls
```

## Takeaway: the reasoner condition *hurts* here

Both models are already near-perfect answering directly. Routing through the
reasoner lowers accuracy, for two distinct, instructive reasons:

- **gpt-5.4-mini — over-strict formalization → false "No".** Its `No` class stays
  perfect (27/27) but Yes recall drops (24/33; 9 `Yes→No`). It formalizes the
  clause as a default prohibition, queries `query Share → F(Share)`, and concludes
  "not permitted in general → No" — even in cases where it ran `abduce` and saw
  `Ps(Share)` (permitted). It distrusts/over-reads the formal result. ContractNLI
  counts "may share with employees who need to know" as entailing the hypothesis;
  the model's strict formal reading does not.
- **deepseek-v4-flash — extraction failures.** Yes recall is perfect (31/31) and it
  uses the reasoner well (`abduce`, 3 calls avg), but 5/60 answers came back
  unparseable (`None`) — long tool transcripts ending without a clean `ANSWER:`
  line — plus 2 false `Yes`.

## What this means

This is exactly the thesis in [`../examples/legalbench/COMPARISON.md`](../examples/legalbench/COMPARISON.md):
the kernel does **not** hand you free accuracy. On a task strong models already
nail, the NL→DDL step (and *which* query to run, and how to map `F`/`Ps`/`P`/
`unknown` back to a label) is the bottleneck, and forcing it can degrade them.
The reasoner's value is auditability/consistency, not raw accuracy here.

Levers to make the `cli`/`tool` condition competitive (future work):
- Sharpen the skill prompt: for "may/permitted" hypotheses use `abduce 'P(X)' --all`,
  and map `Ps/P` (or a permission gated on facts plausibly present) to **Yes** —
  this directly targets gpt-5.4-mini's false-No mode.
- Kill the `None`s: raise `--max-rounds` and/or force a clean final answer.
- Expect bigger wins on *harder* tasks where direct answers are unreliable and a
  consistent formal check disambiguates — not on near-saturated ones.

## Methodology notes

- LegalBench splits are **label-sorted**; always pass `--shuffle` with `--limit`
  (the first un-shuffled 40 were all `Yes` and produced invalid numbers).
- One task only — a full picture needs a sweep across the 14 `contract_nli_*`
  tasks (all mapped in `data.py`). Full transcripts in `runs/*.jsonl`.

Reproduce:
```bash
python eval/run.py --legalbench contract_nli_sharing_with_employees \
  --shuffle --limit 60 --models gpt-5.4-mini,deepseek-v4-flash \
  --condition baseline,cli --out runs/lb_sharing_balanced.jsonl
```

---

# Ambiguous synthetic contract benchmark

Task: **`ambiguous_contracts`**, generated locally by
[`ambiguous_contracts.py`](ambiguous_contracts.py). The dataset has **2,304**
ContractNLI-style examples across 12 clause families: disclosure, retention,
assignment, subcontracting, data use, termination, price changes, audits,
deletion, copying, customer contact, and reverse engineering.

The examples deliberately stack defaults, exceptions, exception-to-exception
rules, priority language ("notwithstanding", "unless"), and irrelevant
distractor facts. Each row includes:

- natural-language clause + scenario,
- Yes/No hypothesis (`may`, `must`, or `must not`),
- gold label,
- the underlying `.ddl` theory and facts used to audit the label.

Offline run, 2026-06-03. Split: 1,608 train / 696 test, stratified by clause
family. The Lean/Lake binary was not installed in this environment, so the
`deontic_system` column used the benchmark's small Python DDL fallback evaluator;
the experiment will call `.lake/build/bin/deontic` automatically when present.

```
condition                    accuracy
surface_no_deontic           57.5% (400/696)
knn_precedent_no_deontic     90.7% (631/696)
deontic_system              100.0% (696/696)
```

By hypothesis type:

```
condition                    may     must    must_not
surface_no_deontic           59.3%   75.9%   36.8%
knn_precedent_no_deontic     87.7%   94.4%   89.9%
deontic_system              100.0%  100.0%  100.0%
```

Takeaway: on this harder ambiguous benchmark, precedent memory is strong but
still misses exception boundaries; the formal rule system is exact when the
NL→DDL representation is supplied. This is the "best case" for the deontic
layer: it tests formal consequence, not extraction from prose.

Reproduce:
```bash
python eval/ambiguous_contracts.py
python eval/ambiguous_contract_experiment.py

# LLM harness, once a model/key and the deontic binary are available:
python eval/run.py --task ambiguous_contracts \
  --data eval/sample/ambiguous_contracts.jsonl \
  --shuffle --limit 100 --condition baseline,cli --model gpt-4o-mini
```
