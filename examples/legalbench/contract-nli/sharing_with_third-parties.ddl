# LegalBench contract_nli_sharing_with_third-parties  (ContractNLI NDA-7)
# Hypothesis: Receiving Party may share some Confidential Information with some
# third-parties (consultants, agents, professional advisors).  ENTAILMENT (gated)
facts:

atom Disclose: holds when the Receiving Party discloses Confidential Information to the recipient
atom ThirdPartyBoundByConfidentiality: holds when the recipient is a third party (consultant, agent or advisor) bound by equivalent confidentiality obligations | quote: may share some Confidential Information with some third-parties (including consultants, agents and professional advisors) | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L7

no_disclosure:    =>O  ~Disclose
share_thirdparty: ThirdPartyBoundByConfidentiality  ~>O  Disclose
superiority: share_thirdparty > no_disclosure

# Test:  deontic abduce <file> 'P(Disclose)' --all   ->  { ThirdPartyBoundByConfidentiality }
#   Disclosure to a bound third party is permitted -> ENTAILED.
