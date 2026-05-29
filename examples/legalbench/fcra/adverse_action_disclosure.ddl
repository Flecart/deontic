# fcra — "Must a user disclose the report source on adverse action?"  YES.
facts: AdverseActionBasedOnReport

atom AdverseActionBasedOnReport: holds when a user takes adverse action based on a consumer report | quote: takes adverse action based on a consumer report
atom DiscloseReportSource: holds when the user discloses the source of the report to the consumer | quote: shall disclose the source of the report | uri: examples/legalbench/fcra/sources/fcra.md#L5

adverse_action: AdverseActionBasedOnReport =>O DiscloseReportSource

# Test:  deontic query <file> DiscloseReportSource   ->  O(...)   (on adverse action). YES.
