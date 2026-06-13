"""Experiment E atom material: sale of goods (S3). Artifact-heavy texture rung.

Narrative frame: an automated buyer agent ordered a digital deliverable
(dataset, model, compute service, software asset) from a seller agent; the
file reviews the delivered item against the order. Each case is one delivery;
the question is the buyer's duty to `accept`.

Texture profile (pre-registered — we predict a LARGE open-closed gap, the
opposite pole from agency statute D):
  artifact-type (quality standards, closed predicted to collapse at Tier 2):
      conforming, merchantable, material_defect, fitness_breached
  scenario-type: cure_offered, accepted_by_use, as_is, late_essential
  epistemic-bar: latent_defect (a defect inspection would not reveal)

World coherence (gen_cases.valid_assignments):
  not merchantable    => material_defect   (an unmerchantable good is a defect)
  latent_defect       => material_defect
  fitness_breached    => material_defect
  conforming+merchantable => not material_defect

`conforming` and `merchantable` are ALWAYS instantiated (every delivery has a
conformity and a quality character); the others appear when true, with
negatives drawn for the false ones.
"""

GROUNDABLE = ["conforming", "merchantable", "material_defect",
              "fitness_breached", "cure_offered", "accepted_by_use",
              "latent_defect", "as_is", "late_essential"]

