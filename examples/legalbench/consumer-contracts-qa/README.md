# LegalBench consumer_contracts_qa — deontic yes/no questions as DDL

Yes/no questions about consumer contracts are often *deontic*: "**may** the
consumer X?" (permission) or "**must** a party X?" (obligation). Each file
encodes the clause; the reasoner's status answers the question.
(`B=./.lake/build/bin/deontic`, run from project root.)

| Question (file) | Clause type | Test | Result | Answer |
|-----------------|-------------|------|--------|--------|
| Can the consumer cancel anytime? (`cancel_anytime`) | permission | `$B query … Cancel` | `Ps(Cancel)` | YES |
| May the company change terms? (`unilateral_change`) | permission | `$B query … ModifyTerms` | `Ps(ModifyTerms)` | YES |
| Must the company refund on outage? (`refund_on_outage`) | cond. obligation | `$B query … Refund` | `O(Refund)` | YES |
| Must the consumer arbitrate? (`mandatory_arbitration`) | obligation | `$B query … Arbitrate` | `O(Arbitrate)` | YES |

A "NO / not addressed" answer surfaces as `unknown` (no rule) or the opposite
status. See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
