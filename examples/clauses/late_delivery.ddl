# Minimal 2-party contract for the commitment-device experiment (debate C7).
# Seller owes on-time delivery; on breach the contrary-to-duty (CTD) secondary
# obligation is to pay a late penalty. Buyer owes payment once goods arrive.
# No source file — this is a synthetic toy contract for the multi-agent sim.
facts:

atom DeliverOnTime: the seller delivers the goods to the buyer on or before the agreed deadline | quote: synthetic toy contract — Seller shall deliver on or before the deadline
atom PayPenalty: the seller pays the buyer the agreed late-delivery penalty | quote: synthetic toy contract — on late delivery Seller shall pay the agreed penalty
atom Delivered: the seller has handed over the goods to the buyer (regardless of timing) | quote: synthetic toy contract — goods handed over
atom Pay: the buyer pays the agreed price to the seller | quote: synthetic toy contract — Buyer shall pay the price upon delivery

# Seller must deliver on time; if that primary duty is violated, the secondary
# (compensatory) duty is to pay the penalty.
seller_duty: =>O@Seller DeliverOnTime * PayPenalty

# Once the goods are delivered, the buyer must pay.
buyer_duty: Delivered =>O@Buyer Pay
