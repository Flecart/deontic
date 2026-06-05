# Codice Penale — DELITTI CONTRO LA PERSONALITÀ DELLO STATO (270, 283-285, 289).
# ===========================================================================
# Insurrezione armata e devastazione/strage politica comminano l'ERGASTOLO
# (atomo condiviso di definizioni.ddl).
from definizioni.ddl import *

facts:

atom PromuoveAssocSovversiva: the agent promotes, founds, organises or directs associations aimed and apt to violently subvert the constituted economic/social order (art. 270) | quote: promuove, costituisce, organizza o dirige associazioni dirette e idonee a sovvertire violentemente gli ordinamenti | uri: examples/codice_penale/sources/codice_penale_full.md#L3445-L3453
atom AttoViolentoMutareCostituzione: by violent acts, the agent commits a fact apt to change the Constitution or the form of Government (art. 283) | quote: con atti violenti, commette un fatto diretto e idoneo a mutare la Costituzione dello Stato o la forma di Governo | uri: examples/codice_penale/sources/codice_penale_full.md#L3663-L3669
atom PromuoveInsurrezioneArmata: the agent promotes an armed insurrection against the powers of the State (art. 284) | quote: Chiunque promuove un'insurrezione armata contro i poteri dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3669-L3675
atom FattoDevastazioneStrage: the agent commits a fact apt to bring devastation, pillage or massacre in the territory of the State (art. 285) | quote: commette un fatto diretto a portare la devastazione, il saccheggio o la strage nel territorio dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3682-L3690
atom ScopoSicurezzaStato:  with the aim of attacking the security of the State (dolo specifico, art. 285) | quote: allo scopo di attentare alla sicurezza dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3682-L3690
atom AttiViolentiImpedireOrgani: the agent commits violent acts apt to impede, wholly or partly, the exercise of constitutional organs or regional assemblies (art. 289) | quote: chiunque commette atti violenti diretti ad impedire … | uri: examples/codice_penale/sources/codice_penale_full.md#L3722-L3730
atom ReclusioneAssocSovversiva: penalty: reclusion (art. 270) | quote: associazioni dirette e idonee a sovvertire violentemente gli ordinamenti | uri: examples/codice_penale/sources/codice_penale_full.md#L3445-L3453
atom ReclusioneAttentatoCost:  penalty: reclusion not less than 5 years (art. 283) | quote: è punito con la reclusione non inferiore a cinque anni | uri: examples/codice_penale/sources/codice_penale_full.md#L3663-L3669
atom ReclusioneAttentatoOrgani: penalty: reclusion 1-5 years (art. 289) | quote: È punito con la reclusione da uno a cinque anni | uri: examples/codice_penale/sources/codice_penale_full.md#L3722-L3730

precetto_270: =>O@Chiunque ~PromuoveAssocSovversiva
precetto_283: =>O@Chiunque ~AttoViolentoMutareCostituzione
precetto_284: =>O@Chiunque ~PromuoveInsurrezioneArmata
precetto_285: =>O@Chiunque ~FattoDevastazioneStrage
precetto_289: =>O@Chiunque ~AttiViolentiImpedireOrgani

# Associazioni sovversive (270).
PromuoveAssocSovversiva, Dolo {
  tipico_270: =>O@Giudice FattoTipico
  pena_270:   O(Sanziona) =>O@Giudice ReclusioneAssocSovversiva
}

# Attentato contro la costituzione (283).
AttoViolentoMutareCostituzione, Dolo {
  tipico_283: =>O@Giudice FattoTipico
  pena_283:   O(Sanziona) =>O@Giudice ReclusioneAttentatoCost
}

# Insurrezione armata (284) -> ergastolo (atomo condiviso).
PromuoveInsurrezioneArmata, Dolo {
  tipico_284: =>O@Giudice FattoTipico
  pena_284:   O(Sanziona) =>O@Giudice Ergastolo
}

# Devastazione, saccheggio e strage (285), a scopo di sicurezza Stato -> ergastolo.
FattoDevastazioneStrage, ScopoSicurezzaStato, Dolo {
  tipico_285: =>O@Giudice FattoTipico
  pena_285:   O(Sanziona) =>O@Giudice Ergastolo
}

# Attentato contro organi costituzionali (289).
AttiViolentiImpedireOrgani, Dolo {
  tipico_289: =>O@Giudice FattoTipico
  pena_289:   O(Sanziona) =>O@Giudice ReclusioneAttentatoOrgani
}
