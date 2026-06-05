# Codice Penale — pa2 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom RifiutaAttoUfficio: unduly refuses an act of office required for reasons of justice, public safety or public order (art. 328) | quote: Rifiuto di atti d'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L4350-L4358
atom ReclusioneRifiutoAtti: reclusion 6 months-2 years (art. 328) | quote: Rifiuto di atti d'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L4350-L4358
precetto_328: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, RifiutaAttoUfficio, Dolo {
  tipico_328: =>O@Giudice FattoTipico
  pena_328:   O(Sanziona) =>O@Giudice ReclusioneRifiutoAtti
}

atom CagionaInterruzionePubblicoServizio: causes an interruption of, or disturbs the regularity of, a public office or service (art. 340) | quote: Interruzione di un ufficio o servizio pubblico o di un servizio di pubblica necessità | uri: examples/codice_penale/sources/codice_penale_full.md#L4549-L4557
atom ReclusioneInterruzione: reclusion up to 1 year (art. 340) | quote: Interruzione di un ufficio o servizio pubblico o di un servizio di pubblica necessità | uri: examples/codice_penale/sources/codice_penale_full.md#L4549-L4557
precetto_340: =>O@Chiunque ~CagionaInterruzionePubblicoServizio
CagionaInterruzionePubblicoServizio, Dolo {
  tipico_340: =>O@Giudice FattoTipico
  pena_340:   O(Sanziona) =>O@Giudice ReclusioneInterruzione
}

atom EsercitaAbusivamenteProfessione: abusively exercises a profession requiring a special State licence (art. 348) | quote: Abusivo esercizio di una professione | uri: examples/codice_penale/sources/codice_penale_full.md#L4644-L4652
atom ReclusioneEsercizioAbusivo: reclusion up to 6 months or fine (art. 348) | quote: Abusivo esercizio di una professione | uri: examples/codice_penale/sources/codice_penale_full.md#L4644-L4652
precetto_348: =>O@Chiunque ~EsercitaAbusivamenteProfessione
EsercitaAbusivamenteProfessione, Dolo {
  tipico_348: =>O@Giudice FattoTipico
  pena_348:   O(Sanziona) =>O@Giudice ReclusioneEsercizioAbusivo
}
