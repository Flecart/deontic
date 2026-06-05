# Codice Penale — DELITTI CONTRO LA PUBBLICA AMMINISTRAZIONE (artt. 314-337).
# ===========================================================================
# Peculato, corruzione, abuso d'ufficio, violenza/resistenza a pubblico
# ufficiale. Soggetto qualificato CONDIVISO `QualificaPubblica` (definizioni).
# Il peculato riusa `SiAppropria` (come l'appropriazione indebita); 336/337
# riusano `Violenza`/`Minaccia`.
from definizioni.ddl import *

facts:

atom PossessoPerUfficio:    the agent had possession or availability of the money/thing by reason of office or service (art. 314) | quote: avendo per ragione del suo ufficio o servizio il possesso o comunque la disponibilità di danaro o di altra cosa mobile altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L4700-L4708
atom RiceveUtilitaNonDovuta: the official receives, for self or a third party, money or other undue benefit, or accepts the promise of it (artt. 318, 319) | quote: riceve, per sé o per un terzo, in denaro od altra utilità, una retribuzione che non gli è dovuta, o ne accetta la promessa | uri: examples/codice_penale/sources/codice_penale_full.md#L4760-L4768
atom PerAttoUfficio:        the bribe is for performing an act OF the office (corruzione propria impropria, art. 318) | quote: per compiere un atto del suo ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L4760-L4768
atom PerAttoContrarioDoveri: the bribe is for omitting/delaying or performing an act CONTRARY to official duties (art. 319) | quote: per omettere o ritardare … ovvero per compiere … un atto contrario ai doveri di ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L4790-L4798
atom ViolazioneNorme:       acting in the functions, in breach of statute or regulation, or failing to abstain in conflict of interest (art. 323) | quote: in violazione di norme di legge o di regolamento, ovvero omettendo di astenersi in presenza di un interesse proprio | uri: examples/codice_penale/sources/codice_penale_full.md#L4840-L4848
atom IngiustoVantaggioODanno: the agent intentionally procures an unjust advantage to self/others or an unjust harm to another (art. 323) | quote: intenzionalmente procura a sé o ad altri un ingiusto vantaggio … ovvero arreca ad altri un danno ingiusto | uri: examples/codice_penale/sources/codice_penale_full.md#L4840-L4852
atom ControPubblicoUfficiale: the violence or threat is directed at a public official or person charged with a public service (artt. 336-337) | quote: usa violenza o minaccia a un pubblico ufficiale o ad un incaricato di un pubblico servizio | uri: examples/codice_penale/sources/codice_penale_full.md#L5040-L5048
atom PerCostringereAtto:    in order to compel the official to do an act contrary to duty, or to omit an official act (art. 336) | quote: per costringerlo a fare un atto contrario ai propri doveri, o ad omettere un atto dell'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L5040-L5048
atom PerOpporsiAtto:        in order to oppose the official while performing an official act (art. 337) | quote: per opporsi a un pubblico ufficiale … mentre compie un atto d'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L5070-L5078
atom ReclusionePeculato:    penalty: reclusion 3-10 years (art. 314) | quote: è punito con la reclusione da tre a dieci anni | uri: examples/codice_penale/sources/codice_penale_full.md#L4700-L4708
atom ReclusioneCorruzione318: penalty: reclusion 6 months-3 years (art. 318) | quote: è punito con la reclusione da sei mesi a tre anni | uri: examples/codice_penale/sources/codice_penale_full.md#L4760-L4768
atom ReclusioneCorruzione319: penalty: reclusion 2-5 years (art. 319) | quote: è punito con la reclusione da due a cinque anni | uri: examples/codice_penale/sources/codice_penale_full.md#L4790-L4798
atom ReclusioneAbuso:       penalty: reclusion (art. 323, residual — "salvo che il fatto non costituisca un più grave reato") | quote: il pubblico ufficiale … intenzionalmente procura a sé o ad altri un ingiusto vantaggio | uri: examples/codice_penale/sources/codice_penale_full.md#L4840-L4852
atom ReclusioneViolenzaPU:  penalty: reclusion 6 months-5 years (art. 336) | quote: è punito con la reclusione da sei mesi a cinque anni | uri: examples/codice_penale/sources/codice_penale_full.md#L5040-L5048
atom ReclusioneResistenza:  penalty: reclusion 6 months-5 years (art. 337) | quote: è punito con la reclusione da sei mesi a cinque anni | uri: examples/codice_penale/sources/codice_penale_full.md#L5070-L5078

# Precetti
precetto_314: =>O@Chiunque ~SiAppropria
precetto_318: =>O@Chiunque ~RiceveUtilitaNonDovuta
precetto_323: =>O@Chiunque ~IngiustoVantaggioODanno
precetto_336: =>O@Chiunque ~ControPubblicoUfficiale
precetto_337: =>O@Chiunque ~PerOpporsiAtto

# Peculato (314): il PU, possedendo per ufficio, si appropria della cosa.
QualificaPubblica, PossessoPerUfficio, SiAppropria, Dolo {
  tipico_314: =>O@Giudice FattoTipico
  pena_314:   O(Sanziona) =>O@Giudice ReclusionePeculato
}

# Corruzione (318 per atto d'ufficio / 319 per atto contrario): il PU riceve
# un'utilità non dovuta. L'elemento distintivo è il TIPO di atto.
QualificaPubblica, RiceveUtilitaNonDovuta, Dolo {
  tipico_318: PerAttoUfficio =>O@Giudice FattoTipico
  tipico_319: PerAttoContrarioDoveri =>O@Giudice FattoTipico
  pena_318:   PerAttoUfficio, O(Sanziona) =>O@Giudice ReclusioneCorruzione318
  pena_319:   PerAttoContrarioDoveri, O(Sanziona) =>O@Giudice ReclusioneCorruzione319
}

# Abuso d'ufficio (323): il PU, in violazione di norme, procura intenzionalmente
# un vantaggio ingiusto o un danno ingiusto.
QualificaPubblica, ViolazioneNorme, IngiustoVantaggioODanno, Dolo {
  tipico_323: =>O@Giudice FattoTipico
  pena_323:   O(Sanziona) =>O@Giudice ReclusioneAbuso
}

# Violenza/minaccia (336) e resistenza (337) a pubblico ufficiale: usa violenza
# o minaccia (condivise) verso il PU, per costringerlo / per opporsi.
oneof[Violenza, Minaccia], ControPubblicoUfficiale, Dolo {
  tipico_336: PerCostringereAtto =>O@Giudice FattoTipico
  tipico_337: PerOpporsiAtto =>O@Giudice FattoTipico
  pena_336:   PerCostringereAtto, O(Sanziona) =>O@Giudice ReclusioneViolenzaPU
  pena_337:   PerOpporsiAtto, O(Sanziona) =>O@Giudice ReclusioneResistenza
}
