# Multi-statute expansion — candidate scenarios

## The size ladder (decided 2026-06-12)

The suite grows along a **statute-size axis** as well as the domain/texture
axis, because size is a confound the current statutes never vary (both have
8 rules) and it carries a sharp, falsifiable prediction:

> **Pre-registered prediction (size axis):** holistic verdict accuracy
> *degrades* as the rule count grows (the whole statute and its superiority
> structure must be held and resolved in prose), while grounded+engine
> accuracy is *flat in statute size at fixed atom count semantics* (each
> atom's interpretation task is unchanged; the engine absorbs the added
> structure exactly). If confirmed, the verdict-layer tax of RQ4 inverts
> with statute size: holistic wins on toy statutes, the factorization wins
> on law-sized law.

Ladder (rules → statute). Narrator: **claude-sonnet-4.6 for all** (user
decision 2026-06-12: narration quality over style variance; the
shared-narrator confound stays disclosed in the paper's limitations rather
than controlled):

| size | statute | domain axis | structure added |
|---|---|---|---|
| 3  | S-3 park (`eval/expC/`, DONE) | Hart's ordinance | difficulty floor |
| 8  | A transfer (`eval/expA/`, DONE) | privacy | compensation chain |
| 8  | B commons (`eval/expB/`, DONE) | GovSim pool | isomorphic control |
| ~12 | S4 agency/delegation (`eval/expD/`, IN PROGRESS) | authority | **multi-bearer** duties, exception depth 5 |
| ~16 | S3 sale of goods | commerce | depth-3 ⊗ chain |
| ~20 | S5+S7 composite (publication + derived works) | content/IP | shared-vocabulary **imports**, two prohibition families |

Authoring budget: ~1 day/statute (banks are the bottleneck; ~90 items each),
~$15–25/run at the stage-2 grid. Per-statute gates unchanged (oracle exact,
program 100/0/0 recall, leak check, bank validation by two non-narrator
families — now including the temporal-scope class of defect caught in expB).

Goal: lift the paper's biggest limitation (one statute) by growing the
benchmark to ~8 statutes that *vary the two axes the thesis lives on*:

- **structural axis** — which defeasible-deontic structures the statute
  exercises (defaults, exception depth, compensation chains, multi-bearer
  directed obligations, burden-like presumptions);
- **texture axis** — the mix of predicate types the per-atom analysis
  identified: *artifact-type* (extensions are object categories; closed
  collapses at Tier 2), *scenario-type* (gist generalizes; closed survives),
  *epistemic-bar* (intension demands unverifiable fact; open struggles until
  evidentiary redraft).

Every scenario below is statute-agnostic for the existing pipeline: write
`statute.ddl` + `descriptions.py` (open/closed/banks/negatives + coherence
constraints), and `gen_cases.py`/`arms.py`/`score.py` run unchanged. Keep
7±2 groundable atoms and ~50–60 coherent worlds per statute so results stay
comparable.

Predicted per-statute profiles are stated up front on purpose: they are
pre-registrable hypotheses, and a statute whose profile *fails* to behave as
predicted is itself a finding.

## S1. Data transfer (existing)

Privacy/GDPR-like. Baseline: mixed texture profile, compensation chain,
exception-to-exception depth 2. Keep as the anchor statute.

## S2. Shared-resource commons (the GovSim statute) — **DONE**: `eval/expB/`

Implemented and run at full stage-2 scale (288 cases × 4 families; see
`eval/expB/RESULTS.md`). Headline replicated (all four Tier-2 gaps positive,
CIs clear of zero). Pre-registered texture profile scored 5/7 — the two
misses (`contention`, `essential_workload`) revealed that *verifiability*
dominates the artifact/scenario axis for system-state predicates; the
`offset_posted` redraft exposed the example-list failure mode of evidentiary
redrafting. Both corrections are in the paper (RQ3).

Agents draw compute/bandwidth/API quota from a common pool. Default
permission to draw; prohibition above fair share; duty to throttle during
contention; emergency exemption for safety-critical workloads;
restore-then-compensate chain for overdraw. Connects directly to the
GovSim/agent-society motivation in the intro.
- Atoms: `over_quota` (program-checkable — good program-arm contrast),
  `essential_workload` (scenario), `contention` (scenario),
  `pool_degraded` (epistemic-bar: "the pool *cannot* serve baseline demand"),
  `delegated_draw`, `offset_posted` (artifact).
- Tier-2 seeds: novel workload kinds (model distillation jobs, speculative
  pre-fetch swarms), quota purchased via secondary markets, draws by spawned
  sub-agents.
- Variance added: quantitative predicates + a *program-favourable* atom; tests
  whether the open-vs-closed gap shrinks when extensions are numeric.

## S3. Agent-to-agent sale of goods/services

Mini sale-of-goods law: duty to deliver conforming output; "merchantable
quality" standard vs closed spec checklist; reject-then-cure-then-refund
compensation chain (depth-3 ⊗ — deeper than S1); inspection-window
exception.
- Atoms: `conforming` (THE classic standard — artifact-type),
  `material_defect`, `timely` (scenario), `cure_offered`,
  `spec_waived`, `paid`.
