# Codice Penale — stato2 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom IntelligenzeStranieroGuerra: holds dealings with a foreigner so the Italian State makes war or commits hostile acts against another State (art. 243) | quote: Intelligenze con lo straniero a scopo di guerra contro lo Stato italiano | uri: examples/codice_penale/sources/codice_penale_full.md#L3124-L3132
atom ReclusioneIntelligenze: reclusion not less than 10 years (art. 243) | quote: Intelligenze con lo straniero a scopo di guerra contro lo Stato italiano | uri: examples/codice_penale/sources/codice_penale_full.md#L3124-L3132
precetto_243: =>O@Chiunque ~IntelligenzeStranieroGuerra
IntelligenzeStranieroGuerra, Dolo {
  tipico_243: =>O@Giudice FattoTipico
  pena_243:   O(Sanziona) =>O@Giudice ReclusioneIntelligenze
}

atom FavoreggiamentoBellico: holds dealings with a foreigner to favour enemy military operations to the harm of the Italian State (art. 247) | quote: Favoreggiamento bellico | uri: examples/codice_penale/sources/codice_penale_full.md#L3168-L3175
atom ReclusioneFavoreggiamentoBellico: reclusion not less than 10 years (art. 247) | quote: Favoreggiamento bellico | uri: examples/codice_penale/sources/codice_penale_full.md#L3168-L3175
precetto_247: =>O@Chiunque ~FavoreggiamentoBellico
FavoreggiamentoBellico, TempoGuerra, Dolo {
  tipico_247: =>O@Giudice FattoTipico
  pena_247:   O(Sanziona) =>O@Giudice ReclusioneFavoreggiamentoBellico
}

atom SomministraNemico: in time of war, supplies the enemy with provisions or other things harmful to war operations (art. 248) | quote: Somministrazione al nemico di provvigioni | uri: examples/codice_penale/sources/codice_penale_full.md#L3176-L3183
atom ReclusioneSomministrazioneNemico: reclusion not less than 5 years (art. 248) | quote: Somministrazione al nemico di provvigioni | uri: examples/codice_penale/sources/codice_penale_full.md#L3176-L3183
precetto_248: =>O@Chiunque ~SomministraNemico
SomministraNemico, Dolo {
  tipico_248: =>O@Giudice FattoTipico
  pena_248:   O(Sanziona) =>O@Giudice ReclusioneSomministrazioneNemico
}

atom DistruggeOpereMilitari: destroys or renders unusable military works, ships, aircraft or other things destined to the State's defence (art. 253) | quote: Distruzione o sabotaggio di opere militari | uri: examples/codice_penale/sources/codice_penale_full.md#L3223-L3231
atom ReclusioneSabotaggioMilitare: reclusion not less than 8 years (art. 253) | quote: Distruzione o sabotaggio di opere militari | uri: examples/codice_penale/sources/codice_penale_full.md#L3223-L3231
precetto_253: =>O@Chiunque ~DistruggeOpereMilitari
DistruggeOpereMilitari, Dolo {
  tipico_253: =>O@Giudice FattoTipico
  pena_253:   O(Sanziona) =>O@Giudice ReclusioneSabotaggioMilitare
}

atom SottraeAttiSicurezza: suppresses, falsifies, subtracts, destroys or conceals acts or documents concerning the security of the State (art. 255) | quote: Soppressione, falsificazione o sottrazione di atti o documenti concernenti la sicurezza dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3244-L3252
atom ReclusioneAttiSicurezza: reclusion 8-15 years (art. 255) | quote: Soppressione, falsificazione o sottrazione di atti o documenti concernenti la sicurezza dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3244-L3252
precetto_255: =>O@Chiunque ~SottraeAttiSicurezza
SottraeAttiSicurezza, Dolo {
  tipico_255: =>O@Giudice FattoTipico
  pena_255:   O(Sanziona) =>O@Giudice ReclusioneAttiSicurezza
}

