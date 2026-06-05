# Codice Penale — persona3 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom CostringeAttiLibidine: compels another to undergo acts of lust other than carnal union (art. 521) | quote: Atti di libidine violenti | uri: examples/codice_penale/sources/codice_penale_full.md#L6968-L6976
atom ReclusioneAttiLibidine: reclusion, violent acts of lust (art. 521) | quote: Atti di libidine violenti | uri: examples/codice_penale/sources/codice_penale_full.md#L6968-L6976
precetto_521: =>O@Chiunque ~CostringeAttiLibidine
oneof[Violenza, Minaccia], CostringeAttiLibidine, Dolo {
  tipico_521: =>O@Giudice FattoTipico
  pena_521:   O(Sanziona) =>O@Giudice ReclusioneAttiLibidine
}

atom SottraeFineMatrimonio: abducts or detains a person for the purpose of marriage (art. 522) | quote: Ratto a fine di matrimonio | uri: examples/codice_penale/sources/codice_penale_full.md#L6979-L6987
atom ReclusioneRattoMatrimonio: reclusion 1-3 years (art. 522) | quote: Ratto a fine di matrimonio | uri: examples/codice_penale/sources/codice_penale_full.md#L6979-L6987
precetto_522: =>O@Chiunque ~SottraeFineMatrimonio
oneof[Violenza, Minaccia, Inganno], SottraeFineMatrimonio, Dolo {
  tipico_522: =>O@Giudice FattoTipico
  pena_522:   O(Sanziona) =>O@Giudice ReclusioneRattoMatrimonio
}

atom UccideAnimale: causes the death of an animal (art. 544-bis) | quote: Uccisione di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L7256-L7261
atom CrudeltaSenzaNecessita: out of cruelty or without necessity (art. 544-bis) | quote: Uccisione di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L7256-L7261
atom ReclusioneUccisioneAnimali: reclusion 4 months-2 years (art. 544-bis) | quote: Uccisione di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L7256-L7261
precetto_544bis: =>O@Chiunque ~UccideAnimale
UccideAnimale, CrudeltaSenzaNecessita, Dolo {
  tipico_544bis: =>O@Giudice FattoTipico
  pena_544bis:   O(Sanziona) =>O@Giudice ReclusioneUccisioneAnimali
}

atom LesioneAnimale: causes injury to an animal, or subjects it to torture or to behaviour intolerable for its characteristics, out of cruelty or without necessity (art. 544-ter) | quote: Maltrattamento di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L7262-L7270
atom ReclusioneMaltrattamentoAnimali: reclusion 3 months-18 months or fine (art. 544-ter) | quote: Maltrattamento di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L7262-L7270
precetto_544ter: =>O@Chiunque ~LesioneAnimale
LesioneAnimale, Dolo {
  tipico_544ter: =>O@Giudice FattoTipico
  pena_544ter:   O(Sanziona) =>O@Giudice ReclusioneMaltrattamentoAnimali
}

atom CagionaAborto: causes the abortion of a woman (art. 545) | quote: Aborto di donna non consenziente | uri: examples/codice_penale/sources/codice_penale_full.md#L7325-L7330
atom SenzaConsensoDonna: without her consent (art. 545) | quote: Aborto di donna non consenziente | uri: examples/codice_penale/sources/codice_penale_full.md#L7325-L7330
atom ReclusioneAbortoNonConsenziente: reclusion 4-8 years (art. 545) | quote: Aborto di donna non consenziente | uri: examples/codice_penale/sources/codice_penale_full.md#L7325-L7330
precetto_545: =>O@Chiunque ~CagionaAborto
CagionaAborto, SenzaConsensoDonna, Dolo {
  tipico_545: =>O@Giudice FattoTipico
  pena_545:   O(Sanziona) =>O@Giudice ReclusioneAbortoNonConsenziente
}

