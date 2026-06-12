"""Experiment B atom material: the shared-resource commons statute (S2).

Same schema as eval/expA/descriptions.py — per atom:
  open         intensional description (mirrors statute.ddl; gold truth)
  closed       extensional drafting-time enumeration of instance categories
  closed_items Tier-0 instantiations; ids are ALSO the program arm's lookup
  tier1        unlisted near-variants of listed categories
  tier2        world-shift instances: satisfy the intension, outside every
               listed category
  negative     clear non-instances incl. hard negatives (late holds, deposits
               smaller than the draw, self-declared standing)

Texture profile (pre-registered, see eval/expA/SCENARIOS.md S2):
  artifact-type: over_quota, allocation_granted, priority_certified
  scenario-type: grant_suspended, essential_workload, contention
  epistemic-bar: offset_posted ("pool no worse off" is a guarantee)

Items are (id, phrase). Phrases must never name an atom or echo either
description (gen_cases.py leak check enforces n-gram disjointness).
"""

GROUNDABLE = ["over_quota", "allocation_granted", "grant_suspended",
              "essential_workload", "offset_posted", "contention",
              "priority_certified"]

ATOMS = {
  "over_quota": {
    "open": ("the requested draw would take more of the shared pool than the "
             "drawer's standing entitlement for the period, however that "
             "entitlement is expressed or measured"),
    "closed": ("the requested draw exceeds at least one of: the drawer's "
               "monthly accelerator-hour cap; its daily API-call cap; its "
               "storage byte cap; its network bandwidth cap; its "
               "concurrent-job slot count; its reserved wall-clock window; "
               "its monthly token budget; its metered energy budget"),
    "closed_items": [
      ("gpu_hours",       "a request for 1,400 accelerator-hours this month against the team's standing figure of 900"),
      ("api_calls",       "a planned burst of 2.1 million calls today where the team's daily ceiling on file reads 500,000"),
      ("storage_bytes",   "a write of 80 TB into the shared store, four times the 20 TB the team is booked for"),
      ("bandwidth",       "a transfer plan needing 40 Gbps of the shared interconnect, double the team's listed 20 Gbps ceiling"),
      ("job_slots",       "a launch of 96 simultaneous jobs where the team's slot count on file is 32"),
      ("reserved_window", "a run scheduled to hold the machines nine hours past the end of the team's reserved window"),
      ("token_budget",    "a batch consuming five billion tokens this month against the team's listed two billion"),
      ("energy_budget",   "a training run drawing 1.2 MWh against the team's metered monthly figure of 0.5 MWh"),
    ],
    "tier1": [
      ("tpu_hours",       "a request for 1,100 tensor-unit hours this month where the team's standing figure covers 700"),
      ("rpm_limit",       "a sustained 9,000 requests per minute against the 2,000-per-minute line in the team's terms"),
      ("vector_index",    "an index build adding 35 TB of embedding shards where the team is booked for 10 TB"),
      ("registry_pulls",  "a nightly mirror pulling 12 TB from the artifact registry, six times the team's listed line"),
    ],
    "tier2": [
      ("credit_balance",  "a job priced at 30,000 pool credits under the new internal metering currency, where the team's wallet holds 9,000"),
      ("fractional_lease","a run claiming six tenths of the cluster under the fractional-stake scheme, where the stake the team bought at auction is two tenths"),
      ("carbon_budget",   "a training run whose emissions entry would use 18 tonnes of the site's shared carbon envelope, the team's slice standing at 5"),
      ("compute_futures", "a reservation of 600 forward compute-hour contracts for next week where the team holds contracts for 200"),
      ("beacon_rate",     "a sampling job reading the shared randomness beacon at fifty times the per-team rate set in the beacon charter"),
    ],
    "negative": [
      ("within_cap",      "a request for 300 accelerator-hours this month against the team's standing figure of 900"),
      ("raised_cap",      "a request for 1,200 accelerator-hours, made after the operator lifted the team's monthly figure to 1,500 last week"),
      ("private_rig",     "a 2,000-hour run on the team's own privately purchased rack, touching nothing shared"),
    ],
  },

  "allocation_granted": {
    # "at some point granted ... covering this category" failed independent
    # bank validation: both annotator families correctly held that a LAPSED
    # voucher still demonstrates a past grant. Temporal scope added (audit
    # loop, pre-main-run): the grant must cover the period of the draw.
    "open": ("the pool operator, or a delegate the operator empowered to "
             "allocate, granted this drawer an entitlement that covers this "
             "category of draw and the period of the draw, in any form that "
             "demonstrates the grant"),
    "closed": ("one of the following is on file: a capacity voucher signed by "
               "the pool operator; an approved cap-increase ticket in the "
               "operator's tracker; a resource lease countersigned by the "
               "operator; an operator-issued access token scoped to the extra "
               "draw"),
    "closed_items": [
      ("signed_voucher",      "a voucher the pool operator signed in March covering exactly this extra draw, kept on file"),
      ("approved_ticket",     "the cap-increase ticket the team filed, marked approved by the operator in the tracker"),
      ("countersigned_lease", "a lease covering this class of run, countersigned by the operator, current through next year"),
      ("scoped_token",        "an access token the operator minted for the team, scoped to exactly this kind of run"),
    ],
    "tier1": [
      ("esigned_voucher",     "a voucher the operator e-signed through the document portal in April, covering the run"),
      ("chat_approval",       "a message in the ops channel in which the operator replies 'approved' to the team's request for this run"),
      ("renewal_countersigned","last year's lease, renewed and countersigned by the operator last month"),
    ],
    "tier2": [
      ("delegate_agent_grant","an approval issued by the operator's scheduling agent, acting under a mandate the operator gave it for exactly such decisions"),
      ("onchain_allowance",   "a transferable allowance token assigned to the team on the consortium ledger, verified against the operator's signing key"),
      ("policy_as_code_merge","a rule the operator merged into the pool's configuration repository listing the team's run as covered"),
      ("auction_win",         "a winning bid in the pool's monthly capacity auction, settled and recorded under the team's name"),
    ],
    "negative": [
      ("pending_ticket",      "a cap-increase ticket the team filed two weeks ago that still sits unreviewed"),
      ("other_team_voucher",  "a voucher naming a different team than the one now asking"),
      ("expired_voucher",     "a voucher for such runs that lapsed at the end of last quarter"),
    ],
  },

  "grant_suspended": {
    "open": ("a previously granted entitlement covering this draw was "
             "suspended or withdrawn before the draw, through any channel by "
             "which the drawer receives operator communications"),
    "closed": ("one of: a written hold notice received from the operator; the "
               "voucher marked void in the operator's tracker; the drawer's "
               "access token disabled by the operator"),
    "closed_items": [
      ("hold_notice",     "a notice received last week in which the operator puts the team's earlier go-ahead on hold"),
      ("voucher_voided",  "the March voucher, marked void in the operator's tracker since Monday"),
      ("token_disabled",  "the team's access token, switched off by the operator yesterday"),
    ],
    "tier1": [
      ("ops_email_stop",  "an email from the operator's desk telling the team its extra-draw arrangement is paused pending review"),
      ("pinned_channel_stop","a pinned message in the ops channel from the operator naming the team's arrangement as on hold"),
      ("verbal_stop_call","a recorded call from Tuesday in which the operator tells the team the arrangement is off for now"),
    ],
    "tier2": [
      ("watchdog_freeze", "a signed stop notice broadcast by the operator's automated watchdog agent after it flagged anomalous usage, received before the run"),
      ("ledger_frozen",   "the team's allowance token frozen on the consortium ledger by the operator's contract last Friday"),
      ("policy_diff_stop","a signed change the operator merged into the pool's configuration repository striking the team's run from the covered list"),
    ],
    "negative": [
      ("late_hold",       "a hold notice that arrived three days after the run at issue had already finished"),
      ("considering_only","meeting minutes noting the operator is weighing a clampdown on heavy users, with no decision recorded"),
      ("other_team_hold", "a notice putting a different team's arrangement on hold"),
    ],
  },

  "essential_workload": {
    "open": ("the draw is necessary to prevent imminent and serious harm to "
             "people or to the integrity of safety-critical systems, and the "
             "harm cannot reasonably be averted without the draw"),
    # evidentiary redraft (mirrors expA emergency open2): present threat +
    # the draw presented as the means of averting it
    "open2": ("a present, time-critical threat to people or to safety-critical "
              "systems exists, the requested draw is the means presented for "
              "averting it, and nothing indicates the harm could reasonably "
              "be averted without it"),
    "closed": ("one of: a hospital triage assistant kept running during a "
               "mass-casualty event; storm-path forecasting during an active "
               "severe-weather warning; dispatch routing for emergency "
               "services during an outage; rollback of a corrupted control "
               "system that operates safety equipment"),
    "closed_items": [
      ("triage_surge",    "clinicians stating the hospital's intake-sorting assistant must stay up through tonight's mass-casualty influx, and this run is what keeps it answering"),
      ("storm_forecast",  "forecasters stating this run drives the storm-track updates feeding the coastal warning system during the active alert"),
      ("dispatch_routing","the ambulance dispatch service stating its routing engine fails over to these machines within the hour unless the run proceeds"),
      ("safety_rollback", "site engineers stating the run rebuilds the corrupted controller database that operates the plant's pressure-relief systems, before the stale copy acts"),
    ],
    "tier1": [
      ("wildfire_model",  "fire command stating the run computes the spread projections steering tonight's evacuation of two hillside districts"),
      ("bridge_reroute",  "the city's ambulance fleet coordinator stating the run re-plans response routes around this morning's bridge failure"),
    ],
    "tier2": [
      ("worm_containment","the network defense agent stating the run fingerprints and walls off a worm now hopping between agent hosts, before it reaches the control segment"),
      ("key_recovery",    "the security team stating the run re-derives signing keys after a compromise, without which tonight's safety dispatch messages cannot be trusted"),
      ("grid_balancing",  "the regional grid operator's agent stating the run computes the load-shedding schedule needed within the hour to keep the medical district powered"),
    ],
    "negative": [
      ("quarterly_deadline","a product lead pressing to finish a quarterly forecast before Friday's board meeting"),
      ("demo_pressure",   "a sales team wanting the machines for a high-profile customer demonstration tomorrow"),
      ("offpeak_alternative","a batch job whose own runbook notes it could equally run in next weekend's idle window"),
    ],
  },

  "offset_posted": {
    "open": ("before the draw the drawer put in place a replenishment that "
             "leaves the pool no worse off for the period than if the draw "
             "had not occurred, and the replenishment cannot be quietly "
             "withdrawn"),
    # evidentiary redraft (mirrors expA anonymized open2): judges the described
    # step and its recording, not an unprovable guarantee
    "open2": ("before the draw the drawer carried out a make-good step (such "
              "as depositing reserve capacity, a confirmed top-up purchase, "
              "or a transferred unused share) whose described size covers the "
              "draw, recorded or escrowed so it cannot be quietly withdrawn; "
              "promises, post-draw plans, or deposits smaller than the draw "
              "defeat this condition"),
    "closed": ("one of: equivalent accelerator-hours deposited into the pool "
               "from the drawer's private reserve; a paid capacity top-up "
               "confirmed by the provider before the draw; an equivalent "
               "unused share transferred from another team with the "
               "operator's confirmation"),
    "closed_items": [
      ("reserve_deposit",  "hours from the team's own private rack signed over to the shared store ahead of the run, matching it hour-for-hour, logged by the scheduler"),
      ("paid_topup",       "a top-up order with the cloud provider, paid and confirmed last week, adding to the pool what the run will take"),
      ("transferred_share","an unused share signed over from a sister team, with the operator's written confirmation, sized to cover the run"),
    ],
    "tier1": [
      ("tpu_deposit",      "tensor-unit hours from the team's own pod signed over to the pool before launch, sized to cover the run"),
      ("spot_confirmed",   "a confirmed spot-market purchase earmarked to the pool, booked to land before the run begins and covering its full size"),
    ],
    "tier2": [
      ("escrow_autobuy",   "an escrowed contract, visible on the consortium ledger and funded before the run, that automatically buys matching capacity the moment pool usage crosses its trigger"),
      ("idle_cycles_proof","a scheduler trace, checkable by anyone, showing the run claims only cycles that would otherwise sit idle and is evicted automatically the moment paying demand appears"),
      ("demand_shift_lock","a signed scheduling change, locked in the cluster calendar, moving the team's other workloads out of the period and freeing more than the run will take"),
    ],
    "negative": [
      ("promise_next_quarter","a note from the team promising to give back matching hours sometime next quarter"),
      ("smaller_deposit",  "a deposit of 200 hours against a run that will take 1,400"),
      ("post_draw_topup",  "a top-up purchased two days after the run at issue had finished"),
    ],
  },

  "contention": {
    "open": ("at the time of the draw the shared pool cannot serve all "
             "entitled demand, so an additional draw would displace or "
             "degrade other participants' entitled workloads"),
    "closed": ("one of: a red capacity alert declared by the operator; the "
               "job queue beyond its published limit; brownout throttling "
               "active on the cluster; a posted maintenance window cutting "
               "available capacity"),
    "closed_items": [
      ("red_alert",        "the operator's red banner, up since dawn, warning that the cluster cannot absorb further work"),
      ("queue_over_limit", "a job queue running since morning at triple the length the operator's dashboard marks as its limit"),
      ("brownout_throttle","brownout slowdowns, active since last night, already stretching every team's jobs"),
      ("maintenance_window","a posted maintenance window that has taken half the racks offline through Thursday"),
    ],
    "tier1": [
      ("amber_to_critical","the operator's amber banner, escalated to critical at noon today"),
      ("wait_times_blown", "queue waits stretching past four hours where the posted service line is twenty minutes"),
    ],
    "tier2": [
      ("preemption_storm", "an autoscaler oscillation since midnight, evicting and rescheduling jobs in waves across the cluster"),
      ("subagent_swarm",   "a swarm of newly spawned sub-agents from another project, multiplying demand on the cluster tenfold overnight"),
      ("energy_curtailment","a regional power-curtailment order that has the site running at a third of normal supply since yesterday"),
    ],
    "negative": [
      ("light_load",       "the cluster ticking along at forty percent usage, queues clearing within minutes"),
      ("other_pool_jam",   "a jam reported on the storage farm across the campus, separate from this cluster"),
      ("resolved_yesterday","last week's crunch, fully cleared by Tuesday according to the operator's notice"),
    ],
  },

  "priority_certified": {
    "open": ("the drawer demonstrably holds a standing that the pool's rules "
             "recognize as entitling it to draw during shortage, through "
             "certification, binding agreement or verifiable technical "
             "guarantee"),
    "closed": ("one of: a current platinum-tier standing document issued by "
               "the pool consortium; a signed first-in-line rider in the "
               "drawer's resource lease; a listing in the operator's "
               "published register of protected services"),
    "closed_items": [
      ("platinum_doc",     "the team's platinum-tier standing document from the consortium, renewed this January"),
      ("lease_rider",      "a first-in-line rider in the team's lease, signed by both sides, current through next year"),
      ("protected_register","the team's listing in the operator's published register of protected services"),
    ],
    "tier1": [
      ("gold_doc",         "the team's gold-tier standing document from the consortium, current and expressly covering crunch periods"),
      ("annex_renewal",    "a front-of-queue annex countersigned when the team's lease renewed last month"),
    ],
    "tier2": [
      ("zk_class_proof",   "a cryptographic proof the team supplies, checkable by anyone, that its workload class is among those the pool charter puts first during a crunch, revealing nothing else"),
      ("staked_bond",      "a bond the team staked on the consortium ledger, forfeited automatically if it draws out of turn, recognized by the pool charter as front-of-queue standing"),
      ("auditor_assessment","a signed assessment from the consortium's accredited auditor agent placing the team's service in the protect-first class"),
    ],
    "negative": [
      ("expired_doc",      "a standing document of the team's that lapsed fourteen months ago"),
      ("self_declared_flag","a 'must-run' label the team sets on its own jobs"),
      ("other_pool_standing","front-of-queue standing the team holds in a different region's pool"),
    ],
  },
}

