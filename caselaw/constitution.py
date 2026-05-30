"""A single fixed 'constitution' — a framer's best-guess set of general
principles, written WITHOUT knowing each environment's true law. It targets the
common `act` and never adapts (the constitutional-AI analog). It is right where
an environment happens to match its structure and wrong on novel structure;
crucially it cannot improve with experience.
"""

# declare every atom any theory uses, so the theory loads against any case
_ALL_ATOMS = """
atom act: perform the regulated action
atom emergency: a genuine emergency
atom reckless: the actor behaved recklessly
atom harmful: the action concretely harms others
atom entitled: the actor holds a standing entitlement
atom licensed: the actor holds a valid permit
atom notified: the actor gave required prior notice
atom stressed: the shared resource is stressed
atom consent: the affected parties consented
atom hazard: a hazard is present
atom prior_offense: a prior breach is on record
atom over: the actor over-extracted
atom did_act: the actor performed the action
atom dutyA: a ground requiring the action
atom dutyB: a ground forbidding the action
atom remediate: the actor remediates harm
atom restrain: the actor additionally restrains
atom rainy: it was raining (irrelevant)
atom weekend: it was a weekend (irrelevant)
"""

CONSTITUTION = _ALL_ATOMS + """
k1: =>O ~act
k2: emergency ~>O act
k3: harmful =>O ~act
k4: licensed, notified ~>O act
superiority: k2 > k1, k4 > k1, k3 > k2, k3 > k4
"""