atom CagionaAborto: causes the abortion of a woman (art. 546) | quote: Aborto di donna consenziente | uri: examples/codice_penale/sources/codice_penale_full.md#L7331-L7339
atom ConsensoDonna: with her consent (art. 546) | quote: Aborto di donna consenziente | uri: examples/codice_penale/sources/codice_penale_full.md#L7331-L7339
atom ReclusioneAbortoConsenziente: reclusion 6 months-2 years (art. 546) | quote: Aborto di donna consenziente | uri: examples/codice_penale/sources/codice_penale_full.md#L7331-L7339
precetto_546: =>O@Chiunque ~CagionaAborto
CagionaAborto, ConsensoDonna, Dolo {
  tipico_546: =>O@Giudice FattoTipico
  pena_546:   O(Sanziona) =>O@Giudice ReclusioneAbortoConsenziente
}

atom IstigaAborto: outside participation, instigates a woman to abort, and the abortion occurs (art. 548) | quote: Istigazione all'aborto | uri: examples/codice_penale/sources/codice_penale_full.md#L7351-L7357
atom ReclusioneIstigAborto: reclusion up to 4 years (art. 548) | quote: Istigazione all'aborto | uri: examples/codice_penale/sources/codice_penale_full.md#L7351-L7357
precetto_548: =>O@Chiunque ~IstigaAborto
IstigaAborto, Dolo {
  tipico_548: =>O@Giudice FattoTipico
  pena_548:   O(Sanziona) =>O@Giudice ReclusioneIstigAborto
}

atom ContagioVenereo: being affected by syphilis/gonorrhoea and concealing it, has sexual relations infecting another (art. 554) | quote: Contagio di sifilide e di blenorragia | uri: examples/codice_penale/sources/codice_penale_full.md#L7402-L7410
atom ReclusioneContagio: reclusion, venereal infection (art. 554) | quote: Contagio di sifilide e di blenorragia | uri: examples/codice_penale/sources/codice_penale_full.md#L7402-L7410
precetto_554: =>O@Chiunque ~ContagioVenereo
ContagioVenereo, Dolo {
  tipico_554: =>O@Giudice FattoTipico
  pena_554:   O(Sanziona) =>O@Giudice ReclusioneContagio
}

atom InduceMatrimonioInganno: in contracting a marriage with civil effects, by fraudulent means induces the other party in error on an invalidating impediment (art. 558) | quote: Induzione al matrimonio mediante inganno | uri: examples/codice_penale/sources/codice_penale_full.md#L7455-L7463
atom ReclusioneIndMatrimonio: reclusion 6 months-3 years (art. 558) | quote: Induzione al matrimonio mediante inganno | uri: examples/codice_penale/sources/codice_penale_full.md#L7455-L7463
precetto_558: =>O@Chiunque ~InduceMatrimonioInganno
InduceMatrimonioInganno, Dolo {
  tipico_558: =>O@Giudice FattoTipico
  pena_558:   O(Sanziona) =>O@Giudice ReclusioneIndMatrimonio
}

atom CommetteIncesto: commits incest with a descendant, ascendant or sibling, in a way producing public scandal (art. 564) | quote: Chiunque, in modo che ne derivi pubblico scandalo, commette incesto con un discendente o un ascendente, o con un affine | uri: examples/codice_penale/sources/codice_penale_full.md#L7540-L7548
atom ReclusioneIncesto: reclusion 1-5 years (art. 564) | quote: Chiunque, in modo che ne derivi pubblico scandalo, commette incesto con un discendente o un ascendente, o con un affine | uri: examples/codice_penale/sources/codice_penale_full.md#L7540-L7548
precetto_564: =>O@Chiunque ~CommetteIncesto
CommetteIncesto, Dolo {
  tipico_564: =>O@Giudice FattoTipico
  pena_564:   O(Sanziona) =>O@Giudice ReclusioneIncesto
}

atom SupponeSopprimeStato: makes a non-existent birth figure in the civil-status registers (art. 566) | quote: Supposizione o soppressione di stato | uri: examples/codice_penale/sources/codice_penale_full.md#L7567-L7575
atom ReclusioneSupposizioneStato: reclusion 3-10 years (art. 566) | quote: Supposizione o soppressione di stato | uri: examples/codice_penale/sources/codice_penale_full.md#L7567-L7575
precetto_566: =>O@Chiunque ~SupponeSopprimeStato
SupponeSopprimeStato, Dolo {
  tipico_566: =>O@Giudice FattoTipico
  pena_566:   O(Sanziona) =>O@Giudice ReclusioneSupposizioneStato
}

