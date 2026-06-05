# Codice Penale — persona2 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom ReclusioneOmicidioColposo: reclusion 6 months-5 years, causing death by negligence (art. 589) | quote: Omicidio colposo | uri: examples/codice_penale/sources/codice_penale_full.md#L7975-L7983
precetto_589: =>O@Chiunque ~CagionaMorte
CagionaMorte, Colpa {
  tipico_589: =>O@Giudice FattoTipico
  pena_589:   O(Sanziona) =>O@Giudice ReclusioneOmicidioColposo
}

atom PartecipaRissa: the agent takes part in a brawl (rissa) (art. 588) | quote: Chiunque partecipa a una rissa è punito con la multa fino a euro 309 | uri: examples/codice_penale/sources/codice_penale_full.md#L7966-L7974
atom MultaRissa: fine up to 309 euro for mere participation (art. 588) | quote: Chiunque partecipa a una rissa è punito con la multa fino a euro 309 | uri: examples/codice_penale/sources/codice_penale_full.md#L7966-L7974
precetto_588: =>O@Chiunque ~PartecipaRissa
PartecipaRissa, Dolo {
  tipico_588: =>O@Giudice FattoTipico
  pena_588:   O(Sanziona) =>O@Giudice MultaRissa
}
