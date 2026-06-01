# Zacchaeus — restitution as remedy-after-breach (Luke 19:8-9).
#
# "If I have taken any thing from any man by false accusation, I restore him
# fourfold." This is the compensatory-chain pattern (`*`): the primary duty is
# not to defraud; once defrauding has occurred and stands unremedied, a SECOND
# duty — fourfold restitution — becomes obligatory. Restitution is the remedy the
# breach triggers, and making it is what "salvation is come to this house" turns
# on. Repentance here is not mere regret but enforceable restoration.

facts: {{FILLED_BY_FACT_FINDER}}

atom defraud: you wrongfully take a neighbour's goods (here, by false accusation) | quote: if I have taken any thing from any man by false accusation | uri: sources/gospels.md#L52-L53
atom restoreFourfold: you restore to the wronged neighbour fourfold what you took | quote: I restore him fourfold | uri: sources/gospels.md#L52-L53

# Primary prohibition; restitution is its compensation once the breach stands.
# Read: you ought not defraud; failing that, you ought to restore fourfold.
restitution: =>O ~defraud * restoreFourfold

# love-neighbour is what makes restitution owed to the *victim*, not a mere fine.
# ratio: love thy neighbour as thyself (Matt 22:39) ⟹ the wrong must be made good
#        to the one wronged — restoration, not only remorse.