atom AlteraStatoCivile: by substituting a newborn, alters its civil status (art. 567) | quote: Alterazione di stato | uri: examples/codice_penale/sources/codice_penale_full.md#L7576-L7584
atom ReclusioneAlterazioneStato: reclusion 5-15 years (art. 567) | quote: Alterazione di stato | uri: examples/codice_penale/sources/codice_penale_full.md#L7576-L7584
precetto_567: =>O@Chiunque ~AlteraStatoCivile
AlteraStatoCivile, Dolo {
  tipico_567: =>O@Giudice FattoTipico
  pena_567:   O(Sanziona) =>O@Giudice ReclusioneAlterazioneStato
}

atom AbusaMezziCorrezione: abuses means of correction or discipline against a person, causing danger of illness in body or mind (art. 571) | quote: Abuso dei mezzi di correzione o di disciplina | uri: examples/codice_penale/sources/codice_penale_full.md#L7631-L7639
atom ReclusioneAbusoCorrezione: reclusion up to 6 months (art. 571) | quote: Abuso dei mezzi di correzione o di disciplina | uri: examples/codice_penale/sources/codice_penale_full.md#L7631-L7639
precetto_571: =>O@Chiunque ~AbusaMezziCorrezione
AbusaMezziCorrezione, Dolo {
  tipico_571: =>O@Giudice FattoTipico
  pena_571:   O(Sanziona) =>O@Giudice ReclusioneAbusoCorrezione
}

atom SottraeMinoreConsenziente: abducts a minor over 14, with their consent, from the parent or guardian (art. 573) | quote: Sottrazione consensuale di minorenni | uri: examples/codice_penale/sources/codice_penale_full.md#L7673-L7681
atom ReclusioneSottrazioneConsensuale: reclusion up to 2 years, a querela (art. 573) | quote: Sottrazione consensuale di minorenni | uri: examples/codice_penale/sources/codice_penale_full.md#L7673-L7681
precetto_573: =>O@Chiunque ~SottraeMinoreConsenziente
SottraeMinoreConsenziente, Dolo {
  proc_573:   Querela =>O@Giudice Procedibile
  tipico_573: O(Procedibile) =>O@Giudice FattoTipico
  pena_573:   O(Sanziona) =>O@Giudice ReclusioneSottrazioneConsensuale
}

atom ConsensoVittima: with that person's consent (art. 579) | quote: Omicidio del consenziente | uri: examples/codice_penale/sources/codice_penale_full.md#L7780-L7788
atom ReclusioneOmicidioConsenziente: reclusion 6-15 years (art. 579) | quote: Omicidio del consenziente | uri: examples/codice_penale/sources/codice_penale_full.md#L7780-L7788
precetto_579: =>O@Chiunque ~CagionaMorte
CagionaMorte, ConsensoVittima, Dolo {
  tipico_579: =>O@Giudice FattoTipico
  pena_579:   O(Sanziona) =>O@Giudice ReclusioneOmicidioConsenziente
}

atom MutilazioneGenitaleFemminile: absent therapeutic needs, causes a mutilation of female genital organs (art. 583-bis) | quote: Pratiche di mutilazione degli organi genitali femminili | uri: examples/codice_penale/sources/codice_penale_full.md#L7875-L7883
atom ReclusioneMutilazione: reclusion 4-12 years (art. 583-bis) | quote: Pratiche di mutilazione degli organi genitali femminili | uri: examples/codice_penale/sources/codice_penale_full.md#L7875-L7883
precetto_583bis: =>O@Chiunque ~MutilazioneGenitaleFemminile
MutilazioneGenitaleFemminile, Dolo {
  tipico_583bis: =>O@Giudice FattoTipico
  pena_583bis:   O(Sanziona) =>O@Giudice ReclusioneMutilazione
}

atom DelittoDolosoBase: commits a fact foreseen as an intentional crime (art. 586) | quote: Morte o lesioni come conseguenza di altro delitto | uri: examples/codice_penale/sources/codice_penale_full.md#L7933-L7941
atom DerivaMorteLesione: from which, as an unintended consequence, the death or injury of a person results (art. 586) | quote: Morte o lesioni come conseguenza di altro delitto | uri: examples/codice_penale/sources/codice_penale_full.md#L7933-L7941
atom ReclusioneMorteConseguenza: reclusion (homicide/injury penalties, increased) (art. 586) | quote: Morte o lesioni come conseguenza di altro delitto | uri: examples/codice_penale/sources/codice_penale_full.md#L7933-L7941
precetto_586: =>O@Chiunque ~DelittoDolosoBase
DelittoDolosoBase, DerivaMorteLesione, Dolo {
  tipico_586: =>O@Giudice FattoTipico
  pena_586:   O(Sanziona) =>O@Giudice ReclusioneMorteConseguenza
}

