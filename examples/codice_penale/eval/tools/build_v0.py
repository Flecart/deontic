#!/usr/bin/env python3
"""Build dataset/v0_pilot.jsonl from hand-authored specs + engine-computed gold.

The specs below carry the *authored* parts (narrative, question, tier, the atom
config and which penalty atom is the offence's payoff) — the creative,
human-owned work.  `gold` is NOT written by hand: it is computed by the engine
(via backward_gen.verdict) so labels can never drift from the theory.

Authoring rules honoured here (see PLAN.md §3):
  - the narrative is an Italian story that ENTAILS exactly the config;
  - no leakage: it never names an element atom / its rubric, never states the
    verdict (no "punibile", "reato", "assolto", "scriminante"…);
  - minimal pairs change only the one decisive fact (and the sentence for it).

Run:  python3 build_v0.py   ->   ../dataset/v0_pilot.jsonl
"""
from __future__ import annotations

import json
import os

import backward_gen as bg
import offences as off

OUT = os.path.normpath(os.path.join(off.REPO,
        "examples/codice_penale/eval/dataset/v0_pilot.jsonl"))

F_FUR = "examples/codice_penale/furto.ddl"
F_OMI = "examples/codice_penale/omicidio.ddl"
F_RAP = "examples/codice_penale/rapina.ddl"
F_LES = "examples/codice_penale/lesioni.ddl"

# Shared element bundles (present-atom lists).
FUR = ["Impossessamento", "CosaMobileAltrui", "Sottrazione", "FineDiProfitto"]
OMI = ["CagionaMorte", "Dolo"]

Q_DEF = "È punibile la persona descritta, e per quale reato?"


def item(id, tier, file, penalty, present, narrative,
         pair=None, distractor=False, prior_divergent=False,
         source="synthetic", question=Q_DEF):
    g = bg.verdict(file, penalty, present)
    return {
        "id": id, "tier": tier, "source": source, "theory": file,
        "narrative": narrative.strip(), "question": question,
        "atoms_gold": {a: 1 for a in present},
        "gold": g, "minimal_pair": pair,
        "distractor": distractor, "prior_divergent": prior_divergent,
    }


