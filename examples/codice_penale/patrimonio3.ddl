# Codice Penale — patrimonio3 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom ImpossessamentoInAbitazione: takes possession of another's movable thing, removing it from the holder, by entering a dwelling or private place (art. 624-bis) | quote: Furto in abitazione e furto con strappo | uri: examples/codice_penale/sources/codice_penale_full.md#L9135-L9143
atom ReclusioneFurtoAbitazione: reclusion 1-6 years and fine (art. 624-bis) | quote: Furto in abitazione e furto con strappo | uri: examples/codice_penale/sources/codice_penale_full.md#L9135-L9143
precetto_624bis: =>O@Chiunque ~ImpossessamentoInAbitazione
ImpossessamentoInAbitazione, FineDiProfitto, Dolo {
  tipico_624bis: =>O@Giudice FattoTipico
  pena_624bis:   O(Sanziona) =>O@Giudice ReclusioneFurtoAbitazione
}

atom UsurpaImmobileAltrui: to appropriate another's immovable in whole or part, removes or alters its boundary markers (art. 631) | quote: Chiunque per appropriarsi, in tutto o in parte, dell'altrui cosa immobile, ne rimuove o altera i termini è punito, a | uri: examples/codice_penale/sources/codice_penale_full.md#L9311-L9317
atom ReclusioneUsurpazione2: reclusion up to 2 years, a querela (art. 631) | quote: Chiunque per appropriarsi, in tutto o in parte, dell'altrui cosa immobile, ne rimuove o altera i termini è punito, a | uri: examples/codice_penale/sources/codice_penale_full.md#L9311-L9317
precetto_631: =>O@Chiunque ~UsurpaImmobileAltrui
UsurpaImmobileAltrui, Dolo {
  proc_631:   Querela =>O@Giudice Procedibile
  tipico_631: O(Procedibile) =>O@Giudice FattoTipico
  pena_631:   O(Sanziona) =>O@Giudice ReclusioneUsurpazione2
}

atom DeviaAcque: to profit for self or others, diverts waters or alters the state of another's places (art. 632) | quote: Deviazione di acque e modificazione dello stato dei luoghi | uri: examples/codice_penale/sources/codice_penale_full.md#L9318-L9324
atom ReclusioneDeviazioneAcque: reclusion up to 3 years, a querela (art. 632) | quote: Deviazione di acque e modificazione dello stato dei luoghi | uri: examples/codice_penale/sources/codice_penale_full.md#L9318-L9324
precetto_632: =>O@Chiunque ~DeviaAcque
DeviaAcque, Dolo {
  proc_632:   Querela =>O@Giudice Procedibile
  tipico_632: O(Procedibile) =>O@Giudice FattoTipico
  pena_632:   O(Sanziona) =>O@Giudice ReclusioneDeviazioneAcque
}

atom DanneggiaDatiInformatici: destroys, deteriorates, erases or renders unusable another's computer information, data or programs (art. 635-bis) | quote: Danneggiamento di informazioni, dati e programmi informatici Salvo che il fatto costituisca più grave reato, chiunque | uri: examples/codice_penale/sources/codice_penale_full.md#L9382-L9390
atom ReclusioneDanneggiamentoDati: reclusion 6 months-3 years, a querela (art. 635-bis) | quote: Danneggiamento di informazioni, dati e programmi informatici Salvo che il fatto costituisca più grave reato, chiunque | uri: examples/codice_penale/sources/codice_penale_full.md#L9382-L9390
precetto_635bis: =>O@Chiunque ~DanneggiaDatiInformatici
DanneggiaDatiInformatici, Dolo {
  proc_635bis:   Querela =>O@Giudice Procedibile
  tipico_635bis: O(Procedibile) =>O@Giudice FattoTipico
  pena_635bis:   O(Sanziona) =>O@Giudice ReclusioneDanneggiamentoDati
}

