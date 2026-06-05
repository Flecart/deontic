# Codice Penale — fede2 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom AlteraMonete: alters genuine coins, in any way diminishing their value (art. 454) | quote: Alterazione di monete | uri: examples/codice_penale/sources/codice_penale_full.md#L6134-L6141
atom ReclusioneAlterazioneMonete: reclusion 3-12 years and fine (art. 454) | quote: Alterazione di monete | uri: examples/codice_penale/sources/codice_penale_full.md#L6134-L6141
precetto_454: =>O@Chiunque ~AlteraMonete
AlteraMonete, Dolo {
  tipico_454: =>O@Giudice FattoTipico
  pena_454:   O(Sanziona) =>O@Giudice ReclusioneAlterazioneMonete
}

atom IntroduceSpendeMoneteFalse: without prior agreement, introduces into the State, holds, spends or circulates counterfeit or altered money (art. 455) | quote: Spendita e introduzione nello Stato, senza concerto, di monete falsificate | uri: examples/codice_penale/sources/codice_penale_full.md#L6142-L6150
atom ReclusioneSpenditaMonete: reclusion 3-12 years and fine (art. 455) | quote: Spendita e introduzione nello Stato, senza concerto, di monete falsificate | uri: examples/codice_penale/sources/codice_penale_full.md#L6142-L6150
precetto_455: =>O@Chiunque ~IntroduceSpendeMoneteFalse
IntroduceSpendeMoneteFalse, Dolo {
  tipico_455: =>O@Giudice FattoTipico
  pena_455:   O(Sanziona) =>O@Giudice ReclusioneSpenditaMonete
}

atom SpendeMoneteFalseBuonaFede: spends or circulates counterfeit/altered money received in good faith (art. 457) | quote: Spendita di monete falsificate ricevute in buona fede | uri: examples/codice_penale/sources/codice_penale_full.md#L6160-L6166
atom ReclusioneSpenditaBuonaFede: reclusion up to 6 months or fine (art. 457) | quote: Spendita di monete falsificate ricevute in buona fede | uri: examples/codice_penale/sources/codice_penale_full.md#L6160-L6166
precetto_457: =>O@Chiunque ~SpendeMoneteFalseBuonaFede
SpendeMoneteFalseBuonaFede, Dolo {
  tipico_457: =>O@Giudice FattoTipico
  pena_457:   O(Sanziona) =>O@Giudice ReclusioneSpenditaBuonaFede
}

atom ContraffaCartaFiligranata: counterfeits the watermarked paper used for public-credit notes or stamp values (art. 460) | quote: Contraffazione di carta filigranata in uso per la fabbricazione di carte di pubblico credito o di valori di bollo | uri: examples/codice_penale/sources/codice_penale_full.md#L6188-L6196
atom ReclusioneCartaFiligranata: reclusion 2-6 years and fine (art. 460) | quote: Contraffazione di carta filigranata in uso per la fabbricazione di carte di pubblico credito o di valori di bollo | uri: examples/codice_penale/sources/codice_penale_full.md#L6188-L6196
precetto_460: =>O@Chiunque ~ContraffaCartaFiligranata
ContraffaCartaFiligranata, Dolo {
  tipico_460: =>O@Giudice FattoTipico
  pena_460:   O(Sanziona) =>O@Giudice ReclusioneCartaFiligranata
}

atom FabbricaStrumentiFalsificazione: makes or holds watermarks or instruments destined for the falsification of money, stamp values or watermarked paper (art. 461) | quote: Fabbricazione o detenzione di filigrane o di strumenti destinati alla falsificazione di monete, di valori di bollo o di | uri: examples/codice_penale/sources/codice_penale_full.md#L6197-L6205
atom ReclusioneStrumentiFalsi: reclusion 1-5 years and fine (art. 461) | quote: Fabbricazione o detenzione di filigrane o di strumenti destinati alla falsificazione di monete, di valori di bollo o di | uri: examples/codice_penale/sources/codice_penale_full.md#L6197-L6205
precetto_461: =>O@Chiunque ~FabbricaStrumentiFalsificazione
FabbricaStrumentiFalsificazione, Dolo {
  tipico_461: =>O@Giudice FattoTipico
  pena_461:   O(Sanziona) =>O@Giudice ReclusioneStrumentiFalsi
}

