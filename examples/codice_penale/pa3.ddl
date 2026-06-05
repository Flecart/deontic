# Codice Penale — pa3 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom GiovaErroreAltrui: in the exercise of functions, profits from another's error to appropriate money/utility (art. 316) | quote: Peculato mediante profitto dell'errore altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L4061-L4067
atom ReclusionePeculatoErrore: reclusion 6 months-3 years (art. 316) | quote: Peculato mediante profitto dell'errore altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L4061-L4067
precetto_316: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, GiovaErroreAltrui, Dolo {
  tipico_316: =>O@Giudice FattoTipico
  pena_316:   O(Sanziona) =>O@Giudice ReclusionePeculatoErrore
}

atom OttenutoContributiPubblici: having obtained State/EU public contributions or financing destined to public-interest works/activities (art. 316-bis) | quote: Malversazione a danno dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L4068-L4076
atom DistraeDallaFinalita: fails to use them for those purposes (art. 316-bis) | quote: Malversazione a danno dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L4068-L4076
atom ReclusioneMalversazione: reclusion 6 months-4 years (art. 316-bis) | quote: Malversazione a danno dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L4068-L4076
precetto_316bis: =>O@Chiunque ~OttenutoContributiPubblici
OttenutoContributiPubblici, DistraeDallaFinalita, Dolo {
  tipico_316bis: =>O@Giudice FattoTipico
  pena_316bis:   O(Sanziona) =>O@Giudice ReclusioneMalversazione
}

atom AbusaQualitaPoteri: abusing their quality or powers (art. 317) | quote: Il pubblico ufficiale o l'incaricato di un pubblico servizio, che, abusando della sua qualità o dei suoi poteri | uri: examples/codice_penale/sources/codice_penale_full.md#L4094-L4102
atom CostringeDareUtilita: compels someone to unduly give or promise money or other utility (art. 317) | quote: Il pubblico ufficiale o l'incaricato di un pubblico servizio, che, abusando della sua qualità o dei suoi poteri | uri: examples/codice_penale/sources/codice_penale_full.md#L4094-L4102
atom ReclusioneConcussione: reclusion 6-12 years (art. 317) | quote: Il pubblico ufficiale o l'incaricato di un pubblico servizio, che, abusando della sua qualità o dei suoi poteri | uri: examples/codice_penale/sources/codice_penale_full.md#L4094-L4102
precetto_317: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, AbusaQualitaPoteri, CostringeDareUtilita, Dolo {
  tipico_317: =>O@Giudice FattoTipico
  pena_317:   O(Sanziona) =>O@Giudice ReclusioneConcussione
}

atom OffrePrometteUtilita: offers or promises undue money or other utility to a public official, to induce an act of office or contrary to duty (art. 322) | quote: Istigazione alla corruzione | uri: examples/codice_penale/sources/codice_penale_full.md#L4177-L4185
atom ReclusioneIstigCorruzione: reclusion for instigation to corruption (art. 322) | quote: Istigazione alla corruzione | uri: examples/codice_penale/sources/codice_penale_full.md#L4177-L4185
precetto_322: =>O@Chiunque ~OffrePrometteUtilita
OffrePrometteUtilita, Dolo {
  tipico_322: =>O@Giudice FattoTipico
  pena_322:   O(Sanziona) =>O@Giudice ReclusioneIstigCorruzione
}

atom RivelaSegretiUfficio: violating office duties, reveals or uses secret official information (art. 326) | quote: Rivelazione ed utilizzazione di segreti di ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L4312-L4320
atom ReclusioneRivelazioneSegreti: reclusion 6 months-3 years (art. 326) | quote: Rivelazione ed utilizzazione di segreti di ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L4312-L4320
precetto_326: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, RivelaSegretiUfficio, Dolo {
  tipico_326: =>O@Giudice FattoTipico
  pena_326:   O(Sanziona) =>O@Giudice ReclusioneRivelazioneSegreti
}

atom MillantaCredito: boasting influence with a public official, receives or gets money/utility as the price of their supposed intercession (art. 346) | quote: Millantato credito | uri: examples/codice_penale/sources/codice_penale_full.md#L4621-L4629
atom ReclusioneMillantato: reclusion 1-5 years (art. 346) | quote: Millantato credito | uri: examples/codice_penale/sources/codice_penale_full.md#L4621-L4629
precetto_346: =>O@Chiunque ~MillantaCredito
MillantaCredito, Dolo {
  tipico_346: =>O@Giudice FattoTipico
  pena_346:   O(Sanziona) =>O@Giudice ReclusioneMillantato
}

