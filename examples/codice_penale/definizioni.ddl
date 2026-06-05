# Codice Penale — DEFINIZIONI: vocabolario condiviso.
# ===========================================================================
# Questo modulo riesporta la parte generale (cause di punibilità) e aggiunge
# il vocabolario CONDIVISO fra più reati: gli ELEMENTI costitutivi che
# ricorrono (impossessamento, sottrazione, violenza, dolo…) e le CONSEGUENZE
# identiche (l'ergastolo è la stessa pena ovunque sia comminato).
#
# Principio di RISOLUZIONE DEI RIFERIMENTI: quando due articoli usano lo stesso
# concetto o comminano la stessa pena, qui c'è UN solo atomo, e i file dei reati
# lo compongono. Così il giudice (LLM) accerta una volta "c'è stata violenza?"
# e quel fatto vale per la rapina, l'estorsione, la violenza privata, ecc.
# Si unifica solo dove l'identità è palese; le pene graduate (reclusione "da X a
# Y") restano specifiche dell'articolo perché la cornice edittale cambia.
from parte_generale.ddl import *

facts:

# --- CONSEGUENZE condivise (pena identica fra più articoli) -----------------
atom Ergastolo:        the penalty imposed is life imprisonment (ergastolo) — the SAME consequence wherever the code prescribes it (artt. 576, 577, 422, 630, …) | quote: Si applica la pena dell'ergastolo | uri: examples/codice_penale/sources/codice_penale_full.md#L7751-L7754

# --- ELEMENTO SOGGETTIVO (artt. 42-43) --------------------------------------
atom Dolo:             the agent foresaw and willed the harmful or dangerous event as the result of their action — intent (dolo, art. 43); the default mens rea of delitti unless the article is colposo | quote: è doloso, o secondo l'intenzione, quando l'evento dannoso o pericoloso … è dall'agente preveduto e voluto | uri: examples/codice_penale/sources/codice_penale_full.md#L542-L548
atom Colpa:            the event was not willed but occurred through negligence, imprudence, lack of skill, or breach of rules — fault (colpa, art. 43); required where the article is colposo | quote: è colposo, o contro l'intenzione, quando l'evento … si verifica a causa di negligenza o imprudenza o imperizia | uri: examples/codice_penale/sources/codice_penale_full.md#L542-L560

