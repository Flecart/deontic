# LegalBench maud — "Must the buyer take any antitrust action to get clearance?"  YES.
facts:

atom TakeAntitrustActions: holds when the buyer takes any action (divestitures, etc.) required by antitrust authorities to obtain clearance | quote: shall take any action required by antitrust authorities to obtain clearance | uri: examples/legalbench/maud/sources/dealpoints.md#L8

hell_or_high_water: =>O TakeAntitrustActions

# Test:  deontic query <file> TakeAntitrustActions   ->  O(...)   (hell-or-high-water). YES.
