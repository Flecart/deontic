# fdcpa — "Is harassing the consumer prohibited?"  YES.
facts:

atom HarassConsumer: holds when the collector harasses, oppresses, or abuses any person in collecting a debt | quote: shall not harass, oppress, or abuse any person in collecting a debt | uri: examples/legalbench/fdcpa/sources/fdcpa.md#L3

harassment: =>O ~HarassConsumer

# Test:  deontic query <file> HarassConsumer   ->  F(HarassConsumer)   (prohibited). YES.