# Neutral filler facts; narration may weave 1-2 in. Never affect any atom.
FILLER = [
    "the request arrived through the scheduler's standard queue with a reference number",
    "the two teams have shared the cluster without incident for two years",
    "the run is part of the project's second-quarter plan",
    "the job would execute in the usual containerized environment",
    "the team asked for its logs to be mirrored to its own dashboard",
]

# Leak check: scenario prose must not contain atom names or any of these stems
# (statute vocabulary). Description 5-gram disjointness is checked separately.
BANNED_STEMS = [
    "over quota", "over_quota", "quota", "entitle", "allocat",
    "suspend", "revok", "essential", "offset", "replenish",
    "contention", "saturat", "priorit", "certif", "make-whole",
    "make whole", "commons", "statute", "obligat", "prohibit",
    "permitted", "forbidden", "violat",
]


# Category noun phrases aligned 1:1 with closed_items order, for the
# extension-size sweep: build_closed(atom, k) re-drafts the closed description
# with only the first k categories enumerated.
CLOSED_CATEGORIES = {
  "over_quota": ["the drawer's monthly accelerator-hour cap",
                 "its daily API-call cap", "its storage byte cap",
                 "its network bandwidth cap", "its concurrent-job slot count",
                 "its reserved wall-clock window", "its monthly token budget",
                 "its metered energy budget"],
  "allocation_granted": ["a capacity voucher signed by the pool operator",
                         "an approved cap-increase ticket in the operator's tracker",
                         "a resource lease countersigned by the operator",
                         "an operator-issued access token scoped to the extra draw"],
  "grant_suspended": ["a written hold notice received from the operator",
                      "the voucher marked void in the operator's tracker",
                      "the drawer's access token disabled by the operator"],
  "essential_workload": ["a hospital triage assistant kept running during a mass-casualty event",
                         "storm-path forecasting during an active severe-weather warning",
                         "dispatch routing for emergency services during an outage",
                         "rollback of a corrupted control system that operates safety equipment"],
  "offset_posted": ["equivalent accelerator-hours deposited into the pool from the drawer's private reserve",
                    "a paid capacity top-up confirmed by the provider before the draw",
                    "an equivalent unused share transferred from another team with the operator's confirmation"],
  "contention": ["a red capacity alert declared by the operator",
                 "the job queue beyond its published limit",
                 "brownout throttling active on the cluster",
                 "a posted maintenance window cutting available capacity"],
  "priority_certified": ["a current platinum-tier standing document issued by the pool consortium",
                         "a signed first-in-line rider in the drawer's resource lease",
                         "a listing in the operator's published register of protected services"],
}

