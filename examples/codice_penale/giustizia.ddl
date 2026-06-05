# Codice Penale — DELITTI CONTRO L'AMMINISTRAZIONE DELLA GIUSTIZIA (368, 372, 378).
# ===========================================================================
# Calunnia, falsa testimonianza, favoreggiamento personale.
from definizioni.ddl import *

facts:

atom IncolpaInnocente:     by complaint/charge/report to a judicial (or reporting) authority, the agent accuses of a crime someone they know to be innocent, or fabricates evidence against them (art. 368) | quote: incolpa di un reato taluno che egli sa innocente, ovvero simula a carico di lui le tracce di un reato | uri: examples/codice_penale/sources/codice_penale_full.md#L4886-L4896
atom TestimoneAutorita:    the agent is deposing as a witness before the judicial authority (art. 372) | quote: deponendo come testimone innanzi all'autorità giudiziaria | uri: examples/codice_penale/sources/codice_penale_full.md#L4962-L4968
atom AffermaFalsoNegaVero: the witness affirms what is false, denies what is true, or conceals what they know about the facts asked (art. 372) | quote: afferma il falso o nega il vero, ovvero tace … ciò che sa intorno ai fatti sui quali è interrogato | uri: examples/codice_penale/sources/codice_penale_full.md#L4962-L4968
atom AiutaEludereIndagini: after a crime committed by another, the agent helps someone elude the authority's investigations or escape its searches (art. 378) | quote: aiuta taluno a eludere le investigazioni dell'autorità, o a sottrarsi alle ricerche di questa | uri: examples/codice_penale/sources/codice_penale_full.md#L5066-L5074
atom DelittoAltruiCommesso: a (sufficiently serious) crime has been committed by another person (presupposto of art. 378) | quote: dopo che fu commesso un delitto per il quale la legge stabilisce … l'ergastolo o la reclusione | uri: examples/codice_penale/sources/codice_penale_full.md#L5066-L5074
atom FuoriConcorso:        the agent did not take part in that predicate crime (art. 378, "fuori dei casi di concorso") | quote: fuori dei casi di concorso nel medesimo | uri: examples/codice_penale/sources/codice_penale_full.md#L5066-L5074
atom ReclusioneCalunnia:           penalty: reclusion (art. 368) | quote: incolpa di un reato taluno che egli sa innocente | uri: examples/codice_penale/sources/codice_penale_full.md#L4886-L4896
atom ReclusioneFalsaTestimonianza: penalty: reclusion 2-6 years (art. 372) | quote: è punito con la reclusione da due a sei anni | uri: examples/codice_penale/sources/codice_penale_full.md#L4962-L4968
atom ReclusioneFavoreggiamento:    penalty: reclusion (art. 378) | quote: aiuta taluno a eludere le investigazioni dell'autorità | uri: examples/codice_penale/sources/codice_penale_full.md#L5066-L5074

precetto_368: =>O@Chiunque ~IncolpaInnocente
precetto_372: =>O@Chiunque ~AffermaFalsoNegaVero
precetto_378: =>O@Chiunque ~AiutaEludereIndagini

# Calunnia (368): incolpare chi si sa innocente (dolo — "sa innocente").
IncolpaInnocente, Dolo {
  tipico_368: =>O@Giudice FattoTipico
  pena_368:   O(Sanziona) =>O@Giudice ReclusioneCalunnia
}

# Falsa testimonianza (372): testimone che afferma il falso / nega il vero.
TestimoneAutorita, AffermaFalsoNegaVero, Dolo {
  tipico_372: =>O@Giudice FattoTipico
  pena_372:   O(Sanziona) =>O@Giudice ReclusioneFalsaTestimonianza
}

# Favoreggiamento personale (378): aiutare chi ha commesso un delitto a eludere
# le indagini, fuori dal concorso nel reato presupposto.
DelittoAltruiCommesso, AiutaEludereIndagini, FuoriConcorso, Dolo {
  tipico_378: =>O@Giudice FattoTipico
  pena_378:   O(Sanziona) =>O@Giudice ReclusioneFavoreggiamento
}
