# Codice Penale — giustizia2 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom OmetteDenunciaReato: omits or delays denouncing to the judicial authority a crime known by reason of office (art. 361) | quote: Omessa denuncia di reato da parte del pubblico ufficiale | uri: examples/codice_penale/sources/codice_penale_full.md#L4802-L4810
atom ReclusioneOmessaDenuncia: fine, omitted denunciation of crime (art. 361) | quote: Omessa denuncia di reato da parte del pubblico ufficiale | uri: examples/codice_penale/sources/codice_penale_full.md#L4802-L4810
precetto_361: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, OmetteDenunciaReato, Dolo {
  tipico_361: =>O@Giudice FattoTipico
  pena_361:   O(Sanziona) =>O@Giudice ReclusioneOmessaDenuncia
}

atom ProfessioneSanitaria: exercising a health profession (art. 365) | quote: Omissione di referto | uri: examples/codice_penale/sources/codice_penale_full.md#L4844-L4852
atom OmetteReferto: omits to report to the authority a case bearing the marks of a crime prosecutable ex officio (art. 365) | quote: Omissione di referto | uri: examples/codice_penale/sources/codice_penale_full.md#L4844-L4852
atom ReclusioneOmissioneReferto: reclusion up to 1 year or fine (art. 365) | quote: Omissione di referto | uri: examples/codice_penale/sources/codice_penale_full.md#L4844-L4852
precetto_365: =>O@Chiunque ~ProfessioneSanitaria
ProfessioneSanitaria, OmetteReferto, Dolo {
  tipico_365: =>O@Giudice FattoTipico
  pena_365:   O(Sanziona) =>O@Giudice ReclusioneOmissioneReferto
}

atom SimulaReato: by complaint/charge falsely affirms a crime occurred, or fakes its traces, so that proceedings may begin (art. 367) | quote: Simulazione di reato | uri: examples/codice_penale/sources/codice_penale_full.md#L4874-L4882
atom ReclusioneSimulazione: reclusion 3 months-3 years (art. 367) | quote: Simulazione di reato | uri: examples/codice_penale/sources/codice_penale_full.md#L4874-L4882
precetto_367: =>O@Chiunque ~SimulaReato
SimulaReato, Dolo {
  tipico_367: =>O@Giudice FattoTipico
  pena_367:   O(Sanziona) =>O@Giudice ReclusioneSimulazione
}

atom SiIncolpaFalsamente: before the authority, falsely accuses themselves of a crime they know did not happen or was committed by another (art. 369) | quote: Chiunque, mediante dichiarazione ad alcuna delle autorità indicate nell'articolo precedente, anche se fatta con scritto | uri: examples/codice_penale/sources/codice_penale_full.md#L4910-L4917
atom ReclusioneAutocalunnia: reclusion 1-6 years (art. 369) | quote: Chiunque, mediante dichiarazione ad alcuna delle autorità indicate nell'articolo precedente, anche se fatta con scritto | uri: examples/codice_penale/sources/codice_penale_full.md#L4910-L4917
precetto_369: =>O@Chiunque ~SiIncolpaFalsamente
SiIncolpaFalsamente, Dolo {
  tipico_369: =>O@Giudice FattoTipico
  pena_369:   O(Sanziona) =>O@Giudice ReclusioneAutocalunnia
}

atom ParteInGiudizioCivile: being a party in civil proceedings (art. 371) | quote: Falso giuramento della parte | uri: examples/codice_penale/sources/codice_penale_full.md#L4924-L4932
atom GiuraFalso: swears what is false (art. 371) | quote: Falso giuramento della parte | uri: examples/codice_penale/sources/codice_penale_full.md#L4924-L4932
atom ReclusioneFalsoGiuramento: reclusion 6 months-3 years (art. 371) | quote: Falso giuramento della parte | uri: examples/codice_penale/sources/codice_penale_full.md#L4924-L4932
precetto_371: =>O@Chiunque ~ParteInGiudizioCivile
ParteInGiudizioCivile, GiuraFalso, Dolo {
  tipico_371: =>O@Giudice FattoTipico
  pena_371:   O(Sanziona) =>O@Giudice ReclusioneFalsoGiuramento
}

