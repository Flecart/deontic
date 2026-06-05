# Principi di formalizzazione del Codice Penale in DDL

Linee guida per formalizzare il codice penale **articolo per articolo**, in
modo che un giudice-LLM possa ragionarci sopra. La macchina fa la logica
deontica defeasibile (elementi, eccezioni, aggravanti, superiorità, deadlock);
l'LLM fa il *grounding*: legge il caso concreto e dichiara veri/falsi gli atomi.

> **Obiettivo:** gli atomi sono i FATTI ADIUDICABILI — le cose che il giudice
> verifica su un caso concreto — non frasi d'articolo. La granularità è il
> livello a cui le controversie reali si decidono.

## I principi

1. **Un articolo per volta, scomposto negli elementi costitutivi.** Una
   fattispecie sussiste solo se la **congiunzione** dei suoi elementi è vera, e
   il giudice vede *quale* elemento manca. Ogni elemento = un atomo:
   condotta, evento, nesso causale, oggetto materiale, qualità del soggetto
   (elementi oggettivi) **e** l'elemento soggettivo: dolo / colpa / dolo
   specifico ("al fine di…").

2. **Gli atomi sono predicati sul caso, non periodi dell'articolo.**
   "l'agente ha sottratto la cosa a chi la deteneva", non "condotta dell'art. 624".

3. **Risolvere i riferimenti per istanziazione.** Un rinvio si porta dentro come
   condizioni concrete, mai come puntatore opaco: l'art. 576 (ergastolo) = elementi
   dell'art. 575 + una circostanza; l'art. 625 = elementi dell'art. 624 + una
   circostanza; "cosa mobile" porta con sé l'art. 624 c.2 (energia elettrica).

4. **Stessa cosa, stesso atomo (composizione).** Quando articoli diversi usano
   lo stesso concetto o comminano la **stessa** conseguenza, c'è UN solo atomo,
   che i reati compongono — sta in [`definizioni.ddl`](definizioni.ddl).
   `Ergastolo` è l'esempio limpido: è la medesima pena per artt. 576, 577, 422,
   630… Gli elementi `Impossessamento`, `Sottrazione`, `Violenza` sono condivisi
   fra furto, rapina, estorsione. **Si unifica solo dove l'identità è palese**;
   le pene graduate ("reclusione da X a Y") restano specifiche dell'articolo,
   perché la cornice edittale cambia.

5. **Struttura a strati (già costruita).** precetto (`@Chiunque`) / sanzione
   (`@Giudice`); tipicità (elementi → `FattoTipico`) → antigiuridicità
   (scriminanti, condivise) → colpevolezza/imputabilità (condivise). Aggravanti
   e attenuanti = modificatori defeasibili della pena (lex specialis sull'atomo
   pena, es. premeditazione → ergastolo).

6. **Definizioni interpretative nella descrizione; logica defeasibile nelle
   regole.** Vincolo del motore: gli atomi-corpo "piani" devono essere FATTI, non
   derivati costitutivi. Quindi gli elementi di un reato sono fatti che l'LLM
   asserisce applicando la guida definitoria scritta nella `description` (inclusi
   i riferimenti già risolti); le regole portano solo la logica defeasibile.

7. **Fedeltà, con le scelte dichiarate.** Quando un elemento ammette più di una
   codifica, se ne sceglie una e la si dichiara in commento `#`. I conflitti
   genuinamente irrisolti → `[JUDGE]`. Ogni atomo conserva `quote:` + `uri:`.

8. **Profondità prima dell'ampiezza, incrementale e verificata.** Ogni articolo
   arriva con i suoi testcase: caso positivo (tutti gli elementi → `O(pena)`),
   **negativi con un elemento mancante** (→ nessun reato), e un caso di
   scriminante (→ non punibile). La generazione automatica grossolana è
   abbandonata: rendeva ogni reato un atomo opaco, inutile per il ragionamento.

## Esempio (la prova)

Furto, art. 624 — invece di un `R624` opaco:

```
atom Impossessamento:  the agent took the thing into their own autonomous control
atom Sottrazione:      … removing it from the holder, against the holder's will
atom CosaMobileAltrui: movable thing belonging to another (incl. electricity, art.624 c.2)
atom FineDiProfitto:   acted in order to profit, for self or others (dolo specifico)
tipico_624: Impossessamento, CosaMobileAltrui, Sottrazione, FineDiProfitto, O(Procedibile) =>O@Giudice FattoTipico
```

Se il detentore ha **acconsentito** a consegnare la cosa, il giudice segna
`Sottrazione` falso → **nessun furto**, e si vede perché. La rapina (art. 628)
riusa questi quattro atomi e aggiunge `Violenza`/`Minaccia`: gli **stessi**
fatti diventano furto o rapina secondo la presenza della violenza.

Stato corrente in [`README.md`](README.md).