atom SpionaggioMilitare: for political or military espionage, obtains news that must remain secret in the State's interest (art. 257) | quote: Spionaggio politico o militare | uri: examples/codice_penale/sources/codice_penale_full.md#L3273-L3281
atom ReclusioneSpionaggio: reclusion not less than 15 years (art. 257) | quote: Spionaggio politico o militare | uri: examples/codice_penale/sources/codice_penale_full.md#L3273-L3281
precetto_257: =>O@Chiunque ~SpionaggioMilitare
SpionaggioMilitare, Dolo {
  tipico_257: =>O@Giudice FattoTipico
  pena_257:   O(Sanziona) =>O@Giudice ReclusioneSpionaggio
}

atom RivelaSegretiStato: reveals secret news concerning the State's security (art. 261) | quote: Rivelazione di segreti di Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3326-L3334
atom ReclusioneRivelazioneSegretiStato: reclusion not less than 5 years (art. 261) | quote: Rivelazione di segreti di Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3326-L3334
precetto_261: =>O@Chiunque ~RivelaSegretiStato
RivelaSegretiStato, Dolo {
  tipico_261: =>O@Giudice FattoTipico
  pena_261:   O(Sanziona) =>O@Giudice ReclusioneRivelazioneSegretiStato
}

atom InfedeltaAffariStato: charged by the Government with handling State affairs abroad, acts unfaithfully to deceive the State (art. 264) | quote: Infedeltà in affari di Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3382-L3388
atom ReclusioneInfedelta: reclusion not less than 5 years (art. 264) | quote: Infedeltà in affari di Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3382-L3388
precetto_264: =>O@Chiunque ~InfedeltaAffariStato
InfedeltaAffariStato, Dolo {
  tipico_264: =>O@Giudice FattoTipico
  pena_264:   O(Sanziona) =>O@Giudice ReclusioneInfedelta
}

atom DisfattismoPolitico: in time of war, spreads false news or carries out activity apt to depress public spirit or hinder war operations (art. 265) | quote: Disfattismo politico | uri: examples/codice_penale/sources/codice_penale_full.md#L3389-L3397
atom ReclusioneDisfattismo: reclusion not less than 5 years (art. 265) | quote: Disfattismo politico | uri: examples/codice_penale/sources/codice_penale_full.md#L3389-L3397
precetto_265: =>O@Chiunque ~DisfattismoPolitico
DisfattismoPolitico, TempoGuerra, Dolo {
  tipico_265: =>O@Giudice FattoTipico
  pena_265:   O(Sanziona) =>O@Giudice ReclusioneDisfattismo
}

atom IstigaMilitariDisobbedire: instigates the military to disobey the laws or violate their oath or military duties (art. 266) | quote: Istigazione di militari a disobbedire alle leggi | uri: examples/codice_penale/sources/codice_penale_full.md#L3401-L3409
atom ReclusioneIstigMilitari: reclusion 1-3 years (art. 266) | quote: Istigazione di militari a disobbedire alle leggi | uri: examples/codice_penale/sources/codice_penale_full.md#L3401-L3409
precetto_266: =>O@Chiunque ~IstigaMilitariDisobbedire
IstigaMilitariDisobbedire, Dolo {
  tipico_266: =>O@Giudice FattoTipico
  pena_266:   O(Sanziona) =>O@Giudice ReclusioneIstigMilitari
}

atom PartecipaAssociazioneTerroristica: promotes, organises, directs or is part of an association aimed at terrorism or subversion of the democratic order (art. 270-bis) | quote: Associazioni con finalità di terrorismo anche internazionale o di eversione dell'ordine democratico | uri: examples/codice_penale/sources/codice_penale_full.md#L3457-L3465
atom ReclusioneAssociazioneTerroristica: reclusion 7-15 years (art. 270-bis) | quote: Associazioni con finalità di terrorismo anche internazionale o di eversione dell'ordine democratico | uri: examples/codice_penale/sources/codice_penale_full.md#L3457-L3465
precetto_270bis: =>O@Chiunque ~PartecipaAssociazioneTerroristica
PartecipaAssociazioneTerroristica, Dolo {
  tipico_270bis: =>O@Giudice FattoTipico
  pena_270bis:   O(Sanziona) =>O@Giudice ReclusioneAssociazioneTerroristica
}