atom InduceProstituzioneMinore: induces into prostitution a person under 18, or favours/exploits it (art. 600-bis) | quote: Prostituzione minorile | uri: examples/codice_penale/sources/codice_penale_full.md#L8269-L8277
atom ReclusioneProstituzioneMinorile: reclusion 6-12 years and fine (art. 600-bis) | quote: Prostituzione minorile | uri: examples/codice_penale/sources/codice_penale_full.md#L8269-L8277
precetto_600bis: =>O@Chiunque ~InduceProstituzioneMinore
InduceProstituzioneMinore, Dolo {
  tipico_600bis: =>O@Giudice FattoTipico
  pena_600bis:   O(Sanziona) =>O@Giudice ReclusioneProstituzioneMinorile
}

atom PornografiaMinorile: using minors under 18, makes pornographic exhibitions or produces pornographic material (art. 600-ter) | quote: Pornografia minorile | uri: examples/codice_penale/sources/codice_penale_full.md#L8291-L8299
atom ReclusionePornografiaMinorile: reclusion 6-12 years and fine (art. 600-ter) | quote: Pornografia minorile | uri: examples/codice_penale/sources/codice_penale_full.md#L8291-L8299
precetto_600ter: =>O@Chiunque ~PornografiaMinorile
PornografiaMinorile, Dolo {
  tipico_600ter: =>O@Giudice FattoTipico
  pena_600ter:   O(Sanziona) =>O@Giudice ReclusionePornografiaMinorile
}

atom CommetteTratta: commits trafficking of a person in the conditions of art. 600, by deception/violence/abuse (art. 601) | quote: Tratta di persone | uri: examples/codice_penale/sources/codice_penale_full.md#L8406-L8414
atom ReclusioneTratta: reclusion 8-20 years (art. 601) | quote: Tratta di persone | uri: examples/codice_penale/sources/codice_penale_full.md#L8406-L8414
precetto_601: =>O@Chiunque ~CommetteTratta
CommetteTratta, Dolo {
  tipico_601: =>O@Giudice FattoTipico
  pena_601:   O(Sanziona) =>O@Giudice ReclusioneTratta
}

atom AcquistaAlienaSchiavo: outside art. 601, buys, sells or transfers a person in the conditions of art. 600 (art. 602) | quote: Acquisto e alienazione di schiavi | uri: examples/codice_penale/sources/codice_penale_full.md#L8420-L8428
atom ReclusioneAcquistoSchiavi: reclusion 8-20 years (art. 602) | quote: Acquisto e alienazione di schiavi | uri: examples/codice_penale/sources/codice_penale_full.md#L8420-L8428
precetto_602: =>O@Chiunque ~AcquistaAlienaSchiavo
AcquistaAlienaSchiavo, Dolo {
  tipico_602: =>O@Giudice FattoTipico
  pena_602:   O(Sanziona) =>O@Giudice ReclusioneAcquistoSchiavi
}

atom SottoponeTotaleSoggezione: subjects a person to their power so as to reduce them to a total state of subjection (art. 603) | quote: Chiunque sottopone una persona al proprio potere, in modo da ridurla in totale stato di soggezione, è punito con la | uri: examples/codice_penale/sources/codice_penale_full.md#L8431-L8436
atom ReclusionePlagio: reclusion 5-15 years (art. 603) | quote: Chiunque sottopone una persona al proprio potere, in modo da ridurla in totale stato di soggezione, è punito con la | uri: examples/codice_penale/sources/codice_penale_full.md#L8431-L8436
precetto_603: =>O@Chiunque ~SottoponeTotaleSoggezione
SottoponeTotaleSoggezione, Dolo {
  tipico_603: =>O@Giudice FattoTipico
  pena_603:   O(Sanziona) =>O@Giudice ReclusionePlagio
}

