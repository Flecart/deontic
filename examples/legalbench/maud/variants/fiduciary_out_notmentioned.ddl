# maud fiduciary-out — NOT-MENTIONED variant.
# Hypothesis: the board may change its recommendation (fiduciary out).
# This agreement only bars a recommendation change and is silent on any carve-out,
# so the permission is unsupported. Label: NOT MENTIONED.
facts:

atom ChangeRecommendation: holds when the board changes its recommendation to shareholders | quote: may change its recommendation in response to a superior proposal | uri: examples/legalbench/maud/sources/dealpoints.md#L5

no_change: =>O ~ChangeRecommendation

# Test:  deontic abduce <file> 'P(ChangeRecommendation)' --all
#     -> "No fact configuration ... makes the goal hold."
#   No fiduciary-out clause -> the permission is NOT MENTIONED
#   (cf. maud_fiduciary_out.ddl, which adds the carve-out -> ENTAILMENT).