atom ArruolaTerrorismo: outside concerted cases, recruits one or more persons for terrorism (art. 270-quater) | quote: Arruolamento con finalità di terrorismo anche internazionale | uri: examples/codice_penale/sources/codice_penale_full.md#L3487-L3494
atom ReclusioneArruolamento: reclusion 7-15 years (art. 270-quater) | quote: Arruolamento con finalità di terrorismo anche internazionale | uri: examples/codice_penale/sources/codice_penale_full.md#L3487-L3494
precetto_270quater: =>O@Chiunque ~ArruolaTerrorismo
ArruolaTerrorismo, FineTerrorismo, Dolo {
  tipico_270quater: =>O@Giudice FattoTipico
  pena_270quater:   O(Sanziona) =>O@Giudice ReclusioneArruolamento
}

atom AddestraTerrorismo: trains or instructs in the preparation/use of explosives, weapons or harmful techniques for terrorism (art. 270-quinquies) | quote: Addestramento ad attività con finalità di terrorismo anche internazionale | uri: examples/codice_penale/sources/codice_penale_full.md#L3495-L3503
atom ReclusioneAddestramento: reclusion 5-10 years (art. 270-quinquies) | quote: Addestramento ad attività con finalità di terrorismo anche internazionale | uri: examples/codice_penale/sources/codice_penale_full.md#L3495-L3503
precetto_270quinquies: =>O@Chiunque ~AddestraTerrorismo
AddestraTerrorismo, FineTerrorismo, Dolo {
  tipico_270quinquies: =>O@Giudice FattoTipico
  pena_270quinquies:   O(Sanziona) =>O@Giudice ReclusioneAddestramento
}

atom AttentaPresidente: attacks the life, safety or personal liberty of the President of the Republic (art. 276) | quote: Attentato contro il presidente della Repubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L3583-L3588
atom ReclusioneAttentatoPresidente: reclusion not less than the maximum, life (art. 276) | quote: Attentato contro il presidente della Repubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L3583-L3588
AttentaPresidente, Dolo {
  tipico_276: =>O@Giudice FattoTipico
  pena_276:   O(Sanziona) =>O@Giudice ReclusioneAttentatoPresidente
}

atom OffendePresidente: offends the honour or prestige of the President of the Republic (art. 278) | quote: Offese all'onore o al prestigio del presidente della Repubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L3595-L3603
atom ReclusioneOffesaPresidente: reclusion 1-5 years (art. 278) | quote: Offese all'onore o al prestigio del presidente della Repubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L3595-L3603
precetto_278: =>O@Chiunque ~OffendePresidente
OffendePresidente, Dolo {
  tipico_278: =>O@Giudice FattoTipico
  pena_278:   O(Sanziona) =>O@Giudice ReclusioneOffesaPresidente
}

atom AttentatoTerroristico: for terrorism or subversion, attacks the life or safety of a person (art. 280) | quote: Attentato per finalità terroristiche o di eversione | uri: examples/codice_penale/sources/codice_penale_full.md#L3609-L3617
atom ReclusioneAttentatoTerroristico: reclusion not less than 20 years if against life (art. 280) | quote: Attentato per finalità terroristiche o di eversione | uri: examples/codice_penale/sources/codice_penale_full.md#L3609-L3617
precetto_280: =>O@Chiunque ~AttentatoTerroristico
AttentatoTerroristico, FineTerrorismo, Dolo {
  tipico_280: =>O@Giudice FattoTipico
  pena_280:   O(Sanziona) =>O@Giudice ReclusioneAttentatoTerroristico
}