atom ContraffaBigliettiTrasporto: counterfeits or alters tickets of railways or other public transport enterprises (art. 462) | quote: Falsificazione di biglietti di pubbliche imprese di trasporto | uri: examples/codice_penale/sources/codice_penale_full.md#L6209-L6216
atom ReclusioneBigliettiTrasporto: reclusion up to 1 year and fine (art. 462) | quote: Falsificazione di biglietti di pubbliche imprese di trasporto | uri: examples/codice_penale/sources/codice_penale_full.md#L6209-L6216
precetto_462: =>O@Chiunque ~ContraffaBigliettiTrasporto
ContraffaBigliettiTrasporto, Dolo {
  tipico_462: =>O@Giudice FattoTipico
  pena_462:   O(Sanziona) =>O@Giudice ReclusioneBigliettiTrasporto
}

atom UsaValoriBolloFalsi: not having taken part in the counterfeiting, uses counterfeit or altered stamp values (art. 464) | quote: Uso di valori di bollo contraffatti o alterati | uri: examples/codice_penale/sources/codice_penale_full.md#L6224-L6232
atom ReclusioneUsoBolloFalso: reclusion up to 3 years (art. 464) | quote: Uso di valori di bollo contraffatti o alterati | uri: examples/codice_penale/sources/codice_penale_full.md#L6224-L6232
precetto_464: =>O@Chiunque ~UsaValoriBolloFalsi
UsaValoriBolloFalsi, Dolo {
  tipico_464: =>O@Giudice FattoTipico
  pena_464:   O(Sanziona) =>O@Giudice ReclusioneUsoBolloFalso
}

atom ContraffaSigilloStato: counterfeits the seal of the State destined to be affixed on public acts (art. 467) | quote: Contraffazione del sigillo dello Stato e uso del sigillo contraffatto | uri: examples/codice_penale/sources/codice_penale_full.md#L6260-L6266
atom ReclusioneSigilloStato: reclusion 3-6 years and fine (art. 467) | quote: Contraffazione del sigillo dello Stato e uso del sigillo contraffatto | uri: examples/codice_penale/sources/codice_penale_full.md#L6260-L6266
precetto_467: =>O@Chiunque ~ContraffaSigilloStato
ContraffaSigilloStato, Dolo {
  tipico_467: =>O@Giudice FattoTipico
  pena_467:   O(Sanziona) =>O@Giudice ReclusioneSigilloStato
}

atom ContraffaPubbliciSigilli: counterfeits other public seals or instruments destined for public authentication or certification (art. 468) | quote: Contraffazione di altri pubblici sigilli o strumenti destinati a pubblica autenticazione o certificazione e uso di tali | uri: examples/codice_penale/sources/codice_penale_full.md#L6267-L6275
atom ReclusionePubbliciSigilli: reclusion 1-5 years (art. 468) | quote: Contraffazione di altri pubblici sigilli o strumenti destinati a pubblica autenticazione o certificazione e uso di tali | uri: examples/codice_penale/sources/codice_penale_full.md#L6267-L6275
precetto_468: =>O@Chiunque ~ContraffaPubbliciSigilli
ContraffaPubbliciSigilli, Dolo {
  tipico_468: =>O@Giudice FattoTipico
  pena_468:   O(Sanziona) =>O@Giudice ReclusionePubbliciSigilli
}

atom UsaAbusivamenteSigilliVeri: having procured the genuine seals/instruments of public authentication, abusively uses them to another's harm (art. 471) | quote: Uso abusivo di sigilli e strumenti veri | uri: examples/codice_penale/sources/codice_penale_full.md#L6293-L6299
atom ReclusioneUsoSigilliVeri: reclusion up to 3 years (art. 471) | quote: Uso abusivo di sigilli e strumenti veri | uri: examples/codice_penale/sources/codice_penale_full.md#L6293-L6299
precetto_471: =>O@Chiunque ~UsaAbusivamenteSigilliVeri
UsaAbusivamenteSigilliVeri, Dolo {
  tipico_471: =>O@Giudice FattoTipico
  pena_471:   O(Sanziona) =>O@Giudice ReclusioneUsoSigilliVeri
}

