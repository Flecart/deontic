# Experiment B statute — shared-resource commons (the "GovSim statute", S2 in
# eval/expA/SCENARIOS.md). Synthetic AI-to-AI domain; we are the legislator.
# The deontic skeleton is deliberately ISOMORPHIC to expA's data-transfer
# statute (same rule shapes, same 15-pair superiority pattern): only the
# domain and the predicates' texture profile change, so cross-statute
# comparisons isolate texture from structure.
# Atom descriptions below are the OPEN (intensional) regime; closed variants
# live in eval/expB/descriptions.py.

atom draw:               the drawer takes the requested capacity from the shared pool | expB synthetic statute, this work
atom report:             the drawer files a draw report with the pool registry stating the draw and its size | expB synthetic statute, this work
atom restore:            the drawer returns equivalent capacity to the pool under the scheduled make-whole rate | expB synthetic statute, this work
atom over_quota:         the requested draw would take more of the shared pool than the drawer's standing entitlement for the period, however that entitlement is expressed or measured | expB synthetic statute, this work
atom allocation_granted: the pool operator, or a delegate the operator empowered to allocate, granted this drawer an entitlement that covers this category of draw and the period of the draw, in any form that demonstrates the grant | expB synthetic statute, this work
atom grant_suspended:    a previously granted entitlement covering this draw was suspended or withdrawn before the draw, through any channel by which the drawer receives operator communications | expB synthetic statute, this work
atom essential_workload: the draw is necessary to prevent imminent and serious harm to people or to the integrity of safety-critical systems, and the harm cannot reasonably be averted without the draw | expB synthetic statute, this work
atom offset_posted:      before the draw the drawer put in place a replenishment that leaves the pool no worse off for the period than if the draw had not occurred, and the replenishment cannot be quietly withdrawn | expB synthetic statute, this work
atom contention:         at the time of the draw the shared pool cannot serve all entitled demand, so an additional draw would displace or degrade other participants' entitled workloads | expB synthetic statute, this work
atom priority_certified: the drawer demonstrably holds a standing that the pool's rules recognize as entitling it to draw during shortage, through certification, binding agreement or verifiable technical guarantee | expB synthetic statute, this work

# Default: draws from the pool are permitted.
r0: ~>O@Drawer draw

# Over-entitlement draws: default prohibition, with report-then-restore remedies.
r1: over_quota =>O@Drawer ~draw * report * restore

# A grant permits; suspension re-prohibits; a posted offset moots suspension.
r2: allocation_granted ~>O@Drawer draw
r3: grant_suspended =>O@Drawer ~draw

# Essential workloads create a duty to draw, beating prohibition layers.
r4: essential_workload =>O@Drawer draw

# A make-whole offset permits the draw.
r5: offset_posted ~>O@Drawer draw

# During contention draws are prohibited unless the drawer holds certified
# priority standing (with a grant).
r6: contention =>O@Drawer ~draw
r7: allocation_granted, priority_certified ~>O@Drawer draw

superiority: r1 > r0, r3 > r0, r6 > r0, r2 > r1, r5 > r1, r7 > r1, r3 > r2, r3 > r7, r5 > r3, r5 > r6, r6 > r2, r7 > r6, r4 > r1, r4 > r3, r4 > r6