atom SuscitaGuerraCivile: commits a fact apt to stir up civil war in the territory of the State (art. 286) | quote: Chiunque commette un fatto diretto a suscitare la guerra civile nel territorio dello Stato è punito con l'ergastolo | uri: examples/codice_penale/sources/codice_penale_full.md#L3692-L3700
atom ReclusioneGuerraCivile: life imprisonment / long reclusion for civil war (art. 286) | quote: Chiunque commette un fatto diretto a suscitare la guerra civile nel territorio dello Stato è punito con l'ergastolo | uri: examples/codice_penale/sources/codice_penale_full.md#L3692-L3700
precetto_286: =>O@Chiunque ~SuscitaGuerraCivile
SuscitaGuerraCivile, Dolo {
  tipico_286: =>O@Giudice FattoTipico
  pena_286:   O(Sanziona) =>O@Giudice ReclusioneGuerraCivile
}

atom UsurpaPoterePolitico: usurps a political power or military command, or unduly persists in exercising it (art. 287) | quote: Usurpazione di potere politico o di comando militare | uri: examples/codice_penale/sources/codice_penale_full.md#L3701-L3709
atom ReclusioneUsurpazionePotere: reclusion 6-15 years (art. 287) | quote: Usurpazione di potere politico o di comando militare | uri: examples/codice_penale/sources/codice_penale_full.md#L3701-L3709
precetto_287: =>O@Chiunque ~UsurpaPoterePolitico
UsurpaPoterePolitico, Dolo {
  tipico_287: =>O@Giudice FattoTipico
  pena_287:   O(Sanziona) =>O@Giudice ReclusioneUsurpazionePotere
}

atom SequestroTerrorismo: for terrorism or subversion, seizes a person (art. 289-bis) | quote: Sequestro di persona a scopo di terrorismo o di eversione | uri: examples/codice_penale/sources/codice_penale_full.md#L3733-L3741
atom ReclusioneSequestroTerrorismo: reclusion 25-30 years (art. 289-bis) | quote: Sequestro di persona a scopo di terrorismo o di eversione | uri: examples/codice_penale/sources/codice_penale_full.md#L3733-L3741
precetto_289bis: =>O@Chiunque ~SequestroTerrorismo
SequestroTerrorismo, FineTerrorismo, Dolo {
  tipico_289bis: =>O@Giudice FattoTipico
  pena_289bis:   O(Sanziona) =>O@Giudice ReclusioneSequestroTerrorismo
}

atom VilipendeRepubblica: publicly vilifies the Republic, the constitutional institutions or the armed forces (art. 290) | quote: Vilipendio della Repubblica, delle istituzioni costituzionali e delle forze armate | uri: examples/codice_penale/sources/codice_penale_full.md#L3751-L3759
atom ReclusioneVilipendioRepubblica: fine, vilification of the Republic (art. 290) | quote: Vilipendio della Repubblica, delle istituzioni costituzionali e delle forze armate | uri: examples/codice_penale/sources/codice_penale_full.md#L3751-L3759
precetto_290: =>O@Chiunque ~VilipendeRepubblica
VilipendeRepubblica, Dolo {
  tipico_290: =>O@Giudice FattoTipico
  pena_290:   O(Sanziona) =>O@Giudice ReclusioneVilipendioRepubblica
}

atom VilipendeNazione: publicly vilifies the Italian nation (art. 291) | quote: Vilipendio alla nazione italiana | uri: examples/codice_penale/sources/codice_penale_full.md#L3766-L3771
atom ReclusioneVilipendioNazione: fine, vilification of the nation (art. 291) | quote: Vilipendio alla nazione italiana | uri: examples/codice_penale/sources/codice_penale_full.md#L3766-L3771
precetto_291: =>O@Chiunque ~VilipendeNazione
VilipendeNazione, Dolo {
  tipico_291: =>O@Giudice FattoTipico
  pena_291:   O(Sanziona) =>O@Giudice ReclusioneVilipendioNazione
}

atom VilipendeBandiera: vilifies, with outrageous expressions, the flag or another emblem of the State (art. 292) | quote: Vilipendio o danneggiamento alla bandiera o ad altro emblema dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3772-L3780
atom ReclusioneVilipendioBandiera: fine, vilification of the flag (art. 292) | quote: Vilipendio o danneggiamento alla bandiera o ad altro emblema dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3772-L3780
precetto_292: =>O@Chiunque ~VilipendeBandiera
VilipendeBandiera, Dolo {
  tipico_292: =>O@Giudice FattoTipico
  pena_292:   O(Sanziona) =>O@Giudice ReclusioneVilipendioBandiera
}

