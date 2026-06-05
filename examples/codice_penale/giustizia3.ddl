# Codice Penale — giustizia3 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom RifiutaUfficioDovuto: appointed by the judicial authority as expert, interpreter or custodian, obtains exemption by false pretexts, or refuses to give the required service (art. 366) | quote: Rifiuto di uffici legalmente dovuti | uri: examples/codice_penale/sources/codice_penale_full.md#L4855-L4863
atom ReclusioneRifiutoUffici: reclusion up to 6 months or fine (art. 366) | quote: Rifiuto di uffici legalmente dovuti | uri: examples/codice_penale/sources/codice_penale_full.md#L4855-L4863
precetto_366: =>O@Chiunque ~RifiutaUfficioDovuto
RifiutaUfficioDovuto, Dolo {
  tipico_366: =>O@Giudice FattoTipico
  pena_366:   O(Sanziona) =>O@Giudice ReclusioneRifiutoUffici
}

atom PatrocinioInfedele: the defence lawyer or technical consultant, being unfaithful to their professional duties, harms the party they assist (art. 380) | quote: Patrocinio o consulenza infedele | uri: examples/codice_penale/sources/codice_penale_full.md#L5110-L5118
atom ReclusionePatrocinioInfedele: reclusion 1-3 years and fine (art. 380) | quote: Patrocinio o consulenza infedele | uri: examples/codice_penale/sources/codice_penale_full.md#L5110-L5118
precetto_380: =>O@Chiunque ~PatrocinioInfedele
PatrocinioInfedele, Dolo {
  tipico_380: =>O@Giudice FattoTipico
  pena_380:   O(Sanziona) =>O@Giudice ReclusionePatrocinioInfedele
}

atom Evade: being legally arrested or detained for a crime, escapes (art. 385) | quote: Chiunque, essendo legalmente arrestato o detenuto per un reato, evade è punito con la reclusione da sei mesi ad un anno | uri: examples/codice_penale/sources/codice_penale_full.md#L5193-L5201
atom ReclusioneEvasione: reclusion 6 months-3 years (art. 385) | quote: Chiunque, essendo legalmente arrestato o detenuto per un reato, evade è punito con la reclusione da sei mesi ad un anno | uri: examples/codice_penale/sources/codice_penale_full.md#L5193-L5201
precetto_385: =>O@Chiunque ~Evade
Evade, Dolo {
  tipico_385: =>O@Giudice FattoTipico
  pena_385:   O(Sanziona) =>O@Giudice ReclusioneEvasione
}

atom ProcuraEvasione: procures or facilitates the escape of a person legally arrested or detained (art. 386) | quote: Procurata evasione | uri: examples/codice_penale/sources/codice_penale_full.md#L5215-L5223
atom ReclusioneProcurataEvasione: reclusion 6 months-5 years (art. 386) | quote: Procurata evasione | uri: examples/codice_penale/sources/codice_penale_full.md#L5215-L5223
precetto_386: =>O@Chiunque ~ProcuraEvasione
ProcuraEvasione, Dolo {
  tipico_386: =>O@Giudice FattoTipico
  pena_386:   O(Sanziona) =>O@Giudice ReclusioneProcurataEvasione
}

atom NonEsegueProvvedimentoGiudice: to evade a judge's measure, performs fraudulent acts on their own or others' goods, or otherwise fails to comply (art. 388) | quote: Mancata esecuzione dolosa di un provvedimento del giudice | uri: examples/codice_penale/sources/codice_penale_full.md#L5245-L5253
atom ReclusioneMancataEsecuzione: reclusion up to 3 years or fine, a querela (art. 388) | quote: Mancata esecuzione dolosa di un provvedimento del giudice | uri: examples/codice_penale/sources/codice_penale_full.md#L5245-L5253
precetto_388: =>O@Chiunque ~NonEsegueProvvedimentoGiudice
NonEsegueProvvedimentoGiudice, Dolo {
  proc_388:   Querela =>O@Giudice Procedibile
  tipico_388: O(Procedibile) =>O@Giudice FattoTipico
  pena_388:   O(Sanziona) =>O@Giudice ReclusioneMancataEsecuzione
}

