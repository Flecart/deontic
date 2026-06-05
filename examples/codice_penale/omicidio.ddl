# Codice Penale — OMICIDIO (artt. 575-577), scomposto nei suoi elementi.
# ===========================================================================
#   art. 575: "Chiunque cagiona la morte di un uomo[1]" + dolo[2] (art. 43)
# Il dolo distingue l'omicidio doloso dal colposo (589) e preterintenzionale (584).
# Le aggravanti degli artt. 576-577 portano all'ERGASTOLO: stesso atomo
# `Ergastolo` di definizioni.ddl (medesima pena di strage, sequestro, ecc.).
from definizioni.ddl import *

facts:

atom Reclusione575:              base penalty: reclusion of not less than 21 years (art. 575) | quote: è punito con la reclusione non inferiore ad anni ventuno | uri: examples/codice_penale/sources/codice_penale_full.md#L7708-L7712
atom Premeditazione:             the killing was premeditated (art. 576 n. 5 / art. 577 n. 3) | quote: ovvero quando vi è premeditazione | uri: examples/codice_penale/sources/codice_penale_full.md#L7718-L7748
atom ControAscendenteDiscendente: the victim is an ascendant or descendant of the offender (art. 577 n. 1) | quote: contro l'ascendente o il discendente | uri: examples/codice_penale/sources/codice_penale_full.md#L7751-L7766
atom MezzoInsidioso:             the killing used poison or another insidious means (art. 577 n. 2) | quote: col mezzo di sostanze venefiche, ovvero con un altro mezzo insidioso | uri: examples/codice_penale/sources/codice_penale_full.md#L7751-L7766

# Precetto: non cagionare la morte di un uomo (norma primaria).
precetto_575: =>O@Chiunque ~CagionaMorte

# Evento morte + dolo: comuni a tutte le regole sotto.
CagionaMorte, Dolo {
  # Fatto tipico: omicidio doloso.
  tipico_575: =>O@Giudice FattoTipico
  # Pena base (art. 575): reclusione >= 21 anni.
  pena_575:   O(Sanziona) =>O@Giudice Reclusione575
  # Aggravanti (artt. 576-577) -> ERGASTOLO (atomo condiviso); scavalca la base.
  pena_aggr:  oneof[Premeditazione, ControAscendenteDiscendente, MezzoInsidioso], O(Sanziona) =>O@Giudice Ergastolo  overrides Reclusione575
}

# (Scriminanti / non imputabilità ereditate dalla parte generale: cfr. tests.sh.)