atom AttentaCapoStatoEstero: in the territory of the State, attacks the life or safety of the head of a foreign State (art. 295) | quote: Attentato contro i Capi di Stati esteri | uri: examples/codice_penale/sources/codice_penale_full.md#L3814-L3822
atom ReclusioneAttentatoEstero: reclusion not less than 10 years (art. 295) | quote: Attentato contro i Capi di Stati esteri | uri: examples/codice_penale/sources/codice_penale_full.md#L3814-L3822
AttentaCapoStatoEstero, Dolo {
  tipico_295: =>O@Giudice FattoTipico
  pena_295:   O(Sanziona) =>O@Giudice ReclusioneAttentatoEstero
}

atom IstigaDelittiStato: instigates someone to commit a crime against the personality of the State punishable with life or reclusion (art. 302) | quote: Istigazione a commettere alcuno dei delitti preveduti dai capi primo e secondo | uri: examples/codice_penale/sources/codice_penale_full.md#L3883-L3891
atom ReclusioneIstigDelittiStato: reclusion 1-8 years (art. 302) | quote: Istigazione a commettere alcuno dei delitti preveduti dai capi primo e secondo | uri: examples/codice_penale/sources/codice_penale_full.md#L3883-L3891
precetto_302: =>O@Chiunque ~IstigaDelittiStato
IstigaDelittiStato, Dolo {
  tipico_302: =>O@Giudice FattoTipico
  pena_302:   O(Sanziona) =>O@Giudice ReclusioneIstigDelittiStato
}

atom AttentaIntegritaStato: commits a fact apt to subject the territory of the State to foreign sovereignty, or to harm its integrity, independence or unity (art. 241) | quote: Attentati contro l'integrità, l'indipendenza o l'unità dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3099-L3107
atom ReclusioneAttentatoIntegrita: reclusion not less than 12 years (art. 241) | quote: Attentati contro l'integrità, l'indipendenza o l'unità dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3099-L3107
precetto_241: =>O@Chiunque ~AttentaIntegritaStato
AttentaIntegritaStato, Dolo {
  tipico_241: =>O@Giudice FattoTipico
  pena_241:   O(Sanziona) =>O@Giudice ReclusioneAttentatoIntegrita
}

atom AttiOstiliStatoEstero: without Government approval, commits hostile acts against a foreign State exposing Italy to the danger of war (art. 244) | quote: Atti ostili verso uno Stato estero, che espongono lo Stato italiano al pericolo di guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3136-L3144
atom ReclusioneAttiOstili: reclusion 6-18 years (art. 244) | quote: Atti ostili verso uno Stato estero, che espongono lo Stato italiano al pericolo di guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3136-L3144
precetto_244: =>O@Chiunque ~AttiOstiliStatoEstero
AttiOstiliStatoEstero, Dolo {
  tipico_244: =>O@Giudice FattoTipico
  pena_244:   O(Sanziona) =>O@Giudice ReclusioneAttiOstili
}

atom CorruzioneDaStraniero: a citizen who, even indirectly, receives money/utility from a foreigner to commit acts harmful to national interests (art. 246) | quote: Corruzione del cittadino da parte dello straniero | uri: examples/codice_penale/sources/codice_penale_full.md#L3156-L3164
atom ReclusioneCorruzioneStraniero: reclusion 3-10 years (art. 246) | quote: Corruzione del cittadino da parte dello straniero | uri: examples/codice_penale/sources/codice_penale_full.md#L3156-L3164
precetto_246: =>O@Chiunque ~CorruzioneDaStraniero
CorruzioneDaStraniero, Dolo {
  tipico_246: =>O@Giudice FattoTipico
  pena_246:   O(Sanziona) =>O@Giudice ReclusioneCorruzioneStraniero
}

