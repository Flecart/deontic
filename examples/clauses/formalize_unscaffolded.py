#!/usr/bin/env python3
"""C2 benchmark piece 1 (E5) — UNSCAFFOLDED formalization. Give gpt-4.1 the NDA
disclosure clause as pure prose: no atom names, no mention of the defeat/superiority
relation that makes the specific permission override the general prohibition. Ask it
to emit (a) the .ddl and (b) its OWN assume-config naming which of its atoms encode
"an employee who has been made aware of the terms and the liability". Then score
end-to-end: gold says disclosure is PERMITTED in that case (P(Disclose)). Targets the
predicted failure mode: silently dropping defeasibility -> permission never fires."""
import json, os, subprocess, urllib.request, re

KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ.get("DEONTIC_LLM_MODEL", "gpt-4.1")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
BIN = os.path.join(REPO, ".lake", "build", "bin", "deontic")

GRAMMAR = """Sei un esperto di logica deontica defeasible. Devi formalizzare una clausola in un file .ddl.
GRAMMATICA (minimale):
- Prima riga `facts:` (può essere vuota).
- Ogni atomo usato va dichiarato: `atom Nome: descrizione | quote: citazione`
- Obbligo:    `etichetta: CORPO =>O@Bearer  CONCL`   (CORPO = atomi separati da virgola; `~A` = negazione)
- Permesso:   `etichetta: CORPO ~>O@Bearer  CONCL`
- Una regola può DEFErire un'altra: `etichetta_forte > etichetta_debole` (la prima prevale in conflitto).
Pensa a quali norme sono in conflitto e quale deve prevalere."""

PROSE = """Formalizza questa clausola NDA:
"Il Disclosee farà in modo che, PRIMA della divulgazione a qualunque altra persona
(incluso un consulente professionale) di Informazioni Riservate, tale persona sia
resa consapevole delle disposizioni dell'Accordo e del fatto che il Disclosee sarà
responsabile. Inoltre, la Parte Ricevente PUÒ condividere alcune Informazioni
Riservate con alcuni dei propri dipendenti."

Rispondi SOLO con JSON:
{"ddl": "<testo completo del file .ddl>",
 "assume_permitted": ["<atomi, fra i TUOI, da porre veri perché la divulgazione a un dipendente reso pienamente consapevole sia PERMESSA>"],
 "disclose_atom": "<il nome del TUO atomo che rappresenta 'divulgare'>"}"""


def ask():
    body = {"model": MODEL,
            "messages": [{"role": "system", "content": GRAMMAR},
                         {"role": "user", "content": PROSE}],
            "response_format": {"type": "json_object"},
            "max_completion_tokens": 900}
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(json.loads(r.read().decode())["choices"][0]["message"]["content"])


a = ask()
ddl, assume, datom = a["ddl"], a.get("assume_permitted", []), a.get("disclose_atom", "")
path = "/tmp/llm_unscaffolded.ddl"
open(path, "w").write(ddl)
print("# LLM-emitted .ddl (UNSCAFFOLDED):\n" + ddl.strip())
has_super = bool(re.search(r"^\s*\w+\s*>\s*\w+\s*$", ddl, re.M))
print("=" * 60)
print(f"# contains a defeat/superiority relation (`a > b`)? {has_super}")

def run(args):
    p = subprocess.run([BIN] + args, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()

print("\n# load (deontic check):")
print((run(["check", path]) or "(ok)")[:400])
print(f"\n# query {datom} with assume={assume} (gold: PERMITTED, i.e. P / not O(~)):")
out = run(["query", path, datom, "--assume", ",".join(assume)]) if assume and datom else "(model gave no assume/atom)"
print(out[:500])
permitted = bool(re.search(r"P\(", out)) or (datom and f"O(~{datom})" not in out and "+∂_O" not in out.split(datom)[0][-12:] if datom in out else False)
print(f"\n# end-to-end: disclosure permitted in the aware-employee case? structural_defeat={has_super}")