atom UsaPesiMisureFalse: to another's harm, uses measures or weights bearing a counterfeited or altered legal mark (art. 472) | quote: Uso o detenzione di misure o pesi con falsa impronta | uri: examples/codice_penale/sources/codice_penale_full.md#L6300-L6308
atom ReclusionePesiFalsi: reclusion up to 1 year or fine (art. 472) | quote: Uso o detenzione di misure o pesi con falsa impronta | uri: examples/codice_penale/sources/codice_penale_full.md#L6300-L6308
precetto_472: =>O@Chiunque ~UsaPesiMisureFalse
UsaPesiMisureFalse, Dolo {
  tipico_472: =>O@Giudice FattoTipico
  pena_472:   O(Sanziona) =>O@Giudice ReclusionePesiFalsi
}

atom ContraffaMarchi: counterfeits or alters the marks or distinctive signs of intellectual works or industrial products (art. 473) | quote: Contraffazione, alterazione o uso di segni distintivi di opere dell'ingegno o di prodotti industriali | uri: examples/codice_penale/sources/codice_penale_full.md#L6314-L6322
atom ReclusioneContraffazioneMarchi: reclusion up to 2 years and fine (art. 473) | quote: Contraffazione, alterazione o uso di segni distintivi di opere dell'ingegno o di prodotti industriali | uri: examples/codice_penale/sources/codice_penale_full.md#L6314-L6322
precetto_473: =>O@Chiunque ~ContraffaMarchi
ContraffaMarchi, Dolo {
  tipico_473: =>O@Giudice FattoTipico
  pena_473:   O(Sanziona) =>O@Giudice ReclusioneContraffazioneMarchi
}

atom CommerciaProdottiSegniFalsi: introduces into the State or sells industrial products with counterfeit marks (art. 474) | quote: Introduzione nello Stato e commercio di prodotti con segni falsi | uri: examples/codice_penale/sources/codice_penale_full.md#L6330-L6338
atom ReclusioneCommercioSegniFalsi: reclusion up to 2 years and fine (art. 474) | quote: Introduzione nello Stato e commercio di prodotti con segni falsi | uri: examples/codice_penale/sources/codice_penale_full.md#L6330-L6338
precetto_474: =>O@Chiunque ~CommerciaProdottiSegniFalsi
CommerciaProdottiSegniFalsi, Dolo {
  tipico_474: =>O@Giudice FattoTipico
  pena_474:   O(Sanziona) =>O@Giudice ReclusioneCommercioSegniFalsi
}

atom FormaAttoFalso: in the exercise of functions, materially forms a false public act or alters a true one (art. 476) | quote: Falsità materiale commessa dal pubblico ufficiale in atti pubblici | uri: examples/codice_penale/sources/codice_penale_full.md#L6353-L6361
atom ReclusioneFalsoMaterialePU: reclusion 1-6 years (art. 476) | quote: Falsità materiale commessa dal pubblico ufficiale in atti pubblici | uri: examples/codice_penale/sources/codice_penale_full.md#L6353-L6361
precetto_476: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, FormaAttoFalso, Dolo {
  tipico_476: =>O@Giudice FattoTipico
  pena_476:   O(Sanziona) =>O@Giudice ReclusioneFalsoMaterialePU
}

atom FormaCertificatoFalso: in the exercise of functions, materially counterfeits or alters certificates or administrative authorisations (art. 477) | quote: Falsità materiale commessa da pubblico ufficiale in certificati o autorizzazioni amministrative | uri: examples/codice_penale/sources/codice_penale_full.md#L6362-L6370
atom ReclusioneFalsoCertificatoPU: reclusion 6 months-3 years (art. 477) | quote: Falsità materiale commessa da pubblico ufficiale in certificati o autorizzazioni amministrative | uri: examples/codice_penale/sources/codice_penale_full.md#L6362-L6370
precetto_477: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, FormaCertificatoFalso, Dolo {
  tipico_477: =>O@Giudice FattoTipico
  pena_477:   O(Sanziona) =>O@Giudice ReclusioneFalsoCertificatoPU
}

atom AttestaFalsoAttoPubblico: a private person falsely attests to a public official, in a public act, facts the act is meant to prove (art. 483) | quote: Falsità ideologica commessa dal privato in atto pubblico | uri: examples/codice_penale/sources/codice_penale_full.md#L6427-L6435
atom ReclusioneFalsoPrivatoAtto: reclusion up to 2 years (art. 483) | quote: Falsità ideologica commessa dal privato in atto pubblico | uri: examples/codice_penale/sources/codice_penale_full.md#L6427-L6435
precetto_483: =>O@Chiunque ~AttestaFalsoAttoPubblico
AttestaFalsoAttoPubblico, Dolo {
  tipico_483: =>O@Giudice FattoTipico
  pena_483:   O(Sanziona) =>O@Giudice ReclusioneFalsoPrivatoAtto
}

