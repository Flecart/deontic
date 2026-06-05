# Codice Penale — DELITTI CONTRO LA FEDE PUBBLICA (artt. 479, 481, 485, 494).
# ===========================================================================
# Falsità ideologica del PU, falsità in certificati, falsità in scrittura
# privata, sostituzione di persona. Riusa `QualificaPubblica`, `AttestaFalso`,
# `FineVantaggioODanno` (definizioni).
from definizioni.ddl import *

facts:

atom AttoNelleFunzioni:    the agent is receiving or forming an act in the exercise of their functions (art. 479) | quote: ricevendo o formando un atto nell'esercizio delle sue funzioni | uri: examples/codice_penale/sources/codice_penale_full.md#L6386-L6394
atom ServizioPubblicaNecessita: the agent exercises a health/legal profession or another service of public necessity (art. 481) | quote: nell'esercizio di una professione sanitaria o forense, o di un altro servizio di pubblica necessità | uri: examples/codice_penale/sources/codice_penale_full.md#L6409-L6417
atom AttestaFalsoCertificato: the agent falsely attests, in a certificate, facts the act is meant to prove (art. 481) | quote: attesta falsamente, in un certificato, fatti dei quali l'atto è destinato a provare la verità | uri: examples/codice_penale/sources/codice_penale_full.md#L6409-L6417
atom FormaScritturaFalsa:  the agent forms a false private writing, in whole or part, or alters a true one (art. 485) | quote: forma, in tutto o in parte, una scrittura privata falsa, o altera una scrittura privata vera | uri: examples/codice_penale/sources/codice_penale_full.md#L6449-L6456
atom NeFaUso:              the agent uses the false private writing, or lets another use it (art. 485) | quote: qualora ne faccia uso o lasci che altri ne faccia uso | uri: examples/codice_penale/sources/codice_penale_full.md#L6449-L6456
atom SostituiscePersona:   the agent, inducing another into error, illegitimately substitutes their person for another's, or attributes a false name/status (art. 494) | quote: induce taluno in errore, sostituendo illegittimamente la propria all'altrui persona, o attribuendo … un falso nome | uri: examples/codice_penale/sources/codice_penale_full.md#L6553-L6561
atom ReclusioneFalsoIdeologico:  penalty: reclusion (art. 479) | quote: attesta falsamente che un fatto è stato da lui compiuto | uri: examples/codice_penale/sources/codice_penale_full.md#L6386-L6394
atom ReclusioneFalsoCertificato: penalty: reclusion (art. 481) | quote: attesta falsamente, in un certificato | uri: examples/codice_penale/sources/codice_penale_full.md#L6409-L6417
atom ReclusioneFalsoScrittura:   penalty: reclusion 6 months-3 years (art. 485) | quote: con la reclusione da sei mesi a tre anni | uri: examples/codice_penale/sources/codice_penale_full.md#L6449-L6456
atom ReclusioneSostituzione:     penalty: reclusion up to 1 year (art. 494) | quote: induce taluno in errore, sostituendo illegittimamente la propria all'altrui persona | uri: examples/codice_penale/sources/codice_penale_full.md#L6553-L6561

precetto_479: =>O@Chiunque ~AttestaFalso
precetto_485: =>O@Chiunque ~FormaScritturaFalsa
precetto_494: =>O@Chiunque ~SostituiscePersona

# Falsità ideologica del PU in atti pubblici (479): il PU attesta il falso in un
# atto formato nelle funzioni.
QualificaPubblica, AttoNelleFunzioni, AttestaFalso, Dolo {
  tipico_479: =>O@Giudice FattoTipico
  pena_479:   O(Sanziona) =>O@Giudice ReclusioneFalsoIdeologico
}

# Falsità ideologica in certificati (481): esercente servizio di pubblica
# necessità che attesta il falso in un certificato.
ServizioPubblicaNecessita, AttestaFalsoCertificato, Dolo {
  tipico_481: =>O@Giudice FattoTipico
  pena_481:   O(Sanziona) =>O@Giudice ReclusioneFalsoCertificato
}

# Falsità in scrittura privata (485): formare/alterare una scrittura privata
# falsa E farne uso, a fine di vantaggio/danno.
FormaScritturaFalsa, NeFaUso, FineVantaggioODanno, Dolo {
  tipico_485: =>O@Giudice FattoTipico
  pena_485:   O(Sanziona) =>O@Giudice ReclusioneFalsoScrittura
}

# Sostituzione di persona (494): indurre in errore sostituendo la persona o un
# falso nome/stato, a fine di vantaggio/danno.
SostituiscePersona, FineVantaggioODanno, Dolo {
  tipico_494: =>O@Giudice FattoTipico
  pena_494:   O(Sanziona) =>O@Giudice ReclusioneSostituzione
}