- Tier-2 seeds: novel deliverable formats (fine-tuned adapters, synthetic
  datasets, agent skills/tools) where the closed spec checklist enumerates
  yesterday's artifact types.
- Variance added: longest compensation chain; the canonical legal standard
  ("merchantable/conforming") rather than a privacy concept.

## S4. Delegation and authority (agency law)

When does a sub-agent's act bind its principal? Default: principal not
bound; bound if within delegated scope; apparent-authority exception;
ratification exception-to-exception; revocation of mandate defeats both.
- Atoms: `within_scope` (open: "in furtherance of the delegated purpose" vs
  closed task-type list), `authority_manifested`, `ratified`,
  `mandate_revoked` (scenario), `third_party_good_faith` (epistemic-bar),
  `sub_delegated`.
- Tier-2 seeds: scope expressed as a goal rather than a task list; authority
  manifested via published capability manifests / signed tool registries;
  ratification by silence in an automated workflow.
- Variance added: **first genuinely multi-bearer statute** (duties land on
  @Principal vs @SubAgent vs @Counterparty) — exercises the engine's
  directed-obligation machinery the paper flags as unexercised.

## S5. Content publication in a shared feed

Default permission to publish; prohibition on deceptive or harm-inciting
content; public-interest/warning exceptions; correct-then-retract-then-
compensate chain; certified-fact-check exception-to-exception.
- Atoms: `deceptive`, `incites_harm`, `public_interest` (all scenario-type,
  deliberately), `correction_issued` (artifact), `factcheck_certified`
  (artifact/epistemic-bar), `satire_framed`.
- Tier-2 seeds: novel deception vectors (synthetic personas, steganographic
  prompts to other agents, simulated provenance chains).
- Variance added: a *scenario-heavy* statute — predicted **small**
  closed-open gap. This is the falsification-friendly statute: if the gap is
  large here too, the artifact/scenario story needs revision.

## S6. Irreversible-action safety statute

Default prohibition on irreversible acts (fund transfer, data deletion,
external email) without confirmation; sandboxed-equivalent exception;
emergency override; certified-runtime exception-to-exception. The
"dangerous tools" statute for agent safety.
- Atoms: `irreversible` (epistemic-bar by design: "cannot reasonably be
  undone"), `confirmed` (artifact: confirmation form types evolve),
  `sandboxed_equivalent` (epistemic-bar), `emergency`, `runtime_certified`
  (artifact), `dry_run_passed`.
- Tier-2 seeds: novel confirmation modalities (delegated approval policies,
  threshold signatures), novel reversibility tech (escrowed sends,
  snapshot-restore guarantees).
- Variance added: epistemic-bar-heavy — predicted to need evidentiary
  redrafts out of the gate; directly stress-tests the RQ3
  verifiability finding and the redraft repair loop.

## S7. Derived works and attribution (IP-like)

Agent reuses another agent's output: default permission with attribution
duty; prohibition on unattributed commercial reuse; transformative-use
exception; license-terms exception-to-exception; attribute-then-compensate
chain.
- Atoms: `derived` (artifact), `attributed` (artifact),
  `transformative` (open: "adds purpose or character beyond the original" —
  famously contested standard), `licensed`, `commercial`,
  `original_public`.
- Tier-2 seeds: derivation via distillation, embedding reuse, style
  transfer, agent-skill recombination — the fastest-moving artifact space
  available; predicted **largest** gap of all statutes.
- Variance added: maximal artifact-type concentration; reuses `commercial`
  from S1 (tests whether atom contracts transfer across statutes — the
  import/namespace story).

## S8. Task market / employment

Agents hiring agents: duty to pay on completion; termination requires
notice-then-severance chain; just-cause exception; urgent-reassignment
override; competence misrepresentation prohibition.
- Atoms: `completed` (artifact: deliverable evidence types),
  `competent_for_task` (open standard vs closed credential list — artifact),
  `just_cause` (scenario), `notice_given`, `urgent_reassignment`
  (scenario), `misrepresented` (epistemic-bar).
- Tier-2 seeds: competence evidenced by eval-harness scores, replayable
  transcripts, staked reputation bonds rather than listed credentials.
- Variance added: bilateral duties (@Hirer/@Worker), and a credentialism
  vs demonstrated-capability framing that is independently interesting for
  agent economies.

## Cross-statute design rules

1. **One shared vocabulary file** for atoms reused across statutes
   (`commercial`, `emergency`, `certified`-style): description = contract,
   merge legal only when contracts match — this exercises the engine's
   import semantics and gives the paper a "norms compose" section.
2. **Pre-register per-statute texture profiles** (S5 small gap, S7 largest,
   S6 redraft-needy) before any LLM run, same as Stage 2's P1–P5.
3. **Budget**: at Stage-2 unit costs (~$0.002/case/arm for gpt-4.1-class),
   7 new statutes × 288 cases × 4 families × 4 arms ≈ affordable; narrate
   with the same third family; reuse `validate_banks.py` per statute.
4. **Report atom-wise**, pooled by predicate type across statutes — the
   headline becomes "the gap tracks predicate texture across 8 domains",
   which is a much stronger claim than any single statute supports.