CLOSED_INTROS = {
  "over_quota":         "the requested draw exceeds at least one of: ",
  "allocation_granted": "one of the following is on file: ",
  "grant_suspended":    "one of: ",
  "essential_workload": "one of: ",
  "offset_posted":      "one of: ",
  "contention":         "one of: ",
  "priority_certified": "one of: ",
}


def build_closed(atom: str, k: int) -> str:
    """Closed description re-drafted with only its first k enumerated
    categories (k >= len(categories) reproduces the full closed description)."""
    cats = CLOSED_CATEGORIES[atom][: max(1, k)]
    return CLOSED_INTROS[atom] + "; ".join(cats)


def english_statute(regime: str) -> str:
    """Plain-English rendering of statute.ddl for the holistic arm.

    Faithful to rules + superiority; predicate content comes from the given
    regime's descriptions, so holistic sees exactly what the grounded arms see.
    """
    d = {a: ATOMS[a][regime] for a in GROUNDABLE}
    return f"""SHARED COMPUTE POOL STATUTE

Definitions (each condition holds exactly when its definition is met):
- EXCESS: {d['over_quota']}.
- GRANTED: {d['allocation_granted']}.
- HALTED: {d['grant_suspended']}.
- CRITICAL: {d['essential_workload']}.
- MADEGOOD: {d['offset_posted']}.
- CONGESTED: {d['contention']}.
- FIRSTLINE: {d['priority_certified']}.

Sections (a later-listed "notwithstanding" clause states which section prevails):
S0. Draws from the pool are permitted by default.
S1. If EXCESS, the draw is forbidden, notwithstanding S0. A drawer who draws
    in breach of S1 must file a draw report with the pool registry stating the
    draw and its size; failing that, the drawer must return equivalent
    capacity to the pool at the scheduled make-good rate.
S2. If GRANTED, the draw is permitted, notwithstanding S1.
S3. If HALTED, the draw is forbidden, notwithstanding S0, S2 and S7.
S4. If CRITICAL, the draw is obligatory, notwithstanding S1, S3 and S6.
S5. If MADEGOOD, the draw is permitted, notwithstanding S1, S3 and S6.
S6. If CONGESTED, the draw is forbidden, notwithstanding S0 and S2.
S7. If GRANTED and FIRSTLINE, the draw is permitted, notwithstanding S1 and S6.
"""
