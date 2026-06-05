# Codice Penale — moralita (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom LuogoPubblico: in a public place, or one open or exposed to the public (art. 527) | quote: Chiunque, in luogo pubblico o aperto o esposto al pubblico, compie atti osceni è punito con la reclusione da tre mesi a | uri: examples/codice_penale/sources/codice_penale_full.md#L7029-L7037
atom CompieAttiOsceni: the agent performs obscene acts (art. 527) | quote: Chiunque, in luogo pubblico o aperto o esposto al pubblico, compie atti osceni è punito con la reclusione da tre mesi a | uri: examples/codice_penale/sources/codice_penale_full.md#L7029-L7037
atom ReclusioneAttiOsceni: reclusion 3 months-3 years (art. 527) | quote: Chiunque, in luogo pubblico o aperto o esposto al pubblico, compie atti osceni è punito con la reclusione da tre mesi a | uri: examples/codice_penale/sources/codice_penale_full.md#L7029-L7037
precetto_527: =>O@Chiunque ~LuogoPubblico
LuogoPubblico, CompieAttiOsceni, Dolo {
  tipico_527: =>O@Giudice FattoTipico
  pena_527:   O(Sanziona) =>O@Giudice ReclusioneAttiOsceni
}

atom FabbricaDistribuisceOsceni: fabricates, imports, acquires, holds, exports or distributes obscene writings/images (art. 528) | quote: Pubblicazioni e spettacoli osceni | uri: examples/codice_penale/sources/codice_penale_full.md#L7038-L7046
atom ScopoCommercioOsceni: for the purpose of trade, distribution or public display (art. 528) | quote: Pubblicazioni e spettacoli osceni | uri: examples/codice_penale/sources/codice_penale_full.md#L7038-L7046
atom ReclusionePubblicazioniOscene: reclusion or fine (art. 528) | quote: Pubblicazioni e spettacoli osceni | uri: examples/codice_penale/sources/codice_penale_full.md#L7038-L7046
precetto_528: =>O@Chiunque ~FabbricaDistribuisceOsceni
FabbricaDistribuisceOsceni, ScopoCommercioOsceni, Dolo {
  tipico_528: =>O@Giudice FattoTipico
  pena_528:   O(Sanziona) =>O@Giudice ReclusionePubblicazioniOscene
}
