# Codice Penale — contravvenzioni (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom NonOsservaProvvedimento: does not observe a measure legally given by the authority for justice, public safety, public order or hygiene (art. 650) | quote: Inosservanza dei provvedimenti dell'autorità | uri: examples/codice_penale/sources/codice_penale_full.md#L9846-L9852
atom ArrestoInosservanza: arrest up to 3 months or fine (art. 650) | quote: Inosservanza dei provvedimenti dell'autorità | uri: examples/codice_penale/sources/codice_penale_full.md#L9846-L9852
precetto_650: =>O@Chiunque ~NonOsservaProvvedimento
NonOsservaProvvedimento {
  tipico_650: =>O@Giudice FattoTipico
  pena_650:   O(Sanziona) =>O@Giudice ArrestoInosservanza
}

atom RifiutaIdentita: refuses, to a public official in their functions, to give details of their own personal identity (art. 651) | quote: Rifiuto d'indicazioni sulla propria identità personale | uri: examples/codice_penale/sources/codice_penale_full.md#L9853-L9859
atom ArrestoRifiutoIdentita: arrest up to 1 month or fine (art. 651) | quote: Rifiuto d'indicazioni sulla propria identità personale | uri: examples/codice_penale/sources/codice_penale_full.md#L9853-L9859
precetto_651: =>O@Chiunque ~RifiutaIdentita
RifiutaIdentita {
  tipico_651: =>O@Giudice FattoTipico
  pena_651:   O(Sanziona) =>O@Giudice ArrestoRifiutoIdentita
}

atom RifiutaOperaTumulto: on the occasion of a tumult, public disaster or common danger, refuses without just cause the assistance demanded by the authority (art. 652) | quote: Rifiuto di prestare la propria opera in occasione di un tumulto | uri: examples/codice_penale/sources/codice_penale_full.md#L9860-L9868
atom ArrestoRifiutoOpera: arrest up to 3 months or fine (art. 652) | quote: Rifiuto di prestare la propria opera in occasione di un tumulto | uri: examples/codice_penale/sources/codice_penale_full.md#L9860-L9868
precetto_652: =>O@Chiunque ~RifiutaOperaTumulto
RifiutaOperaTumulto {
  tipico_652: =>O@Giudice FattoTipico
  pena_652:   O(Sanziona) =>O@Giudice ArrestoRifiutoOpera
}

atom FormaCorpoArmato: without authorisation, forms an armed body not aimed at committing crimes (art. 653) | quote: Formazione di corpi armati non diretti a commettere reati | uri: examples/codice_penale/sources/codice_penale_full.md#L9872-L9877
atom ArrestoCorpoArmato: arrest 1-6 months (art. 653) | quote: Formazione di corpi armati non diretti a commettere reati | uri: examples/codice_penale/sources/codice_penale_full.md#L9872-L9877
precetto_653: =>O@Chiunque ~FormaCorpoArmato
FormaCorpoArmato {
  tipico_653: =>O@Giudice FattoTipico
  pena_653:   O(Sanziona) =>O@Giudice ArrestoCorpoArmato
}

atom PartecipaRadunataSediziosa: takes part in a seditious gathering of ten or more persons (art. 655) | quote: Radunata sediziosa | uri: examples/codice_penale/sources/codice_penale_full.md#L9886-L9894
atom ArrestoRadunata: arrest up to 1 year (art. 655) | quote: Radunata sediziosa | uri: examples/codice_penale/sources/codice_penale_full.md#L9886-L9894
precetto_655: =>O@Chiunque ~PartecipaRadunataSediziosa
PartecipaRadunataSediziosa {
  tipico_655: =>O@Giudice FattoTipico
  pena_655:   O(Sanziona) =>O@Giudice ArrestoRadunata
}

atom DiffondeNotizieFalse: publishes or spreads false, exaggerated or tendentious news apt to disturb public order (art. 656) | quote: Pubblicazione o diffusione di notizie false, esagerate o tendenziose, atte a turbare l'ordine pubblico | uri: examples/codice_penale/sources/codice_penale_full.md#L9896-L9904
atom ArrestoNotizieFalse: arrest up to 3 months or fine (art. 656) | quote: Pubblicazione o diffusione di notizie false, esagerate o tendenziose, atte a turbare l'ordine pubblico | uri: examples/codice_penale/sources/codice_penale_full.md#L9896-L9904
precetto_656: =>O@Chiunque ~DiffondeNotizieFalse
DiffondeNotizieFalse {
  tipico_656: =>O@Giudice FattoTipico
  pena_656:   O(Sanziona) =>O@Giudice ArrestoNotizieFalse
}

atom ProcuraAllarme: by announcing non-existent disasters, accidents or dangers, raises alarm with the authority or bodies in charge of public order (art. 658) | quote: Procurato allarme presso l'autorità | uri: examples/codice_penale/sources/codice_penale_full.md#L9913-L9919
atom ArrestoAllarme: arrest up to 6 months or fine (art. 658) | quote: Procurato allarme presso l'autorità | uri: examples/codice_penale/sources/codice_penale_full.md#L9913-L9919
precetto_658: =>O@Chiunque ~ProcuraAllarme
ProcuraAllarme {
  tipico_658: =>O@Giudice FattoTipico
  pena_658:   O(Sanziona) =>O@Giudice ArrestoAllarme
}

atom DisturbaRiposo: by clamour or noise, or abusing sound instruments, disturbs the occupations or rest of persons (art. 659) | quote: Disturbo delle occupazioni o del riposo delle persone | uri: examples/codice_penale/sources/codice_penale_full.md#L9920-L9928
atom ArrestoDisturbo: arrest up to 3 months or fine (art. 659) | quote: Disturbo delle occupazioni o del riposo delle persone | uri: examples/codice_penale/sources/codice_penale_full.md#L9920-L9928
precetto_659: =>O@Chiunque ~DisturbaRiposo
DisturbaRiposo {
  tipico_659: =>O@Giudice FattoTipico
  pena_659:   O(Sanziona) =>O@Giudice ArrestoDisturbo
}

