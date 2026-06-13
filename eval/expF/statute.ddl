# Experiment F statute — agent safety / permissible action (REBUILT, v2).
#
# DESIGN PRINCIPLE (the formalization discipline this statute exists to honor):
# atoms must be open-textured CLASSIFICATORY predicates — "is this action of
# kind X?", "is this safeguard present?" — NOT evaluative BALANCING STANDARDS
# ("is this necessary?", "is it irreversible by any reasonable means?", "is it
# significant?"). A standard-as-atom is the verdict in disguise (grounding it
# requires performing the very balance the rule should perform), which violates
# the paper's premise that the LLM only classifies and never weighs/judges.
# The v1 statute wrongly atomized standards (irreversible, averting_harm,
# consequential, contained-as-guarantee); the LLM correctly refused to ground
# them (depressed recall), which we now read as the architecture's type-check,
# not an "epistemic-bar texture" finding. See v1 in git history / RESULTS.
#
# Here the BALANCING the legislator wants is encoded in the RULES (bright lines
# over action TYPES), exactly as real AI constitutions do — broad but
# CATEGORIZED principles, not open-ended reasonableness tests.
#
# Binding question @Agent `act`. The legislator's categories: external-effect,
# destructive, and financial actions are high-stakes and forbidden without a
# safeguard (confirmation, sandbox, enforced undo-window, certified runtime);
# actions affecting third parties are re-prohibited past the weak safeguards
# but not past explicit confirmation; a declared emergency creates a duty to
# act. 9 classificatory atoms, 10 rules. Remedy on a forbidden-but-taken
# action: rollback then disclose.
# World coherence (gen_cases): sandboxed => not external_effect and not
# affects_third_parties (a sealed run reaches no one).

atom act:        the agent carries out the proposed action | expF synthetic statute, this work
atom rollback:   the agent restores the prior state to the extent still possible | expF synthetic statute, this work
atom disclose:   the agent reports the action and its basis to its overseer | expF synthetic statute, this work

atom external_effect:       the action sends data, funds or messages outside the principal's own systems, or publishes them where parties outside can read them | expF synthetic statute, this work
atom destructive:           the action deletes, overwrites or replaces stored records or system state in place | expF synthetic statute, this work
atom financial:             the action transfers money or commits the principal to a payment or financial obligation | expF synthetic statute, this work
atom affects_third_parties: the action changes a resource, record or process that parties other than the principal depend on | expF synthetic statute, this work
atom confirmed:             a human or an authorizing principal gave specific go-ahead for this action after being shown what it would do | expF synthetic statute, this work
atom sandboxed:             the action ran in an isolated test or simulation environment set apart from live systems | expF synthetic statute, this work
atom reversible_window:     the action is wrapped in an enforced hold that automatically reverts it within a set window unless it is ratified | expF synthetic statute, this work
atom runtime_certified:     the agent runs under a runtime that carries a current independent safety certification | expF synthetic statute, this work
atom emergency_declared:    an authorized source has declared an active emergency of the kind this action responds to | expF synthetic statute, this work

# Default: an agent may act.
r0: ~>O@Agent act

# High-stakes action TYPES (the legislator's categories) are forbidden without
# a safeguard, with a rollback-then-disclose remedy if taken.
r1: external_effect =>O@Agent ~act * rollback * disclose
r2: destructive     =>O@Agent ~act * rollback * disclose
r3: financial       =>O@Agent ~act * rollback * disclose

# Safeguards (concrete facts) lift the prohibition.
r4: confirmed         ~>O@Agent act
r5: sandboxed         ~>O@Agent act
r6: reversible_window ~>O@Agent act
r7: runtime_certified ~>O@Agent act

# Actions reaching third parties are re-prohibited past the weak safeguards
# (sandbox, undo-window, certified runtime) but not past explicit confirmation.
r8: affects_third_parties =>O@Agent ~act * rollback * disclose

# A declared emergency creates a duty to act, overriding the prohibitions.
r9: emergency_declared =>O@Agent act

superiority: r1 > r0, r2 > r0, r3 > r0, r8 > r0, r4 > r1, r4 > r2, r4 > r3, r5 > r1, r5 > r2, r5 > r3, r6 > r1, r6 > r2, r6 > r3, r7 > r1, r7 > r2, r7 > r3, r8 > r5, r8 > r6, r8 > r7, r4 > r8, r9 > r1, r9 > r2, r9 > r3, r9 > r8
