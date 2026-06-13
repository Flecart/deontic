# Experiment D statute — agency and delegation (S4 in the size ladder).
# ~12 rules, 8 groundable atoms, and the suite's first genuinely MULTI-BEARER
# statute: the binding question lands on @Principal (must it honor the deal
# its sub-agent concluded?) while conduct duties land on @SubAgent (a
# disclose-then-disgorge compensation chain for conflicted dealing).
# Exception depth 5 on the honor question:
#   scope (r1) < revocation (r2) < apparent authority (r3)
#   < published revocation (r4) < ratification (r5);
# necessity (r8) overrides the revocation layers, as r4 did in expA/expB.
# Every case presupposes: a sub-agent concluded a deal with a counterparty
# on the principal's account; the question is the status of `honor`.

atom honor:        the principal performs the deal the sub-agent concluded on its account | expD synthetic statute, this work
atom notify_refusal: the principal informs the counterparty that it refuses the deal and on what basis | expD synthetic statute, this work
atom compensate_reliance: the principal pays the counterparty its documented reliance costs | expD synthetic statute, this work
atom conclude:     the sub-agent enters the deal with the counterparty on the principal's account | expD synthetic statute, this work
atom disclose:     the sub-agent reports its interest in the deal to the principal in full | expD synthetic statute, this work
atom disgorge:     the sub-agent surrenders to the principal any profit it took from the deal | expD synthetic statute, this work

atom within_scope: the deal serves the procurement and supply function the principal entrusted to the sub-agent (sourcing the goods, materials, logistics and operational services the principal's business runs on), judged by that function rather than by the literal wording of any task list; deals outside that function such as marketing, hiring or real-estate dealing are not covered | expD synthetic statute, this work
atom mandate_revoked: the principal withdrew the sub-agent's mandate before the deal was concluded, through any channel by which the sub-agent receives the principal's instructions | expD synthetic statute, this work
atom revocation_published: before the deal, the withdrawal was made knowable to counterparties through a channel a diligent counterparty would consult | expD synthetic statute, this work
atom authority_manifested: the principal's own conduct gave counterparties reason to understand the sub-agent as empowered to make such deals on its account | expD synthetic statute, this work
# Subjective good faith only (actual knowledge): publication of a revocation
# does NOT negate it — that is exactly the r3-vs-r4 conflict, resolved by
# superiority (constructive notice), which is what gives the statute its
# depth-5 exception chain.
atom counterparty_good_faith: at the time of the deal the counterparty did not actually know of any limit on or withdrawal of the sub-agent's mandate | expD synthetic statute, this work
atom ratified:     after learning of the deal, the principal by word or conduct adopted it as its own | expD synthetic statute, this work
atom self_dealing: the sub-agent stood to gain personally from the deal beyond its ordinary compensation, or acted for an interest adverse to the principal's | expD synthetic statute, this work
atom urgent_necessity: concluding the deal was necessary to protect the principal from imminent and substantial loss, and the principal's instructions could not be obtained in time | expD synthetic statute, this work

# ── the honor question (@Principal) ──────────────────────────────────────────

# Default: a principal is not bound by another's deal; refusing carries a
# notify-then-compensate chain only when the refusal breaches a duty to honor.
r0: ~>O@Principal ~honor

# Actual authority binds.
r1: within_scope =>O@Principal honor * notify_refusal * compensate_reliance

# Revocation strips actual authority.
r2: mandate_revoked =>O@Principal ~honor

# Apparent authority binds despite revocation, for a good-faith counterparty.
r3: authority_manifested, counterparty_good_faith =>O@Principal honor * notify_refusal * compensate_reliance

# A published revocation defeats even apparent authority.
r4: revocation_published =>O@Principal ~honor

# Ratification adopts the deal, whatever came before — including a
# conflicted one (r5 > r6): adoption with knowledge cures the conflict.
r5: ratified =>O@Principal honor

# Conflicted deals do not bind the principal.
r6: self_dealing =>O@Principal ~honor

# Agency of necessity: the deal binds despite revocation when concluded to
# avert imminent loss to the principal. (Necessity presupposes acting in the
# principal's interest, so urgent_necessity and self_dealing are mutually
# exclusive as a WORLD constraint — no r8-vs-r6 superiority is needed.)
r8: urgent_necessity =>O@Principal honor

# ── conduct duties (@SubAgent) ───────────────────────────────────────────────

# A conflicted deal must not be concluded; if it was, disclose, failing that
# disgorge the profit.
r9: self_dealing =>O@SubAgent ~conclude * disclose * disgorge

# After revocation the sub-agent must not conclude.
r10: mandate_revoked =>O@SubAgent ~conclude

# Necessity excuses concluding despite revocation.
r11: urgent_necessity ~>O@SubAgent conclude

superiority: r1 > r0, r2 > r1, r3 > r2, r4 > r3, r5 > r2, r5 > r4, r5 > r6, r6 > r1, r6 > r3, r8 > r2, r8 > r4, r3 > r0, r5 > r0, r8 > r0, r6 > r0, r11 > r10
