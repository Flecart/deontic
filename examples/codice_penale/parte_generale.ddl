# Codice Penale — PARTE GENERALE (Libro I): la (non) punibilità.
# ===========================================================================
# Modulo riusabile importato da ogni fattispecie di reato (omicidio.ddl,
# furto.ddl, ...). Definisce SOLO ciò che è condiviso fra tutti i reati:
# le cause di giustificazione (Titolo III, Capo I) e di esclusione
# dell'imputabilità (Titolo IV) — tutte ancorate al codice come "non è
# punibile chi ...".
#
# CARDINE DEL MODELLO — l'atomo `Sanziona` e i due BEARER
# -------------------------------------------------------
# Ogni reato ha due norme con DESTINATARI (bearer) diversi (cfr. omicidio.ddl):
#   - il PRECETTO, norma primaria rivolta a chiunque:   =>O@Chiunque ~Condotta
#   - la SANZIONE, norma secondaria rivolta al giudice: Condotta =>O@Giudice Sanziona
# Il tag `@Bearer` (obbligazione hohfeldiana diretta) rende esplicito CHI è
# tenuto: il consociato a non delinquere, il giudice a punire. Lo scoping per
# bearer fa sì che il dovere del reo e quello del giudice non entrino in
# conflitto fra loro: vivono su piani distinti.
# `Sanziona` = "il reo deve essere punito per il fatto commesso". Tutte le cause
# di (non) punibilità qui sotto incidono su questo cardine generico — e, poiché
# vincolano il dovere di punire, sono anch'esse rivolte a `@Giudice` (così
# possono battere la sanzione: solo regole dello STESSO bearer si attaccano).
#
# SCELTA DI MODELLAZIONE (più di una codifica era fedele — la dichiariamo):
#   - Le scriminanti (artt. 50-54) escludono l'antigiuridicità; le cause di
#     non imputabilità (artt. 85/88/97) escludono la colpevolezza. La dottrina
#     le distingue, ma il codice usa per entrambe la formula operativa
#     "non è punibile / non è imputabile" => qui le facciamo confluire tutte
#     nello stesso esito `O ~Sanziona` (il giudice non deve punire), annotando
#     in commento la differenza dogmatica.
#   - Il PRECETTO resta incondizionato: un omicidio per legittima difesa viola
#     comunque `O ~Kill` (il reasoner segnala la violazione del precetto), ma
#     `Sanziona` non è dovuta. Si separa così "il fatto tipico è avvenuto"
#     (violazione del precetto) da "il reo va punito" (la sanzione).
#
# Il modulo non fissa fatti: è una libreria. La superiorità che fa prevalere
# ogni scriminante sulla sanzione di UNO specifico reato è dichiarata nel file
# del reato (la label della sanzione vive lì). Qui resta solo la superiorità
# interna al modulo: le eccezioni-all'-eccezione (artt. 87 e 54 c.2).

facts:

atom Sanziona:               the offender ought to be punished for the offence actually committed (secondary norm addressed to the judge) | quote: è punito con la reclusione | uri: examples/codice_penale/sources/codice_penale.md#L66-L69
atom FattoTipico:            a typical, punishable criminal fact obtains — the generic hinge every offence feeds into (its `tipico_<art>` rule) and on which all causes of non-punishability operate | quote: Nessuno può essere punito per un fatto che non sia espressamente preveduto come reato dalla legge | uri: examples/codice_penale/sources/codice_penale.md#L8-L11

