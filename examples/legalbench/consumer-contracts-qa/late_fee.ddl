# consumer_contracts_qa — "May the company charge a late fee?"  YES (if overdue).
facts:

atom ChargeLateFee: holds when the company charges the consumer a late fee
atom PaymentOverdue: holds when payment was not received by the due date | quote: may charge a late fee if payment is not received by the due date | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L7

no_late_fee:  =>O ~ChargeLateFee
late_fee_ok:  PaymentOverdue ~>O ChargeLateFee
superiority: late_fee_ok > no_late_fee

# Test:  deontic abduce <file> 'P(ChargeLateFee)' --all   ->  { PaymentOverdue }
#   A late fee is permitted when payment is overdue. Answer: YES (conditional).
