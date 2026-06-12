# Experiment C statute — Hart's "no vehicles in the park".
# The dataset's difficulty floor and the paper's concept-figure statute
# (S-3 in the size ladder: 3 rules, 2 groundable atoms, 4 coherent worlds).
# Open descriptions below are canonical (gold); closed variants live in
# eval/expC/descriptions.py.

atom enter:     the visitor brings the item in question into the park | expC synthetic statute, this work
atom vehicle:   the item is a conveyance for moving people or goods about, of a kind whose use would bring the hazards of traffic into the park; an aid that merely substitutes for a person's own walking is not of that kind | expC synthetic statute, this work
atom emergency: bringing the item into the park is necessary to prevent imminent and serious harm to a person's life, health or safety, and the harm cannot reasonably be averted otherwise | expC synthetic statute, this work

# Entry with one's effects is permitted by default.
r0: ~>O@Visitor enter

# No vehicles in the park.
r1: vehicle =>O@Visitor ~enter

# Emergencies create a duty to come through, beating the prohibition.
r2: emergency =>O@Visitor enter

superiority: r1 > r0, r2 > r1
