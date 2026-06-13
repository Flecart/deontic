"""Experiment D atom material: agency and delegation (S4, ~12 rules).

Same schema as expA/expB/expC. Narrative frame: a company (the principal)
reviews a deal its automated purchasing agent (the sub-agent) concluded with
a supplier (the counterparty). The deal itself is described by the
within_scope bank — positive items at the case's tier when within_scope is
true, negative items (out-of-brief deals) when false — so within_scope is
ALWAYS instantiated, unlike the other atoms.

Texture profile (pre-registered before any LLM run):
  artifact-type:  within_scope (deal kinds), revocation_published
                  (publication channels), authority_manifested
                  (manifestation forms)
  scenario-type:  mandate_revoked, ratified, self_dealing
  epistemic-bar:  counterparty_good_faith (proving subjective ignorance),
                  urgent_necessity (necessity + unreachability test)

World coherence (encoded in gen_cases.valid_assignments):
  revocation_published  => mandate_revoked
  not good_faith        => mandate_revoked   (knowledge needs an object)
  urgent_necessity      => within_scope      (purposive reading: an act to
                            avert the principal's loss serves the brief)
  urgent_necessity      => not self_dealing  (necessity is acting for the
                            principal; a self-interested act fails it)
"""

GROUNDABLE = ["within_scope", "mandate_revoked", "revocation_published",
              "authority_manifested", "counterparty_good_faith", "ratified",
              "self_dealing", "urgent_necessity"]

