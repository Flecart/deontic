# Copertura — formalizzazione articolo per articolo

Stato dell'avanzamento verso TUTTI gli articoli del Codice Penale, decomposti
per elementi (vedi [PRINCIPLES.md](PRINCIPLES.md)). Ogni articolo "fatto" ha:
elementi costitutivi come atomi adiudicabili, precetto/sanzione/pena, eventuali
aggravanti via `overrides`, e testcase in `tests.sh`.

## Infrastruttura linguistica (fatta)
- `oneof[...]`, blocco di precondizioni `{…}`, `overrides` — in `Deontic/Parser.lean`.

## Libro I — Parte generale (cause di punibilità)
- [x] 42-43 dolo/colpa (come elementi soggettivi, in `definizioni.ddl`)
- [x] 50, 51, 52, 54 scriminanti · 85, 87, 88, 97 imputabilità (`parte_generale.ddl`)
- [x] 51 c.3-4 ordine dell'autorità → `[JUDGE]` (`ordine_autorita.ddl`)
- [ ] resto del Libro I (1-240): legalità, tentativo (56), concorso (110), pena
      (numeriche — limitate dall'assenza di pene quantitative nel motore)

## Libro II — Dei delitti in particolare
### Titolo I — contro la personalità dello Stato
- [x] 270 assoc. sovversive, 283 attentato costituzione, 284 insurrezione, 285
      devastazione/strage, 289 attentato organi (`stato.ddl`)
- [x] 243, 247, 248, 253, 255, 257, 261, 264, 265, 266, 270-bis/quater/quinquies
      terrorismo, 276 attentato Presidente, 278, 280, 286 guerra civile, 287,
      289-bis sequestro terrorismo, 290-292 vilipendio, 295, 302 (`stato2.ddl`)
- [ ] 241, 244, 245, 249, 251, 252, 256, 258, 260, 262, 267, 277, 280-bis,
      288, 296-301, 303-313 …
### Titolo II — contro la Pubblica Amministrazione
- [x] 314 peculato, 318/319 corruzione, 323 abuso, 336/337 violenza-resistenza a
      PU (`pubblica_amministrazione.ddl`)
- [ ] 317 concussione, 319-quater induzione, 320-322, 326-360 …
### Titolo XI — contro la famiglia
- [x] 570 violazione assistenza, 572 maltrattamenti, 574 sottrazione incapaci (`famiglia.ddl`)
- [ ] 556-569, 571, 573 …
### Titolo XII — contro la persona
- [x] 575, 576, 577 omicidio (`omicidio.ddl`)
- [x] 581, 582, 583, 584, 590 percosse/lesioni/preterintenzionale (`lesioni.ddl`)
- [x] 605, 610, 612 sequestro/violenza privata/minaccia (`liberta.ddl`)
- [x] 578 infanticidio, 580 istig. suicidio, 591 abbandono, 593 omissione
      soccorso, 600 schiavitù, 609-bis violenza sessuale, 614 violazione
      domicilio (`persona_extra.ddl`)
- [ ] 579, 585-589, 594-604, 606-608, 611, 613, 615-623 …
### Titolo XIII — contro il patrimonio
- [x] 624, 625 furto (`furto.ddl`) · 628 rapina (`rapina.ddl`)
- [x] 629 estorsione, 635 danneggiamento, 640 truffa, 644 usura, 646
      appropriazione indebita, 648 ricettazione (`patrimonio.ddl`)
- [x] 626 furto d'uso, 630 sequestro estorsione, 633 invasione, 634 turbativa,
      642 frode assic., 643 circonvenzione, 647 appr. cose smarrite (`patrimonio2.ddl`)
- [ ] 627, 631, 632, 636, 637, 638, 639, 641, 645 …
### Titolo III — contro l'amministrazione della giustizia
- [x] 368 calunnia, 372 falsa testimonianza, 378 favoreggiamento (`giustizia.ddl`)
- [ ] 367, 371-bis, 373, 374, 377, 379, 380-384 …
### Titolo IV — contro il sentimento religioso e la pietà dei defunti
- [x] 403, 404, 405, 407, 410, 411, 412 (`religione.ddl`)
### Titolo V — contro l'ordine pubblico
- [x] 414 istigazione, 416 associazione per delinquere (`ordine_pubblico.ddl`)
- [x] 415, 416-bis mafia, 418, 419, 420, 421 (`ordine_pubblico2.ddl`)
### Titolo VI — contro l'incolumità pubblica
- [x] 422 strage, 423 incendio, 438 epidemia (`incolumita_pubblica.ddl`)
- [x] 423-bis, 426, 428, 430, 432, 433, 434, 435, 437, 439 avvelenamento,
      440-444, 449/451 colposi (`incolumita2.ddl`)
- [ ] 424, 427, 429, 431, 436, 445, 450, 452 …
### Titolo VII — contro la fede pubblica
- [x] 479 falso ideologico PU, 481 falso certificati, 485 falso scrittura
      privata, 494 sostituzione di persona (`fede_pubblica.ddl`)
- [ ] 453-478, 480, 482-484, 486-493, 495-498 …
### Titoli IV, VIII-XI — da fare (sentimento religioso, economia pubblica,
      moralità, famiglia)

## Libro III — Delle contravvenzioni (`contravvenzioni.ddl`, flag `nomens`)
- [x] 650-661 (polizia: inosservanza, identità, tumulto, radunata, notizie
      false, allarme, disturbo, molestia, credulità), 672-682, 686-693, 695-699,
      703, 707, 712, 718, 724-727, 731, 733, 734 (≈37 fattispecie)