# --------------------------------------------------------------------------- #
# The pilot.  ~40 items, organised by minimal pair.                            #
# Narratives describe FACTS only; the decisive element must be *inferable*.    #
# --------------------------------------------------------------------------- #
SPECS = [
    # ----- P1  T1 furto: fine di profitto (furto vs furto d'uso) -----
    dict(id="furto-001", tier=1, file=F_FUR, penalty="ReclusioneFurto",
         present=FUR + ["Querela"], pair="furto-002",
         narrative="""
Marco entra nello spogliatoio della palestra mentre gli altri sono in sala pesi.
Apre l'armadietto di un altro iscritto, prende lo smartphone che vi era riposto
e se lo mette in tasca, deciso a rivenderlo al mercatino il giorno dopo per
arrotondare. Esce e torna a casa con il telefono. Il proprietario, accortosi,
sporge denuncia chiedendo che si proceda."""),
    dict(id="furto-002", tier=1, file=F_FUR, penalty="ReclusioneFurto",
         present=[a for a in FUR if a != "FineDiProfitto"] + ["Querela"],
         pair="furto-001", prior_divergent=True,
         narrative="""
Marco entra nello spogliatoio della palestra e prende dall'armadietto di un
compagno il caricabatterie, perché il suo telefono è scarico e deve fare una
chiamata urgente. Lo usa per dieci minuti nell'atrio e, appena finito, lo
rimette nell'armadietto del compagno esattamente dov'era, senza che manchi
nulla. Il compagno, che lo ha visto, si lamenta con la direzione."""),

    # ----- P2  T1 furto: procedibilità a querela (prior-divergent) -----
    dict(id="furto-003", tier=1, file=F_FUR, penalty="ReclusioneFurto",
         present=FUR + ["Querela"], pair="furto-004",
         narrative="""
Di notte Anna scavalca il muretto del vicino, raccoglie dal giardino la
bicicletta da corsa lasciata appoggiata al gazebo e la porta via per tenerla
per sé. Il vicino, al risveglio, va dai carabinieri e presenta formale
istanza perché si proceda contro di lei."""),
    dict(id="furto-004", tier=1, file=F_FUR, penalty="ReclusioneFurto",
         present=FUR, pair="furto-003", prior_divergent=True,
         narrative="""
Di notte Anna scavalca il muretto del vicino, raccoglie dal giardino la
bicicletta da corsa lasciata appoggiata al gazebo e la porta via per tenerla
per sé. Il vicino se ne accorge ma, per quieto vivere, decide di non rivolgersi
ad alcuna autorità e non presenta alcuna istanza: lascia perdere."""),

    # ----- P3  T1 lesioni: percosse vs lesione (deriva una malattia?) -----
    dict(id="lesioni-001", tier=1, file=F_LES, penalty="ReclusionePercosse",
         present=["Percuote", "Dolo", "Querela"], pair="lesioni-002",
         narrative="""
Durante un diverbio al bar, Luca dà uno spintone e un paio di schiaffi a
Giovanni, volontariamente. Giovanni resta dolorante sul momento ma il medico
del pronto soccorso lo visita e lo dimette subito: nessun livido che duri,
nessun disturbo, nulla che lo costringa a casa. Giovanni sporge querela."""),
    dict(id="lesioni-002", tier=1, file=F_LES, penalty="ReclusioneLesione",
         present=["CagionaLesione", "MalattiaCorpoMente", "Dolo", "Querela"],
         pair="lesioni-001",
         narrative="""
Durante un diverbio al bar, Luca colpisce Giovanni con un pugno deciso al volto.
Giovanni cade, e dalla botta gli resta il setto nasale fratturato: il medico gli
prescrive quindici giorni di cure e riposo prima di poter tornare al lavoro.
Giovanni sporge querela."""),

    # ----- P4  T1 lesioni: lieve vs grave -----
    dict(id="lesioni-003", tier=1, file=F_LES, penalty="ReclusioneLesione",
         present=["CagionaLesione", "MalattiaCorpoMente", "Dolo", "Querela"],
         pair="lesioni-004",
         narrative="""
Per gelosia, Sara colpisce con uno schiaffo violento la collega Elena. Resta a
Elena un labbro spaccato che guarisce in circa una settimana di medicazioni.
Elena presenta querela."""),
    dict(id="lesioni-004", tier=1, file=F_LES, penalty="ReclusioneLesioneGrave",
         present=["CagionaLesione", "MalattiaCorpoMente", "Dolo", "Querela", "LesioneGrave"],
         pair="lesioni-003",
         narrative="""
Per gelosia, Sara getta in faccia alla collega Elena un liquido corrosivo che
aveva portato apposta. Elena perde in modo permanente gran parte della vista
dall'occhio destro, una menomazione che non recupererà."""),

    # ----- P5  T1 omicidio: dolo (doloso vs senza dolo) -----
    dict(id="omicidio-001", tier=1, file=F_OMI, penalty="Reclusione575",
         present=OMI, pair="omicidio-002",
         narrative="""
Dopo mesi di rancore, Paolo aspetta il rivale sotto casa, gli punta contro la
pistola che ha portato proprio per questo e fa fuoco mirando al petto, volendo
ucciderlo. L'uomo muore sul colpo."""),
    dict(id="omicidio-002", tier=1, file=F_OMI, penalty="Reclusione575",
         present=["CagionaMorte"], pair="omicidio-001",
         narrative="""
Paolo guida nel rispetto dei limiti quando un pedone, del tutto inatteso,
gli attraversa la strada di scatto da dietro un furgone. Paolo non fa in tempo
a frenare e lo investe; l'uomo muore. Paolo non aveva alcuna intenzione di
colpirlo e nulla avrebbe potuto fare per evitarlo."""),

    # ----- P6  T2 omicidio: legittima difesa (proporzionata?) -----
    dict(id="omicidio-003", tier=2, file=F_OMI, penalty="Reclusione575",
         present=OMI + ["PericoloAttuale", "DifesaProporzionata"],
         pair="omicidio-004",
         narrative="""
Di notte un rapinatore armato di coltello aggredisce Franco in casa e gli si
avventa contro per colpirlo. Franco, che teme per la propria vita in quell'
istante, afferra l'arma da fuoco legalmente detenuta e spara una sola volta per
fermarlo. Il rapinatore muore. La reazione è stata l'unica via per salvarsi ed
era misurata sulla minaccia ricevuta."""),
    dict(id="omicidio-004", tier=2, file=F_OMI, penalty="Reclusione575",
         present=OMI + ["PericoloAttuale"], pair="omicidio-003",
         narrative="""
Un ragazzino scavalca la recinzione di Franco per recuperare il pallone e Franco
lo vede allontanarsi di corsa, disarmato, già a venti metri dal cancello. Pur
non essendo più in alcun pericolo, Franco imbraccia il fucile e gli spara alla
schiena uccidendolo, perché 'doveva imparare'."""),

    # ----- P7  T2 omicidio: minore di 14 anni (prior-divergent) -----
    dict(id="omicidio-005", tier=2, file=F_OMI, penalty="Reclusione575",
         present=OMI + ["MinoreAnni14"], pair="omicidio-006",
         prior_divergent=True,
         narrative="""
Durante una lite tra famiglie, un bambino di dodici anni afferra il coltello da
cucina e colpisce a morte, volontariamente, l'uomo che stava insultando suo
padre. Al momento del fatto il bambino non aveva ancora compiuto i quattordici
anni."""),
    dict(id="omicidio-006", tier=2, file=F_OMI, penalty="Reclusione575",
         present=OMI, pair="omicidio-005",
         narrative="""
Durante una lite tra famiglie, un uomo di trent'anni afferra il coltello da
cucina e colpisce a morte, volontariamente, chi stava insultando suo padre."""),

    # ----- P8  T3 omicidio: vizio totale vs actio libera in causa -----
    dict(id="omicidio-007", tier=3, file=F_OMI, penalty="Reclusione575",
         present=OMI + ["VizioTotaleMente"], pair="omicidio-008",
         prior_divergent=True,
         narrative="""
Nel pieno di un delirio psicotico documentato dai medici, Stefano, del tutto
incapace in quel momento di comprendere ciò che faceva o di controllarsi,
colpisce a morte un passante. Le perizie confermano che al momento del fatto
la sua mente era totalmente travolta dall'infermità."""),
    dict(id="omicidio-008", tier=3, file=F_OMI, penalty="Reclusione575",
         present=OMI + ["VizioTotaleMente", "Preordinato"], pair="omicidio-007",
         narrative="""
Stefano vuole uccidere un rivale ma vuole poi potersi dire 'fuori di sé'. La
sera del fatto ingerisce di proposito una dose massiccia di sostanze, fino a
ridursi incapace di intendere e di volere, esattamente per commettere
la vittima in quello stato e prepararsi una giustificazione. In quello stato,
come pianificato, la uccide."""),

    # ----- P9  T3 omicidio: stato di necessità vs dovere di esporsi -----
    dict(id="omicidio-009", tier=3, file=F_OMI, penalty="Reclusione575",
         present=OMI + ["StatoNecessita"], pair="omicidio-010",
         prior_divergent=True,
         narrative="""
Dopo un naufragio, due uomini si aggrappano a un relitto che regge il peso di
uno solo. Per non annegare insieme, e non avendo altro modo di salvarsi da quel
pericolo immediato di morte che non aveva provocato, uno spinge via l'altro, che
affoga. Il superstite era un passeggero come l'altro."""),
    dict(id="omicidio-010", tier=3, file=F_OMI, penalty="Reclusione575",
         present=OMI + ["StatoNecessita", "DovereEsporsi"], pair="omicidio-009",
         narrative="""
Durante un naufragio il bagnino di bordo, il cui compito giurato è proprio
mettere in salvo i passeggeri prima di sé, si aggrappa al relitto che regge uno
solo e ne spinge via un passeggero per non annegare; il passeggero affoga.
Su di lui gravava il preciso obbligo di esporsi a quel pericolo."""),

    # ----- P10 T4 rapina: violenza/minaccia (rapina vs niente rapina) -----
    dict(id="rapina-001", tier=4, file=F_RAP, penalty="ReclusioneRapina",
         present=FUR + ["Violenza"], pair="rapina-002",
         narrative="""
All'uscita della banca, Nadia affronta una signora, la afferra per il braccio
e la strattona con forza facendola cadere, poi le strappa di mano la borsa con
il portafogli e fugge per tenersi il contante. La signora riporta solo lo
spavento e qualche graffio."""),
    dict(id="rapina-002", tier=4, file=F_RAP, penalty="ReclusioneRapina",
         present=FUR, pair="rapina-001",
         narrative="""
All'uscita della banca, Nadia nota una signora distratta che ha appoggiato la
borsa sul muretto mentre cerca le chiavi. Senza che la donna se ne avveda, Nadia
sfila la borsa con il portafogli e si allontana svelta per tenersi il contante.
Non c'è alcun contatto: la signora non viene toccata né minacciata."""),

    # ----- P11 T4 omicidio: premeditazione -> ergastolo (penalty flip) -----
    dict(id="omicidio-011", tier=4, file=F_OMI, penalty="Reclusione575",
         present=OMI, pair="omicidio-012",
         narrative="""
In un alterco improvviso al semaforo, Dario perde la testa, scende dall'auto e
in preda all'ira colpisce a morte l'altro automobilista con una chiave inglese
afferrata al momento. Tutto si consuma nel giro di un minuto, senza che vi
fosse stato alcun proposito anteriore."""),
    dict(id="omicidio-012", tier=4, file=F_OMI, penalty="Ergastolo",
         present=OMI + ["Premeditazione"], pair="omicidio-011",
         narrative="""
Dario rimugina per settimane il piano: studia gli orari della vittima, compra
l'arma in anticipo, sceglie il luogo e il momento. La sera stabilita esegue
freddamente quanto preparato e uccide la vittima come da disegno coltivato a
lungo."""),

    # ----- standalone: omicidio preterintenzionale (lesioni.ddl, art.584) -----
    dict(id="lesioni-005", tier=4, file=F_LES, penalty="ReclusionePreterint",
         present=["AttiDirettiLesione", "CagionaMorte"],
         narrative="""
Per punire un conoscente, Bruno gli sferra un pugno volendo soltanto fargli
male, senza alcuna intenzione di ammazzarlo. L'uomo però cade all'indietro,
batte la nuca sul marciapiede e muore per il trauma. Bruno voleva percuoterlo,
non ucciderlo, ma dal suo gesto è derivata la morte."""),
    # ----- standalone: lesione colposa (art.590) -----
    dict(id="lesioni-006", tier=1, file=F_LES, penalty="ReclusioneLesioneColposa",
         present=["CagionaLesione", "Colpa"],
         narrative="""
Tinteggiando il balcone, Carla lascia un secchio di vernice sul parapetto senza
fissarlo, per pura sbadataggine. Il secchio cade sul passante sottostante, che
riporta una contusione e qualche giorno di cure. Carla non voleva colpire
nessuno: è stata solo disattenta."""),

    # ----- distractors: lurid-but-irrelevant facts, gold unchanged -----
    dict(id="furto-005", tier=1, file=F_FUR, penalty="ReclusioneFurto",
         present=FUR + ["Querela"], distractor=True,
         narrative="""
Il derubato, Tizio, è un noto usuraio che molti in paese vorrebbero veder
rovinato, e gira voce che evada le tasse. Nulla di tutto ciò sfiora Gennaro,
che entra nel suo magazzino, carica sul furgone una cassa di utensili altrui
e la porta via per rivenderla. Tizio sporge querela."""),
    dict(id="omicidio-013", tier=2, file=F_OMI, penalty="Reclusione575",
         present=OMI + ["PericoloAttuale", "DifesaProporzionata"], distractor=True,
         narrative="""
La vittima era un uomo odioso, pieno di debiti e mal voluto da tutti. Ciò non
toglie che quella notte fosse lui ad aggredire Rosa in casa con un'accetta,
avventandosi per colpirla. Rosa, in pericolo immediato di vita e senza altra
via di scampo, spara un colpo misurato e lo uccide."""),
    dict(id="lesioni-007", tier=1, file=F_LES, penalty="ReclusioneLesione",
         present=["CagionaLesione", "MalattiaCorpoMente", "Dolo", "Querela"],
         distractor=True,
         narrative="""
Mentre la radio in sottofondo dà la notizia di un colpo milionario in una
gioielleria del centro, e tutti al tavolo ne parlano, Mimmo per stizza spacca volontariamente
una bottiglia sul braccio di Saro, procurandogli un taglio che il medico
ricuce e che lo terrà fermo dieci giorni. Saro sporge querela."""),
    dict(id="furto-006", tier=1, file=F_FUR, penalty="ReclusioneFurto",
         present=[a for a in FUR if a != "FineDiProfitto"] + ["Querela"],
         distractor=True,
         narrative="""
Nel pieno di un temporale spettacolare, con tuoni che fanno tremare i vetri,
Ada prende dalla scrivania della collega la pinzatrice altrui per chiudere una
pratica urgente, la usa un minuto e la riposa subito al suo posto, intatta.
La collega comunque protesta formalmente con l'ufficio."""),
]


def main():
    items = [item(**s) for s in SPECS]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    npairs = sum(1 for it in items if it["minimal_pair"]) // 2
    print(f"wrote {len(items)} items ({npairs} minimal pairs) -> {os.path.relpath(OUT, off.REPO)}")
    # quick verdict tally
    from collections import Counter
    c = Counter(it["gold"]["verdict"] for it in items)
    print("verdicts:", dict(c))


if __name__ == "__main__":
    main()