atom AbusaFoglioFirmatoBianco: abusing a sheet signed in blank in their possession, writes a private act producing legal effects (art. 486) | quote: Falsità in foglio firmato in bianco | uri: examples/codice_penale/sources/codice_penale_full.md#L6458-L6466
atom ReclusioneFoglioBianco: reclusion 6 months-3 years (art. 486) | quote: Falsità in foglio firmato in bianco | uri: examples/codice_penale/sources/codice_penale_full.md#L6458-L6466
precetto_486: =>O@Chiunque ~AbusaFoglioFirmatoBianco
AbusaFoglioFirmatoBianco, Dolo {
  tipico_486: =>O@Giudice FattoTipico
  pena_486:   O(Sanziona) =>O@Giudice ReclusioneFoglioBianco
}

atom UsaAttoFalso: without having taken part in the forgery, uses a false act (art. 489) | quote: Uso di atto falso | uri: examples/codice_penale/sources/codice_penale_full.md#L6486-L6494
atom ReclusioneUsoAttoFalso: reclusion (the penalties of the preceding articles, reduced) (art. 489) | quote: Uso di atto falso | uri: examples/codice_penale/sources/codice_penale_full.md#L6486-L6494
precetto_489: =>O@Chiunque ~UsaAttoFalso
UsaAttoFalso, Dolo {
  tipico_489: =>O@Giudice FattoTipico
  pena_489:   O(Sanziona) =>O@Giudice ReclusioneUsoAttoFalso
}

atom DistruggeAttiVeri: wholly or partly destroys, suppresses or conceals a true public act or private writing (art. 490) | quote: Soppressione, distruzione e occultamento di atti veri | uri: examples/codice_penale/sources/codice_penale_full.md#L6495-L6502
atom ReclusioneSoppressioneAtti: reclusion (as for the corresponding forgery) (art. 490) | quote: Soppressione, distruzione e occultamento di atti veri | uri: examples/codice_penale/sources/codice_penale_full.md#L6495-L6502
precetto_490: =>O@Chiunque ~DistruggeAttiVeri
DistruggeAttiVeri, Dolo {
  tipico_490: =>O@Giudice FattoTipico
  pena_490:   O(Sanziona) =>O@Giudice ReclusioneSoppressioneAtti
}

atom DichiaraFalsaIdentita: falsely declares or attests to a public official the identity or personal qualities of self or others (art. 495) | quote: Falsa attestazione o dichiarazione a un pubblico ufficiale sulla identità o su qualità personali proprie o di altri | uri: examples/codice_penale/sources/codice_penale_full.md#L6562-L6570
atom ReclusioneFalsaIdentita: reclusion 1-6 years (art. 495) | quote: Falsa attestazione o dichiarazione a un pubblico ufficiale sulla identità o su qualità personali proprie o di altri | uri: examples/codice_penale/sources/codice_penale_full.md#L6562-L6570
precetto_495: =>O@Chiunque ~DichiaraFalsaIdentita
DichiaraFalsaIdentita, Dolo {
  tipico_495: =>O@Giudice FattoTipico
  pena_495:   O(Sanziona) =>O@Giudice ReclusioneFalsaIdentita
}

atom ProcuraConFrodeCertificato: fraudulently procures a criminal-record certificate, or makes undue use of it (art. 497) | quote: Frode nel farsi rilasciare certificati del casellario giudiziale e uso indebito di tali certificati | uri: examples/codice_penale/sources/codice_penale_full.md#L6610-L6617
atom ReclusioneFrodeCertificati: reclusion 1-5 years (art. 497) | quote: Frode nel farsi rilasciare certificati del casellario giudiziale e uso indebito di tali certificati | uri: examples/codice_penale/sources/codice_penale_full.md#L6610-L6617
precetto_497: =>O@Chiunque ~ProcuraConFrodeCertificato
ProcuraConFrodeCertificato, Dolo {
  tipico_497: =>O@Giudice FattoTipico
  pena_497:   O(Sanziona) =>O@Giudice ReclusioneFrodeCertificati
}

