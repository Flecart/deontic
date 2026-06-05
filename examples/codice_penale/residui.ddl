# Codice Penale — residui (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom ImpiegaSegretiStato: uses, for own or others' profit, scientific inventions/discoveries that must remain secret in the State's interest (art. 263) | quote: Utilizzazione dei segreti di Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3367-L3375
atom ReclusioneUtilizzazioneSegreti: reclusion not less than 5 years (art. 263) | quote: Utilizzazione dei segreti di Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3367-L3375
precetto_263: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, ImpiegaSegretiStato, Dolo {
  tipico_263: =>O@Giudice FattoTipico
  pena_263:   O(Sanziona) =>O@Giudice ReclusioneUtilizzazioneSegreti
}

atom ImpiegaInvenzioniUfficio: uses, for own or others' profit, inventions or discoveries known by reason of office (art. 325) | quote: Utilizzazione d'invenzioni o scoperte conosciute per ragione d'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L4304-L4311
atom ReclusioneUtilizzazioneInvenzioni: reclusion 1-5 years and fine (art. 325) | quote: Utilizzazione d'invenzioni o scoperte conosciute per ragione d'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L4304-L4311
precetto_325: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, ImpiegaInvenzioniUfficio, Dolo {
  tipico_325: =>O@Giudice FattoTipico
  pena_325:   O(Sanziona) =>O@Giudice ReclusioneUtilizzazioneInvenzioni
}

atom AgenteForzaPubblica: a soldier or agent of the public force (art. 329) | quote: Rifiuto o ritardo di obbedienza commesso da un militare o da un agente della forza pubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L4370-L4378
atom RifiutaEseguireRichiesta: unduly refuses or delays to execute a request lawfully made by the competent authority (art. 329) | quote: Rifiuto o ritardo di obbedienza commesso da un militare o da un agente della forza pubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L4370-L4378
atom ReclusioneRifiutoMilitare: reclusion up to 2 years (art. 329) | quote: Rifiuto o ritardo di obbedienza commesso da un militare o da un agente della forza pubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L4370-L4378
precetto_329: =>O@Chiunque ~AgenteForzaPubblica
AgenteForzaPubblica, RifiutaEseguireRichiesta, Dolo {
  tipico_329: =>O@Giudice FattoTipico
  pena_329:   O(Sanziona) =>O@Giudice ReclusioneRifiutoMilitare
}

atom InterrompeServizioPubblico: running a public-service or public-necessity enterprise, interrupts the service or suspends the work (art. 331) | quote: Interruzione di un servizio pubblico o di pubblica necessità | uri: examples/codice_penale/sources/codice_penale_full.md#L4401-L4409
atom ReclusioneInterruzioneImpresa: reclusion 6 months-1 year and fine (art. 331) | quote: Interruzione di un servizio pubblico o di pubblica necessità | uri: examples/codice_penale/sources/codice_penale_full.md#L4401-L4409
precetto_331: =>O@Chiunque ~InterrompeServizioPubblico
InterrompeServizioPubblico, Dolo {
  tipico_331: =>O@Giudice FattoTipico
  pena_331:   O(Sanziona) =>O@Giudice ReclusioneInterruzioneImpresa
}

atom PatrocinioBiprofessionale: a lawyer or technical consultant who, in proceedings, simultaneously assists opposing parties (art. 381) | quote: Altre infedeltà del patrocinatore o del consulente tecnico | uri: examples/codice_penale/sources/codice_penale_full.md#L5132-L5140
atom ReclusionePatrocinioBi: reclusion 6 months-3 years and fine (art. 381) | quote: Altre infedeltà del patrocinatore o del consulente tecnico | uri: examples/codice_penale/sources/codice_penale_full.md#L5132-L5140
precetto_381: =>O@Chiunque ~PatrocinioBiprofessionale
PatrocinioBiprofessionale, Dolo {
  tipico_381: =>O@Giudice FattoTipico
  pena_381:   O(Sanziona) =>O@Giudice ReclusionePatrocinioBi
}

atom MillantaCreditoGiudice: a lawyer who, boasting influence with the judge, prosecutor or witness, gets given or promised money/utility (art. 382) | quote: Millantato credito del patrocinatore | uri: examples/codice_penale/sources/codice_penale_full.md#L5145-L5153
atom ReclusioneMillantatoPatrocinatore: reclusion 1-5 years (art. 382) | quote: Millantato credito del patrocinatore | uri: examples/codice_penale/sources/codice_penale_full.md#L5145-L5153
precetto_382: =>O@Chiunque ~MillantaCreditoGiudice
MillantaCreditoGiudice, Dolo {
  tipico_382: =>O@Giudice FattoTipico
  pena_382:   O(Sanziona) =>O@Giudice ReclusioneMillantatoPatrocinatore
}

atom FalsificaCopieAutentiche: in the exercise of functions, falsely forms authentic copies of public/private acts or attestations of their content (art. 478) | quote: Falsità materiale commessa dal pubblico ufficiale in copie autentiche di atti pubblici o privati e in attestati del | uri: examples/codice_penale/sources/codice_penale_full.md#L6371-L6379
atom ReclusioneFalsoCopie: reclusion 1-4 years (art. 478) | quote: Falsità materiale commessa dal pubblico ufficiale in copie autentiche di atti pubblici o privati e in attestati del | uri: examples/codice_penale/sources/codice_penale_full.md#L6371-L6379
precetto_478: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, FalsificaCopieAutentiche, Dolo {
  tipico_478: =>O@Giudice FattoTipico
  pena_478:   O(Sanziona) =>O@Giudice ReclusioneFalsoCopie
}