atom IntroduceAnimaliFondo: introduces or abandons animals in another's land, or abusively grazes there (art. 636) | quote: Introduzione o abbandono di animali nel fondo altrui e pascolo abusivo | uri: examples/codice_penale/sources/codice_penale_full.md#L9439-L9447
atom ReclusioneAnimaliFondo: fine, a querela (art. 636) | quote: Introduzione o abbandono di animali nel fondo altrui e pascolo abusivo | uri: examples/codice_penale/sources/codice_penale_full.md#L9439-L9447
precetto_636: =>O@Chiunque ~IntroduceAnimaliFondo
IntroduceAnimaliFondo, Dolo {
  proc_636:   Querela =>O@Giudice Procedibile
  tipico_636: O(Procedibile) =>O@Giudice FattoTipico
  pena_636:   O(Sanziona) =>O@Giudice ReclusioneAnimaliFondo
}

atom IngressoFondoRecinto: without necessity, enters another's enclosed land (art. 637) | quote: Ingresso abusivo nel fondo altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9454-L9459
atom ReclusioneIngressoFondo: fine, a querela (art. 637) | quote: Ingresso abusivo nel fondo altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9454-L9459
precetto_637: =>O@Chiunque ~IngressoFondoRecinto
IngressoFondoRecinto, Dolo {
  proc_637:   Querela =>O@Giudice Procedibile
  tipico_637: O(Procedibile) =>O@Giudice FattoTipico
  pena_637:   O(Sanziona) =>O@Giudice ReclusioneIngressoFondo
}

atom UccideAnimaliAltrui: without necessity, kills or renders unusable another's animals (art. 638) | quote: Uccisione o danneggiamento di animali altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9460-L9468
atom ReclusioneUccisioneAnimaliAltrui: reclusion up to 1 year, a querela (art. 638) | quote: Uccisione o danneggiamento di animali altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9460-L9468
precetto_638: =>O@Chiunque ~UccideAnimaliAltrui
UccideAnimaliAltrui, Dolo {
  proc_638:   Querela =>O@Giudice Procedibile
  tipico_638: O(Procedibile) =>O@Giudice FattoTipico
  pena_638:   O(Sanziona) =>O@Giudice ReclusioneUccisioneAnimaliAltrui
}

atom DeturpaCoseAltrui: defaces or soils another's movable or immovable things (art. 639) | quote: Deturpamento e imbrattamento di cose altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9474-L9482
atom ReclusioneDeturpamento: fine, a querela (art. 639) | quote: Deturpamento e imbrattamento di cose altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9474-L9482
precetto_639: =>O@Chiunque ~DeturpaCoseAltrui
DeturpaCoseAltrui, Dolo {
  proc_639:   Querela =>O@Giudice Procedibile
  tipico_639: O(Procedibile) =>O@Giudice FattoTipico
  pena_639:   O(Sanziona) =>O@Giudice ReclusioneDeturpamento
}

atom FrodeInformatica: altering the functioning of a computer system or intervening on data, procures an unjust profit with another's harm (art. 640-ter) | quote: Frode informatica | uri: examples/codice_penale/sources/codice_penale_full.md#L9534-L9542
atom ReclusioneFrodeInformatica: reclusion 6 months-3 years and fine (art. 640-ter) | quote: Frode informatica | uri: examples/codice_penale/sources/codice_penale_full.md#L9534-L9542
precetto_640ter: =>O@Chiunque ~FrodeInformatica
FrodeInformatica, Dolo {
  tipico_640ter: =>O@Giudice FattoTipico
  pena_640ter:   O(Sanziona) =>O@Giudice ReclusioneFrodeInformatica
}