atom MolestaPersone: in a public place or by telephone, out of petulance or other reprehensible motive, harasses or disturbs persons (art. 660) | quote: Molestia o disturbo alle persone | uri: examples/codice_penale/sources/codice_penale_full.md#L9937-L9945
atom ArrestoMolestia: arrest up to 6 months or fine (art. 660) | quote: Molestia o disturbo alle persone | uri: examples/codice_penale/sources/codice_penale_full.md#L9937-L9945
precetto_660: =>O@Chiunque ~MolestaPersone
MolestaPersone {
  tipico_660: =>O@Giudice FattoTipico
  pena_660:   O(Sanziona) =>O@Giudice ArrestoMolestia
}

atom AbusaCredulita: publicly, by any imposture, tries to abuse popular credulity in a way apt to disturb public order (art. 661) | quote: Abuso della credulità popolare | uri: examples/codice_penale/sources/codice_penale_full.md#L9949-L9957
atom ArrestoCredulita: arrest up to 3 months or fine (art. 661) | quote: Abuso della credulità popolare | uri: examples/codice_penale/sources/codice_penale_full.md#L9949-L9957
precetto_661: =>O@Chiunque ~AbusaCredulita
AbusaCredulita {
  tipico_661: =>O@Giudice FattoTipico
  pena_661:   O(Sanziona) =>O@Giudice ArrestoCredulita
}

atom NonCustodisceAnimali: leaves free, or fails to keep with due care, dangerous animals they possess (art. 672) | quote: Omessa custodia e mal governo di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L10132-L10140
atom ArrestoAnimali: fine, failure to guard dangerous animals (art. 672) | quote: Omessa custodia e mal governo di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L10132-L10140
precetto_672: =>O@Chiunque ~NonCustodisceAnimali
NonCustodisceAnimali {
  tipico_672: =>O@Giudice FattoTipico
  pena_672:   O(Sanziona) =>O@Giudice ArrestoAnimali
}

atom OmetteSegnali: omits to place the signals or barriers prescribed by law or authority, or removes them (art. 673) | quote: Omesso collocamento o rimozione di segnali o ripari | uri: examples/codice_penale/sources/codice_penale_full.md#L10147-L10155
atom ArrestoSegnali: arrest up to 3 months or fine (art. 673) | quote: Omesso collocamento o rimozione di segnali o ripari | uri: examples/codice_penale/sources/codice_penale_full.md#L10147-L10155
precetto_673: =>O@Chiunque ~OmetteSegnali
OmetteSegnali {
  tipico_673: =>O@Giudice FattoTipico
  pena_673:   O(Sanziona) =>O@Giudice ArrestoSegnali
}

atom GettoPericoloso: throws or pours, in a place of public transit or of common use, things apt to offend, soil or harm persons (art. 674) | quote: Getto pericoloso di cose | uri: examples/codice_penale/sources/codice_penale_full.md#L10159-L10167
atom ArrestoGetto: arrest up to 1 month or fine (art. 674) | quote: Getto pericoloso di cose | uri: examples/codice_penale/sources/codice_penale_full.md#L10159-L10167
precetto_674: =>O@Chiunque ~GettoPericoloso
GettoPericoloso {
  tipico_674: =>O@Giudice FattoTipico
  pena_674:   O(Sanziona) =>O@Giudice ArrestoGetto
}

atom CollocamentoPericoloso: without due care, places or hangs things that, falling in a place of public transit, may offend or harm persons (art. 675) | quote: Collocamento pericoloso di cose | uri: examples/codice_penale/sources/codice_penale_full.md#L10174-L10180
atom ArrestoCollocamento: fine, dangerous placing of things (art. 675) | quote: Collocamento pericoloso di cose | uri: examples/codice_penale/sources/codice_penale_full.md#L10174-L10180
precetto_675: =>O@Chiunque ~CollocamentoPericoloso
CollocamentoPericoloso {
  tipico_675: =>O@Giudice FattoTipico
  pena_675:   O(Sanziona) =>O@Giudice ArrestoCollocamento
}

atom RovinaEdificio: having taken part in the design or works of a building, by fault causes its ruin endangering persons (art. 676) | quote: Rovina di edifici o di altre costruzioni | uri: examples/codice_penale/sources/codice_penale_full.md#L10181-L10189
atom ArrestoRovina: fine, ruin of buildings (art. 676) | quote: Rovina di edifici o di altre costruzioni | uri: examples/codice_penale/sources/codice_penale_full.md#L10181-L10189
precetto_676: =>O@Chiunque ~RovinaEdificio
RovinaEdificio {
  tipico_676: =>O@Giudice FattoTipico
  pena_676:   O(Sanziona) =>O@Giudice ArrestoRovina
}

atom FabbricaEsplodenti: without licence or due care, fabricates or trades in explosive materials (art. 678) | quote: Fabbricazione o commercio abusivi di materie esplodenti | uri: examples/codice_penale/sources/codice_penale_full.md#L10207-L10214
atom ArrestoEsplodenti: arrest up to 18 months and fine (art. 678) | quote: Fabbricazione o commercio abusivi di materie esplodenti | uri: examples/codice_penale/sources/codice_penale_full.md#L10207-L10214
precetto_678: =>O@Chiunque ~FabbricaEsplodenti
FabbricaEsplodenti {
  tipico_678: =>O@Giudice FattoTipico
  pena_678:   O(Sanziona) =>O@Giudice ArrestoEsplodenti
}