atom ProcuraInosservanzaPena: outside participation, helps someone evade the execution of a penalty (art. 390) | quote: Procurata inosservanza di pena | uri: examples/codice_penale/sources/codice_penale_full.md#L5303-L5311
atom ReclusioneProcurataInosservanza: reclusion up to 3 years (art. 390) | quote: Procurata inosservanza di pena | uri: examples/codice_penale/sources/codice_penale_full.md#L5303-L5311
precetto_390: =>O@Chiunque ~ProcuraInosservanzaPena
ProcuraInosservanzaPena, Dolo {
  tipico_390: =>O@Giudice FattoTipico
  pena_390:   O(Sanziona) =>O@Giudice ReclusioneProcurataInosservanza
}

atom EsercizioArbitrarioCose: to exercise a claimed right, where they could resort to the judge, arbitrarily does justice using violence on things (art. 392) | quote: Esercizio arbitrario delle proprie ragioni con violenza sulle cose | uri: examples/codice_penale/sources/codice_penale_full.md#L5330-L5338
atom ReclusioneEsercizioArbCose: fine, a querela (art. 392) | quote: Esercizio arbitrario delle proprie ragioni con violenza sulle cose | uri: examples/codice_penale/sources/codice_penale_full.md#L5330-L5338
precetto_392: =>O@Chiunque ~EsercizioArbitrarioCose
EsercizioArbitrarioCose, Dolo {
  proc_392:   Querela =>O@Giudice Procedibile
  tipico_392: O(Procedibile) =>O@Giudice FattoTipico
  pena_392:   O(Sanziona) =>O@Giudice ReclusioneEsercizioArbCose
}

atom EsercizioArbitrarioPersone: to exercise a claimed right, where they could resort to the judge, arbitrarily does justice using violence or threat to persons (art. 393) | quote: Esercizio arbitrario delle proprie ragioni con violenza alle persone | uri: examples/codice_penale/sources/codice_penale_full.md#L5349-L5357
atom ReclusioneEsercizioArbPersone: reclusion up to 1 year, a querela (art. 393) | quote: Esercizio arbitrario delle proprie ragioni con violenza alle persone | uri: examples/codice_penale/sources/codice_penale_full.md#L5349-L5357
precetto_393: =>O@Chiunque ~EsercizioArbitrarioPersone
EsercizioArbitrarioPersone, Dolo {
  proc_393:   Querela =>O@Giudice Procedibile
  tipico_393: O(Procedibile) =>O@Giudice FattoTipico
  pena_393:   O(Sanziona) =>O@Giudice ReclusioneEsercizioArbPersone
}

atom RivelaSegretiProcedimento: reveals secret news concerning a criminal proceeding, covered by secrecy (art. 379-bis) | quote: Rivelazione di segreti inerenti a un procedimento penale | uri: examples/codice_penale/sources/codice_penale_full.md#L5100-L5108
atom ReclusioneSegretiProcedimento: reclusion up to 3 years (art. 379-bis) | quote: Rivelazione di segreti inerenti a un procedimento penale | uri: examples/codice_penale/sources/codice_penale_full.md#L5100-L5108
precetto_379bis: =>O@Chiunque ~RivelaSegretiProcedimento
RivelaSegretiProcedimento, Dolo {
  tipico_379bis: =>O@Giudice FattoTipico
  pena_379bis:   O(Sanziona) =>O@Giudice ReclusioneSegretiProcedimento
}

atom ColpaCustode: charged by office with the custody of an arrested person, by negligence allows their escape (art. 387) | quote: Colpa del custode | uri: examples/codice_penale/sources/codice_penale_full.md#L5235-L5243
atom ReclusioneColpaCustode: reclusion up to 1 year, negligent custody (art. 387) | quote: Colpa del custode | uri: examples/codice_penale/sources/codice_penale_full.md#L5235-L5243
precetto_387: =>O@Chiunque ~ColpaCustode
ColpaCustode, Colpa {
  tipico_387: =>O@Giudice FattoTipico
  pena_387:   O(Sanziona) =>O@Giudice ReclusioneColpaCustode
}

