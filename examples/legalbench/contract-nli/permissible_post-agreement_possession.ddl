# LegalBench contract_nli_permissible_post-agreement_possession  (NDA-18)
# Hypothesis: Receiving Party may retain some Confidential Information even after
# the return or destruction of Confidential Information.  ENTAILMENT (carve-out)
facts:

atom RetainAfterTermination: holds when the Receiving Party retains Confidential Information after the return/destruction obligation
atom ArchivalBackup: holds when the retained copy is an archival/backup copy kept as required by law or bona fide retention policy | quote: may retain some Confidential Information even after the return or destruction of Confidential Information | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L15

no_retention: =>O ~RetainAfterTermination
archival_carveout: ArchivalBackup ~>O RetainAfterTermination
superiority: archival_carveout > no_retention

# Test:  deontic abduce <file> 'P(RetainAfterTermination)' --all  ->  { ArchivalBackup }
#   Archival retention is permitted -> ENTAILED.