atom InsolvenzaFraudolenta: concealing their state of insolvency, contracts an obligation intending not to fulfil it (art. 641) | quote: Insolvenza fraudolenta | uri: examples/codice_penale/sources/codice_penale_full.md#L9571-L9579
atom ReclusioneInsolvenza: reclusion up to 2 years or fine, a querela (art. 641) | quote: Insolvenza fraudolenta | uri: examples/codice_penale/sources/codice_penale_full.md#L9571-L9579
precetto_641: =>O@Chiunque ~InsolvenzaFraudolenta
InsolvenzaFraudolenta, Dolo {
  proc_641:   Querela =>O@Giudice Procedibile
  tipico_641: O(Procedibile) =>O@Giudice FattoTipico
  pena_641:   O(Sanziona) =>O@Giudice ReclusioneInsolvenza
}

atom FrodeEmigrazione: by mendacious assertions or false news, excites someone to emigrate to profit from it (art. 645) | quote: Frode in emigrazione | uri: examples/codice_penale/sources/codice_penale_full.md#L9683-L9691
atom ReclusioneFrodeEmigrazione: reclusion up to 1 year and fine (art. 645) | quote: Frode in emigrazione | uri: examples/codice_penale/sources/codice_penale_full.md#L9683-L9691
precetto_645: =>O@Chiunque ~FrodeEmigrazione
FrodeEmigrazione, Dolo {
  tipico_645: =>O@Giudice FattoTipico
  pena_645:   O(Sanziona) =>O@Giudice ReclusioneFrodeEmigrazione
}

atom Riciclaggio: outside participation, substitutes or transfers money/goods from a crime, or carries out operations to hinder identifying their illicit origin (art. 648-bis) | quote: Fuori dei casi di concorso nel reato, chiunque sostituisce o trasferisce denaro, beni o altre utilità provenienti da | uri: examples/codice_penale/sources/codice_penale_full.md#L9754-L9762
atom ReclusioneRiciclaggio: reclusion 4-12 years and fine (art. 648-bis) | quote: Fuori dei casi di concorso nel reato, chiunque sostituisce o trasferisce denaro, beni o altre utilità provenienti da | uri: examples/codice_penale/sources/codice_penale_full.md#L9754-L9762
precetto_648bis: =>O@Chiunque ~Riciclaggio
Riciclaggio, Dolo {
  tipico_648bis: =>O@Giudice FattoTipico
  pena_648bis:   O(Sanziona) =>O@Giudice ReclusioneRiciclaggio
}

atom ImpiegoProventiIlleciti: outside participation and outside arts. 648/648-bis, uses money/goods of illicit origin in economic or financial activities (art. 648-ter) | quote: Impiego di denaro, beni o utilità di provenienza illecita | uri: examples/codice_penale/sources/codice_penale_full.md#L9773-L9781
atom ReclusioneImpiegoProventi: reclusion 4-12 years and fine (art. 648-ter) | quote: Impiego di denaro, beni o utilità di provenienza illecita | uri: examples/codice_penale/sources/codice_penale_full.md#L9773-L9781
precetto_648ter: =>O@Chiunque ~ImpiegoProventiIlleciti
ImpiegoProventiIlleciti, Dolo {
  tipico_648ter: =>O@Giudice FattoTipico
  pena_648ter:   O(Sanziona) =>O@Giudice ReclusioneImpiegoProventi
}

atom UsuraImpropria: outside art. 644, exploiting another's economic difficulty, gets given or promised usurious interest (art. 644-bis) | quote: Chiunque, fuori dei casi previsti dall'articolo 644, approfittando delle condizioni di difficoltà economica o | uri: examples/codice_penale/sources/codice_penale_full.md#L9660-L9668
atom ReclusioneUsuraImpropria: reclusion 1-5 years and fine (art. 644-bis) | quote: Chiunque, fuori dei casi previsti dall'articolo 644, approfittando delle condizioni di difficoltà economica o | uri: examples/codice_penale/sources/codice_penale_full.md#L9660-L9668
precetto_644bis: =>O@Chiunque ~UsuraImpropria
UsuraImpropria, Dolo {
  tipico_644bis: =>O@Giudice FattoTipico
  pena_644bis:   O(Sanziona) =>O@Giudice ReclusioneUsuraImpropria
}