atom UsurpaFunzionePubblica: usurps a public function or the powers of a public employment (art. 347) | quote: Usurpazione di funzioni pubbliche | uri: examples/codice_penale/sources/codice_penale_full.md#L4633-L4641
atom ReclusioneUsurpazione: reclusion up to 2 years (art. 347) | quote: Usurpazione di funzioni pubbliche | uri: examples/codice_penale/sources/codice_penale_full.md#L4633-L4641
precetto_347: =>O@Chiunque ~UsurpaFunzionePubblica
UsurpaFunzionePubblica, Dolo {
  tipico_347: =>O@Giudice FattoTipico
  pena_347:   O(Sanziona) =>O@Giudice ReclusioneUsurpazione
}

atom CommetteFrodeForniture: commits fraud in the performance of public-supply contracts (art. 356) | quote: Frode nelle pubbliche forniture | uri: examples/codice_penale/sources/codice_penale_full.md#L4740-L4748
atom ReclusioneFrodeForniture: reclusion 1-5 years and fine (art. 356) | quote: Frode nelle pubbliche forniture | uri: examples/codice_penale/sources/codice_penale_full.md#L4740-L4748
precetto_356: =>O@Chiunque ~CommetteFrodeForniture
CommetteFrodeForniture, Dolo {
  tipico_356: =>O@Giudice FattoTipico
  pena_356:   O(Sanziona) =>O@Giudice ReclusioneFrodeForniture
}

atom ViolaSigilli: violates seals affixed by law or authority to ensure the preservation or identity of a thing (art. 349) | quote: Violazione di sigilli | uri: examples/codice_penale/sources/codice_penale_full.md#L4657-L4665
atom ReclusioneViolazioneSigilli: reclusion 6 months-3 years (art. 349) | quote: Violazione di sigilli | uri: examples/codice_penale/sources/codice_penale_full.md#L4657-L4665
precetto_349: =>O@Chiunque ~ViolaSigilli
ViolaSigilli, Dolo {
  tipico_349: =>O@Giudice FattoTipico
  pena_349:   O(Sanziona) =>O@Giudice ReclusioneViolazioneSigilli
}

atom ControCorpoPolitico: directed at a political, administrative or judicial body or a representation of it (art. 338) | quote: Violenza o minaccia ad un corpo politico, amministrativo o giudiziario | uri: examples/codice_penale/sources/codice_penale_full.md#L4519-L4527
atom ReclusioneViolenzaCorpo: reclusion 1-7 years (art. 338) | quote: Violenza o minaccia ad un corpo politico, amministrativo o giudiziario | uri: examples/codice_penale/sources/codice_penale_full.md#L4519-L4527
precetto_338: =>O@Chiunque ~ControCorpoPolitico
oneof[Violenza, Minaccia], ControCorpoPolitico, Dolo {
  tipico_338: =>O@Giudice FattoTipico
  pena_338:   O(Sanziona) =>O@Giudice ReclusioneViolenzaCorpo
}

atom PercepisceIndebitamenteErogazioni: by use or presentation of false declarations/documents, or omission of due information, unduly obtains public contributions/financing (art. 316-ter) | quote: Indebita percezione di erogazioni a danno dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L4077-L4085
atom ReclusioneIndebitaPercezione: reclusion 6 months-3 years (art. 316-ter) | quote: Indebita percezione di erogazioni a danno dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L4077-L4085
precetto_316ter: =>O@Chiunque ~PercepisceIndebitamenteErogazioni
PercepisceIndebitamenteErogazioni, Dolo {
  tipico_316ter: =>O@Giudice FattoTipico
  pena_316ter:   O(Sanziona) =>O@Giudice ReclusioneIndebitaPercezione
}

