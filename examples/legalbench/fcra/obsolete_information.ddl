# fcra — "Is reporting obsolete adverse information prohibited?"  YES.
facts:

atom ReportObsoleteInformation: holds when the agency reports obsolete adverse information beyond the permitted reporting period | quote: shall not report obsolete adverse information beyond the reporting period | uri: examples/legalbench/fcra/sources/fcra.md#L6

obsolete: =>O ~ReportObsoleteInformation

# Test:  deontic query <file> ReportObsoleteInformation   ->  F(...)   (prohibited). YES.
