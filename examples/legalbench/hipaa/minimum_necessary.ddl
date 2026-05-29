# hipaa — "Must PHI use be limited to the minimum necessary?"  YES.
facts:

atom UseMoreThanMinimumNecessary: holds when the covered entity uses or discloses more PHI than the minimum necessary | quote: shall limit PHI use and disclosure to the minimum necessary | uri: examples/legalbench/hipaa/sources/hipaa.md#L2

minimum_necessary: =>O ~UseMoreThanMinimumNecessary

# Test:  deontic query <file> UseMoreThanMinimumNecessary   ->  F(...)   (prohibited). YES.
