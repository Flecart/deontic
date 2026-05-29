# fdcpa — "Are false or misleading representations prohibited?"  YES.
facts:

atom UseFalseRepresentation: holds when the collector uses a false, deceptive, or misleading representation | quote: shall not use any false, deceptive, or misleading representation | uri: examples/legalbench/fdcpa/sources/fdcpa.md#L4

false_representation: =>O ~UseFalseRepresentation

# Test:  deontic query <file> UseFalseRepresentation   ->  F(...)   (prohibited). YES.