atom AttiSessualiMinorenne: performs sexual acts with a person under the age limits set by law (art. 609-quater) | quote: Atti sessuali con minorenne | uri: examples/codice_penale/sources/codice_penale_full.md#L8558-L8566
atom ReclusioneAttiSessualiMinore: reclusion (the penalty of art. 609-bis) (art. 609-quater) | quote: Atti sessuali con minorenne | uri: examples/codice_penale/sources/codice_penale_full.md#L8558-L8566
precetto_609quater: =>O@Chiunque ~AttiSessualiMinorenne
AttiSessualiMinorenne, Dolo {
  tipico_609quater: =>O@Giudice FattoTipico
  pena_609quater:   O(Sanziona) =>O@Giudice ReclusioneAttiSessualiMinore
}

atom CostringeCommettereReato: uses violence or threat to compel or determine another to commit a crime (art. 611) | quote: Violenza o minaccia per costringere a commettere un reato Chiunque usa violenza o minaccia per costringere o | uri: examples/codice_penale/sources/codice_penale_full.md#L8714-L8721
atom ReclusioneCostringereReato: reclusion up to 5 years (art. 611) | quote: Violenza o minaccia per costringere a commettere un reato Chiunque usa violenza o minaccia per costringere o | uri: examples/codice_penale/sources/codice_penale_full.md#L8714-L8721
precetto_611: =>O@Chiunque ~CostringeCommettereReato
oneof[Violenza, Minaccia], CostringeCommettereReato, Dolo {
  tipico_611: =>O@Giudice FattoTipico
  pena_611:   O(Sanziona) =>O@Giudice ReclusioneCostringereReato
}

atom ProcuraIncapacita: by hypnotic suggestion or narcotic substances, or otherwise, puts a person, without their consent, in a state of incapacity to understand or will (art. 613) | quote: Stato di incapacità procurato mediante violenza | uri: examples/codice_penale/sources/codice_penale_full.md#L8763-L8771
atom ReclusioneIncapacitaProcurata: reclusion up to 1 year (art. 613) | quote: Stato di incapacità procurato mediante violenza | uri: examples/codice_penale/sources/codice_penale_full.md#L8763-L8771
precetto_613: =>O@Chiunque ~ProcuraIncapacita
ProcuraIncapacita, Dolo {
  tipico_613: =>O@Giudice FattoTipico
  pena_613:   O(Sanziona) =>O@Giudice ReclusioneIncapacitaProcurata
}

atom CostringeCongiunzioneCarnale: compels another to carnal union (art. 519) | quote: Della violenza carnale | uri: examples/codice_penale/sources/codice_penale_full.md#L6938-L6946
atom ReclusioneViolenzaCarnale: reclusion 5-10 years (art. 519) | quote: Della violenza carnale | uri: examples/codice_penale/sources/codice_penale_full.md#L6938-L6946
precetto_519: =>O@Chiunque ~CostringeCongiunzioneCarnale
oneof[Violenza, Minaccia], CostringeCongiunzioneCarnale, Dolo {
  tipico_519: =>O@Giudice FattoTipico
  pena_519:   O(Sanziona) =>O@Giudice ReclusioneViolenzaCarnale
}

atom AttiAbortiviDonnaCreduta: administers to a woman believed pregnant means apt to cause abortion (art. 550) | quote: Atti abortivi su donna ritenuta incinta | uri: examples/codice_penale/sources/codice_penale_full.md#L7369-L7377
atom ReclusioneAttiAbortivi: reclusion 6 months-2 years (art. 550) | quote: Atti abortivi su donna ritenuta incinta | uri: examples/codice_penale/sources/codice_penale_full.md#L7369-L7377
precetto_550: =>O@Chiunque ~AttiAbortiviDonnaCreduta
AttiAbortiviDonnaCreduta, Dolo {
  tipico_550: =>O@Giudice FattoTipico
  pena_550:   O(Sanziona) =>O@Giudice ReclusioneAttiAbortivi
}