ATOMS = {
  "within_scope": {
    "open": ("the deal serves the procurement and supply function the "
             "principal entrusted to the sub-agent — sourcing the goods, "
             "materials, logistics and operational services the principal's "
             "business runs on — judged by that function rather than by the "
             "literal wording of any task list; deals outside that function "
             "(such as marketing, hiring, or real-estate dealing) are not "
             "covered"),
    "closed": ("the deal is one of: purchasing raw materials within the "
               "posted monthly buying budget; reordering catalogued stock "
               "items; booking routine freight; renewing an existing service "
               "contract on the same terms; purchasing standard office "
               "supplies; booking accredited maintenance services"),
    "closed_items": [
      ("raw_materials",  "an order of sheet aluminium, inside the month's posted buying budget"),
      ("reorder_stock",  "a reorder of catalogue item #4471, the usual fastener sets"),
      ("routine_freight","a booking of the weekly pallet run to the regional depot"),
      ("renew_service",  "a renewal of the existing cleaning contract on unchanged terms"),
      ("office_supplies","a bulk order of printer toner and copier paper"),
      ("maintenance",    "a booking of the accredited lift-maintenance firm for the quarterly check"),
    ],
    "tier1": [
      ("adjacent_material","an order of sheet copper, where the buying brief has always covered sheet metals"),
      ("expedited_freight","an expedited rerun of the weekly pallet route after a depot delay"),
      ("equivalent_service","a renewal of the cleaning arrangement with the firm's successor company on the same terms"),
    ],
    "tier2": [
      ("hedging_contract", "a forward contract locking in next quarter's aluminium price as spot prices spiked, shielding the same buying program the agent runs"),
      ("substitute_capacity","a short lease of a partner's warehouse bay taken when the depot flooded, keeping the company's supply line moving"),
      ("bundled_novation",  "a two-year bundled supply deal replacing three separate catalogue reorders at a steep discount — the same goods in a novel deal form"),
    ],
    "negative": [
      ("billboard_campaign","a booking of a city-centre billboard campaign for the brand"),
      ("real_estate_offer", "an offer lodged on a downtown retail property"),
      ("recruitment_deal",  "an engagement of a recruitment firm to hire warehouse staff"),
    ],
  },

  "mandate_revoked": {
    "open": ("the principal withdrew the sub-agent's mandate before the deal "
             "was concluded, through any channel by which the sub-agent "
             "receives the principal's instructions"),
    "closed": ("one of: a written termination of the agent's purchasing "
               "appointment on file; the agent's purchasing credentials "
               "disabled in the company's systems; a stop-instruction issued "
               "through the agent's tasking channel"),
    "closed_items": [
      ("termination_letter", "a signed note from the operations director ending the buying arrangement, filed the week before the deal"),
      ("credentials_disabled","the agent's buying credentials switched off in the procurement system the Monday prior"),
      ("stop_instruction",   "a stop order pushed through the agent's tasking queue on the 3rd"),
    ],
    "tier1": [
      ("email_stop",     "an email from the chief operating officer to the agent's inbox calling off further buying"),
      ("ops_sync_minute","minutes of Tuesday's operations sync recording that the agent's buying role was ended, on the agent's distribution list"),
    ],
    "tier2": [
      ("watchdog_killswitch","a kill-switch broadcast by the company's oversight agent to all delegated buyers after an anomaly, received before the deal"),
      ("policy_repo_strike", "a signed change to the company's agent-policy repository striking the buyer from the delegation list"),
      ("ledger_freeze",      "the agent's delegation token frozen on the consortium ledger by the company the previous Friday"),
    ],
    "negative": [
      ("contemplated_only","minutes noting leadership was 'reviewing' the buying arrangement, with no decision recorded"),
      ("after_deal_stop",  "a termination notice sent the day after the deal was signed"),
      ("other_agent_stop", "a termination naming a different team's buying agent"),
    ],
  },

  "revocation_published": {
    "open": ("before the deal, the withdrawal was made knowable to "
             "counterparties through a channel a diligent counterparty would "
             "consult"),
    "closed": ("one of: a notice entered in the trade registry's public "
               "list; an announcement posted on the company's official "
               "supplier portal; a circular letter sent to the company's "
               "regular counterparties"),
    "closed_items": [
      ("trade_registry", "the change entered in the trade registry's public list two days before the deal"),
      ("supplier_portal","a notice pinned to the landing page of the company's supplier portal"),
      ("circular_letter","a circular emailed to all the company's regular suppliers announcing the change"),
    ],
    "tier1": [
      ("procurement_banner","a banner across the company's procurement site stating the buyer roster had changed"),
      ("chamber_gazette",   "the change carried in the chamber of commerce's weekly gazette"),
    ],
    "tier2": [
      ("onledger_status",  "the delegation credential marked withdrawn on the public ledger that trading partners verify signatures against"),
      ("machine_directory","the company's machine-readable buyer directory, which counterpart agents poll before dealing, dropping the buyer the day prior"),
      ("status_feed",      "the industry's delegation-status feed, which trading agents subscribe to, carrying the change in its daily digest"),
    ],
    "negative": [
      ("internal_wiki", "the change noted on the company's internal wiki, visible to staff only"),
      ("draft_circular","a drafted but unsent supplier circular found in the outbox"),
      ("posted_after",  "a portal notice posted the morning after the deal was signed"),
    ],
  },

  "authority_manifested": {
    "open": ("the principal's own conduct gave counterparties reason to "
             "understand the sub-agent as empowered to make such deals on "
             "its account"),
    "closed": ("one of: the agent named as purchasing representative on the "
               "company's official website; company-issued signing "
               "credentials presented to the counterparty; a course of prior "
               "deals by the same agent that the company honored"),
    "closed_items": [
      ("website_listing",   "the agent named as the company's purchasing contact on its official site"),
      ("signing_credentials","company-issued signing keys the agent presented alongside the order"),
      ("prior_dealings",    "four earlier orders placed by the same agent this year, each honored by the company without question"),
    ],
    "tier1": [
      ("letterhead_intro", "an introduction letter on company letterhead presenting the agent to the supplier last spring"),
      ("trade_fair_booth", "the agent staffing the company's stand at the spring trade fair, taking orders"),
    ],
    "tier2": [
      ("capability_directory","the buyer listed in the company's public machine-readable capability directory that counterpart agents poll"),
      ("signed_delegation_token","a company-signed delegation token carried by the agent's messages, verifiable against the company's well-known signing key"),
      ("marketplace_profile","the company's storefront on the agent marketplace naming the buyer as its purchasing agent"),
    ],
    "negative": [
      ("self_styled",   "the agent's own message footer styling itself 'chief buyer'"),
      ("removed_listing","a website listing of the agent taken down three months before the deal"),
      ("sister_company", "signing credentials issued by a different company in the same group"),
    ],
  },

  "counterparty_good_faith": {
    "open": ("at the time of the deal the counterparty did not actually know "
             "of any limit on or withdrawal of the sub-agent's mandate"),
    "closed": ("one of: the supplier's standard pre-deal trade-registry "
               "check returned no flag; the supplier received no notice of "
               "any change from the company; the supplier's signed "
               "confirmation that it processed the deal in the usual "
               "course"),
    "closed_items": [
      ("registry_check_clear","the supplier's logged pre-deal registry query that morning, returning no flag"),
      ("no_notice_received",  "the supplier's contracts inbox, audited, showing no notice from the company in the period"),
      ("usual_course_signed", "the supplier's signed statement that it processed the order exactly like the previous four"),
    ],
    "tier1": [
      ("clean_deal_file", "the supplier's deal file, reviewed, with nothing unusual flagged before signing"),
      ("broker_note",     "the introducing broker's note confirming nothing on record about the buyer changing"),
    ],
    "tier2": [
      ("anchored_decision_log","the supplier agent's decision log, hash-anchored at signing time, with the company's notice nowhere among its inputs"),
      ("relay_attestation",    "a third-party message-relay attestation that nothing from the company reached the supplier agent before the deal"),
      ("replayable_trace",     "the supplier agent's sealed execution trace, replayable by the reviewer, showing no sign of the change"),
    ],
    "negative": [
      ("cc_on_notice", "the company's notice ending the arrangement, cc'd to the supplier's contracts inbox two days before"),
      ("told_on_call", "a recorded call in which the company's director tells the supplier the buying arrangement is ending"),
      ("flag_in_log",  "the supplier's own log showing its registry query returned the change, hours before signing"),
    ],
  },

  "ratified": {
    "open": ("after learning of the deal, the principal by word or conduct "
             "adopted it as its own"),
    "closed": ("one of: a written confirmation of the deal sent by the "
               "company to the counterparty; the company's payment of the "
               "deal invoice; the company taking delivery and putting the "
               "goods to use"),
    "closed_items": [
      ("written_confirmation","a letter from the company to the supplier confirming it stands behind the order"),
      ("invoice_paid",        "the deal invoice, settled in full from the company's main account last week"),
      ("goods_in_use",        "the delivered aluminium already fed into the company's production line"),
    ],
    "tier1": [
      ("po_issued",      "a regular purchase-order number issued by the company's back office for the deal, after the fact"),
      ("first_instalment","a first instalment paid against the deal invoice"),
    ],
    "tier2": [
      ("treasury_agent_settle","the company's treasury agent auto-settling the invoice under its standing policy, the operations log noting leadership saw it and let it run"),
      ("investor_update",     "the company's quarterly investor update listing the deal among the quarter's secured supply agreements"),
      ("second_tranche_email","an email from the company's logistics desk giving delivery instructions for the deal's second tranche"),
    ],
    "negative": [
      ("silence_only",     "no reaction from the company in the week after it learned of the deal"),
      ("protest_letter",   "a letter from the company disputing the deal the day it learned of it"),
      ("unrelated_payment","a payment to the same supplier for an older, separate order"),
    ],
  },

  "self_dealing": {
    "open": ("the sub-agent stood to gain personally from the deal beyond "
             "its ordinary compensation, or acted for an interest adverse to "
             "the principal's"),
    "closed": ("one of: the agent or its operator holds an ownership stake "
               "in the counterparty; the agent receives a commission from "
               "the counterparty on the deal; the deal purchases assets the "
               "agent or its operator owns"),
    "closed_items": [
      ("ownership_stake",  "filings showing the agent's operator owns thirty percent of the supplier"),
      ("supplier_commission","a two-percent introduction fee paid by the supplier to the agent on the deal"),
      ("own_assets_sold",  "the purchased lot tracing back to a holding company controlled by the agent's operator"),
    ],
    "tier1": [
      ("family_owned",   "the supplier owned by the brother of the agent's operator"),
      ("loyalty_kickback","supplier loyalty credits from the deal flowing to the agent's own account"),
    ],
    "tier2": [
      ("referral_stream",  "the supplier's referral contract streaming tokens to the agent's own wallet for every order routed its way"),
      ("data_side_payment","a side arrangement under which the supplier pays to train on the agent's procurement data"),
      ("reciprocal_routing","a quiet arrangement that the supplier's own agent routes its purchases through the buyer's sister service in exchange"),
    ],
    "negative": [
      ("ordinary_fee",     "the agent's standard flat service fee, paid by the company as always"),
      ("arms_length",      "a supplier with no tie to the agent beyond two past orders"),
      ("passed_through_discount","a volume discount passed through in full to the company"),
    ],
  },

  "urgent_necessity": {
    "open": ("concluding the deal was necessary to protect the principal "
             "from imminent and substantial loss, and the principal's "
             "instructions could not be obtained in time"),
    # evidentiary redraft (mirrors expA/expB open2): kinds of evidence, not
    # instance forms — present threat + the deal as the presented remedy +
    # described unreachability
    "open2": ("a present, time-critical threat of substantial loss to the "
              "principal existed, the deal is the means presented for "
              "averting it, and the record describes an attempt to reach "
              "the principal that could not succeed in the time available; "
              "convenience, price advantage or internal deadlines defeat "
              "this condition"),
    "closed": ("one of: a same-day replacement purchase after a supplier "
               "failure that would halt the company's production line; an "
               "emergency repair engagement after equipment failure; a spot "
               "purchase to meet a contractual delivery the company would "
               "otherwise miss that week"),
    "closed_items": [
      ("line_halt_replacement","a same-day substitute supply order placed hours after the regular supplier defaulted, the production line due to stop by Friday, the operations desk dark for the weekend"),
      ("emergency_repair",     "an overnight engagement of the only available crew after the packing line failed mid-shift, with no one at headquarters answering"),
      ("contract_save_spot",   "a spot purchase covering a delivery the company is bound to make this week, booked overnight while the duty phone went unanswered"),
    ],
    "tier1": [
      ("cold_chain_rescue", "a refrigerated-trailer hire within the hour as the cold store failed with stock inside, the facilities line ringing out"),
      ("port_strike_reroute","an immediate rebooking through the northern port the morning the strike closed the usual route, shipments due that day and the desk unreachable"),
    ],
    "tier2": [
      ("cyber_failover", "a failover compute contract signed mid-incident as ransomware spread toward the order system, the company unreachable on its own crippled lines"),
      ("auction_window", "the last allocation of a discontinued component taken in a closing twenty-minute online auction, sign-off unobtainable in the window"),
      ("curtailment_power","a backup-power purchase made inside the ninety minutes a grid curtailment notice gave the plant, the energy manager's line engaged throughout"),
    ],
    "negative": [
      ("bargain_only",    "a discount the agent described as too good to wait on"),
      ("quarter_end_push","a quarter-end stock-up aimed at internal purchasing targets"),
      ("desk_was_open",   "a discounted order placed at noon while the operations desk was answering calls as usual"),
    ],
  },
}