atom AperturaAbusivaSpettacolo: opens or keeps open places of public spectacle or entertainment without the authority's licence (art. 681) | quote: Apertura abusiva di luoghi di pubblico spettacolo o trattenimento | uri: examples/codice_penale/sources/codice_penale_full.md#L10236-L10244
atom ArrestoSpettacolo: arrest up to 6 months or fine (art. 681) | quote: Apertura abusiva di luoghi di pubblico spettacolo o trattenimento | uri: examples/codice_penale/sources/codice_penale_full.md#L10236-L10244
precetto_681: =>O@Chiunque ~AperturaAbusivaSpettacolo
AperturaAbusivaSpettacolo {
  tipico_681: =>O@Giudice FattoTipico
  pena_681:   O(Sanziona) =>O@Giudice ArrestoSpettacolo
}

atom IngressoVietatoMilitare: enters places where access is forbidden in the military interest of the State (art. 682) | quote: Ingresso arbitrario in luoghi ove l'accesso è vietato nell'interesse militare dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L10247-L10253
atom ArrestoIngressoMilitare: arrest up to 1 year or fine (art. 682) | quote: Ingresso arbitrario in luoghi ove l'accesso è vietato nell'interesse militare dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L10247-L10253
precetto_682: =>O@Chiunque ~IngressoVietatoMilitare
IngressoVietatoMilitare {
  tipico_682: =>O@Giudice FattoTipico
  pena_682:   O(Sanziona) =>O@Giudice ArrestoIngressoMilitare
}

atom CommercioAbusivoLiquori: against the authority's prohibition, fabricates or trades in liquors or drugs or substances for their composition (art. 686) | quote: Fabbricazione o commercio abusivi di liquori o droghe, o di sostanze destinate alla loro composizione | uri: examples/codice_penale/sources/codice_penale_full.md#L10280-L10288
atom ArrestoLiquori: arrest, abusive trade in liquors/drugs (art. 686) | quote: Fabbricazione o commercio abusivi di liquori o droghe, o di sostanze destinate alla loro composizione | uri: examples/codice_penale/sources/codice_penale_full.md#L10280-L10288
precetto_686: =>O@Chiunque ~CommercioAbusivoLiquori
CommercioAbusivoLiquori {
  tipico_686: =>O@Giudice FattoTipico
  pena_686:   O(Sanziona) =>O@Giudice ArrestoLiquori
}

atom SomministraAlcoolMinori: an innkeeper administers alcoholic drinks to a person under 16 or to a person who is mentally infirm (art. 689) | quote: Somministrazione di bevande alcooliche a minori o a infermi di mente | uri: examples/codice_penale/sources/codice_penale_full.md#L10317-L10325
atom ArrestoAlcoolMinori: arrest up to 1 year (art. 689) | quote: Somministrazione di bevande alcooliche a minori o a infermi di mente | uri: examples/codice_penale/sources/codice_penale_full.md#L10317-L10325
precetto_689: =>O@Chiunque ~SomministraAlcoolMinori
SomministraAlcoolMinori {
  tipico_689: =>O@Giudice FattoTipico
  pena_689:   O(Sanziona) =>O@Giudice ArrestoAlcoolMinori
}

atom SomministraAlcoolUbriaco: administers alcoholic drinks to a person in a state of manifest drunkenness (art. 691) | quote: Somministrazione di bevande alcooliche a persona in stato di manifesta ubriachezza | uri: examples/codice_penale/sources/codice_penale_full.md#L10336-L10344
atom ArrestoAlcoolUbriaco: arrest up to 6 months (art. 691) | quote: Somministrazione di bevande alcooliche a persona in stato di manifesta ubriachezza | uri: examples/codice_penale/sources/codice_penale_full.md#L10336-L10344
precetto_691: =>O@Chiunque ~SomministraAlcoolUbriaco
SomministraAlcoolUbriaco {
  tipico_691: =>O@Giudice FattoTipico
  pena_691:   O(Sanziona) =>O@Giudice ArrestoAlcoolUbriaco
}

atom DetienePesiIllegali: in a commercial activity, holds illegal measures or weights (art. 692) | quote: Detenzione di misure e pesi illegali | uri: examples/codice_penale/sources/codice_penale_full.md#L10346-L10354
atom ArrestoPesiIllegali: fine, holding of illegal weights (art. 692) | quote: Detenzione di misure e pesi illegali | uri: examples/codice_penale/sources/codice_penale_full.md#L10346-L10354
precetto_692: =>O@Chiunque ~DetienePesiIllegali
DetienePesiIllegali {
  tipico_692: =>O@Giudice FattoTipico
  pena_692:   O(Sanziona) =>O@Giudice ArrestoPesiIllegali
}

atom RifiutaMonete: refuses to receive, for their value, coins having legal tender in the State (art. 693) | quote: Rifiuto di monete aventi corso legale | uri: examples/codice_penale/sources/codice_penale_full.md#L10360-L10365
atom ArrestoRifiutoMonete: fine, refusal of legal tender (art. 693) | quote: Rifiuto di monete aventi corso legale | uri: examples/codice_penale/sources/codice_penale_full.md#L10360-L10365
precetto_693: =>O@Chiunque ~RifiutaMonete
RifiutaMonete {
  tipico_693: =>O@Giudice FattoTipico
  pena_693:   O(Sanziona) =>O@Giudice ArrestoRifiutoMonete
}

atom FabbricaArmiAbusiva: without the authority's licence, fabricates, imports or exports weapons (art. 695) | quote: Fabbricazione o commercio non autorizzati di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10377-L10385
atom ArrestoFabbricaArmi: arrest 1-8 years and fine (art. 695) | quote: Fabbricazione o commercio non autorizzati di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10377-L10385
precetto_695: =>O@Chiunque ~FabbricaArmiAbusiva
FabbricaArmiAbusiva {
  tipico_695: =>O@Giudice FattoTipico
  pena_695:   O(Sanziona) =>O@Giudice ArrestoFabbricaArmi
}

