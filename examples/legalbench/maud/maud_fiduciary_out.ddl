# LegalBench maud — "May the board change its recommendation (fiduciary out)?"  YES (gated).
facts:

atom ChangeRecommendation: holds when the board changes its recommendation to shareholders
atom SuperiorProposal: holds when a superior acquisition proposal has been received | quote: in response to a superior proposal | uri: examples/legalbench/maud/sources/dealpoints.md#L5

no_change: =>O ~ChangeRecommendation
fiduciary_out: SuperiorProposal ~>O ChangeRecommendation
superiority: fiduciary_out > no_change

# Test:  deontic abduce <file> 'P(ChangeRecommendation)' --all   ->  { SuperiorProposal }
#   A recommendation change is permitted given a superior proposal. YES (gated).
