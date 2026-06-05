# Codice Penale — altri delitti contro il patrimonio (626, 630, 633, 634, 642, 643, 647).
# ===========================================================================
from definizioni.ddl import *

facts:

atom SottrazioneUso:       the taking was to make momentary use of the thing, immediately returned afterwards — furto d'uso (art. 626 n. 1) | quote: Si applica la reclusione fino a un anno … e il delitto è punibile a querela | uri: examples/codice_penale/sources/codice_penale_full.md#L9202-L9210
atom SequestraPersona:     the agent seizes a person (art. 630) | quote: Chiunque sequestra una persona | uri: examples/codice_penale/sources/codice_penale_full.md#L9278-L9286
atom ScopoPrezzoLiberazione: the seizure aims to obtain an unjust profit as the price of release — ransom (art. 630) | quote: allo scopo di conseguire … un ingiusto profitto come prezzo della liberazione | uri: examples/codice_penale/sources/codice_penale_full.md#L9278-L9286
atom MorteSequestrato:     death of the seized person results (art. 630 aggravated) | quote: se dal fatto deriva la morte … del sequestrato | uri: examples/codice_penale/sources/codice_penale_full.md#L9278-L9292
atom InvadeTerreniEdifici: the agent arbitrarily invades another's land or buildings (art. 633) | quote: invade arbitrariamente terreni o edifici altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9325-L9333
atom FineOccupareProfitto: in order to occupy them or otherwise profit (dolo specifico, art. 633) | quote: al fine di occuparli o di trarne altrimenti profitto | uri: examples/codice_penale/sources/codice_penale_full.md#L9325-L9333
atom TurbaPossesso:        the agent disturbs another's peaceful possession of immovable things (art. 634) | quote: turba … l'altrui pacifico possesso di cose immobili | uri: examples/codice_penale/sources/codice_penale_full.md#L9342-L9350
atom DanneggiaBeniAssicurati: the agent damages their own insured goods (or mutilates their own body) to obtain insurance indemnity (art. 642) | quote: al fine di conseguire … l'indennizzo di una assicurazione | uri: examples/codice_penale/sources/codice_penale_full.md#L9585-L9593
atom AbusaInfermitaBisogni: the agent abuses the needs, passions or inexperience of a minor, or the infirmity/deficiency of a person, inducing a harmful act (art. 643) | quote: abusando dei bisogni, delle passioni o della inesperienza … ovvero abusando dello stato d'infermità | uri: examples/codice_penale/sources/codice_penale_full.md#L9605-L9613
atom SiAppropriaCoseSmarrite: the agent appropriates lost things, treasure, or things received by error or chance (art. 647) | quote: Appropriazione di cose smarrite, del tesoro o di cose avute per errore o caso fortuito | uri: examples/codice_penale/sources/codice_penale_full.md#L9710-L9718
atom ReclusioneFurtoUso:   penalty: reclusion up to 1 year or fine, a querela (art. 626) | quote: Si applica la reclusione fino a un anno ovvero la multa fino a euro 206 | uri: examples/codice_penale/sources/codice_penale_full.md#L9202-L9210
atom ReclusioneSequestroEstorsione: penalty: reclusion 25-30 years (art. 630) | quote: è punito con la reclusione da venticinque a trenta anni | uri: examples/codice_penale/sources/codice_penale_full.md#L9278-L9286
atom ReclusioneInvasione:  penalty: reclusion up to 2 years, a querela (art. 633) | quote: a querela della persona offesa, con la reclusione fino a … | uri: examples/codice_penale/sources/codice_penale_full.md#L9325-L9333
atom ReclusioneTurbativa:  penalty: reclusion up to 2 years (art. 634) | quote: con la reclusione fino a due … | uri: examples/codice_penale/sources/codice_penale_full.md#L9342-L9350
atom ReclusioneFrodeAssic: penalty: reclusion (art. 642) | quote: al fine di conseguire … l'indennizzo di una assicurazione | uri: examples/codice_penale/sources/codice_penale_full.md#L9585-L9593
atom ReclusioneCirconvenzione: penalty: reclusion 2-6 years and fine (art. 643) | quote: è punito con la reclusione da due a sei anni | uri: examples/codice_penale/sources/codice_penale_full.md#L9605-L9613
atom ReclusioneApprSmarrite: penalty: reclusion up to 1 year or fine, a querela (art. 647) | quote: a querela della persona offesa, con la reclusione fino a un anno | uri: examples/codice_penale/sources/codice_penale_full.md#L9710-L9718

precetto_630: =>O@Chiunque ~SequestraPersona
precetto_633: =>O@Chiunque ~InvadeTerreniEdifici
precetto_634: =>O@Chiunque ~TurbaPossesso
precetto_642: =>O@Chiunque ~DanneggiaBeniAssicurati
precetto_643: =>O@Chiunque ~AbusaInfermitaBisogni
precetto_647: =>O@Chiunque ~SiAppropriaCoseSmarrite

# Furto d'uso (626): sottrazione per uso momentaneo, a querela.
SottrazioneUso, Sottrazione, Dolo {
  proc_626:   Querela =>O@Giudice Procedibile
  tipico_626: O(Procedibile) =>O@Giudice FattoTipico
  pena_626:   O(Sanziona) =>O@Giudice ReclusioneFurtoUso
}

# Sequestro a scopo di estorsione (630): se ne deriva la morte -> ergastolo.
SequestraPersona, ScopoPrezzoLiberazione, Dolo {
  tipico_630: =>O@Giudice FattoTipico
  pena_630:   O(Sanziona) =>O@Giudice ReclusioneSequestroEstorsione
  pena_630m:  MorteSequestrato, O(Sanziona) =>O@Giudice Ergastolo  overrides ReclusioneSequestroEstorsione
}

# Invasione di terreni/edifici (633): a querela.
InvadeTerreniEdifici, FineOccupareProfitto, Dolo {
  proc_633:   Querela =>O@Giudice Procedibile
  tipico_633: O(Procedibile) =>O@Giudice FattoTipico
  pena_633:   O(Sanziona) =>O@Giudice ReclusioneInvasione
}

# Turbativa violenta del possesso (634): con violenza o minaccia (condivise).
TurbaPossesso, oneof[Violenza, Minaccia], Dolo {
  tipico_634: =>O@Giudice FattoTipico
  pena_634:   O(Sanziona) =>O@Giudice ReclusioneTurbativa
}

# Frode assicurativa (642).
DanneggiaBeniAssicurati, Dolo {
  tipico_642: =>O@Giudice FattoTipico
  pena_642:   O(Sanziona) =>O@Giudice ReclusioneFrodeAssic
}

# Circonvenzione di incapaci (643): abuso di infermità/bisogni a fine di profitto.
AbusaInfermitaBisogni, FineDiProfitto, Dolo {
  tipico_643: =>O@Giudice FattoTipico
  pena_643:   O(Sanziona) =>O@Giudice ReclusioneCirconvenzione
}

# Appropriazione di cose smarrite (647): a querela.
SiAppropriaCoseSmarrite, Dolo {
  proc_647:   Querela =>O@Giudice Procedibile
  tipico_647: O(Procedibile) =>O@Giudice FattoTipico
  pena_647:   O(Sanziona) =>O@Giudice ReclusioneApprSmarrite
}