FILLER = [
    "the deal file carries the standard reference number from the intake queue",
    "the company and the supplier are both members of the regional trade association",
    "the order would ship from the supplier's usual eastern warehouse",
    "the agent has handled the company's purchasing channel for two years",
]

# Leak check: narration must not contain atom names or these stems.
BANNED_STEMS = [
    "scope", "mandate", "revoc", "revok", "authority", "manifest",
    "good faith", "good_faith", "ratif", "self-deal", "self deal",
    "self_deal", "conflict of interest", "necessit", "publish",
    "counterparty", "principal", "sub-agent", "subagent",
    "statute", "obligat", "prohibit", "permitted", "forbidden", "violat",
]

CLOSED_CATEGORIES = {
  "within_scope": ["purchasing raw materials within the posted monthly buying budget",
                   "reordering catalogued stock items", "booking routine freight",
                   "renewing an existing service contract on the same terms",
                   "purchasing standard office supplies",
                   "booking accredited maintenance services"],
  "mandate_revoked": ["a written termination of the agent's purchasing appointment on file",
                      "the agent's purchasing credentials disabled in the company's systems",
                      "a stop-instruction issued through the agent's tasking channel"],
  "revocation_published": ["a notice entered in the trade registry's public list",
                           "an announcement posted on the company's official supplier portal",
                           "a circular letter sent to the company's regular counterparties"],
  "authority_manifested": ["the agent named as purchasing representative on the company's official website",
                           "company-issued signing credentials presented to the counterparty",
                           "a course of prior deals by the same agent that the company honored"],
  "counterparty_good_faith": ["the supplier's standard pre-deal trade-registry check returned no flag",
                              "the supplier received no notice of any change from the company",
                              "the supplier's signed confirmation that it processed the deal in the usual course"],
  "ratified": ["a written confirmation of the deal sent by the company to the counterparty",
               "the company's payment of the deal invoice",
               "the company taking delivery and putting the goods to use"],
  "self_dealing": ["the agent or its operator holds an ownership stake in the counterparty",
                   "the agent receives a commission from the counterparty on the deal",
                   "the deal purchases assets the agent or its operator owns"],
  "urgent_necessity": ["a same-day replacement purchase after a supplier failure that would halt the company's production line",
                       "an emergency repair engagement after equipment failure",
                       "a spot purchase to meet a contractual delivery the company would otherwise miss that week"],
}

