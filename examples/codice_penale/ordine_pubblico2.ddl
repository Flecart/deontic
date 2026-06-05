# Codice Penale — ordine_pubblico2 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom IstigaDisobbedienza: publicly instigates disobedience of public-order laws, or hatred among social classes (art. 415) | quote: Istigazione a disobbedire alle leggi | uri: examples/codice_penale/sources/codice_penale_full.md#L5623-L5628
atom ReclusioneIstigDisobbedienza: reclusion 6 months-5 years (art. 415) | quote: Istigazione a disobbedire alle leggi | uri: examples/codice_penale/sources/codice_penale_full.md#L5623-L5628
precetto_415: =>O@Chiunque ~IstigaDisobbedienza
IstigaDisobbedienza, Dolo {
  tipico_415: =>O@Giudice FattoTipico
  pena_415:   O(Sanziona) =>O@Giudice ReclusioneIstigDisobbedienza
}

atom FaParteAssociazioneMafiosa: is part of a mafia-type association of three or more persons, using the force of intimidation of the associative bond (art. 416-bis) | quote: Associazione di tipo mafioso Chiunque fa parte di un'associazione di tipo mafioso formata da tre o più persone, è | uri: examples/codice_penale/sources/codice_penale_full.md#L5653-L5661
atom ReclusioneAssociazioneMafiosa: reclusion 10-15 years (art. 416-bis) | quote: Associazione di tipo mafioso Chiunque fa parte di un'associazione di tipo mafioso formata da tre o più persone, è | uri: examples/codice_penale/sources/codice_penale_full.md#L5653-L5661
precetto_416bis: =>O@Chiunque ~FaParteAssociazioneMafiosa
FaParteAssociazioneMafiosa, Dolo {
  tipico_416bis: =>O@Giudice FattoTipico
  pena_416bis:   O(Sanziona) =>O@Giudice ReclusioneAssociazioneMafiosa
}

atom DaRifugioAssociati: outside participation or favouring, gives shelter, food, hospitality or means of transport to members of a criminal/mafia association (art. 418) | quote: Assistenza agli associati | uri: examples/codice_penale/sources/codice_penale_full.md#L5711-L5719
atom FuoriConcorso: did not take part in the association's crimes (art. 418) | quote: Assistenza agli associati | uri: examples/codice_penale/sources/codice_penale_full.md#L5711-L5719
atom ReclusioneAssistenzaAssociati: reclusion 2-4 years (art. 418) | quote: Assistenza agli associati | uri: examples/codice_penale/sources/codice_penale_full.md#L5711-L5719
precetto_418: =>O@Chiunque ~DaRifugioAssociati
DaRifugioAssociati, FuoriConcorso, Dolo {
  tipico_418: =>O@Giudice FattoTipico
  pena_418:   O(Sanziona) =>O@Giudice ReclusioneAssistenzaAssociati
}

atom FattiDevastazioneSaccheggio: outside art. 285, commits acts of devastation or pillage (art. 419) | quote: Devastazione e saccheggio | uri: examples/codice_penale/sources/codice_penale_full.md#L5721-L5729
atom ReclusioneDevastazione: reclusion 8-15 years (art. 419) | quote: Devastazione e saccheggio | uri: examples/codice_penale/sources/codice_penale_full.md#L5721-L5729
precetto_419: =>O@Chiunque ~FattiDevastazioneSaccheggio
FattiDevastazioneSaccheggio, Dolo {
  tipico_419: =>O@Giudice FattoTipico
  pena_419:   O(Sanziona) =>O@Giudice ReclusioneDevastazione
}

atom AttentaImpiantiUtilita: commits a fact apt to damage or destroy public-utility installations (art. 420) | quote: Attentato a impianti di pubblica utilità | uri: examples/codice_penale/sources/codice_penale_full.md#L5730-L5738
atom ReclusioneAttentatoImpianti: reclusion 1-4 years (art. 420) | quote: Attentato a impianti di pubblica utilità | uri: examples/codice_penale/sources/codice_penale_full.md#L5730-L5738
precetto_420: =>O@Chiunque ~AttentaImpiantiUtilita
AttentaImpiantiUtilita, Dolo {
  tipico_420: =>O@Giudice FattoTipico
  pena_420:   O(Sanziona) =>O@Giudice ReclusioneAttentatoImpianti
}

atom MinacciaDelittiIncolumita: publicly threatens to commit crimes against public safety, or acts of devastation/pillage, so as to alarm the population (art. 421) | quote: Pubblica intimidazione | uri: examples/codice_penale/sources/codice_penale_full.md#L5746-L5754
atom ReclusionePubblicaIntimidazione: reclusion 1-6 years (art. 421) | quote: Pubblica intimidazione | uri: examples/codice_penale/sources/codice_penale_full.md#L5746-L5754
precetto_421: =>O@Chiunque ~MinacciaDelittiIncolumita
MinacciaDelittiIncolumita, Dolo {
  tipico_421: =>O@Giudice FattoTipico
  pena_421:   O(Sanziona) =>O@Giudice ReclusionePubblicaIntimidazione
}
