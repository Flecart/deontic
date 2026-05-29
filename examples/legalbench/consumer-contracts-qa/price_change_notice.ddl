# consumer_contracts_qa — "Must the company give notice before a price increase?"  YES.
facts: PriceIncreasePlanned

atom PriceIncreasePlanned: holds when the company plans to increase the price | quote: before any price increase
atom GiveAdvanceNotice: holds when the company gives at least 30 days' advance notice of the increase | quote: shall give at least 30 days' notice before any price increase | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L10

price_notice: PriceIncreasePlanned =>O GiveAdvanceNotice

# Test:  deontic query <file> GiveAdvanceNotice   ->  O(...)   (increase planned). YES.