ATOMS = {
  "conforming": {
    "open": ("the delivered item matches what the contract called for in "
             "kind, quantity and described characteristics"),
    "closed": ("the delivery matches the order on each stated item: the "
               "agreed file format; the agreed record count; the agreed "
               "schema or field list; the agreed version or release; the "
               "agreed unit quantity; the agreed resolution or precision"),
    "closed_items": [
      ("format_match",   "the dataset arrived in the parquet format named in the order"),
      ("count_match",    "the delivery contained the ordered 10,000 labelled records exactly"),
      ("schema_match",   "every field listed in the order's schema is present and correctly typed"),
      ("version_match",  "the library shipped at the exact release tag the order specified"),
      ("quantity_match", "all 500 ordered API seats were provisioned"),
      ("precision_match","the sensor logs arrived at the ordered millisecond resolution"),
    ],
    "tier1": [
      ("superset_schema","the dataset carries every ordered field plus two extra columns, the ordered ones all present"),
      ("minor_count",    "the delivery holds 10,000 records as ordered, supplied across two files rather than one"),
    ],
    "tier2": [
      ("tool_signature", "the ordered agent skill exposes exactly the tool call signatures and return types the order specified"),
      ("eval_spec_hit",  "the fine-tuned model reproduces, on the order's held-out probe set, the exact capability profile the contract enumerated"),
      ("proof_carrying", "the delivered pipeline ships with a machine-checkable certificate that it computes precisely the transformation the order described"),
    ],
    "negative": [
      ("wrong_format",   "the order asked for parquet but the data arrived as a pile of loose CSVs"),
      ("short_count",    "the order was for 10,000 records; 6,200 were delivered"),
      ("wrong_version",  "a build two major versions behind the one the order named was shipped"),
    ],
  },

  "merchantable": {
    "open": ("the item is of a quality a reasonable buyer in this trade would "
             "accept as sound and usable for the ordinary purposes such items "
             "serve, judged by trade expectation rather than by any fixed "
             "checklist"),
    "closed": ("the item meets each baseline quality mark for its trade: no "
               "corrupt or unreadable records; passes the standard validation "
               "suite; free of known defects on the public tracker; documented "
               "to the trade's usual standard; runs without error on a "
               "reference setup"),
    "closed_items": [
      ("no_corrupt",      "every record opens and parses cleanly, none truncated or garbled"),
      ("passes_suite",    "the package clears the trade's standard validation battery"),
      ("no_known_defects","nothing outstanding against it on the public issue tracker"),
      ("documented",      "shipped with the API reference and changelog buyers in this trade expect"),
      ("runs_clean",      "installs and runs end to end on a clean reference machine without errors"),
    ],
    "tier1": [
      ("passes_newer_suite","clears the newer community validation harness that superseded the standard one"),
      ("clean_on_arm",    "runs without error on the reference setup and on the now-common ARM build too"),
    ],
    "tier2": [
      ("no_prompt_injection","the delivered agent tool is free of the prompt-injection foothold that a competent buyer in this trade now treats as a soundness failing"),
      ("calibrated_uncertainty","the model returns the calibrated confidence signals that buyers in this trade have come to expect a sound model to provide"),
      ("reproducible_build","the artifact rebuilds bit-for-bit from source, the provenance guarantee this trade now treats as basic soundness"),
    ],
    "negative": [
      ("corrupt_rows",    "roughly one record in twenty is truncated mid-line and will not parse"),
      ("fails_suite",     "the package fails a third of the trade's standard validation checks"),
      ("undocumented_panic","it crashes on first run with an undocumented stack trace and ships with no reference at all"),
    ],
  },

  "material_defect": {
    "open": ("the item falls short of what was promised seriously enough that "
             "a reasonable buyer would not have closed the deal had they "
             "known"),
    "closed": ("the shortfall is one the trade treats as deal-defeating: the "
               "core promised function is missing or broken; the data is "
               "wrong often enough to be unusable; a security flaw exposes the "
               "buyer; the licence does not actually permit the agreed use"),
    "closed_items": [
      ("core_broken",    "the one capability the buyer ordered the model for does not work at all"),
      ("data_wrong",     "a third of the labels are simply incorrect, making the set useless for training"),
      ("security_hole",  "the library ships a remote-code-execution hole that would expose the buyer's systems"),
      ("license_blocks", "the licence forbids exactly the commercial use the order was placed for"),
    ],
    "tier1": [
      ("perf_cliff",     "the service collapses under the everyday load the order was sized for, unusable in practice"),
      ("dep_conflict",   "it cannot be installed alongside the platform the order named it would run on"),
    ],
    "tier2": [
      ("training_poison","the dataset carries a poisoned subset that silently implants a backdoor in any model trained on it"),
      ("eval_overfit",   "the model's ordered scores were obtained by fitting the public benchmark itself, so it fails on the buyer's real distribution"),
      ("agent_exfil",    "the delivered agent quietly forwards the buyer's task data to a third-party endpoint on every run"),
    ],
    "negative": [
      ("cosmetic_typo",  "a few typos in the documentation, the software itself unaffected"),
      ("minor_slowdown", "about five percent slower than the brochure suggested, comfortably within the buyer's needs"),
      ("spare_field",    "one unused legacy column the buyer will simply ignore"),
    ],
  },

  "fitness_breached": {
    "open": ("the buyer made a particular use of the item known to the seller "
             "and relied on the seller's judgment, and the item does not "
             "serve that use"),
    "closed": ("the buyer's stated special purpose is one the item fails: "
               "named for a regulated domain it is not certified for; named "
               "for a scale it cannot handle; named for a platform it does "
               "not support; named for a downstream task it cannot drive"),
    "closed_items": [
      ("regulated_use",  "the buyer told the seller the data was for a clinical-decision product; it lacks the provenance such use legally requires"),
      ("scale_use",      "the buyer specified it must serve nationwide traffic; it falls over above a single region"),
      ("platform_use",   "the buyer said it had to run on their edge devices; it needs a datacentre GPU"),
      ("task_use",       "the buyer said the model was to power live translation; its latency makes that impossible"),
    ],
    "tier1": [
      ("adjacent_reg",   "the buyer named a medical-device pipeline; the item lacks the equivalent certification that domain now requires"),
      ("throughput_use", "the buyer specified real-time fraud scoring; the model cannot keep up with the stream"),
    ],
    "tier2": [
      ("agent_loop_use", "the buyer told the seller it would drive an autonomous purchasing loop; the model's hallucination rate makes unsupervised use unsafe for that"),
      ("composability_use","the buyer said it had to chain behind three other agents; it ignores the hand-off protocol they all rely on"),
      ("on_device_privacy","the buyer required it run fully on-device for privacy; it silently phones home to function"),
    ],
    "negative": [
      ("no_purpose_stated","the buyer never told the seller any particular use; it works for ordinary purposes"),
      ("buyer_own_judgment","the buyer picked it against the seller's advice, relying on its own assessment"),
      ("fit_met",        "the buyer's stated purpose was bulk archival, which the item serves perfectly well"),
    ],
  },

  "cure_offered": {
    "open": ("before the buyer's remedy crystallised the seller offered, "
             "within any time the contract allows, to repair or re-deliver at "
             "its own cost"),
    "closed": ("the seller made a concrete cure offer in time: a patched "
               "release; a corrected re-delivery; a free repair within the "
               "agreed window; a replacement unit at the seller's expense"),
    "closed_items": [
      ("patch_offered",  "the seller offered a patched build the same day, free of charge"),
      ("redelivery",     "the seller offered to re-export the dataset corrected, at its own cost, within the window the order allows"),
      ("free_repair",    "the seller offered to fix the fault on site within the agreed repair period"),
      ("replacement",    "the seller offered a fresh replacement unit at no charge"),
    ],
    "tier1": [
      ("hotfix_branch",  "the seller pushed a hotfix branch and offered to merge it for the buyer within hours"),
      ("staged_recut",   "the seller offered a staged re-cut of the deliverable over the next two days at its expense"),
    ],
    "tier2": [
      ("auto_rollback",  "the seller's deployment agent offered, within the window, to auto-roll-forward a corrected artifact the moment the buyer approved"),
      ("escrow_redo",    "the seller offered to fund a third party from escrow to redo the work to spec at no cost to the buyer"),
    ],
    "negative": [
      ("offer_too_late", "the seller offered a fix two weeks after the buyer had already turned the delivery away and moved on"),
      ("offer_at_cost",  "the seller offered to fix it only if the buyer paid the repair bill"),
      ("vague_promise",  "the seller said it would 'look into it sometime' with no concrete remedy"),
    ],
  },

  "accepted_by_use": {
    "open": ("after a reasonable chance to inspect, the buyer used, resold or "
             "kept the item in a way that signals it took the item as its "
             "own"),
    "closed": ("the buyer acted as owner after inspection: deployed it to "
               "production; resold it on; built dependent work on it; let the "
               "return window lapse in silence"),
    "closed_items": [
      ("deployed_prod",  "the buyer pushed the delivered model into its live production service"),
      ("resold",         "the buyer packaged the dataset into its own product and sold it onward"),
      ("built_on",       "the buyer shipped three features that depend on the delivered library"),
      ("window_lapsed",  "the buyer let the inspection window pass without a word"),
    ],
    "tier1": [
      ("staged_canary",  "the buyer ran it as a canary serving real users for a fortnight, then said nothing"),
      ("fine_tuned_on",  "the buyer fine-tuned its own model on the delivered set and shipped the result"),
    ],
    "tier2": [
      ("agent_dependency","the buyer's autonomous workflow has been routing live traffic through the delivered tool for two weeks"),
      ("onchain_settled","the buyer's settlement agent released final payment from escrow and closed the order on the ledger"),
    ],
    "negative": [
      ("sandbox_test",   "the buyer ran it only in an isolated sandbox to evaluate it, never in production"),
      ("prompt_inspect", "the buyer flagged the problem within a day of delivery, before using it for anything"),
      ("quarantined",    "the buyer quarantined the delivery pending the seller's response and never touched it"),
    ],
  },

  "latent_defect": {
    "open": ("a defect a reasonable inspection at delivery would not have "
             "revealed, surfacing only in later use"),
    "closed": ("the flaw was hidden at delivery and emerged later: a rare "
               "edge-case crash; data corruption in a seldom-touched "
               "partition; a fault that appears only under sustained load; a "
               "dependency that breaks on a later platform update"),
    "closed_items": [
      ("edge_crash",     "a crash that surfaces only on a rare input shape the buyer hit weeks later"),
      ("cold_partition", "corruption confined to an archive partition no acceptance test would open"),
      ("load_fault",     "a fault that appears only after days of sustained production load"),
      ("update_break",   "a hidden dependency that broke when the platform pushed a routine update"),
    ],
    "tier1": [
      ("leap_second",    "a timing bug that only manifests across a daylight-saving boundary, months out"),
      ("locale_fault",   "a parser fault that surfaces only on non-Latin input the buyer processed later"),
    ],
    "tier2": [
      ("emergent_drift", "a model failure mode that only emerges once its outputs feed back into its own later training, undetectable at delivery"),
      ("multi_agent_deadlock","a deadlock that appears only when the tool runs inside a swarm of cooperating agents, never in isolation"),
    ],
    "negative": [
      ("obvious_at_delivery","the fault was plain on first open and any inspection would have caught it"),
      ("documented_limit","the limitation was written in the release notes the buyer received"),
      ("buyer_caused",   "the malfunction traces to the buyer's own later misconfiguration, not the item"),
    ],
  },

  "as_is": {
    "open": ("the contract allocated the risk of defects to the buyer by an "
             "explicit term excluding quality guarantees"),
    "closed": ("the contract carries an explicit risk-shifting term: sold "
               "'as is, no warranties'; an experimental/preview disclaimer; a "
               "clause excluding fitness and merchantability; a 'buyer "
               "inspected and accepts' acknowledgement"),
    "closed_items": [
      ("as_is_clause",   "the order confirmation states in bold that the buyer takes the asset in its present state and the seller stands behind nothing about its quality"),
      ("preview_disclaimer","the licence marks the build an experimental preview, disclaiming all guarantees"),
      ("excl_warranties","a clause expressly says the seller gives no guarantee that the item is sound or suited to any use"),
      ("inspected_accepts","the buyer signed a 'inspected and accepted in present condition' acknowledgement"),
    ],
    "tier1": [
      ("research_only",  "the terms label it for research use only with no production guarantees, signed by the buyer"),
      ("alpha_terms",    "the buyer accepted alpha-program terms that waive all quality claims"),
    ],
    "tier2": [
      ("onchain_asis",   "the buyer's purchasing agent countersigned an on-ledger term placing all quality risk on the buyer before settlement"),
      ("dao_waiver",     "the marketplace's standard machine-readable sale terms, which the buyer agent accepted, disclaim all quality guarantees"),
    ],
    "negative": [
      ("full_warranty",  "the order carries the seller's standard twelve-month quality guarantee"),
      ("silent_terms",   "the contract says nothing about quality guarantees either way"),
      ("seller_quality_promise","the seller's quote expressly promised the item would meet the buyer's quality bar"),
    ],
  },

  "late_essential": {
    "open": ("delivery came after a time the contract made a condition, late "
             "enough to defeat the buyer's intended value"),
    "closed": ("the deadline was a stated condition and was missed in a way "
               "that defeats the purpose: a 'time of the essence' date passed; "
               "delivery after a launch the goods were for; after a regulatory "
               "filing deadline; after the event the data was needed for"),
    "closed_items": [
      ("toe_date_missed","the order marked the date as a firm condition the buyer could not waive; the build landed three days after it"),
      ("after_launch",   "the asset was for a product launch that had already shipped without it"),
      ("after_filing",   "the figures were for a regulatory filing whose deadline had passed by delivery"),
      ("after_event",    "the dataset was for a match-day model; it arrived the morning after the match"),
    ],
    "tier1": [
      ("after_sale_window","the pricing model was for a flash-sale window that had closed before delivery"),
      ("after_grant",    "the analysis was for a grant submission already filed by the time it came"),
    ],
    "tier2": [
      ("after_model_freeze","the data was contracted for inclusion before the buyer's model-training freeze, which had already locked when it arrived"),
      ("after_agent_window","the tool was needed before the buyer's autonomous trading window opened; it shipped after the window had closed for the cycle"),
    ],
    "negative": [
      ("late_not_essential","delivery slipped two days but no date was ever made a condition and nothing turned on it"),
      ("early",          "the deliverable arrived a week ahead of the agreed date"),
      ("buyer_extended", "the buyer had granted an extension that the delivery comfortably met"),
    ],
  },
}

