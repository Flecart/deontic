# Codice Penale — famiglia2 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom GiaSposato: the agent is already bound by a marriage having civil effects (art. 556) | quote: Chiunque, essendo legato da un matrimonio avente effetti civili, ne contrae un altro, pur avente effetti civili, è | uri: examples/codice_penale/sources/codice_penale_full.md#L7433-L7441
atom ContraeAltroMatrimonio: and contracts another marriage with civil effects (art. 556) | quote: Chiunque, essendo legato da un matrimonio avente effetti civili, ne contrae un altro, pur avente effetti civili, è | uri: examples/codice_penale/sources/codice_penale_full.md#L7433-L7441
atom ReclusioneBigamia: reclusion 1-5 years (art. 556) | quote: Chiunque, essendo legato da un matrimonio avente effetti civili, ne contrae un altro, pur avente effetti civili, è | uri: examples/codice_penale/sources/codice_penale_full.md#L7433-L7441
precetto_556: =>O@Chiunque ~GiaSposato
GiaSposato, ContraeAltroMatrimonio, Dolo {
  tipico_556: =>O@Giudice FattoTipico
  pena_556:   O(Sanziona) =>O@Giudice ReclusioneBigamia
}
