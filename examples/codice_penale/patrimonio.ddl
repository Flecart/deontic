# Codice Penale — DELITTI CONTRO IL PATRIMONIO, oltre furto/rapina (artt. 629-648).
# ===========================================================================
# Estorsione, danneggiamento, truffa, appropriazione indebita, ricettazione.
# Riusa gli atomi condivisi di definizioni.ddl: Costringe, Violenza, Minaccia,
# FineDiProfitto, IngiustoProfittoAltruiDanno. L'estorsione, in particolare, È
# una violenza privata (610) con in più il profitto ingiusto/altrui danno.
from definizioni.ddl import *

facts:

atom Distrugge:            destroys, disperses, deteriorates or renders unusable another's movable or immovable thing (art. 635) | quote: distrugge, disperde, deteriora o rende … inservibili cose mobili o immobili altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9320-L9326
atom ArtifiziRaggiri:      the agent used artifices or deceptions, inducing another into error (art. 640) | quote: con artifizi o raggiri, inducendo taluno in errore | uri: examples/codice_penale/sources/codice_penale_full.md#L9360-L9366
atom AcquistaRiceveOcculta: the agent acquires, receives or conceals (or brokers) money or things, OUTSIDE participation in the predicate crime (art. 648) | quote: acquista, riceve od occulta denaro o cose … o comunque si intromette nel farle acquistare | uri: examples/codice_penale/sources/codice_penale_full.md#L9420-L9428
atom ProvenienzaDelitto:   the money or things come from some crime (art. 648) | quote: denaro o cose provenienti da un qualsiasi delitto | uri: examples/codice_penale/sources/codice_penale_full.md#L9420-L9428
atom ReclusioneEstorsione: penalty: reclusion 5-10 years and fine (art. 629) | quote: è punito con la reclusione da cinque a dieci anni e con la multa | uri: examples/codice_penale/sources/codice_penale_full.md#L9259-L9266
atom ReclusioneDanneggiamento: penalty: reclusion up to 1 year or fine, a querela (art. 635 c.1) | quote: è punito, a querela della persona offesa, con la reclusione fino a un anno o con la multa fino a euro 309 | uri: examples/codice_penale/sources/codice_penale_full.md#L9320-L9326
atom ReclusioneDanneggiamentoViolento: penalty: reclusion 6 months-3 years, d'ufficio, if committed with violence/threat (art. 635 c.2) | quote: La pena è della reclusione da sei mesi a tre anni e si procede d'ufficio … con violenza alla persona o con minaccia | uri: examples/codice_penale/sources/codice_penale_full.md#L9320-L9332
atom ReclusioneTruffa:     penalty: reclusion 6 months-3 years and fine (art. 640) | quote: è punito con la reclusione da sei mesi a tre anni e con la multa da euro 51 a euro 1.032 | uri: examples/codice_penale/sources/codice_penale_full.md#L9360-L9366
atom ReclusioneAppropriazione: penalty: reclusion up to 3 years and fine, a querela (art. 646) | quote: è punito, a querela della persona offesa, con la reclusione fino a tre anni e con la multa | uri: examples/codice_penale/sources/codice_penale_full.md#L9400-L9406
atom ReclusioneRicettazione: penalty: reclusion 2-8 years and fine (art. 648) | quote: è punito con la reclusione da due ad otto anni e con la multa | uri: examples/codice_penale/sources/codice_penale_full.md#L9420-L9428
atom FaDarePromettereInteressiUsurari: the agent gets given or promised, in any form, usurious interest in return for a loan of money or other benefit (art. 644) | quote: si fa dare o promettere … in corrispettivo di una prestazione di denaro o di altra utilità, interessi … usurari | uri: examples/codice_penale/sources/codice_penale_full.md#L9614-L9622
atom ReclusioneUsura:       penalty: reclusion 2-10 years and fine (art. 644) | quote: è punito con la reclusione da due a dieci anni e con la multa | uri: examples/codice_penale/sources/codice_penale_full.md#L9614-L9622

# Precetti
precetto_629: =>O@Chiunque ~IngiustoProfittoAltruiDanno
precetto_635: =>O@Chiunque ~Distrugge
precetto_640: =>O@Chiunque ~ArtifiziRaggiri
precetto_646: =>O@Chiunque ~SiAppropria
precetto_648: =>O@Chiunque ~AcquistaRiceveOcculta
precetto_644: =>O@Chiunque ~FaDarePromettereInteressiUsurari

# Estorsione (629): costrizione con violenza/minaccia + ingiusto profitto/danno.
# = violenza privata (Costringe + violenza|minaccia) PIÙ il profitto ingiusto.
Costringe, oneof[Violenza, Minaccia], IngiustoProfittoAltruiDanno, Dolo {
  tipico_629: =>O@Giudice FattoTipico
  pena_629:   O(Sanziona) =>O@Giudice ReclusioneEstorsione
}

# Danneggiamento (635): a querela; d'ufficio e pena maggiore se con violenza.
Distrugge, Dolo {
  proc_635:   oneof[Querela, Violenza, Minaccia] =>O@Giudice Procedibile
  tipico_635: O(Procedibile) =>O@Giudice FattoTipico
  pena_635:   O(Sanziona) =>O@Giudice ReclusioneDanneggiamento
  pena_635v:  oneof[Violenza, Minaccia], O(Sanziona) =>O@Giudice ReclusioneDanneggiamentoViolento  overrides ReclusioneDanneggiamento
}

# Truffa (640): artifizi/raggiri inducendo in errore + ingiusto profitto/danno.
ArtifiziRaggiri, IngiustoProfittoAltruiDanno, Dolo {
  tipico_640: =>O@Giudice FattoTipico
  pena_640:   O(Sanziona) =>O@Giudice ReclusioneTruffa
}

# Appropriazione indebita (646): appropriarsi della cosa già posseduta, a fine
# di profitto; a querela. (Differenza dal furto: il possesso preesiste.)
SiAppropria, FineDiProfitto, Dolo {
  proc_646:   Querela =>O@Giudice Procedibile
  tipico_646: O(Procedibile) =>O@Giudice FattoTipico
  pena_646:   O(Sanziona) =>O@Giudice ReclusioneAppropriazione
}

# Ricettazione (648): acquistare/ricevere/occultare cose di provenienza
# delittuosa, a fine di profitto, fuori dal concorso nel reato presupposto.
AcquistaRiceveOcculta, ProvenienzaDelitto, FineDiProfitto, Dolo {
  tipico_648: =>O@Giudice FattoTipico
  pena_648:   O(Sanziona) =>O@Giudice ReclusioneRicettazione
}

# Usura (644): farsi dare o promettere interessi usurari in corrispettivo di una
# prestazione di denaro o altra utilità.
FaDarePromettereInteressiUsurari, Dolo {
  tipico_644: =>O@Giudice FattoTipico
  pena_644:   O(Sanziona) =>O@Giudice ReclusioneUsura
}
