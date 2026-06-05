# Codice Penale — RAPINA (art. 628), composta da elementi CONDIVISI.
# ===========================================================================
#   art. 628: "Chiunque, per … ingiusto profitto[4], mediante violenza alla
#   persona o minaccia[5], s'impossessa[1] della cosa mobile altrui[2],
#   sottraendola a chi la detiene[3]"
# La rapina È un furto (elementi 1-4, gli STESSI di furto.ddl) PIÙ la violenza
# o la minaccia [5]. Si riusano gli atomi condivisi e si AGGIUNGE la coercizione.
from definizioni.ddl import *

facts:

atom ReclusioneRapina: penalty: reclusion 3-10 years and fine (art. 628 c.1) | quote: è punito con la reclusione da tre a dieci anni e con la multa da euro 516 a euro 2.065 | uri: examples/codice_penale/sources/codice_penale_full.md#L9233-L9238

# Precetto: vietati sia la sottrazione sia la violenza.
precetto_628_sottr:    =>O@Chiunque ~Sottrazione
precetto_628_violenza: =>O@Chiunque ~Violenza

# I 4 elementi del furto + (violenza OPPURE minaccia): `oneof` rende l'alternativa.
Impossessamento, CosaMobileAltrui, Sottrazione, FineDiProfitto {
  tipico_628: oneof[Violenza, Minaccia] =>O@Giudice FattoTipico
  # Pena (art. 628): reclusione 3-10 anni; procedibile d'ufficio (niente querela).
  pena_628:   O(Sanziona) =>O@Giudice ReclusioneRapina
}

# (Scriminanti / non imputabilità ereditate dalla parte generale.)
# Contrasto-chiave: gli stessi 4 elementi SENZA violenza né minaccia non sono
# rapina (sarebbero furto: vedi furto.ddl con gli stessi fatti).