atom DatoreNonAdempieContratto: an employer or worker who fails the obligations deriving from a collective labour contract (art. 509) | quote: Inosservanza delle norme disciplinanti i rapporti di lavoro | uri: examples/codice_penale/sources/codice_penale_full.md#L6815-L6823
atom ReclusioneInosservanzaLavoro: fine, breach of collective labour contract (art. 509) | quote: Inosservanza delle norme disciplinanti i rapporti di lavoro | uri: examples/codice_penale/sources/codice_penale_full.md#L6815-L6823
precetto_509: =>O@Chiunque ~DatoreNonAdempieContratto
DatoreNonAdempieContratto, Dolo {
  tipico_509: =>O@Giudice FattoTipico
  pena_509:   O(Sanziona) =>O@Giudice ReclusioneInosservanzaLavoro
}

atom CongiunzionePersonaArrestata: has carnal union with a person who is arrested or detained and entrusted to them, or under their authority (art. 520) | quote: Congiunzione carnale commessa con abuso della qualità di pubblico ufficiale | uri: examples/codice_penale/sources/codice_penale_full.md#L6957-L6965
atom ReclusioneCongiunzioneArrestata: reclusion 6 months-3 years (art. 520) | quote: Congiunzione carnale commessa con abuso della qualità di pubblico ufficiale | uri: examples/codice_penale/sources/codice_penale_full.md#L6957-L6965
precetto_520: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, CongiunzionePersonaArrestata, Dolo {
  tipico_520: =>O@Giudice FattoTipico
  pena_520:   O(Sanziona) =>O@Giudice ReclusioneCongiunzioneArrestata
}

atom OrganizzaSpettacoliSevizie: organises or promotes spectacles or events involving cruelty or torture of animals (art. 544-quater) | quote: Spettacoli o manifestazioni vietati | uri: examples/codice_penale/sources/codice_penale_full.md#L7276-L7284
atom ReclusioneSpettacoliSevizie: reclusion 4 months-2 years and fine (art. 544-quater) | quote: Spettacoli o manifestazioni vietati | uri: examples/codice_penale/sources/codice_penale_full.md#L7276-L7284
precetto_544quater: =>O@Chiunque ~OrganizzaSpettacoliSevizie
OrganizzaSpettacoliSevizie, Dolo {
  tipico_544quater: =>O@Giudice FattoTipico
  pena_544quater:   O(Sanziona) =>O@Giudice ReclusioneSpettacoliSevizie
}

atom ArrestoIllegale: proceeds to an arrest abusing the powers inherent in their functions, outside the cases allowed by law (art. 606) | quote: Arresto illegale | uri: examples/codice_penale/sources/codice_penale_full.md#L8467-L8475
atom ReclusioneArrestoIllegale: reclusion up to 3 years (art. 606) | quote: Arresto illegale | uri: examples/codice_penale/sources/codice_penale_full.md#L8467-L8475
precetto_606: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, ArrestoIllegale, Dolo {
  tipico_606: =>O@Giudice FattoTipico
  pena_606:   O(Sanziona) =>O@Giudice ReclusioneArrestoIllegale
}

atom IndebitaRestrizioneDetenuto: in charge of a prison, receives a person without a lawful order, or unduly prolongs their detention (art. 607) | quote: Indebita limitazione di libertà personale | uri: examples/codice_penale/sources/codice_penale_full.md#L8476-L8484
atom ReclusioneIndebitaRestrizione: reclusion up to 15 months (art. 607) | quote: Indebita limitazione di libertà personale | uri: examples/codice_penale/sources/codice_penale_full.md#L8476-L8484
precetto_607: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, IndebitaRestrizioneDetenuto, Dolo {
  tipico_607: =>O@Giudice FattoTipico
  pena_607:   O(Sanziona) =>O@Giudice ReclusioneIndebitaRestrizione
}

atom MisureRigoreIllegali: subjects an arrested or detained person under their authority to measures of rigour not allowed by law (art. 608) | quote: Abuso di autorità contro arrestati o detenuti | uri: examples/codice_penale/sources/codice_penale_full.md#L8485-L8493
atom ReclusioneMisureRigore: reclusion up to 30 months (art. 608) | quote: Abuso di autorità contro arrestati o detenuti | uri: examples/codice_penale/sources/codice_penale_full.md#L8485-L8493
precetto_608: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, MisureRigoreIllegali, Dolo {
  tipico_608: =>O@Giudice FattoTipico
  pena_608:   O(Sanziona) =>O@Giudice ReclusioneMisureRigore
}

atom IntroduceDomicilioAbusoUfficio: abusing the powers of their functions, enters or stays in a private dwelling outside the cases allowed by law (art. 615) | quote: Violazione di domicilio commessa da un pubblico ufficiale | uri: examples/codice_penale/sources/codice_penale_full.md#L8805-L8813
atom ReclusioneDomicilioAbusoUfficio: reclusion (the penalties of art. 614, increased) (art. 615) | quote: Violazione di domicilio commessa da un pubblico ufficiale | uri: examples/codice_penale/sources/codice_penale_full.md#L8805-L8813
precetto_615: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, IntroduceDomicilioAbusoUfficio, Dolo {
  tipico_615: =>O@Giudice FattoTipico
  pena_615:   O(Sanziona) =>O@Giudice ReclusioneDomicilioAbusoUfficio
}
