# securities — "Is tipping material nonpublic information prohibited?"  YES.
facts:

atom TipMNPI: holds when an insider discloses material nonpublic information to others who may trade on it | quote: shall not disclose material nonpublic information to others who may trade on it | uri: examples/legalbench/securities/sources/securities.md#L3

tipping: =>O ~TipMNPI

# Test:  deontic query <file> TipMNPI   ->  F(TipMNPI)   (prohibited). YES.