atom PortaAbusivamenteTitoli: abusively wears in public the uniform or distinctive signs of an office, or assumes titles/honours not due (art. 498) | quote: Usurpazione di titoli o di onori | uri: examples/codice_penale/sources/codice_penale_full.md#L6639-L6647
atom ReclusioneUsurpazioneTitoli: fine, usurpation of titles or honours (art. 498) | quote: Usurpazione di titoli o di onori | uri: examples/codice_penale/sources/codice_penale_full.md#L6639-L6647
precetto_498: =>O@Chiunque ~PortaAbusivamenteTitoli
PortaAbusivamenteTitoli, Dolo {
  tipico_498: =>O@Giudice FattoTipico
  pena_498:   O(Sanziona) =>O@Giudice ReclusioneUsurpazioneTitoli
}

atom FalsificaMonete: counterfeits national or foreign legal-tender money, or, by prior agreement, introduces/spends it (art. 453) | quote: Falsificazione di monete, spendita e introduzione nello Stato, previo concerto, di monete falsificate | uri: examples/codice_penale/sources/codice_penale_full.md#L6116-L6124
atom ReclusioneFalsoMonete: reclusion 3-12 years and fine (art. 453) | quote: Falsificazione di monete, spendita e introduzione nello Stato, previo concerto, di monete falsificate | uri: examples/codice_penale/sources/codice_penale_full.md#L6116-L6124
precetto_453: =>O@Chiunque ~FalsificaMonete
FalsificaMonete, Dolo {
  tipico_453: =>O@Giudice FattoTipico
  pena_453:   O(Sanziona) =>O@Giudice ReclusioneFalsoMonete
}

atom ContraffaImpronteAutenticazione: by means other than seals, counterfeits the imprints of a public authentication or certification (art. 469) | quote: Contraffazione delle impronte di una pubblica autenticazione o certificazione | uri: examples/codice_penale/sources/codice_penale_full.md#L6277-L6284
atom ReclusioneImpronteAutenticazione: reclusion up to 2 years (art. 469) | quote: Contraffazione delle impronte di una pubblica autenticazione o certificazione | uri: examples/codice_penale/sources/codice_penale_full.md#L6277-L6284
precetto_469: =>O@Chiunque ~ContraffaImpronteAutenticazione
ContraffaImpronteAutenticazione, Dolo {
  tipico_469: =>O@Giudice FattoTipico
  pena_469:   O(Sanziona) =>O@Giudice ReclusioneImpronteAutenticazione
}

atom FalsificaRegistri: being legally obliged to keep registers subject to public-security inspection, makes false entries (art. 484) | quote: Falsità in registri e notificazioni | uri: examples/codice_penale/sources/codice_penale_full.md#L6441-L6448
atom ReclusioneFalsoRegistri: reclusion up to 6 months or fine (art. 484) | quote: Falsità in registri e notificazioni | uri: examples/codice_penale/sources/codice_penale_full.md#L6441-L6448
precetto_484: =>O@Chiunque ~FalsificaRegistri
FalsificaRegistri, Dolo {
  tipico_484: =>O@Giudice FattoTipico
  pena_484:   O(Sanziona) =>O@Giudice ReclusioneFalsoRegistri
}

atom DichiaraFalseQualita: outside the preceding articles, when questioned about identity or personal qualities, falsely declares them (art. 496) | quote: False dichiarazioni sull'identità o su qualità personali proprie o di altri | uri: examples/codice_penale/sources/codice_penale_full.md#L6600-L6608
atom ReclusioneFalseDichiarazioni: reclusion up to 3 years (art. 496) | quote: False dichiarazioni sull'identità o su qualità personali proprie o di altri | uri: examples/codice_penale/sources/codice_penale_full.md#L6600-L6608
precetto_496: =>O@Chiunque ~DichiaraFalseQualita
DichiaraFalseQualita, Dolo {
  tipico_496: =>O@Giudice FattoTipico
  pena_496:   O(Sanziona) =>O@Giudice ReclusioneFalseDichiarazioni
}

atom PossiedeDocumentiFalsi: is found in possession of a false identity document valid for expatriation, or fabricates such documents (art. 497-bis) | quote: Possesso e fabbricazione di documenti di identificazione falsi | uri: examples/codice_penale/sources/codice_penale_full.md#L6618-L6626
atom ReclusioneDocumentiFalsi: reclusion 1-4 years (art. 497-bis) | quote: Possesso e fabbricazione di documenti di identificazione falsi | uri: examples/codice_penale/sources/codice_penale_full.md#L6618-L6626
precetto_497bis: =>O@Chiunque ~PossiedeDocumentiFalsi
PossiedeDocumentiFalsi, Dolo {
  tipico_497bis: =>O@Giudice FattoTipico
  pena_497bis:   O(Sanziona) =>O@Giudice ReclusioneDocumentiFalsi
}

