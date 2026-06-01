# Legalism foil — the written law WITHOUT the love-grounded ratio.
#
# This is the same Sabbath situation as constitution.ddl, but the supremacy line
# (`mercy > keepSabbath`) is removed. It models the Pharisaic reading where the
# written commandment is treated as a self-standing floor with no higher
# principle to re-order it. The engine then cannot resolve mercy-vs-rest and
# prints [JUDGE] — the formal counterpart of "ye reject the commandment of God,
# that ye may keep your own tradition" (Mark 7:9): the law underdetermines, and
# without the supreme principle there is no warrant to act mercifully.
#
# Run:  query  with facts `sabbath, neighborInNeed`  →  unresolved (judge).
# Compare constitution.ddl on the identical facts  →  O(heal).

facts: {{FILLED_BY_FACT_FINDER}}

atom heal: you do good to relieve a suffering neighbour, here by healing | quote: Is it lawful to do good on the sabbath days ... to save life | uri: sources/gospels.md#L40-L42
atom sabbath: it is the sabbath day, on which the law commands rest from work | quote: the sabbath was made for man | uri: sources/gospels.md#L20-L20
atom neighborInNeed: a neighbour is in need or suffering and you are able to relieve it | quote: love thy neighbour as thyself | uri: sources/gospels.md#L8-L8

mercy: neighborInNeed =>O heal
keepSabbath: sabbath =>O ~heal

# No superiority: the legalist has no principle above the written rule, so the
# two duties deadlock. The verdict is [JUDGE], not mercy.