atom DetieneArmiAbusiva: holds weapons or munitions without having declared them to the authority when required (art. 697) | quote: Detenzione abusiva di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10392-L10400
atom ArrestoDetenzioneArmi: arrest up to 12 months or fine (art. 697) | quote: Detenzione abusiva di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10392-L10400
precetto_697: =>O@Chiunque ~DetieneArmiAbusiva
DetieneArmiAbusiva {
  tipico_697: =>O@Giudice FattoTipico
  pena_697:   O(Sanziona) =>O@Giudice ArrestoDetenzioneArmi
}

atom PortoAbusivoArmi: without the authority's licence, when required, carries a weapon outside their dwelling (art. 699) | quote: Porto abusivo di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10410-L10418
atom ArrestoPortoArmi: arrest 6-18 months (art. 699) | quote: Porto abusivo di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10410-L10418
precetto_699: =>O@Chiunque ~PortoAbusivoArmi
PortoAbusivoArmi {
  tipico_699: =>O@Giudice FattoTipico
  pena_699:   O(Sanziona) =>O@Giudice ArrestoPortoArmi
}

atom AccensioniPericolose: without licence, in or near an inhabited place, sets off fireworks or dangerous explosions (art. 703) | quote: Accensioni ed esplosioni pericolose | uri: examples/codice_penale/sources/codice_penale_full.md#L10450-L10458
atom ArrestoAccensioni: arrest up to 1 month or fine (art. 703) | quote: Accensioni ed esplosioni pericolose | uri: examples/codice_penale/sources/codice_penale_full.md#L10450-L10458
precetto_703: =>O@Chiunque ~AccensioniPericolose
AccensioniPericolose {
  tipico_703: =>O@Giudice FattoTipico
  pena_703:   O(Sanziona) =>O@Giudice ArrestoAccensioni
}

atom PossessoGrimaldelli: having been convicted of crimes for gain, is found in possession of altered keys or picklocks without justifying their use (art. 707) | quote: Possesso ingiustificato di chiavi alterate o di grimaldelli | uri: examples/codice_penale/sources/codice_penale_full.md#L10491-L10499
atom ArrestoGrimaldelli: arrest 6 months-2 years (art. 707) | quote: Possesso ingiustificato di chiavi alterate o di grimaldelli | uri: examples/codice_penale/sources/codice_penale_full.md#L10491-L10499
precetto_707: =>O@Chiunque ~PossessoGrimaldelli
PossessoGrimaldelli {
  tipico_707: =>O@Giudice FattoTipico
  pena_707:   O(Sanziona) =>O@Giudice ArrestoGrimaldelli
}

atom AcquistoSospettaProvenienza: without first ascertaining the lawful provenance, acquires or receives things that, by their quality or the offeror's condition, give reason to suspect they come from crime (art. 712) | quote: Acquisto di cose di sospetta provenienza | uri: examples/codice_penale/sources/codice_penale_full.md#L10550-L10558
atom ArrestoSospettaProvenienza: arrest up to 6 months or fine (art. 712) | quote: Acquisto di cose di sospetta provenienza | uri: examples/codice_penale/sources/codice_penale_full.md#L10550-L10558
precetto_712: =>O@Chiunque ~AcquistoSospettaProvenienza
AcquistoSospettaProvenienza {
  tipico_712: =>O@Giudice FattoTipico
  pena_712:   O(Sanziona) =>O@Giudice ArrestoSospettaProvenienza
}

atom EserciziGiocoAzzardo: in a public place or private club, runs a game of chance or facilitates it (art. 718) | quote: Esercizio di giuochi d'azzardo | uri: examples/codice_penale/sources/codice_penale_full.md#L10631-L10639
atom ArrestoGiocoAzzardo: arrest 3 months-1 year and fine (art. 718) | quote: Esercizio di giuochi d'azzardo | uri: examples/codice_penale/sources/codice_penale_full.md#L10631-L10639
precetto_718: =>O@Chiunque ~EserciziGiocoAzzardo
EserciziGiocoAzzardo {
  tipico_718: =>O@Giudice FattoTipico
  pena_718:   O(Sanziona) =>O@Giudice ArrestoGiocoAzzardo
}

atom Bestemmia: publicly blasphemes, with invectives or outrageous words, against the Divinity (art. 724) | quote: Bestemmia e manifestazioni oltraggiose verso i defunti | uri: examples/codice_penale/sources/codice_penale_full.md#L10697-L10705
atom ArrestoBestemmia: fine, blasphemy (art. 724) | quote: Bestemmia e manifestazioni oltraggiose verso i defunti | uri: examples/codice_penale/sources/codice_penale_full.md#L10697-L10705
precetto_724: =>O@Chiunque ~Bestemmia
Bestemmia {
  tipico_724: =>O@Giudice FattoTipico
  pena_724:   O(Sanziona) =>O@Giudice ArrestoBestemmia
}

atom CommercioOggettiIndecenti: exposes to public view, or trades, writings/images/objects contrary to public decency (art. 725) | quote: Commercio di scritti, disegni o altri oggetti contrari alla pubblica decenza | uri: examples/codice_penale/sources/codice_penale_full.md#L10711-L10717
atom ArrestoOggettiIndecenti: arrest up to 1 year or fine (art. 725) | quote: Commercio di scritti, disegni o altri oggetti contrari alla pubblica decenza | uri: examples/codice_penale/sources/codice_penale_full.md#L10711-L10717
precetto_725: =>O@Chiunque ~CommercioOggettiIndecenti
CommercioOggettiIndecenti {
  tipico_725: =>O@Giudice FattoTipico
  pena_725:   O(Sanziona) =>O@Giudice ArrestoOggettiIndecenti
}