atom UsaBigliettiTrasportoFalsi: not having taken part in the forgery, uses counterfeit or altered public-transport tickets (art. 465) | quote: Uso di biglietti falsificati di pubbliche imprese di trasporto | uri: examples/codice_penale/sources/codice_penale_full.md#L6234-L6242
atom ReclusioneUsoBigliettiFalsi: reclusion up to 6 months or fine (art. 465) | quote: Uso di biglietti falsificati di pubbliche imprese di trasporto | uri: examples/codice_penale/sources/codice_penale_full.md#L6234-L6242
precetto_465: =>O@Chiunque ~UsaBigliettiTrasportoFalsi
UsaBigliettiTrasportoFalsi, Dolo {
  tipico_465: =>O@Giudice FattoTipico
  pena_465:   O(Sanziona) =>O@Giudice ReclusioneUsoBigliettiFalsi
}

atom AbusaFoglioBiancoPubblico: abusing a sheet signed in blank in their official possession, forms a false public act (art. 487) | quote: Falsità in foglio firmato in bianco | uri: examples/codice_penale/sources/codice_penale_full.md#L6470-L6477
atom ReclusioneFoglioBiancoPubblico: reclusion 1-6 years (art. 487) | quote: Falsità in foglio firmato in bianco | uri: examples/codice_penale/sources/codice_penale_full.md#L6470-L6477
precetto_487: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, AbusaFoglioBiancoPubblico, Dolo {
  tipico_487: =>O@Giudice FattoTipico
  pena_487:   O(Sanziona) =>O@Giudice ReclusioneFoglioBiancoPubblico
}

atom AlteraSegniBollo: erases or makes disappear the signs of cancellation on used stamp values or tickets, and uses the altered objects (art. 466) | quote: Alterazione di segni nei valori di bollo o nei biglietti usati e uso degli oggetti così alterati | uri: examples/codice_penale/sources/codice_penale_full.md#L6244-L6252
atom ReclusioneAlterazioneSegni: reclusion up to 1 year or fine (art. 466) | quote: Alterazione di segni nei valori di bollo o nei biglietti usati e uso degli oggetti così alterati | uri: examples/codice_penale/sources/codice_penale_full.md#L6244-L6252
precetto_466: =>O@Chiunque ~AlteraSegniBollo
AlteraSegniBollo, Dolo {
  tipico_466: =>O@Giudice FattoTipico
  pena_466:   O(Sanziona) =>O@Giudice ReclusioneAlterazioneSegni
}

atom VendeImpronteContraffatte: outside participation in the forgery, sells or acquires things bearing counterfeit imprints of public authentication (art. 470) | quote: Vendita o acquisto di cose con impronte contraffatte di una pubblica autenticazione o certificazione | uri: examples/codice_penale/sources/codice_penale_full.md#L6285-L6292
atom ReclusioneVenditaImpronte: reclusion, sale of falsely-marked things (art. 470) | quote: Vendita o acquisto di cose con impronte contraffatte di una pubblica autenticazione o certificazione | uri: examples/codice_penale/sources/codice_penale_full.md#L6285-L6292
precetto_470: =>O@Chiunque ~VendeImpronteContraffatte
VendeImpronteContraffatte, Dolo {
  tipico_470: =>O@Giudice FattoTipico
  pena_470:   O(Sanziona) =>O@Giudice ReclusioneVenditaImpronte
}

atom FalsoIdeologicoCertificato: in the exercise of functions, falsely attests in certificates or administrative authorisations facts they are meant to prove (art. 480) | quote: Falsità ideologica commessa dal pubblico ufficiale in certificati o in autorizzazioni amministrative | uri: examples/codice_penale/sources/codice_penale_full.md#L6401-L6408
atom ReclusioneFalsoIdeoCertificato: reclusion 3 months-2 years (art. 480) | quote: Falsità ideologica commessa dal pubblico ufficiale in certificati o in autorizzazioni amministrative | uri: examples/codice_penale/sources/codice_penale_full.md#L6401-L6408
precetto_480: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, FalsoIdeologicoCertificato, Dolo {
  tipico_480: =>O@Giudice FattoTipico
  pena_480:   O(Sanziona) =>O@Giudice ReclusioneFalsoIdeoCertificato
}
