# Codice Penale — economia (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom DistruggeMateriePrime: destroys raw materials, agricultural/industrial products or means of production, causing serious harm to national production (art. 499) | quote: Distruzione di materie prime o di prodotti agricoli o industriali, ovvero di mezzi di produzione | uri: examples/codice_penale/sources/codice_penale_full.md#L6663-L6671
atom ReclusioneDistruzioneMaterie: reclusion 1-5 years (art. 499) | quote: Distruzione di materie prime o di prodotti agricoli o industriali, ovvero di mezzi di produzione | uri: examples/codice_penale/sources/codice_penale_full.md#L6663-L6671
precetto_499: =>O@Chiunque ~DistruggeMateriePrime
DistruggeMateriePrime, Dolo {
  tipico_499: =>O@Giudice FattoTipico
  pena_499:   O(Sanziona) =>O@Giudice ReclusioneDistruzioneMaterie
}

atom DiffondeMalattiaPianteAnimali: causes the spread of a plant or animal disease dangerous to the national economy (art. 500) | quote: Diffusione di una malattia delle piante o degli animali | uri: examples/codice_penale/sources/codice_penale_full.md#L6672-L6680
atom ReclusioneMalattiaPiante: reclusion 1-5 years (art. 500) | quote: Diffusione di una malattia delle piante o degli animali | uri: examples/codice_penale/sources/codice_penale_full.md#L6672-L6680
precetto_500: =>O@Chiunque ~DiffondeMalattiaPianteAnimali
DiffondeMalattiaPianteAnimali, Dolo {
  tipico_500: =>O@Giudice FattoTipico
  pena_500:   O(Sanziona) =>O@Giudice ReclusioneMalattiaPiante
}

atom ManipolaPrezziMercato: spreads false news or uses fraudulent means to cause a rise or fall in prices on the public market or exchanges (art. 501) | quote: Rialzo e ribasso fraudolento di prezzi sul pubblico mercato o nelle borse di commercio | uri: examples/codice_penale/sources/codice_penale_full.md#L6681-L6689
atom FineTurbareMercato: in order to disturb the internal market of securities or goods (art. 501) | quote: Rialzo e ribasso fraudolento di prezzi sul pubblico mercato o nelle borse di commercio | uri: examples/codice_penale/sources/codice_penale_full.md#L6681-L6689
atom ReclusioneAggiotaggio: reclusion up to 3 years and fine (art. 501) | quote: Rialzo e ribasso fraudolento di prezzi sul pubblico mercato o nelle borse di commercio | uri: examples/codice_penale/sources/codice_penale_full.md#L6681-L6689
precetto_501: =>O@Chiunque ~ManipolaPrezziMercato
ManipolaPrezziMercato, FineTurbareMercato, Dolo {
  tipico_501: =>O@Giudice FattoTipico
  pena_501:   O(Sanziona) =>O@Giudice ReclusioneAggiotaggio
}

atom InvadeOccupaAzienda: arbitrarily invades or occupies another's agricultural or industrial enterprise, or sabotages it (art. 508) | quote: Arbitraria invasione e occupazione di aziende agricole o industriali | uri: examples/codice_penale/sources/codice_penale_full.md#L6803-L6811
atom ScopoImpedireLavoro: with the sole aim of impeding or disturbing the normal course of work (art. 508) | quote: Arbitraria invasione e occupazione di aziende agricole o industriali | uri: examples/codice_penale/sources/codice_penale_full.md#L6803-L6811
atom ReclusioneInvasioneAzienda: reclusion 3-7 years (art. 508) | quote: Arbitraria invasione e occupazione di aziende agricole o industriali | uri: examples/codice_penale/sources/codice_penale_full.md#L6803-L6811
precetto_508: =>O@Chiunque ~InvadeOccupaAzienda
InvadeOccupaAzienda, ScopoImpedireLavoro, Dolo {
  tipico_508: =>O@Giudice FattoTipico
  pena_508:   O(Sanziona) =>O@Giudice ReclusioneInvasioneAzienda
}

atom TurbaEsercizioIndustria: uses violence on things or fraudulent means to impede or disturb the exercise of an industry or trade (art. 513) | quote: Turbata libertà dell'industria o del commercio | uri: examples/codice_penale/sources/codice_penale_full.md#L6851-L6858
atom ReclusioneTurbataIndustria: reclusion up to 2 years and fine (art. 513) | quote: Turbata libertà dell'industria o del commercio | uri: examples/codice_penale/sources/codice_penale_full.md#L6851-L6858
precetto_513: =>O@Chiunque ~TurbaEsercizioIndustria
TurbaEsercizioIndustria, Dolo {
  tipico_513: =>O@Giudice FattoTipico
  pena_513:   O(Sanziona) =>O@Giudice ReclusioneTurbataIndustria
}

atom AttiConcorrenzaIllecita: in a commercial/industrial activity, performs acts of unlawful competition (art. 513-bis) | quote: Illecita concorrenza con minaccia o violenza | uri: examples/codice_penale/sources/codice_penale_full.md#L6859-L6867
atom ReclusioneConcorrenzaIllecita: reclusion 2-6 years (art. 513-bis) | quote: Illecita concorrenza con minaccia o violenza | uri: examples/codice_penale/sources/codice_penale_full.md#L6859-L6867
precetto_513bis: =>O@Chiunque ~AttiConcorrenzaIllecita
oneof[Violenza, Minaccia], AttiConcorrenzaIllecita, Dolo {
  tipico_513bis: =>O@Giudice FattoTipico
  pena_513bis:   O(Sanziona) =>O@Giudice ReclusioneConcorrenzaIllecita
}

