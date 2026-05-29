# LegalBench maud — "Must the target operate in the ordinary course pre-closing?"  YES.
facts:

atom ConductOrdinaryCourse: holds when the target conducts its business in the ordinary course between signing and closing | quote: shall conduct its business in the ordinary course | uri: examples/legalbench/maud/sources/dealpoints.md#L2

ordinary_course: =>O ConductOrdinaryCourse

# Test:  deontic query <file> ConductOrdinaryCourse   ->  O(...)   (covenant). YES.
