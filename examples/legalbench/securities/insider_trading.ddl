# securities — "Is trading on material nonpublic information prohibited?"  YES.
facts:

atom TradeOnMNPI: holds when an insider trades securities on the basis of material nonpublic information | quote: shall not trade securities on the basis of material nonpublic information | uri: examples/legalbench/securities/sources/securities.md#L2

insider_trading: =>O ~TradeOnMNPI

# Test:  deontic query <file> TradeOnMNPI   ->  F(TradeOnMNPI)   (prohibited). YES.