atom AttiContrariDecenza: in a public place, performs acts contrary to public decency, or foul language (art. 726) | quote: Atti contrari alla pubblica decenza | uri: examples/codice_penale/sources/codice_penale_full.md#L10718-L10726
atom ArrestoDecenza: fine, acts against public decency (art. 726) | quote: Atti contrari alla pubblica decenza | uri: examples/codice_penale/sources/codice_penale_full.md#L10718-L10726
precetto_726: =>O@Chiunque ~AttiContrariDecenza
AttiContrariDecenza {
  tipico_726: =>O@Giudice FattoTipico
  pena_726:   O(Sanziona) =>O@Giudice ArrestoDecenza
}

atom AbbandonaAnimali: abandons domestic animals, or animals that have acquired habits of captivity (art. 727) | quote: Abbandono di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L10729-L10737
atom ArrestoAbbandonoAnimali: arrest up to 1 year or fine (art. 727) | quote: Abbandono di animali | uri: examples/codice_penale/sources/codice_penale_full.md#L10729-L10737
precetto_727: =>O@Chiunque ~AbbandonaAnimali
AbbandonaAnimali {
  tipico_727: =>O@Giudice FattoTipico
  pena_727:   O(Sanziona) =>O@Giudice ArrestoAbbandonoAnimali
}

atom OmetteIstruzioneMinore: being vested with authority or charged with the supervision of a minor, omits to provide for their elementary instruction (art. 731) | quote: Inosservanza dell'obbligo dell'istruzione elementare dei minori | uri: examples/codice_penale/sources/codice_penale_full.md#L10777-L10785
atom ArrestoIstruzione: fine, failure to provide elementary instruction (art. 731) | quote: Inosservanza dell'obbligo dell'istruzione elementare dei minori | uri: examples/codice_penale/sources/codice_penale_full.md#L10777-L10785
precetto_731: =>O@Chiunque ~OmetteIstruzioneMinore
OmetteIstruzioneMinore {
  tipico_731: =>O@Giudice FattoTipico
  pena_731:   O(Sanziona) =>O@Giudice ArrestoIstruzione
}

atom DanneggiaPatrimonioArtistico: destroys, deteriorates or damages a monument or other thing of their own of recognised archaeological, historical or artistic value (art. 733) | quote: Danneggiamento al patrimonio archeologico, storico o artistico nazionale | uri: examples/codice_penale/sources/codice_penale_full.md#L10798-L10806
atom ArrestoPatrimonioArtistico: arrest up to 1 year or fine (art. 733) | quote: Danneggiamento al patrimonio archeologico, storico o artistico nazionale | uri: examples/codice_penale/sources/codice_penale_full.md#L10798-L10806
precetto_733: =>O@Chiunque ~DanneggiaPatrimonioArtistico
DanneggiaPatrimonioArtistico {
  tipico_733: =>O@Giudice FattoTipico
  pena_733:   O(Sanziona) =>O@Giudice ArrestoPatrimonioArtistico
}

atom DistruggeBellezzeNaturali: by constructions, demolitions or otherwise, destroys or alters natural beauties of places subject to special protection (art. 734) | quote: Distruzione o deturpamento di bellezze naturali | uri: examples/codice_penale/sources/codice_penale_full.md#L10808-L10816
atom ArrestoBellezzeNaturali: fine, destruction of natural beauties (art. 734) | quote: Distruzione o deturpamento di bellezze naturali | uri: examples/codice_penale/sources/codice_penale_full.md#L10808-L10816
precetto_734: =>O@Chiunque ~DistruggeBellezzeNaturali
DistruggeBellezzeNaturali {
  tipico_734: =>O@Giudice FattoTipico
  pena_734:   O(Sanziona) =>O@Giudice ArrestoBellezzeNaturali
}

atom GridaSediziose: in a non-private meeting or public place, utters seditious cries or makes seditious demonstrations (art. 654) | quote: Grida e manifestazioni sediziose | uri: examples/codice_penale/sources/codice_penale_full.md#L9878-L9885
atom ArrestoGrida: arrest up to 1 year (art. 654) | quote: Grida e manifestazioni sediziose | uri: examples/codice_penale/sources/codice_penale_full.md#L9878-L9885
precetto_654: =>O@Chiunque ~GridaSediziose
GridaSediziose {
  tipico_654: =>O@Giudice FattoTipico
  pena_654:   O(Sanziona) =>O@Giudice ArrestoGrida
}

atom VendeScrittiAbusiva: in a public place, sells or distributes writings or drawings without observing the prescribed rules (art. 663) | quote: Vendita, distribuzione o affissione abusiva di scritti o disegni | uri: examples/codice_penale/sources/codice_penale_full.md#L9968-L9976
atom ArrestoVenditaScritti: fine, abusive sale of writings (art. 663) | quote: Vendita, distribuzione o affissione abusiva di scritti o disegni | uri: examples/codice_penale/sources/codice_penale_full.md#L9968-L9976
precetto_663: =>O@Chiunque ~VendeScrittiAbusiva
VendeScrittiAbusiva {
  tipico_663: =>O@Giudice FattoTipico
  pena_663:   O(Sanziona) =>O@Giudice ArrestoVenditaScritti
}

atom DistruggeAffissioni: detaches, tears or renders illegible writings or drawings lawfully posted (art. 664) | quote: Distruzione o deterioramento di affissioni | uri: examples/codice_penale/sources/codice_penale_full.md#L9993-L10001
atom ArrestoAffissioni: fine, destruction of postings (art. 664) | quote: Distruzione o deterioramento di affissioni | uri: examples/codice_penale/sources/codice_penale_full.md#L9993-L10001
precetto_664: =>O@Chiunque ~DistruggeAffissioni
DistruggeAffissioni {
  tipico_664: =>O@Giudice FattoTipico
  pena_664:   O(Sanziona) =>O@Giudice ArrestoAffissioni
}

