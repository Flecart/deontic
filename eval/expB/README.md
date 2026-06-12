# Experiment B — the commons statute (S2)

Second statute of the multi-statute expansion planned in
`../expA/SCENARIOS.md`: a **shared-resource commons** ("GovSim") statute —
agents drawing compute from a common pool. The deontic skeleton is
**isomorphic to expA's** data-transfer statute (same rule shapes, same 15-pair
superiority pattern, same world-coherence structure → same 56 coherent
worlds): only the domain and the predicates' texture profile change, so
cross-statute comparison isolates *texture* from *structure*.

Atom ↔ expA correspondence and pre-registered texture profile:

| expB atom | expA analog | type | prediction |
|---|---|---|---|
| over_quota | personal_data | artifact (entitlement forms) | closed collapses at T2 |
| allocation_granted | consent | artifact (grant forms) | closed collapses at T2 |
| grant_suspended | revoked | scenario | gist generalizes; small gap |
| essential_workload | emergency | scenario + epistemic bar | necessity test hard for open |
| offset_posted | anonymized | epistemic bar | open depressed; open2 repairs |
| contention | commercial | scenario | gist generalizes; small gap |
| priority_certified | certified | artifact | closed collapses at T2 |

Pipeline files mirror `../expA/` (gen_cases.py / arms.py / score.py /
validate_banks.py / bootstrap_ci.py); verdict = engine status of `draw`,
remedy chain = report ⊗ restore, verdict keys `draw_status` /
`report_required`.

## Reproduce

```bash
python gen_cases.py --out cases_memo.jsonl --n-assignments 48 --seed 2 \
    --variants 2 --narrator openrouter:anthropic/claude-sonnet-4.6
python arms.py --cases cases_memo.jsonl --out results_main.jsonl \
    --models gpt-4.1,gpt-5.4,deepseek-v4-flash,qwen3.6-plus
python score.py --results results_main.jsonl --exclude-leaky cases_memo.jsonl
python bootstrap_ci.py --results results_main.jsonl --cases cases_memo.jsonl
```

Validation gates (must be green before reading results): oracle = gold on
every case; program = 100% verdict at Tier 0 with true-atom recall exactly
100/0/0; leak-flagged cases excluded. Dry run (template narration, $0):
all green — verdict mix 120 obligatory / 102 permitted / 66 forbidden,
identical to expA Stage 2 by isomorphism.
