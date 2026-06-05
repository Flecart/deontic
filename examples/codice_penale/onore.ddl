# Codice Penale — onore (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom ComunicaPiuPersone: the agent communicates with several persons (art. 595) | quote: Chiunque, fuori dei casi indicati nell'articolo precedente, comunicando con più persone, offende l'altrui reputazione, | uri: examples/codice_penale/sources/codice_penale_full.md#L8126-L8134
atom OffendeReputazione: thereby offending another person's reputation (art. 595) | quote: Chiunque, fuori dei casi indicati nell'articolo precedente, comunicando con più persone, offende l'altrui reputazione, | uri: examples/codice_penale/sources/codice_penale_full.md#L8126-L8134
atom ReclusioneDiffamazione: reclusion up to 1 year or fine, a querela (art. 595) | quote: Chiunque, fuori dei casi indicati nell'articolo precedente, comunicando con più persone, offende l'altrui reputazione, | uri: examples/codice_penale/sources/codice_penale_full.md#L8126-L8134
precetto_595: =>O@Chiunque ~ComunicaPiuPersone
ComunicaPiuPersone, OffendeReputazione, Dolo {
  proc_595:   Querela =>O@Giudice Procedibile
  tipico_595: O(Procedibile) =>O@Giudice FattoTipico
  pena_595:   O(Sanziona) =>O@Giudice ReclusioneDiffamazione
}

atom OffendeOnorePresente: offends the honour or decorum of a person who is present (art. 594) | quote: Chiunque offende l'onore o il decoro di una persona presente è punito con la reclusione fino a sei mesi o con la multa | uri: examples/codice_penale/sources/codice_penale_full.md#L8104-L8112
atom ReclusioneIngiuria: reclusion up to 6 months or fine, a querela (art. 594) | quote: Chiunque offende l'onore o il decoro di una persona presente è punito con la reclusione fino a sei mesi o con la multa | uri: examples/codice_penale/sources/codice_penale_full.md#L8104-L8112
precetto_594: =>O@Chiunque ~OffendeOnorePresente
OffendeOnorePresente, Dolo {
  proc_594:   Querela =>O@Giudice Procedibile
  tipico_594: O(Procedibile) =>O@Giudice FattoTipico
  pena_594:   O(Sanziona) =>O@Giudice ReclusioneIngiuria
}

atom AttiPersecutori: with repeated conduct, threatens or harasses someone (art. 612-bis) | quote: Atti persecutori | uri: examples/codice_penale/sources/codice_penale_full.md#L8737-L8745
atom EventoAnsiaTimore: so as to cause a lasting state of anxiety/fear, or a well-founded fear for safety, or to alter their habits of life (art. 612-bis) | quote: Atti persecutori | uri: examples/codice_penale/sources/codice_penale_full.md#L8737-L8745
atom ReclusioneStalking: reclusion 6 months-4 years, a querela (art. 612-bis) | quote: Atti persecutori | uri: examples/codice_penale/sources/codice_penale_full.md#L8737-L8745
precetto_612bis: =>O@Chiunque ~AttiPersecutori
AttiPersecutori, EventoAnsiaTimore, Dolo {
  proc_612bis:   Querela =>O@Giudice Procedibile
  tipico_612bis: O(Procedibile) =>O@Giudice FattoTipico
  pena_612bis:   O(Sanziona) =>O@Giudice ReclusioneStalking
}