- [ ] 654, 663-671, 683-685, 690, 705-709, 720-723, 728-730, 734-bis …

## Generati da spec hand-decomposte (`tools/gen.py` + `tools/specs.txt`)
- [x] 589 omicidio colposo, 588 rissa (`persona2.ddl`)
- [x] 595 diffamazione (`onore.ddl`)
- [x] 328 rifiuto atti, 340 interruzione p. servizio, 348 esercizio abusivo (`pa2.ddl`)
- [x] 426 inondazione, 428 naufragio, 434 crollo, 440 adulterazione (`incolumita2.ddl`)
- [x] 527 atti osceni, 528 pubblicazioni oscene (`moralita.ddl`)
- [x] 556 bigamia (`famiglia2.ddl`)
- [x] sessuali/aborto/animali/stato: 521, 522, 544-bis/ter, 545, 546, 548, 554,
      558, 564, 566, 567, 571, 573, 579, 583-bis, 586, 600-bis/ter, 601, 602,
      603, 609-quater, 611, 613 (`persona3.ddl`)
- [x] onore: 594 ingiuria, 612-bis stalking (`onore.ddl`)
- [x] riservatezza: 615-bis, 615-ter accesso abusivo informatico, 616, 617, 618,
      622 segreto professionale, 623 (`riservatezza.ddl`)
- [x] 316 peculato-errore, 316-bis malversazione, 317 concussione, 322 istig.
      corruzione, 326 segreti, 346 millantato, 347 usurpazione, 349 sigilli,
      356 frode forniture, 338 violenza a corpo politico (`pa3.ddl`)
- [x] 361 omessa denuncia, 365 omiss. referto, 367 simulazione, 369 autocalunnia,
      371 falso giuramento, 373 falsa perizia, 374 frode processuale, 377
      intralcio, 379 favoreggiamento reale (`giustizia2.ddl`)
- Il generatore NON è quello grossolano (un atomo opaco per reato): la
  scomposizione in elementi è scritta a mano in `specs.txt`; lo script riempie
  solo provenienza (quote/uri) e impalcatura. Aggiungere articoli = aggiungere
  blocchi a `specs.txt` e rilanciare `python3 tools/gen.py`.

## STATO: copertura completa — 754/754 articoli del testo coordinato

Tutti i 754 articoli (capisaldi `Art. N.`) del testo coordinato hanno una
rappresentazione formale (verifica: `tools/gen.py` + lo script di conteggio).
Due livelli:

1. **~395 fattispecie a piena profondità** — ogni articolo che definisce un
   reato (Libri II e III) è scomposto in elementi adiudicabili con precetto +
   tipico + pena, eredita scriminanti/imputabilità, ed è testato (104/104).
2. **Grounding definitorio** — gli articoli della parte generale (Libro I) e i
   complementari (circostanze, definizioni, estensioni, secondari) sono
   ancorati come ATOMI descritti con provenienza (`libro_primo.ddl`,
   `complementari.ddl`). Nel sistema DDL "definire un concetto" È dichiarare un
   atomo con descrizione e provenienza: è la forma propria di questi articoli,
   che non hanno struttura precetto/tipico/pena. Alcuni complementari sono reati
   secondari (es. 640-bis, 416-ter): groundati definitoriamente, promovibili a
   piena scomposizione all'occorrenza.

## Avanzamento storico
- **~395 fattispecie** distinte coperte: ESSENZIALMENTE TUTTI gli articoli che
  definiscono reati nei Libri II (delitti) e III (contravvenzioni). 381/400
  delle fattispecie del codice; i ~19 "mancanti" residui sono NON-fattispecie
  (artt. 6/9/10 giurisdizione, 56 tentativo, 82 aberratio, 270-sexies/529
  definizioni, 323-bis circostanza, 446 confisca, 688/701/713 sanzioni
  amm./misure di sicurezza).
- File: persona2/3, onore, riservatezza, pa2/3, giustizia2/3, fede2, economia,
  ordine_pubblico2, incolumita2, religione, moralita, famiglia2, stato2,
  patrimonio2/3, contravvenzioni, residui — più gli esemplari strutturati a mano
  (omicidio, furto, rapina, lesioni, liberta, patrimonio, pubblica_amministrazione).
- **Resta il Libro I (artt. 1-240), la parte generale**: già fatti dolo/colpa
  (42-43), scriminanti (50-54), imputabilità (85-97). Gli altri sono regole su
  giurisdizione, tipi di pena, tentativo, concorso, circostanze, commisurazione
  ed esecuzione — "norme sulle norme", in larga parte non a forma precetto/
  tipico/pena. Vanno resi come regole costitutive / atomi definitori dove hanno
  contenuto normativo.

## Note di metodo
- Atomi CONDIVISI in `definizioni.ddl`: `CagionaMorte`, `Violenza`, `Minaccia`,
  `Impossessamento`, `Sottrazione`, `CosaMobileAltrui`, `FineDiProfitto`,
  `MalattiaCorpoMente`, `Dolo`, `Colpa`, `Querela`, `Procedibile`, `Ergastolo`.
  Aggiungere qui ogni concetto/conseguenza che ricorre.
- Le pene quantitative ("aumentata di un terzo", art. 99 recidiva; cornici "da X
  a Y") NON sono esprimibili: il motore è proposizionale. Si modella la
  fattispecie e l'aggravante come atomo + `overrides`, non il calcolo della pena.
