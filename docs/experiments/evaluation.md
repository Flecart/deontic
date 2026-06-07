Ignore me if you just want to understand the repo.

# Does the deontic tool actually help? — how to test it

The claim to falsify: **an LLM equipped with the deontic reasoner reaches more
correct, more consistent, more auditable normative conclusions than the same LLM
without it** — and the gap *widens* as the norm set gets larger and more
interlocking (which is exactly where the project aims: agent-society rulebooks).

The mechanism we expect: the LLM's job shrinks to **grounding** (map a concrete
scenario → which element atoms are true — a perception task LLMs are good at);
the **deductive bookkeeping** (exceptions, superiority, exceptions-to-exceptions,
concurrent offences, deadlocks) is offloaded to a deterministic engine — exactly
where LLMs fail. So the experiments should isolate *deduction* from *knowledge
access*.

## Arms to compare (hold the base model + fact-extraction prompt fixed)

1. **LLM-only** — give it the relevant statute text + scenario, ask for the
   conclusion. (Don't starve it: the fairest baseline also gets the rules as an
   in-context numbered list, so we test reasoning, not retrieval.)
2. **LLM + RAG** — same, with retrieval over the corpus.
3. **LLM + deontic** (neuro-symbolic) — LLM grounds the scenario into atoms, the
   engine computes the verdict, the LLM verbalizes it.

## Experiments, ranked by signal-per-effort

1. **Scaling/stress curve (start here).** Generate scenarios at increasing
   interaction depth: 1 offence → + the 6 scriminanti → + exceptions-to-exceptions
   (art. 88 vizio → art. 87 *actio libera*) → + concurrent offences. Plot verdict
   accuracy vs depth for each arm. Prediction: LLM-only degrades with depth; the
   engine arm stays flat. **The widening gap is the evidence.** Cheap to build
   from `examples/codice_penale/` (the engine + a hand-checked sample give gold).
2. **Consistency under paraphrase / fact-order / distractors.** One scenario, N
   paraphrases, reorderings, and added irrelevant facts. Measure answer variance.
   LLM-only is surface/position/distractor sensitive; the engine is invariant once
   grounded. Needs **no gold labels** — self-consistency is the metric.
3. **Calibrated abstention.** Count cases the engine flags `[JUDGE]` (genuine
   deadlock, no superiority) where LLM-only instead confabulates a confident
   single answer. Also count LLM self-contradictions (`O(a)` and `O(~a)`). The
   engine removes these by construction.
4. **Faithfulness vs priors (letter-of-the-law).** Construct scenarios where the
   *codified* answer diverges from the LLM's intuition or mis-remembered law (a
   technically-non-punishable act that "feels" wrong; a rulebook-specific norm).
   Does the system follow the written rules? This is the core value for an
   agent-society where the rulebook is *yours*, not the training-data majority.
5. **Abduction completeness.** "What must be true for X to be permitted?" Compare
   the LLM's enumerated fact-sets to the engine's `abduce` minimal configurations
   (sound + exhaustive over abducibles). Measure precision/recall of the LLM set.
6. **End-to-end agent society (the real target).** Put LLM agents in a
   commons/GovSim-style game under a rulebook, three institution variants: none /
   rulebook-as-NL-prompt (LLM self-adjudicates) / rulebook-as-deontic-theory
   (engine adjudicates violations + sanctions). Measure compliance, commons
   sustainability, sanction consistency, and **exploitability** (can an agent
   argue its way past the LLM-judge but not the engine?). A "rule-by-law GovSim"
   run already exists in `~/Desktop/work/prosocial-agents` — lean on it.

## Metrics

Verdict accuracy / F1 vs gold · answer variance (consistency) · abstention
precision (`[JUDGE]` vs forced-wrong) · self-contradiction rate · faithfulness on
prior-divergent items · abduction recall · end-to-end commons/compliance/exploit
rate · **all divided by cost** (tokens + latency the engine step adds).

## Controls & honest caveats

- **Split the two error sources** in arm 3: grounding error (LLM picks wrong
  atoms) vs deduction (engine). Report grounding accuracy separately — it bounds
  the neuro-symbolic ceiling and tells you where to invest.
- The neuro-symbolic system is only as right as **(a) the encoded theory** and
  **(b) the grounding**. A wrong theory makes the engine *confidently* wrong —
  so also evaluate the authoring loop (does `prompts/law-to-ddl.md` produce
  correct theories? round-trip a held-out statute and check).
- Beware circularity: don't score the engine against `tests.sh` (those are the
  theory's own outputs). Use independent vignettes with externally-known answers.
- Report where the engine *doesn't* help: shallow single-rule questions, or
  scenarios dominated by open-textured terms the grounding must judge anyway.
