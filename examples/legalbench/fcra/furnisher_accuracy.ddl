# fcra — "Is furnishing known-inaccurate information prohibited?"  YES.
facts:

atom FurnishKnownInaccurateInfo: holds when a furnisher reports information it knows or has reasonable cause to believe is inaccurate | quote: shall not report information it knows or has reasonable cause to believe is inaccurate | uri: examples/legalbench/fcra/sources/fcra.md#L7

furnisher_accuracy: =>O ~FurnishKnownInaccurateInfo

# Test:  deontic query <file> FurnishKnownInaccurateInfo   ->  F(...)   (prohibited). YES.
