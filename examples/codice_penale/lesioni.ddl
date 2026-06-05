# Codice Penale — PERCOSSE, LESIONI, OMICIDIO PRETERINTENZIONALE (artt. 581-590).
# ===========================================================================
# Capo "dei delitti contro la vita e l'incolumità individuale". Mostra la
# gradazione per elementi: percuotere → (se ne deriva malattia) lesione → (se
# grave) lesione grave; e la distinzione dolo/colpa.
from definizioni.ddl import *

facts:

atom Percuote:                strikes or beats a person (art. 581) | quote: Chiunque percuote taluno | uri: examples/codice_penale/sources/codice_penale_full.md#L7800-L7806
atom CagionaLesione:          causes a personal injury to someone (art. 582) | quote: Chiunque cagiona ad alcuno una lesione personale | uri: examples/codice_penale/sources/codice_penale_full.md#L7815-L7820
atom LesioneGrave:            the injury is grave — life-endangering illness, illness/incapacity over 40 days, or permanent weakening of a sense or organ (art. 583) | quote: La lesione personale è grave … una malattia che metta in pericolo la vita | uri: examples/codice_penale/sources/codice_penale_full.md#L7828-L7840
atom AttiDirettiLesione:      the acts were aimed at committing percosse or lesione of artt. 581-582 (art. 584, preterintenzione) | quote: con atti diretti a commettere uno dei delitti preveduti dagli articoli 581 e 582 | uri: examples/codice_penale/sources/codice_penale_full.md#L7847-L7852
atom ReclusionePercosse:      penalty: reclusion up to 6 months or fine, a querela (art. 581) | quote: con la reclusione fino a sei mesi o con la multa fino a euro 309 | uri: examples/codice_penale/sources/codice_penale_full.md#L7800-L7806
atom ReclusioneLesione:       penalty: reclusion 3 months-3 years (art. 582) | quote: è punito con la reclusione da tre mesi a tre anni | uri: examples/codice_penale/sources/codice_penale_full.md#L7815-L7820
atom ReclusioneLesioneGrave:  penalty: reclusion 3-7 years (art. 583) | quote: si applica la reclusione da tre a sette anni | uri: examples/codice_penale/sources/codice_penale_full.md#L7828-L7840
atom ReclusionePreterint:     penalty: reclusion 10-18 years (art. 584) | quote: è punito con la reclusione da dieci a diciotto anni | uri: examples/codice_penale/sources/codice_penale_full.md#L7847-L7852
atom ReclusioneLesioneColposa: penalty: reclusion up to 3 months or fine (art. 590) | quote: è punito con la reclusione fino a tre mesi o con la multa fino a euro 309 | uri: examples/codice_penale/sources/codice_penale_full.md#L7920-L7928

precetto_581: =>O@Chiunque ~Percuote
precetto_582: =>O@Chiunque ~CagionaLesione

# Percosse (581): a querela, e solo se NON deriva malattia (581 c.1) — il che è
# reso dal fatto che la lesione (582) scavalca le percosse quando c'è malattia.
Percuote, Dolo {
  proc_581:   Querela =>O@Giudice Procedibile
  tipico_581: O(Procedibile) =>O@Giudice FattoTipico
  pena_581:   O(Sanziona) =>O@Giudice ReclusionePercosse
}

# Lesione personale (582 dolosa): cagiona lesione da cui deriva malattia.
# La lesione lieve è a querela, la grave (583) d'ufficio.
CagionaLesione, MalattiaCorpoMente, Dolo {
  proc_582:   oneof[Querela, LesioneGrave] =>O@Giudice Procedibile
  tipico_582: O(Procedibile) =>O@Giudice FattoTipico
  pena_582:   O(Sanziona) =>O@Giudice ReclusioneLesione  overrides ReclusionePercosse
  # Lesione grave (583): pena maggiore, scavalca la lesione semplice.
  pena_583:   LesioneGrave, O(Sanziona) =>O@Giudice ReclusioneLesioneGrave  overrides ReclusioneLesione
}

# Omicidio preterintenzionale (584): atti diretti a percosse/lesione + morte
# (NON voluta: niente dolo di omicidio — è ciò che lo distingue dal 575).
AttiDirettiLesione, CagionaMorte {
  tipico_584: =>O@Giudice FattoTipico
  pena_584:   O(Sanziona) =>O@Giudice ReclusionePreterint
}

# Lesioni personali colpose (590): lesione cagionata per colpa (non per dolo).
CagionaLesione, Colpa {
  tipico_590: =>O@Giudice FattoTipico
  pena_590:   O(Sanziona) =>O@Giudice ReclusioneLesioneColposa
}
