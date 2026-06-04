# LLM ambiguous-contract experiment

The offline benchmark in [`RESULTS.md`](RESULTS.md) compared a text heuristic, KNN
label-voting, and the formal reasoner with **no language model in the loop**.
This report puts real models in the loop on the same
[`ambiguous_contracts`](ambiguous_contracts.py) data and compares three
conditions *per model*:

- **baseline** — prompt the model directly for Yes/No (no tools, no precedents).
- **tool** — give the model the `run_deontic` reasoner; it must formalize the
  clause as a DDL theory and query it (`query`/`abduce`/`check`) for up to 4
  rounds, then map the formal result to the label. *The DDL is not handed over —
  the model writes it from prose.*
- **knn** — retrieve the `k=5` nearest decided precedents (structured Jaccard
  over template/mode/facts, same retrieval as the offline script) and show them
  as labelled few-shot context; the model answers with no reasoner.

Models: the **gpt-5.4 family** and **gpt-4.1** (OpenAI), **deepseek-v4-flash**
and **grok-4.3** (OpenRouter) — all agentic/tool-aware — plus **gpt-4o** as a
deliberately older contrast.

Run 2026-06-04. One stratified split: **1,608 precedent pool / 90 evaluated**
test rows, balanced across modes (30 `may` / 30 `must` / 30 `must_not`; 31 Yes /
59 No). All models see the identical 90-row slice (seed 11).

## Accuracy (n=90)

```
model               baseline   tool              knn
gpt-5.4             96.7%      95.6%  (1.0 calls)  100%
grok-4.3            93.3%      87.8%  (1.7 calls)  100%
gpt-4.1             94.4%      83.3%  (1.6 calls)  100%
gpt-4o (old)        93.3%      84.4%  (1.7 calls)  96.7%
deepseek-v4-flash   90.0%      82.2%  (3.2 calls)  100%   (5 unparseable)
gpt-5.4-mini        88.9%      76.7%  (1.3 calls)  100%
```

`tool` shows the average reasoner calls per example; deepseek also returned 5
`None` (unparseable) answers, counted wrong.

By hypothesis type, **tool** condition (where the degradation concentrates):

```
model               may     must    must_not
gpt-5.4             93.3%   96.7%   96.7%
grok-4.3            80.0%   93.3%   90.0%
gpt-4.1             73.3%   96.7%   80.0%
gpt-4o              83.3%   90.0%   80.0%
deepseek-v4-flash   86.7%   93.3%   66.7%
gpt-5.4-mini        66.7%   83.3%   80.0%
```

## Takeaways

1. **Precedent retrieval (knn) wins — and is near-saturated.** Five of six
   models hit **100%**; gpt-4o is the lone exception at 96.7%. The structured
   retrieval surfaces near-duplicate decided cases, so this is close to an upper
   bound: when a matching precedent is in context, every modern model copies its
   label reliably. It rewards pattern-matching, not formal reasoning — read it
   as "how well can the model reuse a precedent", not "can it reason about the
   clause" (see the caveat below).

2. **The reasoner condition *hurts* every model** — exactly the thesis in
   [`RESULTS.md`](RESULTS.md) and
   [`../examples/legalbench/COMPARISON.md`](../examples/legalbench/COMPARISON.md).
   Every model scores below its own baseline under `tool` (gpt-5.4 −1.1pp,
   deepseek −7.8pp, gpt-5.4-mini −12.2pp). The kernel does not hand out free
   accuracy: the NL→DDL step, choosing the right query, and mapping
   `O`/`F`/`Ps`/`unknown` back to Yes/No is the bottleneck, and forcing it
   degrades models that already answer well directly.

3. **The damage is in `may` and `must_not`**, not `must`. `must`→`O(X)` is the
   easy mapping and stays high (83–97%). Permission (`may`, needs
   `abduce 'P(X)'` and a permitted→Yes mapping) and prohibition (`must_not`)
   are where the formalization slips — e.g. gpt-4.1 drops to 73% on `may`,
   deepseek to 67% on `must_not`. This is the same false-No / mis-mapping mode
   `RESULTS.md` flagged for gpt-5.4-mini.

4. **More tool calls ≠ better.** deepseek used the most (3.2 calls/example) yet
   landed second-lowest under `tool` and produced 5 unparseable transcripts —
   the long agentic loops that the original LegalBench run also saw it fail to
   close with a clean `ANSWER:` line.

5. **Capability ordering is clearest under stress.** Baselines are bunched
   (89–97%); the `tool` condition spreads them out. **gpt-5.4 is the most robust
   formalizer** (barely moves: 96.7→95.6%), while small/old models lose 9–12pp.
   **gpt-4o (old)** is competitive when answering directly but is the only model
   that can't saturate knn and degrades like the small models on tools —
   consistent with weaker precedent-copying and tool discipline.

## Caveats

- **knn's 100% is partly a benchmark artifact.** The data is synthetic, so the
  precedent pool contains cases that differ from a test item by only a fact or
  two, and structured Jaccard finds them. Real precedent retrieval over prose
  wouldn't be this clean; treat knn as an *upper bound on precedent reuse*, not
  a claim that retrieval beats reasoning in the wild.
- **`tool` is the honest hard setting:** the model formalizes from prose with no
  DDL given. That is the realistic cost of routing through the kernel, and it is
  where the auditability win (a checkable theory + trace) trades against raw
  accuracy on a task models already nearly solve.
- One task, n=90, temperature 0. Per-mode cells are 30 each — read as trends,
  not precise rates. Full per-example transcripts are in `runs/*.jsonl`.

## Reproduce

```bash
# build the reasoner once
export PATH="$HOME/.elan/bin:$PATH" && lake build deontic

# OpenAI models
python eval/ambiguous_contract_llm_experiment.py \
  --models gpt-5.4-mini,gpt-5.4,gpt-4.1,gpt-4o \
  --limit 90 --k 5 --condition baseline,tool,knn \
  --out eval/runs/ambiguous_llm.jsonl --results eval/runs/ambiguous_llm_results.json

# OpenRouter models (needs OPENROUTER_API_KEY)
python eval/ambiguous_contract_llm_experiment.py \
  --models deepseek-v4-flash,grok-4.3 \
  --limit 90 --k 5 --condition baseline,tool,knn \
  --out eval/runs/ambiguous_llm_or.jsonl --results eval/runs/ambiguous_llm_or_results.json
```
