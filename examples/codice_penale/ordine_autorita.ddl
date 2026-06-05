# Codice Penale — ORDINE DELLA PUBBLICA AUTORITÀ (art. 51, commi 3-4).
# ===========================================================================
# Un caso che il codice stesso LASCIA APERTO. Chi esegue un ordine criminoso
# della pubblica autorità "risponde del reato" (c. 3), MA "salvo che, per errore
# di fatto, abbia ritenuto di obbedire a un ordine legittimo" (c. 3 ult.) e
# "non è punibile chi esegue l'ordine illegittimo quando la legge non gli
# consente alcun sindacato sulla legittimità dell'ordine" (c. 4).
#
# Se l'esecutore ha eseguito l'ordine E ha errato sulla sua legittimità, due
# norme tirano in direzioni opposte sul dovere di punire (@Giudice) e il codice
# NON fissa quale prevalga: dipende dalla sindacabilità in concreto dell'ordine.
# Deliberatamente NON dichiariamo superiorità fra le due: il reasoner deve
# emettere un [JUDGE] e rimettere la scelta al giudice (è il comportamento
# corretto — il motore non indovina il diritto).
#
# Riusa l'omicidio come reato di base (porta con sé la parte generale).
from omicidio.ddl import *

facts:

atom OrdineEseguito:      the agent carried out a criminal order of the public authority (art. 51 c.3) | quote: Risponde del reato altresì chi ha eseguito l'ordine | uri: examples/codice_penale/sources/codice_penale.md#L18-L27
atom ErroreSullOrdine:    the agent, by a mistake of fact, believed he was obeying a legitimate order (art. 51 c.3, last sentence) | quote: salvo che, per errore di fatto abbia ritenuto di obbedire a un ordine legittimo | uri: examples/codice_penale/sources/codice_penale.md#L18-L27

# c.3: chi esegue l'ordine risponde del reato -> il giudice deve punire.
ordine_risponde: OrdineEseguito   =>O@Giudice Sanziona
# c.3 ult.: salvo errore di fatto sulla legittimità -> il giudice non deve punire.
ordine_errore:   ErroreSullOrdine =>O@Giudice ~Sanziona

# NESSUNA superiorità fra ordine_risponde / sanzione_base e ordine_errore:
# coi fatti {CagionaMorte, Dolo, OrdineEseguito, ErroreSullOrdine} il conflitto
# su Sanziona resta irrisolto e il motore stampa [JUDGE: aggiungere superiorità].
#
# Prova:
#   deontic check examples/codice_penale/ordine_autorita.ddl \
#       --assume CagionaMorte,Dolo,OrdineEseguito,ErroreSullOrdine
#     -> WARNING: unresolved obligation conflict on Sanziona (il giudice decide
#        se l'ordine fosse in concreto sindacabile).
#   Aggiungendo `superiority: ordine_errore > ordine_risponde, ordine_errore > sanzione_base`
#   il conflitto si scioglie in F(Sanziona) (esecutore non punibile).