atom ProcacciaNotizieSicurezza: obtains news that, in the State's interest, must remain secret (art. 256) | quote: Procacciamento di notizie concernenti la sicurezza dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3257-L3265
atom ReclusioneProcacciamento: reclusion 3-10 years (art. 256) | quote: Procacciamento di notizie concernenti la sicurezza dello Stato | uri: examples/codice_penale/sources/codice_penale_full.md#L3257-L3265
precetto_256: =>O@Chiunque ~ProcacciaNotizieSicurezza
ProcacciaNotizieSicurezza, Dolo {
  tipico_256: =>O@Giudice FattoTipico
  pena_256:   O(Sanziona) =>O@Giudice ReclusioneProcacciamento
}

atom RivelaNotizieVietate: reveals news whose divulgation the competent authority has forbidden (art. 262) | quote: Rivelazione di notizie di cui sia stata vietata la divulgazione | uri: examples/codice_penale/sources/codice_penale_full.md#L3345-L3353
atom ReclusioneNotizieVietate: reclusion not less than 3 years (art. 262) | quote: Rivelazione di notizie di cui sia stata vietata la divulgazione | uri: examples/codice_penale/sources/codice_penale_full.md#L3345-L3353
precetto_262: =>O@Chiunque ~RivelaNotizieVietate
RivelaNotizieVietate, Dolo {
  tipico_262: =>O@Giudice FattoTipico
  pena_262:   O(Sanziona) =>O@Giudice ReclusioneNotizieVietate
}

atom DisfattismoEconomico: in time of war, uses means apt to depress exchange rates or undermine public credit (art. 267) | quote: Disfattismo economico | uri: examples/codice_penale/sources/codice_penale_full.md#L3417-L3425
atom ReclusioneDisfattismoEcon: reclusion not less than 5 years (art. 267) | quote: Disfattismo economico | uri: examples/codice_penale/sources/codice_penale_full.md#L3417-L3425
precetto_267: =>O@Chiunque ~DisfattismoEconomico
DisfattismoEconomico, TempoGuerra, Dolo {
  tipico_267: =>O@Giudice FattoTipico
  pena_267:   O(Sanziona) =>O@Giudice ReclusioneDisfattismoEcon
}

atom OffendeLibertaPresidente: outside art. 276, offends the personal liberty of the President of the Republic (art. 277) | quote: Offesa alla libertà del presidente della Repubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L3589-L3594
atom ReclusioneLibertaPresidente: reclusion 3-10 years (art. 277) | quote: Offesa alla libertà del presidente della Repubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L3589-L3594
OffendeLibertaPresidente, Dolo {
  tipico_277: =>O@Giudice FattoTipico
  pena_277:   O(Sanziona) =>O@Giudice ReclusioneLibertaPresidente
}

atom AttoTerrorismoOrdigni: for terrorism, commits an act apt to damage things by lethal or explosive devices (art. 280-bis) | quote: Atto di terrorismo con ordigni micidiali o esplosivi | uri: examples/codice_penale/sources/codice_penale_full.md#L3629-L3637
atom ReclusioneTerrorismoOrdigni: reclusion 2-5 years (art. 280-bis) | quote: Atto di terrorismo con ordigni micidiali o esplosivi | uri: examples/codice_penale/sources/codice_penale_full.md#L3629-L3637
precetto_280bis: =>O@Chiunque ~AttoTerrorismoOrdigni
AttoTerrorismoOrdigni, FineTerrorismo, Dolo {
  tipico_280bis: =>O@Giudice FattoTipico
  pena_280bis:   O(Sanziona) =>O@Giudice ReclusioneTerrorismoOrdigni
}

atom ArruolamentiNonAutorizzati: in the territory of the State, without Government approval, recruits or arms citizens for service of a foreign State (art. 288) | quote: Arruolamenti o armamenti non autorizzati a servizio di uno Stato estero | uri: examples/codice_penale/sources/codice_penale_full.md#L3713-L3721
atom ReclusioneArruolamentiEstero: reclusion 4-15 years (art. 288) | quote: Arruolamenti o armamenti non autorizzati a servizio di uno Stato estero | uri: examples/codice_penale/sources/codice_penale_full.md#L3713-L3721
precetto_288: =>O@Chiunque ~ArruolamentiNonAutorizzati
ArruolamentiNonAutorizzati, Dolo {
  tipico_288: =>O@Giudice FattoTipico
  pena_288:   O(Sanziona) =>O@Giudice ReclusioneArruolamentiEstero
}

