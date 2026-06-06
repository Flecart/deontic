#!/usr/bin/env python3
"""E2 — independent-annotator check to break the oracle-circularity objection.

The Skeptic's charge: the engine grades the LLM against gold the *engine itself*
produced, so its offence-ID lead is self-marking. This script asks a strong
model (gpt-4.1) to act as an INDEPENDENT legal annotator: it sees the narrative
+ the FULL cross-offence catalogue (every penalty atom across furto/omicidio/
rapina/lesioni) and must pick which offence applies, with room to deliberate.

We then measure how often the independent annotator AGREES with the engine gold.
High agreement => the engine's labels are legally sound (corroborated by an
independent reasoner), not merely self-consistent. We also re-print the single
-pass llm_only offence-ID from predictions.jsonl for contrast.
"""
import json, os, sys
import llm

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.normpath(os.path.join(HERE, ".."))

CATALOGUE = """ReclusioneFurto         = furto semplice (art. 624): sottrazione di cosa mobile altrui, impossessamento, fine di profitto.
ReclusioneFurtoAggravata = furto aggravato (art. 625): furto con violenza sulle cose o destrezza.
Reclusione575           = omicidio doloso (art. 575): cagionare la morte di un uomo con dolo.
ReclusioneRapina        = rapina (art. 628): sottrazione mediante violenza o minaccia alla persona.
ReclusionePercosse      = percosse (art. 581): percuotere senza causare malattia.
ReclusioneLesione       = lesioni personali (art. 582): causare una malattia nel corpo o nella mente.
ReclusioneLesioneGrave  = lesioni gravi (art. 582/583): lesione con malattia grave.
ReclusionePreterint     = omicidio preterintenzionale (art. 584): morte non voluta da atti diretti a percuotere/ledere.
ReclusioneLesioneColposa = lesioni colpose (art. 590): lesione causata per colpa."""

SYSTEM = """Sei un giurista esperto del Codice Penale italiano e fai da ANNOTATORE
INDIPENDENTE. Ti viene dato un FATTO (storia in italiano) e l'INTERO CATALOGO dei
reati possibili. Ragiona con calma, elemento per elemento, e stabilisci se la
persona descritta e' punibile e per QUALE singolo reato (l'atomo-pena piu'
specifico che si applica: vale la lex specialis, scegli il reato piu' specifico
i cui elementi sono tutti presenti). Considera anche scriminanti (legittima
difesa, stato di necessita') e non imputabilita' (minore di 14 anni, vizio
totale di mente).

CATALOGO DEI REATI (atomo-pena = descrizione):
""" + CATALOGUE + """

Rispondi SOLO con JSON valido:
{"reasoning":"<ragionamento elemento-per-elemento, 2-4 frasi>",
 "verdict":"offence"|"no-offence"|"unresolved",
 "offence":"<atomo-pena>"|null}"""


def load_llm_only(path):
    """offence-id predicted by the single-pass llm_only arm, keyed by item id."""
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path):
        r = json.loads(line)
        if r.get("arm") == "llm_only":
            out[r["id"]] = (r.get("pred") or {}).get("offence")
    return out


def main():
    ds = os.path.join(EVAL, "dataset", "v0_pilot.jsonl")
    items = [json.loads(l) for l in open(ds)]
    llm_only = load_llm_only(os.path.join(EVAL, "results", "predictions.jsonl"))

    # only items whose gold IS an offence (offence-ID is defined there)
    items = [it for it in items if it["gold"].get("offence")]
    print(f"# E2 independent annotator ({llm.PROVIDER}/{llm.MODEL}) on {len(items)} offence items\n")

    agree_indep = agree_llm = n = 0
    rows = []
    for it in items:
        gold = it["gold"]["offence"]
        user = f"FATTO:\n{it['narrative']}\n\nDOMANDA: {it['question']}"
        try:
            c = llm.complete(SYSTEM, user, max_tokens=700)
            pred = json.loads(c.text)
            ind = pred.get("offence")
        except Exception as e:
            ind = f"ERR:{e}"
        lo = llm_only.get(it["id"])
        a_i = (ind == gold); a_l = (lo == gold)
        agree_indep += a_i; agree_llm += a_l; n += 1
        rows.append((it["id"], gold, ind, lo, a_i))
        print(f"{it['id']:<14} gold={gold:<24} indep={str(ind):<24} {'OK' if a_i else 'XX'}  (llm_only={lo})")

    print(f"\n# independent-annotator agreement w/ engine gold : {agree_indep}/{n} = {round(100*agree_indep/n)}%")
    print(f"# single-pass llm_only agreement w/ engine gold  : {agree_llm}/{n} = {round(100*agree_llm/n)}%")
    print("# (high indep agreement => engine gold is legally sound, not self-marked)")


if __name__ == "__main__":
    main()