atom ConsegnaAliudProQuo: in trade, delivers to the buyer a movable thing different in origin, provenance, quality or quantity from that declared or agreed (art. 515) | quote: Frode nell'esercizio del commercio | uri: examples/codice_penale/sources/codice_penale_full.md#L6880-L6888
atom ReclusioneFrodeCommercio: reclusion up to 2 years or fine (art. 515) | quote: Frode nell'esercizio del commercio | uri: examples/codice_penale/sources/codice_penale_full.md#L6880-L6888
precetto_515: =>O@Chiunque ~ConsegnaAliudProQuo
ConsegnaAliudProQuo, Dolo {
  tipico_515: =>O@Giudice FattoTipico
  pena_515:   O(Sanziona) =>O@Giudice ReclusioneFrodeCommercio
}

atom VendeAlimentiNonGenuini: offers for sale or markets as genuine food substances that are not genuine (art. 516) | quote: Vendita di sostanze alimentari non genuine come genuine | uri: examples/codice_penale/sources/codice_penale_full.md#L6892-L6896
atom ReclusioneVenditaNonGenuini: reclusion up to 6 months or fine (art. 516) | quote: Vendita di sostanze alimentari non genuine come genuine | uri: examples/codice_penale/sources/codice_penale_full.md#L6892-L6896
precetto_516: =>O@Chiunque ~VendeAlimentiNonGenuini
VendeAlimentiNonGenuini, Dolo {
  tipico_516: =>O@Giudice FattoTipico
  pena_516:   O(Sanziona) =>O@Giudice ReclusioneVenditaNonGenuini
}

atom VendeProdottiSegniMendaci: offers for sale industrial products with names/marks apt to mislead the buyer on origin or quality (art. 517) | quote: Vendita di prodotti industriali con segni mendaci | uri: examples/codice_penale/sources/codice_penale_full.md#L6897-L6905
atom ReclusioneSegniMendaci: reclusion up to 2 years or fine (art. 517) | quote: Vendita di prodotti industriali con segni mendaci | uri: examples/codice_penale/sources/codice_penale_full.md#L6897-L6905
precetto_517: =>O@Chiunque ~VendeProdottiSegniMendaci
VendeProdottiSegniMendaci, Dolo {
  tipico_517: =>O@Giudice FattoTipico
  pena_517:   O(Sanziona) =>O@Giudice ReclusioneSegniMendaci
}

atom ManovreSpeculativeMerci: in a productive/commercial activity, carries out speculative manoeuvres or hoards essential goods, causing scarcity or price rises (art. 501-bis) | quote: Manovre speculative su merci | uri: examples/codice_penale/sources/codice_penale_full.md#L6704-L6712
atom ReclusioneManovreSpeculative: reclusion 6 months-3 years and fine (art. 501-bis) | quote: Manovre speculative su merci | uri: examples/codice_penale/sources/codice_penale_full.md#L6704-L6712
precetto_501bis: =>O@Chiunque ~ManovreSpeculativeMerci
ManovreSpeculativeMerci, Dolo {
  tipico_501bis: =>O@Giudice FattoTipico
  pena_501bis:   O(Sanziona) =>O@Giudice ReclusioneManovreSpeculative
}

atom FrodiIndustrieNazionali: selling on national or foreign markets industrial products with counterfeit marks, harms the national industry (art. 514) | quote: Frodi contro le industrie nazionali | uri: examples/codice_penale/sources/codice_penale_full.md#L6868-L6876
atom ReclusioneFrodiIndustrie: reclusion 1-5 years and fine (art. 514) | quote: Frodi contro le industrie nazionali | uri: examples/codice_penale/sources/codice_penale_full.md#L6868-L6876
precetto_514: =>O@Chiunque ~FrodiIndustrieNazionali
FrodiIndustrieNazionali, Dolo {
  tipico_514: =>O@Giudice FattoTipico
  pena_514:   O(Sanziona) =>O@Giudice ReclusioneFrodiIndustrie
}

atom Boicottaggio: for the aims of arts. 502-505, by propaganda or use of force/authority, induces a boycott harming an industry/trade (art. 507) | quote: Chiunque, per uno degli scopi indicati negli articoli 502, 503, 504 e 505, mediante propaganda o valendosi della forza | uri: examples/codice_penale/sources/codice_penale_full.md#L6789-L6797
atom ReclusioneBoicottaggio: reclusion 6 months-3 years (art. 507) | quote: Chiunque, per uno degli scopi indicati negli articoli 502, 503, 504 e 505, mediante propaganda o valendosi della forza | uri: examples/codice_penale/sources/codice_penale_full.md#L6789-L6797
precetto_507: =>O@Chiunque ~Boicottaggio
Boicottaggio, Dolo {
  tipico_507: =>O@Giudice FattoTipico
  pena_507:   O(Sanziona) =>O@Giudice ReclusioneBoicottaggio
}
