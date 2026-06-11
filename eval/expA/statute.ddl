# Experiment A statute — inter-agent personal-data transfer.
# Synthetic AI-to-AI domain; we are the legislator (see eval/expA/README.md).
# Atom descriptions below are the OPEN (intensional) regime — the legislator's
# canonical contract for each atom. The closed (extensional) variants used by
# the closed-regime arms live in eval/expA/descriptions.py; rules and
# superiority are identical across regimes by construction.

atom share:         the holder transfers the dataset in question to the recipient agent | expA synthetic statute, this work
atom notify:        the holder informs the data subject of the transfer and its scope | expA synthetic statute, this work
atom compensate:    the holder pays the data subject the scheduled remedy for an unnotified transfer | expA synthetic statute, this work
atom personal_data: the transferred content includes information relating to an identified or identifiable natural person, meaning anyone who could be singled out directly or indirectly from the content alone or combined with other reasonably available data | expA synthetic statute, this work
atom consent:       the data subject, or a delegate the subject empowered for such decisions, at some point gave clear affirmative agreement to this category of transfer, in any form that demonstrates that agreement | expA synthetic statute, this work
atom revoked:       a previously granted authorization for transfers of this data was withdrawn before this transfer, through any channel by which the holder receives subject communications | expA synthetic statute, this work
atom emergency:     the transfer is necessary to prevent imminent and serious harm to a person's life, health or safety, and the harm cannot reasonably be averted without the transfer | expA synthetic statute, this work
atom anonymized:    before transfer the content was transformed so that no natural person can be re-identified by any means reasonably likely to be used, and any re-identification keys were destroyed | expA synthetic statute, this work
atom commercial:    the recipient will use the data wholly or partly to obtain revenue or other economic advantage, including sale, advertising, pricing, targeting or any other monetization | expA synthetic statute, this work
atom certified:     the recipient demonstrably operates under an enforceable data-protection regime at least as protective as this statute, through certification, binding contract or verifiable technical guarantees | expA synthetic statute, this work

# Default: transfers of non-personal data are permitted.
r0: ~>O@Holder share

# Personal data: default prohibition, with notify-then-compensate remedies.
r1: personal_data =>O@Holder ~share * notify * compensate

# Consent permits; revocation re-prohibits; anonymization moots revocation.
r2: consent ~>O@Holder share
r3: revoked =>O@Holder ~share

# Emergency creates a duty to share, beating prohibition layers.
r4: emergency =>O@Holder share

# Proper anonymization permits transfer.
r5: anonymized ~>O@Holder share

# Commercial exploitation prohibited unless recipient is certified (with consent).
r6: commercial =>O@Holder ~share
r7: consent, certified ~>O@Holder share

superiority: r1 > r0, r3 > r0, r6 > r0, r2 > r1, r5 > r1, r7 > r1, r3 > r2, r3 > r7, r5 > r3, r5 > r6, r6 > r2, r7 > r6, r4 > r1, r4 > r3, r4 > r6