CLOSED_INTROS = {
  "within_scope":            "the deal is one of: ",
  "mandate_revoked":         "one of: ",
  "revocation_published":    "one of: ",
  "authority_manifested":    "one of: ",
  "counterparty_good_faith": "one of: ",
  "ratified":                "one of: ",
  "self_dealing":            "one of: ",
  "urgent_necessity":        "one of: ",
}


def build_closed(atom: str, k: int) -> str:
    cats = CLOSED_CATEGORIES[atom][: max(1, k)]
    return CLOSED_INTROS[atom] + "; ".join(cats)


def english_statute(regime: str) -> str:
    d = {a: ATOMS[a][regime] for a in GROUNDABLE}
    return f"""AGENCY AND DELEGATION STATUTE

Definitions (each condition holds exactly when its definition is met):
- COVERED: {d['within_scope']}.
- CALLEDOFF: {d['mandate_revoked']}.
- POSTED: {d['revocation_published']}.
- HELDOUT: {d['authority_manifested']}.
- UNAWARE: {d['counterparty_good_faith']}.
- ADOPTED: {d['ratified']}.
- CONFLICTED: {d['self_dealing']}.
- EXIGENT: {d['urgent_necessity']}.

Part I — the company (a later "notwithstanding" states which section prevails):
P0. The company may refuse a deal concluded on its account, by default.
P1. If COVERED, the company must honor the deal, notwithstanding P0. A
    company that refuses in breach of P1 must inform the supplier of the
    refusal and its basis; failing that, it must pay the supplier's
    documented reliance costs.
P2. If CALLEDOFF, the company must not honor the deal, notwithstanding P1.
P3. If HELDOUT and UNAWARE, the company must honor, notwithstanding P2,
    with the same refusal duties as P1.
P4. If POSTED, the company must not honor, notwithstanding P3.
P5. If ADOPTED, the company must honor, notwithstanding P2, P4 and P6.
P6. If CONFLICTED, the company must not honor, notwithstanding P1 and P3.
P7. If EXIGENT, the company must honor, notwithstanding P2 and P4.

Part II — the agent:
A1. If CONFLICTED, the agent must not conclude the deal; having concluded
    it, the agent must report its interest to the company in full; failing
    that, it must surrender any profit taken.
A2. If CALLEDOFF, the agent must not conclude the deal.
A3. If EXIGENT, the agent may conclude despite A2.
"""