atom SpettacoloSenzaLicenza: gives public spectacles or entertainments in a public place without the authority's licence (art. 666) | quote: Spettacoli o trattenimenti pubblici senza licenza | uri: examples/codice_penale/sources/codice_penale_full.md#L10022-L10030
atom ArrestoSpettacoloSenzaLicenza: arrest up to 3 months or fine (art. 666) | quote: Spettacoli o trattenimenti pubblici senza licenza | uri: examples/codice_penale/sources/codice_penale_full.md#L10022-L10030
precetto_666: =>O@Chiunque ~SpettacoloSenzaLicenza
SpettacoloSenzaLicenza {
  tipico_666: =>O@Giudice FattoTipico
  pena_666:   O(Sanziona) =>O@Giudice ArrestoSpettacoloSenzaLicenza
}

atom MestiereGirovagoSenzaLicenza: exercises an itinerant trade without the authority's licence or the prescribed rules (art. 669) | quote: Esercizio abusivo di mestieri girovaghi | uri: examples/codice_penale/sources/codice_penale_full.md#L10084-L10092
atom ArrestoMestiereGirovago: arrest up to 6 months or fine (art. 669) | quote: Esercizio abusivo di mestieri girovaghi | uri: examples/codice_penale/sources/codice_penale_full.md#L10084-L10092
precetto_669: =>O@Chiunque ~MestiereGirovagoSenzaLicenza
MestiereGirovagoSenzaLicenza {
  tipico_669: =>O@Giudice FattoTipico
  pena_669:   O(Sanziona) =>O@Giudice ArrestoMestiereGirovago
}

atom ImpiegaMinoriAccattonaggio: uses, to beg, a person under 14 or otherwise incapable (art. 671) | quote: Impiego di minori nell'accattonaggio | uri: examples/codice_penale/sources/codice_penale_full.md#L10115-L10123
atom ArrestoAccattonaggio: arrest 3 months-1 year (art. 671) | quote: Impiego di minori nell'accattonaggio | uri: examples/codice_penale/sources/codice_penale_full.md#L10115-L10123
precetto_671: =>O@Chiunque ~ImpiegaMinoriAccattonaggio
ImpiegaMinoriAccattonaggio {
  tipico_671: =>O@Giudice FattoTipico
  pena_671:   O(Sanziona) =>O@Giudice ArrestoAccattonaggio
}

atom OmetteDenunciaEsplodenti: omits to declare to the authority that they hold explosive materials (art. 679) | quote: Omessa denuncia di materie esplodenti | uri: examples/codice_penale/sources/codice_penale_full.md#L10215-L10223
atom ArrestoOmessaDenunciaEsplodenti: arrest up to 12 months or fine (art. 679) | quote: Omessa denuncia di materie esplodenti | uri: examples/codice_penale/sources/codice_penale_full.md#L10215-L10223
precetto_679: =>O@Chiunque ~OmetteDenunciaEsplodenti
OmetteDenunciaEsplodenti {
  tipico_679: =>O@Giudice FattoTipico
  pena_679:   O(Sanziona) =>O@Giudice ArrestoOmessaDenunciaEsplodenti
}

atom PubblicaAttiProcedimento: publishes, in whole or part, acts of a criminal proceeding whose publication is forbidden (art. 684) | quote: Pubblicazione arbitraria di atti di un procedimento penale | uri: examples/codice_penale/sources/codice_penale_full.md#L10263-L10269
atom ArrestoPubblicazioneAtti: arrest up to 30 days or fine (art. 684) | quote: Pubblicazione arbitraria di atti di un procedimento penale | uri: examples/codice_penale/sources/codice_penale_full.md#L10263-L10269
precetto_684: =>O@Chiunque ~PubblicaAttiProcedimento
PubblicaAttiProcedimento {
  tipico_684: =>O@Giudice FattoTipico
  pena_684:   O(Sanziona) =>O@Giudice ArrestoPubblicazioneAtti
}

atom DeterminaUbriachezzaAltrui: in a public place, causes another's drunkenness by administering alcoholic drinks (art. 690) | quote: Determinazione in altri dello stato di ubriachezza | uri: examples/codice_penale/sources/codice_penale_full.md#L10329-L10335
atom ArrestoUbriachezzaAltrui: fine, causing drunkenness of others (art. 690) | quote: Determinazione in altri dello stato di ubriachezza | uri: examples/codice_penale/sources/codice_penale_full.md#L10329-L10335
precetto_690: =>O@Chiunque ~DeterminaUbriachezzaAltrui
DeterminaUbriachezzaAltrui {
  tipico_690: =>O@Giudice FattoTipico
  pena_690:   O(Sanziona) =>O@Giudice ArrestoUbriachezzaAltrui
}

atom OmetteConsegnaMoneteFalse: having received as genuine money recognised as counterfeit, fails to deliver it to the authority (art. 694) | quote: Omessa consegna di monete riconosciute contraffatte | uri: examples/codice_penale/sources/codice_penale_full.md#L10366-L10374
atom ArrestoOmessaConsegnaMonete: fine, failure to hand over counterfeit money (art. 694) | quote: Omessa consegna di monete riconosciute contraffatte | uri: examples/codice_penale/sources/codice_penale_full.md#L10366-L10374
precetto_694: =>O@Chiunque ~OmetteConsegnaMoneteFalse
OmetteConsegnaMoneteFalse {
  tipico_694: =>O@Giudice FattoTipico
  pena_694:   O(Sanziona) =>O@Giudice ArrestoOmessaConsegnaMonete
}

atom VenditaAmbulanteArmi: exercises the itinerant sale of weapons (art. 696) | quote: Vendita ambulante di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10387-L10391
atom ArrestoVenditaArmi: arrest up to 3 years and fine (art. 696) | quote: Vendita ambulante di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10387-L10391
precetto_696: =>O@Chiunque ~VenditaAmbulanteArmi
VenditaAmbulanteArmi {
  tipico_696: =>O@Giudice FattoTipico
  pena_696:   O(Sanziona) =>O@Giudice ArrestoVenditaArmi
}

