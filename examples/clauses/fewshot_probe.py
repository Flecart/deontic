#!/usr/bin/env python3
"""C2 benchmark piece 3 (E7) — isolate the two bottleneck layers. Re-run the two
E6 clauses that FAILED TO LOAD, now WITH a few-shot syntax spec (one fully worked
permission+superiority example showing comma-conjunction, distinct labels, `~>` on
the act, and `specific > general`). Prediction: the SYNTAX layer is scaffolding-
solvable (they now load); the open question is whether SEMANTICS (permission on the
act, superiority direction) also come out right. Grades: loads · uses_~> · superiority
references real labels · (manual read for direction)."""
import json, os, subprocess, urllib.request, re

KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ.get("DEONTIC_LLM_MODEL", "gpt-4.1")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
BIN = os.path.join(REPO, ".lake", "build", "bin", "deontic")

GRAMMAR = """Sei un esperto di logica deontica defeasible. Formalizza la clausola in .ddl.
REGOLE DI SINTASSI (rispettale ESATTAMENTE):
- Prima riga: `facts:`
- Dichiara ogni atomo: `atom Nome: descrizione | quote: citazione`
- Congiunzione nel corpo = VIRGOLA (NON `&`):  `et: A, B =>O@Bearer C`
- Obbligo `=>O@Bearer`, permesso `~>O@Bearer`, negazione `~A`.
- Ogni regola ha UN'ETICHETTA UNICA (et1, et2, ...).
- Superiorità SOLO fra etichette di regole: `et2 > et1` (et2 prevale su et1).

ESEMPIO COMPLETO (clausola: "Vietato fumare; ma è permesso fumare nell'area fumatori"):
facts:
atom Fuma: il soggetto fuma | quote: "fumare"
atom AreaFumatori: il soggetto si trova nell'area fumatori designata | quote: "area fumatori"
divieto: =>O@Soggetto ~Fuma
eccezione: AreaFumatori ~>O@Soggetto Fuma
eccezione > divieto

Rispondi SOLO con JSON {"ddl":"<file completo, stessa forma dell'esempio>"}."""

CLAUSES = {
    "weekend_oncall": '"I dipendenti non devono lavorare nei fine settimana. Tuttavia, il '
        'personale di reperibilità per emergenze può essere chiamato a lavorare nei fine settimana."',
    "no_pets_service": '"Agli inquilini è vietato tenere animali. È consentito tenere un cane '
        'guida per persone non vedenti."',
}


def ask(prose):
    body = {"model": MODEL,
            "messages": [{"role": "system", "content": GRAMMAR},
                         {"role": "user", "content": "Formalizza:\n" + prose}],
            "response_format": {"type": "json_object"}, "max_completion_tokens": 800}
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(json.loads(r.read().decode())["choices"][0]["message"]["content"])["ddl"]


def run(args):
    p = subprocess.run([BIN] + args, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()


for name, prose in CLAUSES.items():
    ddl = ask(prose)
    path = f"/tmp/fs_{name}.ddl"
    open(path, "w").write(ddl)
    chk = run(["check", path])
    loads = "error" not in chk.lower()
    labels = set(re.findall(r"^\s*(\w+):", ddl, re.M))
    sup = re.findall(r"^\s*(\w+)\s*>\s*(\w+)\s*$", ddl, re.M)
    sup_valid = all(a in labels and b in labels for a, b in sup) and bool(sup)
    print(f"\n===== {name} =====")
    print(ddl.strip())
    print(f"--- loads={loads}  uses_~>={'~>O' in ddl}  superiority={sup}  refs_real_labels={sup_valid}")
    if not loads:
        print("    LOAD ERR: " + chk.splitlines()[0][:160] if chk else "")