atom ProcurataImpotenza: performs, with consent, acts apt to render a person impotent to procreate (art. 552) | quote: Procurata impotenza alla procreazione | uri: examples/codice_penale/sources/codice_penale_full.md#L7386-L7393
atom ReclusioneProcurataImpotenza: reclusion 6 months-2 years (art. 552) | quote: Procurata impotenza alla procreazione | uri: examples/codice_penale/sources/codice_penale_full.md#L7386-L7393
precetto_552: =>O@Chiunque ~ProcurataImpotenza
ProcurataImpotenza, Dolo {
  tipico_552: =>O@Giudice FattoTipico
  pena_552:   O(Sanziona) =>O@Giudice ReclusioneProcurataImpotenza
}

atom DetieneMaterialePornografico: outside art. 600-ter, knowingly holds pornographic material produced using minors under 18 (art. 600-quater) | quote: Detenzione di materiale pornografico | uri: examples/codice_penale/sources/codice_penale_full.md#L8321-L8329
atom ReclusioneDetenzionePorno: reclusion up to 3 years and fine (art. 600-quater) | quote: Detenzione di materiale pornografico | uri: examples/codice_penale/sources/codice_penale_full.md#L8321-L8329
precetto_600quater: =>O@Chiunque ~DetieneMaterialePornografico
DetieneMaterialePornografico, Dolo {
  tipico_600quater: =>O@Giudice FattoTipico
  pena_600quater:   O(Sanziona) =>O@Giudice ReclusioneDetenzionePorno
}

atom CorruzioneMinorenne: performs sexual acts in the presence of a person under 14, to make them witness it (art. 609-quinquies) | quote: Corruzione di minorenne | uri: examples/codice_penale/sources/codice_penale_full.md#L8590-L8595
atom ReclusioneCorruzioneMinore: reclusion 1-5 years (art. 609-quinquies) | quote: Corruzione di minorenne | uri: examples/codice_penale/sources/codice_penale_full.md#L8590-L8595
precetto_609quinquies: =>O@Chiunque ~CorruzioneMinorenne
CorruzioneMinorenne, Dolo {
  tipico_609quinquies: =>O@Giudice FattoTipico
  pena_609quinquies:   O(Sanziona) =>O@Giudice ReclusioneCorruzioneMinore
}

atom SottraeFineLibidine: abducts or detains a minor for the purpose of lust (art. 523) | quote: Ratto a fine di libidine | uri: examples/codice_penale/sources/codice_penale_full.md#L6989-L6996
atom ReclusioneRattoLibidine: reclusion 1-3 years (art. 523) | quote: Ratto a fine di libidine | uri: examples/codice_penale/sources/codice_penale_full.md#L6989-L6996
precetto_523: =>O@Chiunque ~SottraeFineLibidine
oneof[Violenza, Minaccia, Inganno], SottraeFineLibidine, Dolo {
  tipico_523: =>O@Giudice FattoTipico
  pena_523:   O(Sanziona) =>O@Giudice ReclusioneRattoLibidine
}

atom CombattimentiAnimali: promotes, organises or directs unauthorised fights or competitions between animals causing danger to their integrity (art. 544-quinquies) | quote: Divieto di combattimenti tra animali | uri: examples/codice_penale/sources/codice_penale_full.md#L7287-L7295
atom ReclusioneCombattimentiAnimali: reclusion 1-3 years and fine (art. 544-quinquies) | quote: Divieto di combattimenti tra animali | uri: examples/codice_penale/sources/codice_penale_full.md#L7287-L7295
precetto_544quinquies: =>O@Chiunque ~CombattimentiAnimali
CombattimentiAnimali, Dolo {
  tipico_544quinquies: =>O@Giudice FattoTipico
  pena_544quinquies:   O(Sanziona) =>O@Giudice ReclusioneCombattimentiAnimali
}

atom IncitaPraticheAntiprocreative: publicly incites practices against procreation, or makes propaganda for them (art. 553) | quote: Incitamento a pratiche contro la procreazione | uri: examples/codice_penale/sources/codice_penale_full.md#L7394-L7401
atom ReclusioneIncitamento: fine, incitement to anti-procreative practices (art. 553) | quote: Incitamento a pratiche contro la procreazione | uri: examples/codice_penale/sources/codice_penale_full.md#L7394-L7401
precetto_553: =>O@Chiunque ~IncitaPraticheAntiprocreative
IncitaPraticheAntiprocreative, Dolo {
  tipico_553: =>O@Giudice FattoTipico
  pena_553:   O(Sanziona) =>O@Giudice ReclusioneIncitamento
}

