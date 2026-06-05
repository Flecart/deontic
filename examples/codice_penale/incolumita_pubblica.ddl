# Codice Penale — DELITTI CONTRO L'INCOLUMITÀ PUBBLICA (artt. 422, 423, 438).
# ===========================================================================
# Strage, incendio, epidemia. Strage ed epidemia comminano l'ERGASTOLO: stesso
# atomo `Ergastolo` di definizioni.ddl (la pena di morte è abolita).
from definizioni.ddl import *

facts:

atom AttiPericoloIncolumita: the agent performs acts apt to endanger public safety (art. 422) | quote: compie atti tali da porre in pericolo la pubblica incolumità | uri: examples/codice_penale/sources/codice_penale_full.md#L5759-L5766
atom FineDiUccidere:         the agent acted with the aim of killing (dolo specifico, art. 422) | quote: al fine di uccidere | uri: examples/codice_penale/sources/codice_penale_full.md#L5759-L5766
atom MorteDiPiuPersone:      the death of several persons results from the act (event of art. 422) | quote: se dal fatto deriva la morte di più persone | uri: examples/codice_penale/sources/codice_penale_full.md#L5759-L5766
atom CagionaIncendio:        the agent causes a fire (art. 423) | quote: Chiunque cagiona un incendio | uri: examples/codice_penale/sources/codice_penale_full.md#L5768-L5775
atom CagionaEpidemia:        the agent causes an epidemic by spreading pathogenic germs (art. 438) | quote: Chiunque cagiona un'epidemia mediante la diffusione di germi patogeni | uri: examples/codice_penale/sources/codice_penale_full.md#L5953-L5959
atom ReclusioneIncendio:     penalty: reclusion 3-7 years (art. 423) | quote: è punito con la reclusione da tre a sette anni | uri: examples/codice_penale/sources/codice_penale_full.md#L5768-L5775

precetto_422: =>O@Chiunque ~AttiPericoloIncolumita
precetto_423: =>O@Chiunque ~CagionaIncendio
precetto_438: =>O@Chiunque ~CagionaEpidemia

# Strage (422): atti che pongono in pericolo la pubblica incolumità, al fine di
# uccidere, da cui deriva la morte di più persone -> ERGASTOLO (atomo condiviso).
AttiPericoloIncolumita, FineDiUccidere, MorteDiPiuPersone, Dolo {
  tipico_422: =>O@Giudice FattoTipico
  pena_422:   O(Sanziona) =>O@Giudice Ergastolo
}

# Incendio (423): cagionare un incendio.
CagionaIncendio, Dolo {
  tipico_423: =>O@Giudice FattoTipico
  pena_423:   O(Sanziona) =>O@Giudice ReclusioneIncendio
}

# Epidemia (438): cagionare un'epidemia diffondendo germi patogeni -> ergastolo.
CagionaEpidemia, Dolo {
  tipico_438: =>O@Giudice FattoTipico
  pena_438:   O(Sanziona) =>O@Giudice Ergastolo
}
