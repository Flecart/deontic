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