atom OltraggioCorpoPolitico: offends the honour or prestige of a political, administrative or judicial body or its representation (art. 342) | quote: Oltraggio a un corpo politico, amministrativo o giudiziario | uri: examples/codice_penale/sources/codice_penale_full.md#L4580-L4588
atom ReclusioneOltraggioCorpo: reclusion, outrage to a public body (art. 342) | quote: Oltraggio a un corpo politico, amministrativo o giudiziario | uri: examples/codice_penale/sources/codice_penale_full.md#L4580-L4588
precetto_342: =>O@Chiunque ~OltraggioCorpoPolitico
OltraggioCorpoPolitico, Dolo {
  tipico_342: =>O@Giudice FattoTipico
  pena_342:   O(Sanziona) =>O@Giudice ReclusioneOltraggioCorpo
}

atom OltraggioMagistrato: offends the honour or prestige of a magistrate at a hearing (art. 343) | quote: Oltraggio a un magistrato in udienza | uri: examples/codice_penale/sources/codice_penale_full.md#L4595-L4603
atom ReclusioneOltraggioMagistrato: reclusion up to 3 years (art. 343) | quote: Oltraggio a un magistrato in udienza | uri: examples/codice_penale/sources/codice_penale_full.md#L4595-L4603
precetto_343: =>O@Chiunque ~OltraggioMagistrato
OltraggioMagistrato, Dolo {
  tipico_343: =>O@Giudice FattoTipico
  pena_343:   O(Sanziona) =>O@Giudice ReclusioneOltraggioMagistrato
}

atom ViolaPubblicaCustodia: subtracts, suppresses, destroys or damages corpora delicti, acts or documents in public custody (art. 351) | quote: Violazione della pubblica custodia di cose | uri: examples/codice_penale/sources/codice_penale_full.md#L4680-L4687
atom ReclusioneViolazioneCustodia: reclusion 6 months-3 years (art. 351) | quote: Violazione della pubblica custodia di cose | uri: examples/codice_penale/sources/codice_penale_full.md#L4680-L4687
precetto_351: =>O@Chiunque ~ViolaPubblicaCustodia
ViolaPubblicaCustodia, Dolo {
  tipico_351: =>O@Giudice FattoTipico
  pena_351:   O(Sanziona) =>O@Giudice ReclusioneViolazioneCustodia
}

atom TurbaGaraIncanti: by gifts, promises, collusion or fraud, impedes or disturbs a public auction or tender (art. 353) | quote: Turbata libertà degli incanti | uri: examples/codice_penale/sources/codice_penale_full.md#L4695-L4703
atom ReclusioneTurbataIncanti: reclusion up to 2 years and fine (art. 353) | quote: Turbata libertà degli incanti | uri: examples/codice_penale/sources/codice_penale_full.md#L4695-L4703
precetto_353: =>O@Chiunque ~TurbaGaraIncanti
oneof[Violenza, Minaccia], TurbaGaraIncanti, Dolo {
  tipico_353: =>O@Giudice FattoTipico
  pena_353:   O(Sanziona) =>O@Giudice ReclusioneTurbataIncanti
}

atom InadempimentoForniturePubbliche: failing the obligations of a supply contract with the State, causes a lack of things needed for a public service (art. 355) | quote: Inadempimento di contratti di pubbliche forniture | uri: examples/codice_penale/sources/codice_penale_full.md#L4717-L4725
atom ReclusioneInadempimentoForniture: reclusion 6 months-3 years and fine (art. 355) | quote: Inadempimento di contratti di pubbliche forniture | uri: examples/codice_penale/sources/codice_penale_full.md#L4717-L4725
precetto_355: =>O@Chiunque ~InadempimentoForniturePubbliche
InadempimentoForniturePubbliche, Dolo {
  tipico_355: =>O@Giudice FattoTipico
  pena_355:   O(Sanziona) =>O@Giudice ReclusioneInadempimentoForniture
}

atom DanneggiaAffissioniAutorita: out of contempt for the authority, removes, tears or renders unusable lawfully made postings (art. 345) | quote: Offesa all'autorità mediante danneggiamento di affissioni | uri: examples/codice_penale/sources/codice_penale_full.md#L4614-L4620
atom ReclusioneDanneggioAffissioni: fine, offence to the authority by damaging postings (art. 345) | quote: Offesa all'autorità mediante danneggiamento di affissioni | uri: examples/codice_penale/sources/codice_penale_full.md#L4614-L4620
precetto_345: =>O@Chiunque ~DanneggiaAffissioniAutorita
DanneggiaAffissioniAutorita, Dolo {
  tipico_345: =>O@Giudice FattoTipico
  pena_345:   O(Sanziona) =>O@Giudice ReclusioneDanneggioAffissioni
}

