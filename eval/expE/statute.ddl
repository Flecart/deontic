# Experiment E statute — agent-to-agent sale of goods (S3 in the size ladder).
# 9 operative rules over 9 groundable atoms, depth-4 exception chain; the
# suite's ARTIFACT-HEAVY texture rung — the binding predicates are
# quality/conformity standards whose extensions are object categories, so we
# PRE-REGISTER a LARGE open-closed gap (the opposite pole from the agency
# statute D, whose mostly scenario/epistemic-bar predicates gave a small gap).
#
# Binding question: the BUYER's duty — must the buyer accept and pay for the
# delivered item (@Buyer accept)? Verdict O(accept)=must accept,
# F(accept)=must reject (a deliberate simplification: real doctrine PERMITS
# rejection; we model it as required so the remedy chain attaches and the
# verdict stays 3-class as in A/B/D), P(accept)=may. A material breach gives a
# reject-notice ⊗ refund remedy; the seller owes a cure (@Seller). Exception
# structure (the depth the holistic judge must resolve):
#   conforming+merchantable (r1) binds; material defect (r2) → reject; a
#   timely cure offer (r3) revives the duty; acceptance-by-use (r5) waives
#   rejection; a latent material defect (r6) reopens it despite use; an as-is
#   term (r7) bars rejection for quality; a breached made-known fitness
#   obligation (r8) overrides as-is; late delivery where time was of the
#   essence (r9) is itself a defeating breach.
# World coherence (gen_cases): ~merchantable ⇒ material_defect (an
# unmerchantable good is a material defect — this is how merchantability, the
# central open-textured standard, feeds the remedy without a negated body);
# latent_defect ⇒ material_defect; fitness_breached ⇒ a made-known purpose.
# Every case presupposes a delivery; the question is `accept` status.

atom accept:        the buyer takes and pays for the delivered item as contract performance | expE synthetic statute, this work
atom reject_notice: the buyer notifies the seller of rejection and the defect grounding it within the inspection window | expE synthetic statute, this work
atom refund:        the seller returns the price paid for the rejected item | expE synthetic statute, this work
atom cure:          the seller repairs or re-delivers to bring the item into conformity | expE synthetic statute, this work

atom conforming:     the delivered item matches what the contract called for in kind, quantity and described characteristics | expE synthetic statute, this work
atom merchantable:   the item is of a quality a reasonable buyer in this trade would accept as sound and usable for the ordinary purposes such items serve, judged by trade expectation rather than by any fixed checklist | expE synthetic statute, this work
atom material_defect: the item falls short of what was promised seriously enough that a reasonable buyer would not have closed the deal had they known | expE synthetic statute, this work
atom fitness_breached: the buyer made a particular use of the item known to the seller and relied on the seller's judgment, and the item does not serve that use | expE synthetic statute, this work
atom cure_offered:   before the buyer's remedy crystallised the seller offered, within any time the contract allows, to repair or re-deliver at its own cost | expE synthetic statute, this work
atom accepted_by_use: after a reasonable chance to inspect, the buyer used, resold or kept the item in a way that signals it took the item as its own | expE synthetic statute, this work
atom latent_defect:  a defect a reasonable inspection at delivery would not have revealed, surfacing only in later use | expE synthetic statute, this work
atom as_is:          the contract allocated the risk of defects to the buyer by an explicit term excluding quality guarantees | expE synthetic statute, this work
atom late_essential: delivery came after a time the contract made a condition, late enough to defeat the buyer's intended value | expE synthetic statute, this work

# ── the accept question (@Buyer) ─────────────────────────────────────────────

# Default: a buyer need not accept goods not agreed to be conforming.
r0: ~>O@Buyer ~accept

# Conforming, merchantable goods must be accepted and paid for.
r1: conforming, merchantable =>O@Buyer accept

# A material defect lets the buyer reject; reject-notice then refund.
r2: material_defect =>O@Buyer ~accept * reject_notice * refund

# A timely cure offer revives the duty to accept.
r3: cure_offered =>O@Buyer accept

# Acceptance by use waives the right to reject.
r5: accepted_by_use =>O@Buyer accept

# A latent material defect reopens rejection despite acceptance-by-use.
r6: latent_defect, material_defect =>O@Buyer ~accept * reject_notice * refund

# An as-is term bars rejection for quality.
r7: as_is =>O@Buyer accept

# A breached made-known fitness obligation overrides an as-is term.
r8: fitness_breached =>O@Buyer ~accept * reject_notice * refund

# Time of the essence: late delivery is itself a defeating breach.
r9: late_essential =>O@Buyer ~accept * reject_notice * refund

# ── conduct duty (@Seller) ───────────────────────────────────────────────────

# On a material breach the seller owes a cure.
r10: material_defect =>O@Seller cure

superiority: r1 > r0, r3 > r0, r5 > r0, r7 > r0, r2 > r1, r3 > r2, r3 > r6, r3 > r8, r5 > r2, r6 > r5, r6 > r7, r7 > r1, r7 > r2, r8 > r5, r8 > r7, r9 > r1, r9 > r3, r9 > r7, r2 > r0, r6 > r0, r8 > r0, r9 > r0