# --- PROCEDIBILITÀ (condivisa: molti reati sono punibili "a querela") --------
atom Querela:          the injured person filed a complaint — querela (the procedural condition of prosecution for offences punishable "a querela della persona offesa") | quote: è punibile a querela della persona offesa | uri: examples/codice_penale/sources/codice_penale_full.md#L9116-L9128
atom Procedibile:      the offence may be prosecuted — the procedural precondition of punishment (fed by querela, or by an aggravator that makes it procedibile d'ufficio) | quote: si procede d'ufficio | uri: examples/codice_penale/sources/codice_penale_full.md#L8701-L8706

# --- EVENTI condivisi (omicidio, preterintenzionale, lesioni, ...) ----------
atom CagionaMorte:       the agent causes the death of a human being — the lethal event and its causal link to the conduct (artt. 575, 584, ...) | quote: Chiunque cagiona la morte di un uomo | uri: examples/codice_penale/sources/codice_penale_full.md#L7708-L7712
atom MalattiaCorpoMente: an illness of body or mind results from the act — the dividing line between percosse (no illness) and lesione (illness), artt. 581-582 | quote: dalla quale deriva una malattia nel corpo o nella mente | uri: examples/codice_penale/sources/codice_penale_full.md#L7815-L7820

# --- ELEMENTI patrimoniali (furto, rapina, estorsione, …) -------------------
atom Impossessamento:  the agent took the thing into their own autonomous control (impossessamento) | quote: s'impossessa della cosa mobile altrui | uri: examples/codice_penale/sources/codice_penale_full.md#L9116-L9128
atom Sottrazione:      the agent removed the thing from whoever held it, against the holder's will (sottrazione) | quote: sottraendola a chi la detiene | uri: examples/codice_penale/sources/codice_penale_full.md#L9116-L9128
atom CosaMobileAltrui: the thing is movable and belongs to another — including electricity and any energy of economic value (art. 624 c.2) | quote: si considera cosa mobile anche l'energia elettrica e ogni altra energia che abbia un valore economico | uri: examples/codice_penale/sources/codice_penale_full.md#L9116-L9128
atom FineDiProfitto:   the agent acted in order to gain a profit, for self or for others (dolo specifico di profitto) | quote: al fine di trarne profitto per sé o per altri | uri: examples/codice_penale/sources/codice_penale_full.md#L9116-L9128
atom SiAppropria:      the agent appropriated money or another's movable thing of which they already had possession on some title (appropriazione indebita art. 646, peculato art. 314) | quote: si appropria il denaro o la cosa mobile altrui di cui abbia, a qualsiasi titolo, il possesso | uri: examples/codice_penale/sources/codice_penale_full.md#L9400-L9406

# --- SOGGETTO QUALIFICATO (delitti contro la PA) ----------------------------
atom QualificaPubblica: the agent is a public official or a person charged with a public service (the qualified subject of artt. 314, 318, 319, 323, ...) | quote: Il pubblico ufficiale o l'incaricato di un pubblico servizio | uri: examples/codice_penale/sources/codice_penale_full.md#L4700-L4706

# --- Finalità e circostanze condivise (contro lo Stato) ---------------------
atom FineTerrorismo:   the conduct was carried out for the purpose of terrorism or subversion of the democratic order (dolo specifico shared by artt. 270-bis, 270-quater, 280, 289-bis) | quote: per finalità di terrorismo o di eversione dell'ordine democratico | uri: examples/codice_penale/sources/codice_penale_full.md#L3470-L3476
atom TempoGuerra:      the act was committed in time of war (circumstance shared by artt. 247, 248, 265, 267) | quote: in tempo di guerra | uri: examples/codice_penale/sources/codice_penale_full.md#L3200-L3206

# --- ELEMENTI dei falsi e dolo specifico di vantaggio/danno -----------------
atom AttestaFalso:     the agent falsely attests a fact in an act/certificate (the false statement of the falsità ideologica, artt. 479, 481) | quote: attesta falsamente che un fatto è stato da lui compiuto o è avvenuto alla sua presenza | uri: examples/codice_penale/sources/codice_penale_full.md#L6386-L6394
atom FineVantaggioODanno: the agent acted in order to gain an advantage for self/others or to harm another (dolo specifico shared by falsità in scrittura privata art. 485 and sostituzione di persona art. 494) | quote: al fine di procurare a sé o ad altri un vantaggio o di recare ad altri un danno | uri: examples/codice_penale/sources/codice_penale_full.md#L6449-L6456

# --- ELEMENTI contro la persona (rapina, estorsione, violenza privata, …) ---
atom Violenza:         the agent used physical violence against a person | quote: mediante violenza alla persona o minaccia | uri: examples/codice_penale/sources/codice_penale_full.md#L9233-L9238
atom Minaccia:         the agent threatened a person (minaccia) | quote: mediante violenza alla persona o minaccia | uri: examples/codice_penale/sources/codice_penale_full.md#L9233-L9238
atom Costringe:        by the conduct, the agent compels another to do, tolerate or omit something (the coerced result shared by violenza privata art. 610 and estorsione art. 629) | quote: costringe altri a fare, tollerare, od omettere qualche cosa | uri: examples/codice_penale/sources/codice_penale_full.md#L8701-L8706
atom Inganno:          the result was achieved by deception (a coercive/fraudulent modality alongside violence and threat, e.g. artt. 522, 523, 558) | quote: con violenza, minaccia o inganno | uri: examples/codice_penale/sources/codice_penale_full.md#L8430-L8436
atom IngiustoProfittoAltruiDanno: the agent procured an unjust profit, for self or others, with harm to another (the patrimonial event of estorsione art. 629 and truffa art. 640) | quote: procura a sé o ad altri un ingiusto profitto con altrui danno | uri: examples/codice_penale/sources/codice_penale_full.md#L9259-L9266