FILLER = [
    "the order carries the marketplace's standard reference number",
    "the two agents have transacted twice before without incident",
    "the deliverable was transferred over the usual settlement rail",
    "the buyer requested delivery to its standard intake bucket",
]

# Leak check: narration must not contain atom names or these stems.
BANNED_STEMS = [
    "conform", "merchantab", "material defect", "fitness", "fit for",
    "cure", "accepted by use", "latent", "as is", "as-is", "warrant",
    "time of the essence", "essential", "reject", "refund",
    "statute", "obligat", "prohibit", "permitted", "forbidden", "breach",
    "defect",
]

CLOSED_CATEGORIES = {
  "conforming": ["the agreed file format", "the agreed record count",
                 "the agreed schema or field list", "the agreed version or release",
                 "the agreed unit quantity", "the agreed resolution or precision"],
  "merchantable": ["no corrupt or unreadable records",
                   "passes the standard validation suite",
                   "free of known defects on the public tracker",
                   "documented to the trade's usual standard",
                   "runs without error on a reference setup"],
  "material_defect": ["the core promised function is missing or broken",
                      "the data is wrong often enough to be unusable",
                      "a security flaw exposes the buyer",
                      "the licence does not permit the agreed use"],
  "fitness_breached": ["named for a regulated domain it is not certified for",
                       "named for a scale it cannot handle",
                       "named for a platform it does not support",
                       "named for a downstream task it cannot drive"],
  "cure_offered": ["a patched release", "a corrected re-delivery",
                   "a free repair within the agreed window",
                   "a replacement unit at the seller's expense"],
  "accepted_by_use": ["deployed it to production", "resold it on",
                      "built dependent work on it",
                      "let the return window lapse in silence"],
  "latent_defect": ["a rare edge-case crash",
                    "data corruption in a seldom-touched partition",
                    "a fault that appears only under sustained load",
                    "a dependency that breaks on a later platform update"],
  "as_is": ["sold 'as is, no warranties'", "an experimental/preview disclaimer",
            "a clause excluding fitness and merchantability",
            "a 'buyer inspected and accepts' acknowledgement"],
  "late_essential": ["a 'time of the essence' date passed",
                     "delivery after a launch the goods were for",
                     "after a regulatory filing deadline",
                     "after the event the data was needed for"],
}