atom OffendeLibertaCapoEstero: in the territory of the State, offends the personal liberty of the head of a foreign State (art. 296) | quote: Offesa alla libertà dei capi di Stati esteri | uri: examples/codice_penale/sources/codice_penale_full.md#L3823-L3831
atom ReclusioneLibertaCapoEstero: reclusion 3-10 years (art. 296) | quote: Offesa alla libertà dei capi di Stati esteri | uri: examples/codice_penale/sources/codice_penale_full.md#L3823-L3831
OffendeLibertaCapoEstero, Dolo {
  tipico_296: =>O@Giudice FattoTipico
  pena_296:   O(Sanziona) =>O@Giudice ReclusioneLibertaCapoEstero
}

atom OffendeBandieraEstera: in the territory of the State, vilifies the flag or emblem of a foreign State, displayed publicly (art. 299) | quote: Offesa alla bandiera o ad altro emblema di uno Stato estero | uri: examples/codice_penale/sources/codice_penale_full.md#L3846-L3853
atom ReclusioneBandieraEstera: fine, offence to a foreign flag (art. 299) | quote: Offesa alla bandiera o ad altro emblema di uno Stato estero | uri: examples/codice_penale/sources/codice_penale_full.md#L3846-L3853
precetto_299: =>O@Chiunque ~OffendeBandieraEstera
OffendeBandieraEstera, Dolo {
  tipico_299: =>O@Giudice FattoTipico
  pena_299:   O(Sanziona) =>O@Giudice ReclusioneBandieraEstera
}

atom AssistenzaCospiratori: outside participation or favouring, gives shelter, food or means to participants in a conspiracy or armed band (art. 307) | quote: Assistenza ai partecipi di cospirazione o di banda armata | uri: examples/codice_penale/sources/codice_penale_full.md#L3934-L3942
atom ReclusioneAssistenzaCospiratori: reclusion up to 2 years (art. 307) | quote: Assistenza ai partecipi di cospirazione o di banda armata | uri: examples/codice_penale/sources/codice_penale_full.md#L3934-L3942
precetto_307: =>O@Chiunque ~AssistenzaCospiratori
AssistenzaCospiratori, Dolo {
  tipico_307: =>O@Giudice FattoTipico
  pena_307:   O(Sanziona) =>O@Giudice ReclusioneAssistenzaCospiratori
}

atom IntelligenzeNeutralita: holds dealings with a foreigner to commit the Italian State to neutrality or war (art. 245) | quote: Intelligenze con lo straniero per impegnare lo Stato italiano alla neutralità o alla guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3148-L3155
atom ReclusioneIntelligenzeNeutralita: reclusion 3-10 years (art. 245) | quote: Intelligenze con lo straniero per impegnare lo Stato italiano alla neutralità o alla guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3148-L3155
precetto_245: =>O@Chiunque ~IntelligenzeNeutralita
IntelligenzeNeutralita, Dolo {
  tipico_245: =>O@Giudice FattoTipico
  pena_245:   O(Sanziona) =>O@Giudice ReclusioneIntelligenzeNeutralita
}

atom PartecipaPrestitiNemico: in time of war, takes part in loans or payments to the enemy (art. 249) | quote: Partecipazione a prestiti a favore del nemico | uri: examples/codice_penale/sources/codice_penale_full.md#L3184-L3190
atom ReclusionePrestitiNemico: reclusion 5-15 years (art. 249) | quote: Partecipazione a prestiti a favore del nemico | uri: examples/codice_penale/sources/codice_penale_full.md#L3184-L3190
precetto_249: =>O@Chiunque ~PartecipaPrestitiNemico
PartecipaPrestitiNemico, TempoGuerra, Dolo {
  tipico_249: =>O@Giudice FattoTipico
  pena_249:   O(Sanziona) =>O@Giudice ReclusionePrestitiNemico
}

