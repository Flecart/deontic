# Related work survey — AI-to-AI normative benchmarks and adjacent settings

> Surveyed 2026-06-11 via web search before implementing Experiment A. Purpose:
> know the state of the art on (a) LLM + formal-engine normative pipelines,
> (b) rule/policy-application benchmarks, (c) open-texture interpretation,
> (d) multi-agent norm societies, (e) AI dispute resolution, (f) agent-commerce
> infrastructure. Each entry ends with a **Δ** line: what it does *not* cover
> that we do. Single-pass survey, mostly from abstracts — re-verify quotes and
> numbers before camera-ready. §8 preserves our experiment designs (to be moved
> elsewhere).

---

## 1. Closest technical neighbors: LLM grounding + formal engine

These are the papers a reviewer will say "isn't this just X?" about.

- **Language Models and Logic Programs for Trustworthy Tax Reasoning**
  ([arXiv:2508.21051](https://arxiv.org/abs/2508.21051)). LLM + Prolog on SARA:
  statutes semantically parsed into logic programs up front, case facts grounded
  via retrieved exemplars, solver computes liability. Reports dramatic
  improvement over end-to-end LLMs and argues from auditability. **The single
  closest pipeline to ours.** **Δ**: monotonic logic program, no defeasibility /
  exceptions / superiority / compensation / bearers; human tax law (contamination,
  no OOD control); no open-texture variable — SARA statutes were *edited to be
  unambiguous*, i.e. the open-texture problem is defined away rather than studied;
  no dispute/judge loop.

- **On Verifiable Legal Reasoning: A Multi-Agent Framework with Formalized
  Knowledge Representations** ([arXiv:2509.00710](https://arxiv.org/abs/2509.00710)).
  Two-stage: agents formalize statutes into verifiable intermediate
  representations + ontology; case facts mapped to schema; symbolic inference
  derives conclusions. 76.4% vs 18.8% baseline on statutory tax tasks. **Δ**:
  same as above — ontology/symbolic, not defeasible deontic; accuracy framing
  only, no error-anatomy of grounding vs deduction; no novelty tiers; no
  adversarial or multi-agent setting.

- **LOGicalThought: Logic-Based Ontological Grounding of LLMs for High-Assurance
  Reasoning** ([arXiv:2510.01530](https://arxiv.org/pdf/2510.01530)). Neurosymbolic
  architecture: dual symbolic-graph + logic-based context from guidelines, LLM
  inference grounded against it. **Δ**: guideline QA, not norm systems; no
  obligations/violations/remedies; no per-atom audit trail.

- **LogiSafetyBench / LogiSafetyGen — Evaluating Implicit Regulatory Compliance
  in LLM Tool Invocation via Logic-Guided Synthesis**
  ([arXiv:2601.08196](https://arxiv.org/abs/2601.08196)). Converts regulations
  into LTL oracles, logic-guided fuzzing synthesizes 240 verified
  safety-critical tool-use tasks; finds larger models trade compliance for task
  completion. **Methodologically the closest *benchmark-construction* work**:
  formal-spec-as-oracle + synthesized cases = our "gold labels by construction."
  **Δ**: LTL temporal safety, not deontic logic — no defeasibility, permission,
  violation-vs-compensation distinction, no conflicting norms; the LLM is the
  *regulated agent*, not the *fact-grounder/interpreter*; no open-texture
  manipulation (constraints are crisp); single-agent.

- **Reinforcement Learning Guided by Provable Normative Compliance**
  ([arXiv:2203.16275](https://arxiv.org/pdf/2203.16275)). Uses defeasible deontic
  logic (the same Governatori line) as an RL shield. Notably documents that the
  serious DDL implementations (Regorous, RuleRS) are **not publicly available**
  (Data61 copyright); SPINdle ([LGPL](https://research.csiro.au/bpli/tools/spindle/),
  [Lam & Governatori 2009](http://www.governatori.net/papers/2009/ruleml09spindle.pdf))
  covers only the non-deontic standard/modal fragment and is unmaintained.
  **Δ**: no LLM anywhere; symbolic state assumed given (the grounding problem —
  our entire bottleneck per the June postmortem — does not arise).

- **Rules as Code + LLMs**
  ([Law School Policy Review 2025](https://lawschoolpolicyreview.com/2025/02/28/rules-as-code-and-large-language-models/)),
  Catala, OpenFisca, Symboleo, Accord Project. The Rules-as-Code movement
  formalizes the *closed-textured* fragment of law (tax, benefits); the linked
  essay explicitly speculates LLMs "may be of some assistance in scaling up
  Rules as Code systems to address the problem of open texture, although
  detailed testing will be necessary." **Δ**: that "detailed testing" is
  precisely what does not exist — our Experiment A is it.

**Section takeaway**: the pipeline shape (LLM grounds facts → formal engine
decides) now exists in several monotonic-logic variants on human tax law. What
does not exist anywhere in this cluster: defeasible deontic semantics
(exceptions, superiority, compensation, bearers), open texture as a *manipulated
variable*, contamination-free synthetic domains with controlled novelty, and any
dispute/judge mechanism.

## 2. Rule/policy-application benchmarks

- **SARA** ([JHU NLP](https://nlp.jhu.edu/law/); in LegalBench). 9 self-contained
  US tax code sections + 376 hand-crafted cases; ground truth via Prolog.
  Companion result: GPT-3 **fails on simple synthetic statutes it cannot have
  seen in training** — the earliest contamination-controlled evidence that
  statutory reasoning ≠ memorization, and a direct precedent for our synthetic
  move. **Δ**: statutes deliberately disambiguated (closed texture by design);
  no atoms/grounding decomposition; no novelty tiers; single-agent.

- **RuleArena** ([arXiv:2412.08972](https://arxiv.org/pdf/2412.08972)). 95 real
  rules (airline baggage, NBA, tax), 816 problems; LLM applies rules to user
  instances end-to-end. **Δ**: no formal layer at all (rules stay NL); real-world
  rules → contamination; tests computation-heavy application, not interpretation
  under novelty.

- **τ-bench** ([arXiv:2406.12045](https://arxiv.org/pdf/2406.12045)) and the
  [τ-bench extensions](https://toloka.ai/blog/tau-bench-extension-benchmarking-policy-aware-agents-in-realistic-settings/);
  **Effective Red-Teaming of Policy-Adherent Agents**
  ([arXiv:2506.09600](https://arxiv.org/pdf/2506.09600)). Agents must satisfy a
  domain policy document across multi-turn tool use; the red-teaming paper
  attacks policy adherence adversarially (cf. our "open texture as attack
  surface" concern). **Δ**: policy is an NL prompt internalized by the agent —
  no external verifiable layer, no proof of compliance/violation, no dispute
  semantics; the agent is judge of its own compliance.

- **Enforcing Temporal Constraints for LLM Agents**
  ([arXiv:2512.23738](https://arxiv.org/pdf/2512.23738)) — runtime enforcement
  flavor, LTL again. Same Δ as LogiSafetyBench.

**Section takeaway**: rule-following benchmarks measure *the agent's* adherence
to crisp rules. None separate the interpreter role from the decision role, none
score grounding vs deduction separately (our oracle/ground/llm arm design), none
vary description openness.

## 3. Open texture and legal interpretation with LLMs

- Background: Hart's "no vehicles in the park" and
  [Schauer, *On the Open Texture of Law*](http://www.horty.umiacs.io/courses/readings/schauer-2011-open-texture.pdf);
  the [classic exposition](https://thelure.wordpress.com/2014/08/17/no-vehicles-in-the-park/)
  of penumbral cases (rollerblades, the WWII-truck memorial — our Tier-2/Tier-3
  prototypes).
- **Legal interpretation and AI: from expert systems to argumentation and LLMs**
  ([arXiv:2603.05392](https://arxiv.org/pdf/2603.05392)) — survey positioning
  LLMs in the interpretation pipeline; notes judicial experimentation (Judge
  Newsom using ChatGPT on "landscaping" / "physically restrained" — real-world
  evidence that LLM-as-predicate-interpreter is taken seriously by courts).
- **Automating Legal Interpretation with LLMs: Retrieval, Generation, and
  Evaluation** ([arXiv:2501.01743](https://arxiv.org/pdf/2501.01743)) — LLMs
  generating interpretations of vague legal concepts; finds LLMs filter
  relevance of cases to vague concepts at >96%.
- **Rules, Cases, and Reasoning: Positivist Legal Theory as a Framework for
  Pluralistic AI Alignment** ([arXiv:2410.17271](https://arxiv.org/pdf/2410.17271))
  — uses the same Hartian frame (rules + open texture + case law) as an
  *alignment* proposal. Conceptual ally; cite for the framing.
- **Ambiguity Collapse by LLMs: A Taxonomy of Epistemic Risks**
  ([arXiv:2603.05801](https://arxiv.org/pdf/2603.05801)) — LLMs resolve
  ambiguity silently; relevant as a risk citation for the grounding interface
  (our abstention/burden-of-proof fix).

**Section takeaway**: open texture is discussed (theory, surveys, alignment
proposals) and LLM-interpretation is piloted anecdotally, but **no controlled
benchmark exists that varies definition openness (intensional vs extensional)
against instance novelty and measures generalization**. This is the
clearest free square on the board and is exactly Experiment A.

## 4. Multi-agent norm societies (LLM)

- **GovSim — Cooperate or Collapse** ([arXiv:2404.16698](https://arxiv.org/html/2404.16698v2),
  [NeurIPS 2024](https://neurips.cc/virtual/2024/poster/96895)): commons
  sustainability among LLM agents; most models collapse without communication.
  (Our own prior work plugged a DDL statute into GovSim as an institution.)
- **Emergent social conventions and collective bias in LLM populations**
  ([Science Advances 2025](https://www.science.org/doi/10.1126/sciadv.adu9368);
  [arXiv:2410.08948](https://arxiv.org/html/2410.08948v2)): naming-game
  conventions emerge spontaneously; tipping-point dynamics.
- Norm-formation frameworks: **CRSEC**
  ([IJCAI 2024](https://www.ijcai.org/proceedings/2024/0874.pdf)) —
  creation/spreading/evaluation/compliance modules; **Evolution of Social Norms
  in LLM Agents using Natural Language**
  ([arXiv:2409.00993](https://arxiv.org/pdf/2409.00993)); **Social Learning and
  Collective Norm Formation** ([arXiv:2510.14401](https://arxiv.org/pdf/2510.14401)).
- **AgentSociety** ([overview](https://www.emergentmind.com/topics/agentsociety))
  — large-scale societal simulation; claims interaction schemas can encode
  obligations/permissions/sanctions, but as simulation scaffolding, not a
  verifiable reasoner.
- **PIMMUR Principles** ([arXiv:2509.18052](https://arxiv.org/pdf/2509.18052)) —
  validity requirements for LLM-society experiments (Profile, Interaction,
  Memory, Minimal-control, Unawareness, Realism). **Use as a methodological
  checklist for our case generation** (e.g., grounder must not see the
  generator's latent state = Unawareness).
- Privacy/safety in MAS: **Got a Secret? LLM Agents Can't Keep It**
  ([arXiv:2605.27766](https://arxiv.org/html/2605.27766v1)) — confidentiality
  norm violations in multi-agent pipelines; candidate *domain* for our statute
  (data-sharing norms are measurably violated today).
- Classic (pre-LLM) normative MAS: electronic institutions, norm
  representation/enforcement — via [Agentic LLMs survey](https://arxiv.org/pdf/2503.23037)
  and [LLM vs classic MAS](https://arxiv.org/pdf/2509.02515). One-line cite: the
  formal machinery existed; the missing piece was an interpreter for
  open-textured predicates — which is the LLM.

**Section takeaway**: norms in LLM societies are either *emergent conventions*
(no formal layer, no verifiability) or *prompt-injected policies*. Nobody runs a
society against an external formal normative layer with proofs, violations,
remedies, and adjudication. Evaluation surveys
([arXiv:2503.16416](https://arxiv.org/html/2503.16416v2),
[arXiv:2507.21504](https://arxiv.org/html/2507.21504v1)) explicitly flag
policy-compliance evaluation as underdeveloped.

## 5. AI judges and dispute resolution

- **AgentCourt** ([arXiv:2408.08089](https://arxiv.org/pdf/2408.08089)) —
  adversarially evolving lawyer agents, Court-Bench, +12.1% from evolution.
- **AgentsCourt / SimCourt / Chinese court simulation**
  ([arXiv:2508.17322](https://arxiv.org/pdf/2508.17322),
  [AgentsBench](https://www.mdpi.com/2079-8954/13/8/641)) — multi-role courtroom
  simulation for legal judgment prediction; expert-rated quality sometimes above
  real trial participants.
- **Simulating Dispute Mediation with LLM-Based Agents**
  ([AAAI 2026](https://www.zhouyujia.cn/attaches/AAAI2026-Chen2.pdf);
  [arXiv:2509.06586](https://arxiv.org/html/2509.06586v1)) — mediator agent
  between disputants.
- **Agent-as-a-Judge** ([arXiv:2508.02994](https://arxiv.org/pdf/2508.02994)) —
  survey; judging as evaluation paradigm, not normative adjudication.

**Δ for the whole section**: all simulate *human* courts on *human* cases —
contamination and the genre-leakage problem our postmortem quantified (judgments
are post-hoc narratives); verdicts are holistic LLM outputs with no formal
theory, no proof certificates, no precedent mechanism that accretes into a
machine-checkable rule base. The judge's output cannot be replayed or verified.

## 6. Agent-commerce infrastructure and blockchain arbitration

- **Agent payment protocols 2026**: x402 (Coinbase), ACP (OpenAI+Stripe), AP2
  (Google), MPP (Stripe) — see [comparison](https://www.crossmint.com/learn/agentic-payments-protocols-compared),
  [2026 guide](https://www.openhermit.com/blog/ai-agent-payments-guide),
  [AP2 docs](https://ap2-protocol.org/). Industry state: x402 settlements are
  *final* (no recourse); AP2 provides cryptographic mandates as *evidence*;
  dispute frameworks for agent commerce are explicitly named "the big legal
  question of 2026," expected to emerge 2026–27. **Δ**: audit trails without
  reasoning — they can prove *what happened*, not *what was owed*. A normative
  layer with violation/remedy semantics is the named missing piece; strong
  motivation paragraph material.
- **Kleros** ([yellowpaper](https://kleros.io/yellowpaper.pdf);
  [Stanford socio-legal case study](https://law.stanford.edu/publications/kleros-a-socio-legal-case-study-of-decentralized-justice-blockchain-arbitration/))
  — decentralized arbitration: staked human jurors, game-theoretic coherence
  incentives, for "subjective conflicts that smart contracts cannot resolve."
  The blockchain world's own admission that closed rules don't generalize and
  the penumbra must be outsourced — to crowds, at human speed and cost. **Δ**:
  human jurors, no formal norm theory, no reasoned/verifiable rulings; our
  contrast object for "more dynamic than blockchain."
- **Virtual Agent Economies** ([arXiv:2509.10147](https://arxiv.org/abs/2509.10147),
  DeepMind) — the "sandbox economy" frame: agent economies need institutions,
  verifiability, steerability; identifies loophole exploitation and collusion as
  core risks. Agenda paper, no system. **Δ**: we are an instantiation of the
  institutional layer it calls for.
- **Law-Following AI**
  ([Fordham L. Rev. 2025, O'Keefe et al.](https://ir.lawnet.fordham.edu/flr/vol94/iss1/2/);
  critique [arXiv:2509.08009](https://arxiv.org/abs/2509.08009)) — proposal that
  agents be designed to obey law as NL text internalized by the agent; the
  critique argues alignment cannot durably embed legal compliance in weights.
  **Δ**: internalized NL law vs our *external, verifiable* normative layer — the
  critique's objection is precisely an argument for externalization; strong
  positioning cite.

## 7. Gap analysis (the positioning claim)

No existing work combines, and most have none of:

| Capability | §1 pipelines | §2 benchmarks | §4 societies | §5 courts | §6 infra | **Ours** |
|---|---|---|---|---|---|---|
| Defeasible deontic semantics (exceptions, superiority, violation≠falsity, compensation, bearers) | – (monotonic) | – | – | – | – | ✓ |
| LLM-as-interpreter isolated from decision (grounding/deduction split, per-atom audit) | partial | – | – | – | – | ✓ |
| Open texture as manipulated variable (intensional vs extensional defs × novelty tiers) | – | – | – | – | – | ✓ (Exp A) |
| Contamination-free synthetic domain, gold by construction | – (human law) | SARA-synthetic only | – | – | – | ✓ |
| Leakage measured and controlled (pre-verdict scenarios; narrated-variant control) | – | – | – | – | – | ✓ |
| Dispute → judge → precedent accretion into machine-checkable rules | – | – | – | holistic only | named as open | ✓ (Exp B) |
| Proof certificates / replayable rulings | partial | – | – | – | crypto-trail only | ✓ |

One-sentence positioning: *existing work either gives agents crisp rules without
interpretation (smart contracts, LTL benchmarks, Rules-as-Code), or gives them
open-textured norms without verification (policy prompts, emergent conventions,
courtroom simulations); we test the factorization — formal defeasible skeleton,
open-textured atoms, LLM interpreter, accreting precedent — on a
contamination-free AI-to-AI domain where novelty is a controlled variable.*

Risks to our novelty: the §1 cluster is moving fast (three 2025–26 papers);
someone adding "OOD novelty tiers" to a SARA-style pipeline would crowd
Experiment A. The AAAI 2026 mediation paper shows the venue fit but also the
clock. PIMMUR-style validity critiques will apply to our generator — design for
them upfront.

---

## 8. Our planned experiments (parked here for later extraction)

Context: the 10–11 June postmortem showed (i) the deductive layer is sound
(oracle 146/146 — every failure is grounding), (ii) errors compound
multiplicatively (~0.97^k), only flip-set atoms matter, (iii) the worst atom
(`PiMaintainOutweighs`) was a *standard stuffed into an atom* — the holding
elicited as a fact, (iv) the holistic arm partly free-rides on genre leakage in
post-hoc judgment narratives. Design principles below respond point-for-point.

### Experiment A — the predicate generalization curve

Hypothesis: open-textured (intensional) atom descriptions + LLM grounding
generalize to novel instantiations; closed (extensional) descriptions do not;
the engine converts atom-level correctness into verdict-level correctness
without the compounding tax, given staged grounding.

- **Statute**: one AI-to-AI domain in DDL (agent-marketplace contracts or
  inter-agent data-sharing; bearers, exceptions, compensatory chains all occur
  naturally; we are the legislator). 10–20 rules. **Atom-height discipline by
  construction**: every atom answerable by local classification of the scenario;
  all weighing lives in rules + superiority (derived, never elicited).
- **Manipulated variable** — two description regimes per atom:
  *closed* = extensional, enumerates drafting-time instances;
  *open* = intensional with purpose ("any action whose effects are costly to
  reverse for parties other than the actor").
- **Novelty tiers** (cases generated from latent gold atom assignments by a
  different model than the grounder; leak check: scenario must not name the atom
  or echo its description):
  - Tier 0: instances listed in the closed definitions.
  - Tier 1: unlisted near-variants of the same categories.
  - Tier 2: satisfies the intension, far from the extension (adversarially
    generated: "concept applies but no listed example does").
  - Tier 3 (no gold): genuinely penumbral; consistency measurement only.
- **Arms**: closed+engine; open+engine (naive batched grounding); open+engine
  **staged** (engine computes criticality by abducing both verdicts and diffing
  supporting sets; posture atoms first; universe restricted to engaged rules;
  dedicated full-context K=1 calls for flip-set atoms; abstention with
  burden-of-proof thresholds from defeasible semantics); holistic LLM; oracle
  ceiling.
- **Preregistered predictions**:
  1. Atom-level accuracy by tier: closed falls Tier 0→2, open stays ~flat
     (the headline figure; the claim lives at atom level).
  2. Primary endpoint is atom-level OOD accuracy; dispositions reported under
     staged grounding (effective k = |flip set|, not |universe|).
  3. Holistic edge shrinks vs FOIA because scenarios are pre-verdict by
     construction; the **narrated-variant control** (re-render the same case as
     a post-hoc judgment) makes leakage quantitative: llm jumps, ground doesn't.
  4. Dose-response (universe size sweep) replicates; staged grounding flattens it.
  5. Capability scaling: open-defs Tier-2 accuracy slopes up with grounder
     model capability; closed-defs doesn't.
- Scale: ~40 latent assignments × 3 tiers × ~4 paraphrases ≈ 500 instances per
  regime; gold exact, generation cheap.

### Experiment B — standard structuration (the case-law mechanism, instrumented)

Responds to the PiMaintainOutweighs failure and to "both predicate and structure
are true": common law's response to a statutory standard is *gradual
structuration* — tribunals accrete factor lists and weights (cf. the FOIA public
interest test). Plant one deliberate standard (balance atom) in the statute as a
negative control. Initially the judge LLM decides it holistically; after each
decided case the judge may accrete a factor rule + superiority pair (the
amendment loop). Measure on held-out cases, as a function of cases decided:
disposition accuracy, paraphrase flip-rate (consistency), and fraction of
verdicts derivable without invoking the judge. Prediction: the structurated
standard climbs toward the factored arms and flip-rate drops — common-law
convergence as a curve. This also supplies atom-level precedent caching, closing
the determinism gap (deterministic engine + stochastic atoms = stochastic
verdicts) identified in critique.

### Shared threats

- **Headroom**: frontier models may saturate; treat the weak-model regime
  (small grounder + engine ≈ frontier holistic) as a first-class result.
- **Strawman baseline**: closed definitions must be authored as the *best
  possible* operationalization; the closed/open comparison is an ablation with
  identical skeleton, so texture is the only variable.
- **Honest novelty**: Tier-2 generation must produce real novelty, not
  paraphrase — adversarial generation + audit sample; this is where design
  effort goes. PIMMUR (Unawareness, Minimal-control) as checklist.
