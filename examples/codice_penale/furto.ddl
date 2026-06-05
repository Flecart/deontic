# Codice Penale — FURTO (artt. 624-625), scomposto nei suoi elementi.
# ===========================================================================
# Il furto è la CONGIUNZIONE dei suoi elementi costitutivi, ciascuno un fatto
# che il giudice accerta da solo. Se UNO manca, il reato non sussiste e si vede
# QUALE manca.
#   art. 624: "Chiunque s'impossessa[1] della cosa mobile altrui[2],
#   sottraendola a chi la detiene[3], al fine di trarne profitto[4]"
# Gli elementi 1-4 sono CONDIVISI (definizioni.ddl) con rapina/estorsione.
#
# Usa lo zucchero sintattico: blocco di precondizioni `{…}`, `oneof[…]`,
# `overrides` (la pena aggravata scavalca quella base, che resta in vigore).
from definizioni.ddl import *

facts:

atom ViolenzaSulleCose:        the offender used violence on things or a fraudulent means (art. 625 n. 2) | quote: se il colpevole usa violenza sulle cose o si vale di un qualsiasi mezzo fraudolento | uri: examples/codice_penale/sources/codice_penale_full.md#L9154-L9188
atom Destrezza:                the theft was committed with dexterity — pickpocketing (art. 625 n. 4) | quote: se il fatto è commesso con destrezza | uri: examples/codice_penale/sources/codice_penale_full.md#L9154-L9188
atom ReclusioneFurto:          base penalty: reclusion 6 months-3 years and fine (art. 624) | quote: è punito con la reclusione da sei mesi a tre anni e con la multa da euro 154 a euro 516 | uri: examples/codice_penale/sources/codice_penale_full.md#L9116-L9128
atom ReclusioneFurtoAggravata: aggravated penalty: reclusion 1-6 years and a heavier fine (art. 625) | quote: La pena per il fatto previsto dall'articolo 624 è della reclusione da uno a sei anni e della multa da euro 103 a euro 1.032 | uri: examples/codice_penale/sources/codice_penale_full.md#L9154-L9188

# Precetto: non sottrarre la cosa altrui (atto appropriativo caratteristico).
precetto_624: =>O@Chiunque ~Sottrazione

# Procedibilità (art. 624 c.3): a querela, oppure d'ufficio se aggravato (625).
proc_querela: Querela =>O@Giudice Procedibile
proc_aggr:    oneof[ViolenzaSulleCose, Destrezza] =>O@Giudice Procedibile

# I quattro elementi del furto valgono per tutte le regole del blocco.
Impossessamento, CosaMobileAltrui, Sottrazione, FineDiProfitto {
  # Fatto tipico punibile: i 4 elementi + la procedibilità.
  tipico_624: O(Procedibile) =>O@Giudice FattoTipico
  # Pena base (art. 624).
  pena_624:   O(Sanziona) =>O@Giudice ReclusioneFurto
  # Pena aggravata (art. 625): scavalca la base (lex specialis).
  pena_625:   oneof[ViolenzaSulleCose, Destrezza], O(Sanziona) =>O@Giudice ReclusioneFurtoAggravata  overrides ReclusioneFurto
}

# (Scriminanti e non imputabilità si applicano da sé via `sanzione_base` nella
#  parte generale — nessun cablaggio per il furto.)