atom InadempimentoFornitureGuerra: in time of war, fails wholly or partly to perform a war-supply contract with the State (art. 251) | quote: Inadempimento di contratti di forniture in tempo di guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3200-L3208
atom ReclusioneFornitureGuerra: reclusion 2-10 years and fine (art. 251) | quote: Inadempimento di contratti di forniture in tempo di guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3200-L3208
precetto_251: =>O@Chiunque ~InadempimentoFornitureGuerra
InadempimentoFornitureGuerra, TempoGuerra, Dolo {
  tipico_251: =>O@Giudice FattoTipico
  pena_251:   O(Sanziona) =>O@Giudice ReclusioneFornitureGuerra
}

atom FrodeFornitureGuerra: in time of war, commits fraud in the performance of war-supply contracts (art. 252) | quote: Frode in forniture in tempo di guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3215-L3222
atom ReclusioneFrodeForniture2: reclusion not less than 10 years (art. 252) | quote: Frode in forniture in tempo di guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3215-L3222
precetto_252: =>O@Chiunque ~FrodeFornitureGuerra
FrodeFornitureGuerra, TempoGuerra, Dolo {
  tipico_252: =>O@Giudice FattoTipico
  pena_252:   O(Sanziona) =>O@Giudice ReclusioneFrodeForniture2
}

atom SpionaggioNotizieVietate: for espionage, obtains news whose divulgation the authority has forbidden (art. 258) | quote: Spionaggio di notizie di cui è stata vietata la divulgazione | uri: examples/codice_penale/sources/codice_penale_full.md#L3287-L3295
atom ReclusioneSpionaggioVietate: reclusion not less than 3 years (art. 258) | quote: Spionaggio di notizie di cui è stata vietata la divulgazione | uri: examples/codice_penale/sources/codice_penale_full.md#L3287-L3295
precetto_258: =>O@Chiunque ~SpionaggioNotizieVietate
SpionaggioNotizieVietate, Dolo {
  tipico_258: =>O@Giudice FattoTipico
  pena_258:   O(Sanziona) =>O@Giudice ReclusioneSpionaggioVietate
}

atom IntroduzioneLuoghiMilitari: clandestinely enters military places, or is found in unjustified possession of means of espionage (art. 260) | quote: Introduzione clandestina in luoghi militari e possesso ingiustificato di mezzi di spionaggio | uri: examples/codice_penale/sources/codice_penale_full.md#L3312-L3320
atom ReclusioneLuoghiMilitari: reclusion 1-5 years (art. 260) | quote: Introduzione clandestina in luoghi militari e possesso ingiustificato di mezzi di spionaggio | uri: examples/codice_penale/sources/codice_penale_full.md#L3312-L3320
precetto_260: =>O@Chiunque ~IntroduzioneLuoghiMilitari
IntroduzioneLuoghiMilitari, Dolo {
  tipico_260: =>O@Giudice FattoTipico
  pena_260:   O(Sanziona) =>O@Giudice ReclusioneLuoghiMilitari
}

atom AssistenzaTerroristi: outside participation or favouring, gives shelter, food or means to members of terrorist/subversive associations (art. 270-ter) | quote: Assistenza agli associati | uri: examples/codice_penale/sources/codice_penale_full.md#L3477-L3485
atom FuoriConcorso: did not take part in the association's crimes (art. 270-ter) | quote: Assistenza agli associati | uri: examples/codice_penale/sources/codice_penale_full.md#L3477-L3485
atom ReclusioneAssistenzaTerroristi: reclusion up to 4 years (art. 270-ter) | quote: Assistenza agli associati | uri: examples/codice_penale/sources/codice_penale_full.md#L3477-L3485
precetto_270ter: =>O@Chiunque ~AssistenzaTerroristi
AssistenzaTerroristi, FuoriConcorso, Dolo {
  tipico_270ter: =>O@Giudice FattoTipico
  pena_270ter:   O(Sanziona) =>O@Giudice ReclusioneAssistenzaTerroristi
}