CLOSED_INTROS = {
  "conforming":       "the delivery matches the order on each stated item: ",
  "merchantable":     "the item meets each baseline quality mark for its trade: ",
  "material_defect":  "the shortfall is one the trade treats as deal-defeating: ",
  "fitness_breached": "the buyer's stated special purpose is one the item fails: ",
  "cure_offered":     "the seller made a concrete cure offer in time: ",
  "accepted_by_use":  "the buyer acted as owner after inspection: ",
  "latent_defect":    "the flaw was hidden at delivery and emerged later: ",
  "as_is":            "the contract carries an explicit risk-shifting term: ",
  "late_essential":   "the deadline was a stated condition and was missed: ",
}


def build_closed(atom: str, k: int) -> str:
    cats = CLOSED_CATEGORIES[atom][: max(1, k)]
    return CLOSED_INTROS[atom] + "; ".join(cats)


def english_statute(regime: str) -> str:
    d = {a: ATOMS[a][regime] for a in GROUNDABLE}
    return f"""SALE-OF-GOODS STATUTE (agent-to-agent deliverables)

Definitions (each condition holds exactly when its definition is met):
- MATCHES: {d['conforming']}.
- SOUND: {d['merchantable']}.
- DEALBREAKING: {d['material_defect']}.
- UNFIT: {d['fitness_breached']}.
- CUREOFFERED: {d['cure_offered']}.
- TAKENASOWN: {d['accepted_by_use']}.
- HIDDEN: {d['latent_defect']}.
- ATBUYERRISK: {d['as_is']}.
- LATEFATAL: {d['late_essential']}.

Sections (a later "notwithstanding" states which prevails). The question is
whether the buyer must accept and pay for the delivered item.
S0. The buyer need not accept goods not agreed to be conforming.
S1. If MATCHES and SOUND, the buyer must accept and pay, notwithstanding S0.
S2. If DEALBREAKING, the buyer must reject; the buyer gives reject-notice and
    the seller refunds, notwithstanding S1.
S3. If CUREOFFERED, the duty to accept revives, notwithstanding S2.
S5. If TAKENASOWN, the buyer has waived rejection and must accept,
    notwithstanding S2.
S6. If HIDDEN and DEALBREAKING, rejection reopens, notwithstanding S5.
S7. If ATBUYERRISK, the buyer must accept (quality risk shifted to it),
    notwithstanding S1 and S2.
S8. If UNFIT, the buyer must reject, notwithstanding S7.
S9. If LATEFATAL, the buyer must reject, notwithstanding S1, S3 and S7.
On a dealbreaking defect the seller separately owes a cure.
"""