atom VendeStampatiSequestrati: sells, distributes or posts writings/drawings whose seizure has been ordered (art. 352) | quote: Vendita di stampati dei quali è stato ordinato il sequestro | uri: examples/codice_penale/sources/codice_penale_full.md#L4688-L4694
atom ReclusioneStampatiSequestrati: arrest or fine, sale of seized printed matter (art. 352) | quote: Vendita di stampati dei quali è stato ordinato il sequestro | uri: examples/codice_penale/sources/codice_penale_full.md#L4688-L4694
precetto_352: =>O@Chiunque ~VendeStampatiSequestrati
VendeStampatiSequestrati, Dolo {
  tipico_352: =>O@Giudice FattoTipico
  pena_352:   O(Sanziona) =>O@Giudice ReclusioneStampatiSequestrati
}

atom SottraeCoseSequestrate: subtracts, suppresses, destroys or damages a thing under seizure in criminal or administrative proceedings (art. 334) | quote: Sottrazione o danneggiamento di cose sottoposte a sequestro disposto nel corso di un procedimento penale o | uri: examples/codice_penale/sources/codice_penale_full.md#L4441-L4449
atom ReclusioneSottrazioneSequestro: reclusion 6 months-3 years (art. 334) | quote: Sottrazione o danneggiamento di cose sottoposte a sequestro disposto nel corso di un procedimento penale o | uri: examples/codice_penale/sources/codice_penale_full.md#L4441-L4449
precetto_334: =>O@Chiunque ~SottraeCoseSequestrate
SottraeCoseSequestrate, Dolo {
  tipico_334: =>O@Giudice FattoTipico
  pena_334:   O(Sanziona) =>O@Giudice ReclusioneSottrazioneSequestro
}

atom ColpaCustodiaSequestro: charged with the custody of seized things, by negligence makes their subtraction or damage possible (art. 335) | quote: Violazione colposa di doveri inerenti alla custodia di cose sottoposte a sequestro disposto nel corso di un | uri: examples/codice_penale/sources/codice_penale_full.md#L4463-L4471
atom ReclusioneColpaSequestro: reclusion up to 6 months or fine (art. 335) | quote: Violazione colposa di doveri inerenti alla custodia di cose sottoposte a sequestro disposto nel corso di un | uri: examples/codice_penale/sources/codice_penale_full.md#L4463-L4471
precetto_335: =>O@Chiunque ~ColpaCustodiaSequestro
ColpaCustodiaSequestro, Colpa {
  tipico_335: =>O@Giudice FattoTipico
  pena_335:   O(Sanziona) =>O@Giudice ReclusioneColpaSequestro
}

atom OccultaMezziTrasporto: conceals, keeps or alters transport means whose features have been changed to evade controls (art. 337-bis) | quote: Occultamento, custodia o alterazione di mezzi di trasporto | uri: examples/codice_penale/sources/codice_penale_full.md#L4504-L4512
atom ReclusioneOccultamentoMezzi: reclusion 2-8 years (art. 337-bis) | quote: Occultamento, custodia o alterazione di mezzi di trasporto | uri: examples/codice_penale/sources/codice_penale_full.md#L4504-L4512
precetto_337bis: =>O@Chiunque ~OccultaMezziTrasporto
OccultaMezziTrasporto, Dolo {
  tipico_337bis: =>O@Giudice FattoTipico
  pena_337bis:   O(Sanziona) =>O@Giudice ReclusioneOccultamentoMezzi
}

atom AstensioneIncanti: for money or other utility given or promised, abstains from bidding in a public auction (art. 354) | quote: Astensione dagli incanti | uri: examples/codice_penale/sources/codice_penale_full.md#L4710-L4716
atom ReclusioneAstensioneIncanti: reclusion up to 6 months or fine (art. 354) | quote: Astensione dagli incanti | uri: examples/codice_penale/sources/codice_penale_full.md#L4710-L4716
precetto_354: =>O@Chiunque ~AstensioneIncanti
AstensioneIncanti, Dolo {
  tipico_354: =>O@Giudice FattoTipico
  pena_354:   O(Sanziona) =>O@Giudice ReclusioneAstensioneIncanti
}