atom PeritoInterprete: court-appointed expert or interpreter (art. 373) | quote: Falsa perizia o interpretazione | uri: examples/codice_penale/sources/codice_penale_full.md#L4974-L4982
atom ParereMendace: gives lying opinions or interpretations, or affirms facts not conforming to truth (art. 373) | quote: Falsa perizia o interpretazione | uri: examples/codice_penale/sources/codice_penale_full.md#L4974-L4982
atom ReclusioneFalsaPerizia: reclusion 2-6 years (art. 373) | quote: Falsa perizia o interpretazione | uri: examples/codice_penale/sources/codice_penale_full.md#L4974-L4982
precetto_373: =>O@Chiunque ~PeritoInterprete
PeritoInterprete, ParereMendace, Dolo {
  tipico_373: =>O@Giudice FattoTipico
  pena_373:   O(Sanziona) =>O@Giudice ReclusioneFalsaPerizia
}

atom AlteraStatoLuoghi: in civil/administrative proceedings, immutably alters the state of places, things or persons (art. 374) | quote: Frode processuale | uri: examples/codice_penale/sources/codice_penale_full.md#L4983-L4991
atom IngannareGiudice: to deceive the judge in an inspection or experiment (art. 374) | quote: Frode processuale | uri: examples/codice_penale/sources/codice_penale_full.md#L4983-L4991
atom ReclusioneFrodeProcessuale: reclusion 6 months-3 years (art. 374) | quote: Frode processuale | uri: examples/codice_penale/sources/codice_penale_full.md#L4983-L4991
precetto_374: =>O@Chiunque ~AlteraStatoLuoghi
AlteraStatoLuoghi, IngannareGiudice, Dolo {
  tipico_374: =>O@Giudice FattoTipico
  pena_374:   O(Sanziona) =>O@Giudice ReclusioneFrodeProcessuale
}

atom OffrePrometteATestimone: offers or promises money/utility to a person called to make declarations before the judicial authority, to induce false statements or silence (art. 377) | quote: Intralcio alla giustizia | uri: examples/codice_penale/sources/codice_penale_full.md#L5030-L5038
atom ReclusioneIntralcio: reclusion 2-6 years (art. 377) | quote: Intralcio alla giustizia | uri: examples/codice_penale/sources/codice_penale_full.md#L5030-L5038
precetto_377: =>O@Chiunque ~OffrePrometteATestimone
OffrePrometteATestimone, Dolo {
  tipico_377: =>O@Giudice FattoTipico
  pena_377:   O(Sanziona) =>O@Giudice ReclusioneIntralcio
}

atom AiutaAssicurareProdottoReato: outside participation and outside receiving/laundering, helps someone secure the product, profit or price of a crime (art. 379) | quote: Favoreggiamento reale | uri: examples/codice_penale/sources/codice_penale_full.md#L5090-L5098
atom FuoriConcorso: did not take part in the predicate crime (art. 379) | quote: Favoreggiamento reale | uri: examples/codice_penale/sources/codice_penale_full.md#L5090-L5098
atom ReclusioneFavoreggiamentoReale: reclusion, up to the punishment for the predicate crime (art. 379) | quote: Favoreggiamento reale | uri: examples/codice_penale/sources/codice_penale_full.md#L5090-L5098
precetto_379: =>O@Chiunque ~AiutaAssicurareProdottoReato
AiutaAssicurareProdottoReato, FuoriConcorso, Dolo {
  tipico_379: =>O@Giudice FattoTipico
  pena_379:   O(Sanziona) =>O@Giudice ReclusioneFavoreggiamentoReale
}
