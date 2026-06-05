# Codice Penale — DELITTI CONTRO LA LIBERTÀ INDIVIDUALE (artt. 605, 610, 612).
# ===========================================================================
# Sequestro di persona, violenza privata, minaccia. Violenza e minaccia sono
# gli atomi CONDIVISI di definizioni.ddl (gli stessi della rapina).
from definizioni.ddl import *

facts:

atom PrivaLibertaPersonale: deprives someone of their personal liberty (art. 605) | quote: Chiunque priva taluno della libertà personale | uri: examples/codice_penale/sources/codice_penale_full.md#L8450-L8456
atom MinacciaIngiustoDanno: threatens another with an unjust harm (art. 612) | quote: Chiunque minaccia ad altri un ingiusto danno | uri: examples/codice_penale/sources/codice_penale_full.md#L8730-L8736
atom MinacciaGrave:         the threat is grave, or made in the manners of art. 339 (art. 612 c.2 — procedibile d'ufficio) | quote: Se la minaccia è grave … si procede d'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L8730-L8736
atom ReclusioneSequestro:   penalty: reclusion 6 months-8 years (art. 605) | quote: è punito con la reclusione da sei mesi a otto anni | uri: examples/codice_penale/sources/codice_penale_full.md#L8450-L8456
atom ReclusioneViolPrivata: penalty: reclusion up to 4 years (art. 610) | quote: è punito con la reclusione fino a quattro anni | uri: examples/codice_penale/sources/codice_penale_full.md#L8701-L8706
atom MultaMinaccia:         penalty: fine up to 51 euro, a querela (art. 612 c.1) | quote: è punito, a querela della persona offesa, con la multa fino a euro 51 | uri: examples/codice_penale/sources/codice_penale_full.md#L8730-L8736
atom ReclusioneMinacciaGrave: penalty: reclusion up to 1 year, d'ufficio (art. 612 c.2) | quote: la pena è della reclusione fino a un anno e si procede d'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L8730-L8736

precetto_605: =>O@Chiunque ~PrivaLibertaPersonale
precetto_610: =>O@Chiunque ~Costringe
precetto_612: =>O@Chiunque ~MinacciaIngiustoDanno

# Sequestro di persona (605): privazione della libertà personale, dolosa.
PrivaLibertaPersonale, Dolo {
  tipico_605: =>O@Giudice FattoTipico
  pena_605:   O(Sanziona) =>O@Giudice ReclusioneSequestro
}

# Violenza privata (610): costrizione MEDIANTE violenza o minaccia (condivise).
Costringe, oneof[Violenza, Minaccia], Dolo {
  tipico_610: =>O@Giudice FattoTipico
  pena_610:   O(Sanziona) =>O@Giudice ReclusioneViolPrivata
}

# Minaccia (612): a querela; se grave, d'ufficio e pena maggiore (scavalca).
MinacciaIngiustoDanno, Dolo {
  proc_612:   oneof[Querela, MinacciaGrave] =>O@Giudice Procedibile
  tipico_612: O(Procedibile) =>O@Giudice FattoTipico
  pena_612:   O(Sanziona) =>O@Giudice MultaMinaccia
  pena_612g:  MinacciaGrave, O(Sanziona) =>O@Giudice ReclusioneMinacciaGrave  overrides MultaMinaccia
}