atom ProcuraInosservanzaMisure: procures or facilitates the escape of a person held under a detentive security measure (art. 391) | quote: Procurata inosservanza di misure di sicurezza detentive | uri: examples/codice_penale/sources/codice_penale_full.md#L5316-L5324
atom ReclusioneInosservanzaMisure: reclusion up to 3 years (art. 391) | quote: Procurata inosservanza di misure di sicurezza detentive | uri: examples/codice_penale/sources/codice_penale_full.md#L5316-L5324
precetto_391: =>O@Chiunque ~ProcuraInosservanzaMisure
ProcuraInosservanzaMisure, Dolo {
  tipico_391: =>O@Giudice FattoTipico
  pena_391:   O(Sanziona) =>O@Giudice ReclusioneInosservanzaMisure
}

atom InduceNonRendereDichiarazioni: induces a person called to make declarations to the judicial authority to stay silent or lie (art. 377-bis) | quote: Induzione a non rendere dichiarazioni o a rendere dichiarazioni mendaci all'autorità giudiziaria | uri: examples/codice_penale/sources/codice_penale_full.md#L5056-L5064
atom ReclusioneInduzioneDichiarazioni: reclusion 2-6 years (art. 377-bis) | quote: Induzione a non rendere dichiarazioni o a rendere dichiarazioni mendaci all'autorità giudiziaria | uri: examples/codice_penale/sources/codice_penale_full.md#L5056-L5064
precetto_377bis: =>O@Chiunque ~InduceNonRendereDichiarazioni
oneof[Violenza, Minaccia], InduceNonRendereDichiarazioni, Dolo {
  tipico_377bis: =>O@Giudice FattoTipico
  pena_377bis:   O(Sanziona) =>O@Giudice ReclusioneInduzioneDichiarazioni
}

atom FalseInfoPM: in a criminal proceeding, when asked by the public prosecutor for information, gives false statements or stays silent (art. 371-bis) | quote: False informazioni al pubblico ministero | uri: examples/codice_penale/sources/codice_penale_full.md#L4934-L4942
atom ReclusioneFalseInfoPM: reclusion up to 4 years (art. 371-bis) | quote: False informazioni al pubblico ministero | uri: examples/codice_penale/sources/codice_penale_full.md#L4934-L4942
precetto_371bis: =>O@Chiunque ~FalseInfoPM
FalseInfoPM, Dolo {
  tipico_371bis: =>O@Giudice FattoTipico
  pena_371bis:   O(Sanziona) =>O@Giudice ReclusioneFalseInfoPM
}

atom FalseAttestazioniGiudiziarie: makes false declarations or attestations in acts destined for the judicial authority (art. 374-bis) | quote: False dichiarazioni o attestazioni in atti destinati all'autorità giudiziaria | uri: examples/codice_penale/sources/codice_penale_full.md#L5000-L5008
atom ReclusioneFalseAttestazioni: reclusion 1-5 years (art. 374-bis) | quote: False dichiarazioni o attestazioni in atti destinati all'autorità giudiziaria | uri: examples/codice_penale/sources/codice_penale_full.md#L5000-L5008
precetto_374bis: =>O@Chiunque ~FalseAttestazioniGiudiziarie
FalseAttestazioniGiudiziarie, Dolo {
  tipico_374bis: =>O@Giudice FattoTipico
  pena_374bis:   O(Sanziona) =>O@Giudice ReclusioneFalseAttestazioni
}

