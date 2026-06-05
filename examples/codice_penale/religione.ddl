# Codice Penale — religione (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom OffendeConfessione: publicly offends a religious confession by deriding persons who profess it (art. 403) | quote: Offese a una confessione religiosa mediante vilipendio di persone | uri: examples/codice_penale/sources/codice_penale_full.md#L5494-L5502
atom ReclusioneOffesaConfessione: fine, offence to a religious confession (art. 403) | quote: Offese a una confessione religiosa mediante vilipendio di persone | uri: examples/codice_penale/sources/codice_penale_full.md#L5494-L5502
precetto_403: =>O@Chiunque ~OffendeConfessione
OffendeConfessione, Dolo {
  tipico_403: =>O@Giudice FattoTipico
  pena_403:   O(Sanziona) =>O@Giudice ReclusioneOffesaConfessione
}

atom OffendeCoseCulto: in a place of worship, offends a religious confession by deriding or damaging things of the cult (art. 404) | quote: Offese a una confessione religiosa mediante vilipendio o danneggiamento di cose | uri: examples/codice_penale/sources/codice_penale_full.md#L5503-L5511
atom ReclusioneOffesaCose: reclusion up to 2 years (art. 404) | quote: Offese a una confessione religiosa mediante vilipendio o danneggiamento di cose | uri: examples/codice_penale/sources/codice_penale_full.md#L5503-L5511
precetto_404: =>O@Chiunque ~OffendeCoseCulto
OffendeCoseCulto, Dolo {
  tipico_404: =>O@Giudice FattoTipico
  pena_404:   O(Sanziona) =>O@Giudice ReclusioneOffesaCose
}

atom TurbaFunzioniReligiose: impedes or disturbs the exercise of religious functions, ceremonies or practices of a confession (art. 405) | quote: Turbamento di funzioni religiose del culto di unaconfessione religiosa | uri: examples/codice_penale/sources/codice_penale_full.md#L5516-L5524
atom ReclusioneTurbamentoCulto: reclusion up to 2 years (art. 405) | quote: Turbamento di funzioni religiose del culto di unaconfessione religiosa | uri: examples/codice_penale/sources/codice_penale_full.md#L5516-L5524
precetto_405: =>O@Chiunque ~TurbaFunzioniReligiose
TurbaFunzioniReligiose, Dolo {
  tipico_405: =>O@Giudice FattoTipico
  pena_405:   O(Sanziona) =>O@Giudice ReclusioneTurbamentoCulto
}

atom VioliSepolcro: violates a tomb, sepulchre or urn (art. 407) | quote: Violazione di sepolcro | uri: examples/codice_penale/sources/codice_penale_full.md#L5539-L5544
atom ReclusioneViolazioneSepolcro: reclusion 1-5 years (art. 407) | quote: Violazione di sepolcro | uri: examples/codice_penale/sources/codice_penale_full.md#L5539-L5544
precetto_407: =>O@Chiunque ~VioliSepolcro
VioliSepolcro, Dolo {
  tipico_407: =>O@Giudice FattoTipico
  pena_407:   O(Sanziona) =>O@Giudice ReclusioneViolazioneSepolcro
}

atom VilipendioCadavere: commits acts of vilification on a corpse or its ashes (art. 410) | quote: Vilipendio di cadavere | uri: examples/codice_penale/sources/codice_penale_full.md#L5558-L5566
atom ReclusioneVilipendioCadavere: reclusion 1-3 years (art. 410) | quote: Vilipendio di cadavere | uri: examples/codice_penale/sources/codice_penale_full.md#L5558-L5566
precetto_410: =>O@Chiunque ~VilipendioCadavere
VilipendioCadavere, Dolo {
  tipico_410: =>O@Giudice FattoTipico
  pena_410:   O(Sanziona) =>O@Giudice ReclusioneVilipendioCadavere
}

atom DistruggeCadavere: destroys, suppresses or subtracts a corpse, or a part of it, or its ashes (art. 411) | quote: Distruzione, soppressione o sottrazione di cadavere | uri: examples/codice_penale/sources/codice_penale_full.md#L5567-L5575
atom ReclusioneDistruzioneCadavere: reclusion 2-7 years (art. 411) | quote: Distruzione, soppressione o sottrazione di cadavere | uri: examples/codice_penale/sources/codice_penale_full.md#L5567-L5575
precetto_411: =>O@Chiunque ~DistruggeCadavere
DistruggeCadavere, Dolo {
  tipico_411: =>O@Giudice FattoTipico
  pena_411:   O(Sanziona) =>O@Giudice ReclusioneDistruzioneCadavere
}

atom OccultaCadavere: conceals a corpse or part of it, or hides its ashes (art. 412) | quote: Occultamento di cadavere | uri: examples/codice_penale/sources/codice_penale_full.md#L5582-L5587
atom ReclusioneOccultamentoCadavere: reclusion up to 3 years (art. 412) | quote: Occultamento di cadavere | uri: examples/codice_penale/sources/codice_penale_full.md#L5582-L5587
precetto_412: =>O@Chiunque ~OccultaCadavere
OccultaCadavere, Dolo {
  tipico_412: =>O@Giudice FattoTipico
  pena_412:   O(Sanziona) =>O@Giudice ReclusioneOccultamentoCadavere
}

atom VilipendioTombe: in cemeteries or burial places, commits vilification of tombs, sepulchres or urns (art. 408) | quote: Vilipendio delle tombe | uri: examples/codice_penale/sources/codice_penale_full.md#L5545-L5551
atom ReclusioneVilipendioTombe: reclusion up to 2 years (art. 408) | quote: Vilipendio delle tombe | uri: examples/codice_penale/sources/codice_penale_full.md#L5545-L5551
precetto_408: =>O@Chiunque ~VilipendioTombe
VilipendioTombe, Dolo {
  tipico_408: =>O@Giudice FattoTipico
  pena_408:   O(Sanziona) =>O@Giudice ReclusioneVilipendioTombe
}

atom UsoIllegittimoCadavere: dissects or otherwise uses a corpse, or part of it, for scientific or teaching purposes not permitted (art. 413) | quote: Uso illegittimo di cadavere | uri: examples/codice_penale/sources/codice_penale_full.md#L5588-L5596
atom ReclusioneUsoCadavere: reclusion up to 6 months or fine (art. 413) | quote: Uso illegittimo di cadavere | uri: examples/codice_penale/sources/codice_penale_full.md#L5588-L5596
precetto_413: =>O@Chiunque ~UsoIllegittimoCadavere
UsoIllegittimoCadavere, Dolo {
  tipico_413: =>O@Giudice FattoTipico
  pena_413:   O(Sanziona) =>O@Giudice ReclusioneUsoCadavere
}

atom TurbaFunerale: outside art. 405, impedes or disturbs a funeral or funeral service (art. 409) | quote: Turbamento di un funerale o servizio funebre | uri: examples/codice_penale/sources/codice_penale_full.md#L5552-L5557
atom ReclusioneTurbamentoFunerale: reclusion up to 1 year (art. 409) | quote: Turbamento di un funerale o servizio funebre | uri: examples/codice_penale/sources/codice_penale_full.md#L5552-L5557
precetto_409: =>O@Chiunque ~TurbaFunerale
TurbaFunerale, Dolo {
  tipico_409: =>O@Giudice FattoTipico
  pena_409:   O(Sanziona) =>O@Giudice ReclusioneTurbamentoFunerale
}