# --- Cause di giustificazione (scriminanti) — escludono l'antigiuridicità ---
atom ConsensoAventeDiritto:  the victim, who may validly dispose of the right, consented to its injury or endangerment (art. 50) | quote: Non è punibile chi lede o pone in pericolo un diritto, col consenso della persona che può validamente disporne | uri: examples/codice_penale/sources/codice_penale.md#L13-L16
atom EsercizioDirittoDovere: the act is the exercise of a right or the fulfilment of a duty imposed by law or by a legitimate order of the public authority (art. 51 c.1) | quote: L'esercizio di un diritto o l'adempimento di un dovere imposto da una norma giuridica o da un ordine legittimo della pubblica autorità, esclude la punibilità | uri: examples/codice_penale/sources/codice_penale.md#L18-L21
atom PericoloAttuale:        the agent acted under the necessity of defending a right (own or another's) against a present danger of an unjust offence (art. 52) | quote: contro il pericolo attuale di una offesa ingiusta | uri: examples/codice_penale/sources/codice_penale.md#L29-L33
atom DifesaProporzionata:    the defensive reaction was proportionate to the offence (art. 52, last clause) | quote: sempre che la difesa sia proporzionata all'offesa | uri: examples/codice_penale/sources/codice_penale.md#L29-L33
atom StatoNecessita:         the agent was forced to commit the act to save self or others from a present danger of grave personal harm, not voluntarily caused nor otherwise avoidable, the act being proportionate (art. 54 c.1) | quote: Non è punibile chi ha commesso il fatto per esservi stato costretto dalla necessità di salvare sé od altri dal pericolo attuale di un danno grave alla persona | uri: examples/codice_penale/sources/codice_penale.md#L35-L42
atom DovereEsporsi:          the agent had a particular legal duty to expose himself to the danger (art. 54 c.2 — necessity does not apply) | quote: Questa disposizione non si applica a chi ha un particolare dovere giuridico di esporsi al pericolo | uri: examples/codice_penale/sources/codice_penale.md#L35-L42

# --- Esclusione dell'imputabilità (colpevolezza) — "non è imputabile" ---
atom MinoreAnni14:           the agent had not yet completed fourteen years of age at the time of the act (art. 97) | quote: Non è imputabile chi nel momento in cui ha commesso il fatto, non aveva compiuto i quattordici anni | uri: examples/codice_penale/sources/codice_penale.md#L61-L64
atom VizioTotaleMente:       a mental infirmity at the time of the act excluded the capacity to understand or to will (art. 88) | quote: era, per infermità, in tale stato di mente da escludere la capacità d'intendere o di volere | uri: examples/codice_penale/sources/codice_penale.md#L56-L59
atom Preordinato:            the agent put himself into the state of incapacity on purpose, to commit the offence or to prepare an excuse (art. 87 — art. 85 does not apply) | quote: chi si è messo in stato d'incapacità d'intendere o di volere al fine di commettere il reato, o di prepararsi una scusa | uri: examples/codice_penale/sources/codice_penale.md#L50-L54

# --- Sanzione di base: ogni fatto tipico va punito, salvo le cause sotto ----
# Ogni fattispecie di reato conclude (con la sua `tipico_<art>`) sul cardine
# generico `FattoTipico`; questa unica regola lo trasforma nel dovere di punire.
# Così le cause di non punibilità qui sotto battono UNA sola regola
# (`sanzione_base`) e si applicano a TUTTI i reati senza alcun cablaggio per
# singolo articolo. (`O(FattoTipico)` è un espediente: solo la forma deontica
# alimenta i corpi delle regole — un atomo costitutivo "piano" non lo farebbe.)
sanzione_base: O(FattoTipico) =>O@Giudice Sanziona

# --- Scriminanti: il giudice non deve punire ("non è punibile chi ...") ---
giust_consenso:   ConsensoAventeDiritto             =>O@Giudice ~Sanziona   # art. 50
giust_diritto:    EsercizioDirittoDovere            =>O@Giudice ~Sanziona   # art. 51 c.1
giust_difesa:     PericoloAttuale, DifesaProporzionata =>O@Giudice ~Sanziona # art. 52 (congiunzione: pericolo attuale E proporzione)
giust_necessita:  StatoNecessita                    =>O@Giudice ~Sanziona   # art. 54 c.1

# --- Non imputabilità: il giudice non deve punire ---
imp_minore:       MinoreAnni14                       =>O@Giudice ~Sanziona  # art. 97
imp_vizio:        VizioTotaleMente                   =>O@Giudice ~Sanziona  # art. 88

# --- Eccezioni-all'-eccezione: la punibilità è ripristinata ---
imp_preordinato:  Preordinato                        =>O@Giudice Sanziona   # art. 87 (actio libera in causa)
nec_dovere:       DovereEsporsi                      =>O@Giudice Sanziona   # art. 54 c.2

# Superiorità del modulo (vale per OGNI reato che importi questa parte generale):
#  - ogni scriminante / causa di non imputabilità batte la sanzione di base;
#  - l'eccezione-all'-eccezione (artt. 87, 54 c.2) batte a sua volta la scusa.
superiority: giust_consenso > sanzione_base, giust_diritto > sanzione_base, giust_difesa > sanzione_base, giust_necessita > sanzione_base, imp_minore > sanzione_base, imp_vizio > sanzione_base, imp_preordinato > imp_vizio, nec_dovere > giust_necessita
