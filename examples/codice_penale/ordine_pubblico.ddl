# Codice Penale — DELITTI CONTRO L'ORDINE PUBBLICO (artt. 414, 416).
# ===========================================================================
# Istigazione a delinquere, associazione per delinquere.
from definizioni.ddl import *

facts:

atom IstigaPubblicamente:   the agent publicly instigates the commission of one or more crimes (art. 414) | quote: Chiunque pubblicamente istiga a commettere uno o più reati | uri: examples/codice_penale/sources/codice_penale_full.md#L5601-L5609
atom TrePiuPersoneAssociate: three or more persons associate for the purpose of committing several crimes (art. 416) | quote: Quando tre o più persone si associano allo scopo di commettere più delitti | uri: examples/codice_penale/sources/codice_penale_full.md#L5629-L5637
atom PromuoveOrganizza:     the agent promotes, founds or organises the criminal association (art. 416 c.1 — the aggravated role) | quote: coloro che promuovono o costituiscono od organizzano l'associazione | uri: examples/codice_penale/sources/codice_penale_full.md#L5629-L5637
atom ReclusioneIstigazione: penalty: reclusion 1-5 years (art. 414 n. 1) | quote: con la reclusione da uno a cinque anni, se trattasi di istigazione a commettere delitti | uri: examples/codice_penale/sources/codice_penale_full.md#L5601-L5609
atom ReclusioneAssociazione: penalty: reclusion 3-7 years for promoters/organisers (art. 416 c.1) | quote: sono puniti, per ciò solo, con la reclusione da tre a sette anni | uri: examples/codice_penale/sources/codice_penale_full.md#L5629-L5637

precetto_414: =>O@Chiunque ~IstigaPubblicamente
precetto_416: =>O@Chiunque ~PromuoveOrganizza

# Istigazione a delinquere (414): istigare pubblicamente a commettere reati.
IstigaPubblicamente, Dolo {
  tipico_414: =>O@Giudice FattoTipico
  pena_414:   O(Sanziona) =>O@Giudice ReclusioneIstigazione
}

# Associazione per delinquere (416): tre o più associati per più delitti; chi
# promuove/organizza è punito per ciò solo.
TrePiuPersoneAssociate, PromuoveOrganizza, Dolo {
  tipico_416: =>O@Giudice FattoTipico
  pena_416:   O(Sanziona) =>O@Giudice ReclusioneAssociazione
}