atom MancataEsecuzioneSanzioni: to evade the execution of pecuniary sanctions, performs fraudulent acts on their own goods (art. 388-ter) | quote: Mancata esecuzione dolosa di sanzioni pecuniarie | uri: examples/codice_penale/sources/codice_penale_full.md#L5286-L5293
atom ReclusioneMancataEsecSanzioni: reclusion up to 3 years or fine (art. 388-ter) | quote: Mancata esecuzione dolosa di sanzioni pecuniarie | uri: examples/codice_penale/sources/codice_penale_full.md#L5286-L5293
precetto_388ter: =>O@Chiunque ~MancataEsecuzioneSanzioni
MancataEsecuzioneSanzioni, Dolo {
  tipico_388ter: =>O@Giudice FattoTipico
  pena_388ter:   O(Sanziona) =>O@Giudice ReclusioneMancataEsecSanzioni
}

atom InosservanzaPeneAccessorie: having a conviction entailing an accessory penalty, transgresses its obligations (art. 389) | quote: Inosservanza di pene accessorie | uri: examples/codice_penale/sources/codice_penale_full.md#L5294-L5302
atom ReclusioneInosservanzaPene: reclusion up to 2 years or fine (art. 389) | quote: Inosservanza di pene accessorie | uri: examples/codice_penale/sources/codice_penale_full.md#L5294-L5302
precetto_389: =>O@Chiunque ~InosservanzaPeneAccessorie
InosservanzaPeneAccessorie, Dolo {
  tipico_389: =>O@Giudice FattoTipico
  pena_389:   O(Sanziona) =>O@Giudice ReclusioneInosservanzaPene
}

atom OmetteDenunciaIncaricato: omits or delays to denounce to the authority a crime known by reason of their service (art. 362) | quote: Omessa denuncia da parte di un incaricato di pubblico servizio | uri: examples/codice_penale/sources/codice_penale_full.md#L4815-L4823
atom ReclusioneOmessaDenunciaIncaricato: fine, omitted denunciation by a public-service agent (art. 362) | quote: Omessa denuncia da parte di un incaricato di pubblico servizio | uri: examples/codice_penale/sources/codice_penale_full.md#L4815-L4823
precetto_362: =>O@Chiunque ~QualificaPubblica
QualificaPubblica, OmetteDenunciaIncaricato, Dolo {
  tipico_362: =>O@Giudice FattoTipico
  pena_362:   O(Sanziona) =>O@Giudice ReclusioneOmessaDenunciaIncaricato
}

atom FalseDichiarazioniDifensore: when asked by the defence lawyer for information for investigative purposes, gives false statements (art. 371-ter) | quote: False dichiarazioni al difensore | uri: examples/codice_penale/sources/codice_penale_full.md#L4950-L4958
atom ReclusioneFalseDichDifensore: reclusion up to 4 years (art. 371-ter) | quote: False dichiarazioni al difensore | uri: examples/codice_penale/sources/codice_penale_full.md#L4950-L4958
precetto_371ter: =>O@Chiunque ~FalseDichiarazioniDifensore
FalseDichiarazioniDifensore, Dolo {
  tipico_371ter: =>O@Giudice FattoTipico
  pena_371ter:   O(Sanziona) =>O@Giudice ReclusioneFalseDichDifensore
}

atom ColpaCustodiaPignoramento: charged with custody of things under attachment, by negligence allows their loss or damage (art. 388-bis) | quote: Violazione colposa dei doveri inerenti alla custodia di cose sottoposte a pignoramento ovvero a sequestro giudiziario o | uri: examples/codice_penale/sources/codice_penale_full.md#L5277-L5285
atom ReclusioneColpaPignoramento: reclusion up to 1 year or fine (art. 388-bis) | quote: Violazione colposa dei doveri inerenti alla custodia di cose sottoposte a pignoramento ovvero a sequestro giudiziario o | uri: examples/codice_penale/sources/codice_penale_full.md#L5277-L5285
precetto_388bis: =>O@Chiunque ~ColpaCustodiaPignoramento
ColpaCustodiaPignoramento, Colpa {
  tipico_388bis: =>O@Giudice FattoTipico
  pena_388bis:   O(Sanziona) =>O@Giudice ReclusioneColpaPignoramento
}