atom ViolenzaSessualeGruppo: takes part, with several persons gathered, in sexual violence (art. 609-octies) | quote: Violenza sessuale di gruppo | uri: examples/codice_penale/sources/codice_penale_full.md#L8638-L8646
atom ReclusioneViolenzaGruppo: reclusion 6-12 years (art. 609-octies) | quote: Violenza sessuale di gruppo | uri: examples/codice_penale/sources/codice_penale_full.md#L8638-L8646
precetto_609octies: =>O@Chiunque ~ViolenzaSessualeGruppo
ViolenzaSessualeGruppo, Dolo {
  tipico_609octies: =>O@Giudice FattoTipico
  pena_609octies:   O(Sanziona) =>O@Giudice ReclusioneViolenzaGruppo
}

atom SeduzionePromessaMatrimonio: by promise of marriage, seduces a woman, being a married person concealing their status (art. 526) | quote: Seduzione con promessa di matrimonio commessa da persona coniugata | uri: examples/codice_penale/sources/codice_penale_full.md#L7015-L7023
atom ReclusioneSeduzione: reclusion up to 2 years (art. 526) | quote: Seduzione con promessa di matrimonio commessa da persona coniugata | uri: examples/codice_penale/sources/codice_penale_full.md#L7015-L7023
precetto_526: =>O@Chiunque ~SeduzionePromessaMatrimonio
SeduzionePromessaMatrimonio, Dolo {
  tipico_526: =>O@Giudice FattoTipico
  pena_526:   O(Sanziona) =>O@Giudice ReclusioneSeduzione
}

atom AttentatiMoraleFamiliare: in the press, harms the family morals by attributing facts contrary to it (art. 565) | quote: Attentati alla morale familiare commessi col mezzo della stampa periodica | uri: examples/codice_penale/sources/codice_penale_full.md#L7556-L7564
atom ReclusioneMoraleFamiliare: reclusion up to 1 year, a querela (art. 565) | quote: Attentati alla morale familiare commessi col mezzo della stampa periodica | uri: examples/codice_penale/sources/codice_penale_full.md#L7556-L7564
precetto_565: =>O@Chiunque ~AttentatiMoraleFamiliare
AttentatiMoraleFamiliare, Dolo {
  proc_565:   Querela =>O@Giudice Procedibile
  tipico_565: O(Procedibile) =>O@Giudice FattoTipico
  pena_565:   O(Sanziona) =>O@Giudice ReclusioneMoraleFamiliare
}

atom OccultaStatoFanciullo: deposits or presents a child, already registered, so as to alter or conceal its civil status (art. 568) | quote: Occultamento di stato di un fanciullo legittimo o naturale riconosciuto | uri: examples/codice_penale/sources/codice_penale_full.md#L7585-L7591
atom ReclusioneOccultamentoStato: reclusion up to 5 years (art. 568) | quote: Occultamento di stato di un fanciullo legittimo o naturale riconosciuto | uri: examples/codice_penale/sources/codice_penale_full.md#L7585-L7591
precetto_568: =>O@Chiunque ~OccultaStatoFanciullo
OccultaStatoFanciullo, Dolo {
  tipico_568: =>O@Giudice FattoTipico
  pena_568:   O(Sanziona) =>O@Giudice ReclusioneOccultamentoStato
}

atom TurismoSessualeMinori: organises or propagandises trips aimed at exploiting child prostitution (art. 600-quinquies) | quote: Iniziative turistiche volte allo sfruttamento della prostituzione minorile | uri: examples/codice_penale/sources/codice_penale_full.md#L8348-L8356
atom ReclusioneTurismoSessuale: reclusion 6-12 years and fine (art. 600-quinquies) | quote: Iniziative turistiche volte allo sfruttamento della prostituzione minorile | uri: examples/codice_penale/sources/codice_penale_full.md#L8348-L8356
precetto_600quinquies: =>O@Chiunque ~TurismoSessualeMinori
TurismoSessualeMinori, Dolo {
  tipico_600quinquies: =>O@Giudice FattoTipico
  pena_600quinquies:   O(Sanziona) =>O@Giudice ReclusioneTurismoSessuale
}