atom OmessaConsegnaArmi: disobeys the authority's order to hand over weapons within the prescribed time (art. 698) | quote: Omessa consegna di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10403-L10409
atom ArrestoOmessaConsegnaArmi: arrest, failure to hand over weapons (art. 698) | quote: Omessa consegna di armi | uri: examples/codice_penale/sources/codice_penale_full.md#L10403-L10409
precetto_698: =>O@Chiunque ~OmessaConsegnaArmi
OmessaConsegnaArmi {
  tipico_698: =>O@Giudice FattoTipico
  pena_698:   O(Sanziona) =>O@Giudice ArrestoOmessaConsegnaArmi
}

atom CommercioCosePreziose: without licence or the legal prescriptions, trades in precious objects (art. 705) | quote: Commercio non autorizzato di cose preziose | uri: examples/codice_penale/sources/codice_penale_full.md#L10473-L10481
atom ArrestoCosePreziose: arrest up to 1 year or fine (art. 705) | quote: Commercio non autorizzato di cose preziose | uri: examples/codice_penale/sources/codice_penale_full.md#L10473-L10481
precetto_705: =>O@Chiunque ~CommercioCosePreziose
CommercioCosePreziose {
  tipico_705: =>O@Giudice FattoTipico
  pena_705:   O(Sanziona) =>O@Giudice ArrestoCosePreziose
}

atom OmessaDenunciaCoseDelitto: having received or acquired things coming from crime, omits to declare their provenance to the authority (art. 709) | quote: Omessa denuncia di cose provenienti da delitto | uri: examples/codice_penale/sources/codice_penale_full.md#L10521-L10529
atom ArrestoOmessaDenunciaCose: arrest 3 months-1 year (art. 709) | quote: Omessa denuncia di cose provenienti da delitto | uri: examples/codice_penale/sources/codice_penale_full.md#L10521-L10529
precetto_709: =>O@Chiunque ~OmessaDenunciaCoseDelitto
OmessaDenunciaCoseDelitto {
  tipico_709: =>O@Giudice FattoTipico
  pena_709:   O(Sanziona) =>O@Giudice ArrestoOmessaDenunciaCose
}

atom PartecipaGiocoAzzardo: in a public place or private club, is found taking part in a game of chance (art. 720) | quote: Partecipazione a giuochi d'azzardo | uri: examples/codice_penale/sources/codice_penale_full.md#L10654-L10662
atom ArrestoPartecipazioneGioco: arrest up to 6 months or fine (art. 720) | quote: Partecipazione a giuochi d'azzardo | uri: examples/codice_penale/sources/codice_penale_full.md#L10654-L10662
precetto_720: =>O@Chiunque ~PartecipaGiocoAzzardo
PartecipaGiocoAzzardo {
  tipico_720: =>O@Giudice FattoTipico
  pena_720:   O(Sanziona) =>O@Giudice ArrestoPartecipazioneGioco
}

atom SopprimeCoscienza: with consent, puts a person in a state of narcosis or hypnosis, or otherwise suppresses their consciousness or will (art. 728) | quote: Trattamento idoneo a sopprimere la coscienza o la volontà altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L10745-L10753
atom ArrestoSoppressioneCoscienza: arrest up to 6 months (art. 728) | quote: Trattamento idoneo a sopprimere la coscienza o la volontà altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L10745-L10753
precetto_728: =>O@Chiunque ~SopprimeCoscienza
SopprimeCoscienza {
  tipico_728: =>O@Giudice FattoTipico
  pena_728:   O(Sanziona) =>O@Giudice ArrestoSoppressioneCoscienza
}

atom SomministraSostanzeNociveMinori: being authorised to sell medicines, delivers to a minor poisonous or harmful substances outside the prescribed cases (art. 730) | quote: Somministrazione a minori di sostanze velenose o nocive | uri: examples/codice_penale/sources/codice_penale_full.md#L10765-L10773
atom ArrestoSostanzeNocive: arrest, supply of harmful substances to minors (art. 730) | quote: Somministrazione a minori di sostanze velenose o nocive | uri: examples/codice_penale/sources/codice_penale_full.md#L10765-L10773
precetto_730: =>O@Chiunque ~SomministraSostanzeNociveMinori
SomministraSostanzeNociveMinori {
  tipico_730: =>O@Giudice FattoTipico
  pena_730:   O(Sanziona) =>O@Giudice ArrestoSostanzeNocive
}

atom DivulgaIdentitaVittimaSessuale: divulges the identity or image of a victim of sexual violence without their consent (art. 734-bis) | quote: Divulgazione delle generalità o dell'immagine di persona offesa da atti di violenza sessuale | uri: examples/codice_penale/sources/codice_penale_full.md#L10818-L10826
atom ArrestoDivulgazioneVittima: fine, divulging a sexual-violence victim's identity (art. 734-bis) | quote: Divulgazione delle generalità o dell'immagine di persona offesa da atti di violenza sessuale | uri: examples/codice_penale/sources/codice_penale_full.md#L10818-L10826
precetto_734bis: =>O@Chiunque ~DivulgaIdentitaVittimaSessuale
DivulgaIdentitaVittimaSessuale {
  tipico_734bis: =>O@Giudice FattoTipico
  pena_734bis:   O(Sanziona) =>O@Giudice ArrestoDivulgazioneVittima
}

atom DivulgaStampaClandestina: in any way divulges clandestinely published press or printed matter (art. 663-bis) | quote: Divulgazione di stampa clandestina | uri: examples/codice_penale/sources/codice_penale_full.md#L9983-L9991
atom ArrestoStampaClandestina: arrest or fine, clandestine press (art. 663-bis) | quote: Divulgazione di stampa clandestina | uri: examples/codice_penale/sources/codice_penale_full.md#L9983-L9991
precetto_663bis: =>O@Chiunque ~DivulgaStampaClandestina
DivulgaStampaClandestina {
  tipico_663bis: =>O@Giudice FattoTipico
  pena_663bis:   O(Sanziona) =>O@Giudice ArrestoStampaClandestina
}

atom RappresentazioniAbusive: publicly recites dramas or gives shows without observing the prescribed rules (art. 668) | quote: Rappresentazioni teatrali o cinematografiche abusive | uri: examples/codice_penale/sources/codice_penale_full.md#L10065-L10073
atom ArrestoRappresentazioni: arrest up to 6 months or fine (art. 668) | quote: Rappresentazioni teatrali o cinematografiche abusive | uri: examples/codice_penale/sources/codice_penale_full.md#L10065-L10073
precetto_668: =>O@Chiunque ~RappresentazioniAbusive
RappresentazioniAbusive {
  tipico_668: =>O@Giudice FattoTipico
  pena_668:   O(Sanziona) =>O@Giudice ArrestoRappresentazioni
}

atom PubblicaDeliberazioniCamere: without authorisation, publishes the secret discussions or deliberations of a Chamber (art. 683) | quote: Pubblicazione delle discussioni o delle deliberazioni segrete di una delle Camere | uri: examples/codice_penale/sources/codice_penale_full.md#L10254-L10262
atom ArrestoDeliberazioni: fine, publication of secret parliamentary deliberations (art. 683) | quote: Pubblicazione delle discussioni o delle deliberazioni segrete di una delle Camere | uri: examples/codice_penale/sources/codice_penale_full.md#L10254-L10262
precetto_683: =>O@Chiunque ~PubblicaDeliberazioniCamere
PubblicaDeliberazioniCamere {
  tipico_683: =>O@Giudice FattoTipico
  pena_683:   O(Sanziona) =>O@Giudice ArrestoDeliberazioni
}

atom PubblicaNomiGiudici: unduly publishes the names of judges with indication of their votes, in a criminal proceeding (art. 685) | quote: Indebita pubblicazione di notizie concernenti un procedimento penale | uri: examples/codice_penale/sources/codice_penale_full.md#L10270-L10278
atom ArrestoNomiGiudici: fine, undue publication of proceeding news (art. 685) | quote: Indebita pubblicazione di notizie concernenti un procedimento penale | uri: examples/codice_penale/sources/codice_penale_full.md#L10270-L10278
precetto_685: =>O@Chiunque ~PubblicaNomiGiudici
PubblicaNomiGiudici {
  tipico_685: =>O@Giudice FattoTipico
  pena_685:   O(Sanziona) =>O@Giudice ArrestoNomiGiudici
}

atom ConsumoAlcoolVietato: buys or consumes, in a public establishment, alcoholic drinks at a time when their sale is not allowed (art. 687) | quote: Consumo di bevande alcooliche in tempo di vendita non consentita | uri: examples/codice_penale/sources/codice_penale_full.md#L10300-L10305
atom ArrestoConsumoAlcool: fine, alcohol consumption at forbidden time (art. 687) | quote: Consumo di bevande alcooliche in tempo di vendita non consentita | uri: examples/codice_penale/sources/codice_penale_full.md#L10300-L10305
precetto_687: =>O@Chiunque ~ConsumoAlcoolVietato
ConsumoAlcoolVietato {
  tipico_687: =>O@Giudice FattoTipico
  pena_687:   O(Sanziona) =>O@Giudice ArrestoConsumoAlcool
}

atom PossessoValoriIngiustificato: being in the personal conditions of art. 707, is found in unjustified possession of money or valuables (art. 708) | quote: Possesso ingiustificato di valori | uri: examples/codice_penale/sources/codice_penale_full.md#L10509-L10517
atom ArrestoPossessoValori: arrest 6 months-2 years (art. 708) | quote: Possesso ingiustificato di valori | uri: examples/codice_penale/sources/codice_penale_full.md#L10509-L10517
precetto_708: =>O@Chiunque ~PossessoValoriIngiustificato
PossessoValoriIngiustificato {
  tipico_708: =>O@Giudice FattoTipico
  pena_708:   O(Sanziona) =>O@Giudice ArrestoPossessoValori
}

atom OmessoAvvisoEvasioneMinori: a public official charged with a detention facility omits to notify the authority of the escape or flight of minors (art. 716) | quote: Omesso avviso all'autorità dell'evasione o fuga di minori | uri: examples/codice_penale/sources/codice_penale_full.md#L10602-L10610
atom ArrestoOmessoAvviso: arrest, failure to report escape of minors (art. 716) | quote: Omesso avviso all'autorità dell'evasione o fuga di minori | uri: examples/codice_penale/sources/codice_penale_full.md#L10602-L10610
precetto_716: =>O@Chiunque ~OmessoAvvisoEvasioneMinori
OmessoAvvisoEvasioneMinori {
  tipico_716: =>O@Giudice FattoTipico
  pena_716:   O(Sanziona) =>O@Giudice ArrestoOmessoAvviso
}

atom GiocoNonAzzardoAbusivo: authorised to keep game rooms, tolerates that games of chance are played there (art. 723) | quote: Esercizio abusivo di un giuoco non d'azzardo | uri: examples/codice_penale/sources/codice_penale_full.md#L10685-L10693
atom ArrestoGiocoNonAzzardo: fine, abusive non-chance game (art. 723) | quote: Esercizio abusivo di un giuoco non d'azzardo | uri: examples/codice_penale/sources/codice_penale_full.md#L10685-L10693
precetto_723: =>O@Chiunque ~GiocoNonAzzardoAbusivo
GiocoNonAzzardoAbusivo {
  tipico_723: =>O@Giudice FattoTipico
  pena_723:   O(Sanziona) =>O@Giudice ArrestoGiocoNonAzzardo
}
