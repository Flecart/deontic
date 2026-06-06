#!/usr/bin/env python3
"""C2 benchmark piece 2 (E6) — replication. Does E5's failure mode (reifying
permission as an obligated proposition; getting the defeat direction wrong) recur
on FRESH unscaffolded permission-exception clauses? Structural diagnostics per clause:
  loads? · uses the `~>` permission operator at all? · reifies permittedness as an
  atom (bad)? · has a `>` superiority line?
Gold structure for all three: a `~>` permission on the ACT, with the SPECIFIC
exception rule defeating the GENERAL prohibition."""
import json, os, subprocess, urllib.request, re

KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ.get("DEONTIC_LLM_MODEL", "gpt-4.1")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
BIN = os.path.join(REPO, ".lake", "build", "bin", "deontic")

GRAMMAR = """Sei un esperto di logica deontica defeasible. Formalizza la clausola in un file .ddl.
GRAMMATICA: prima riga `facts:`; dichiara ogni atomo `atom Nome: descrizione | quote: ...`;
obbligo `et: CORPO =>O@Bearer CONCL`; permesso `et: CORPO ~>O@Bearer CONCL`; `~A` = negazione;
una regola può deferirne un'altra con `et_forte > et_debole`.
Rispondi SOLO con JSON {"ddl":"<file completo>"}."""

CLAUSES = {
    "weekend_oncall": '"I dipendenti non devono lavorare nei fine settimana. Tuttavia, il '
        'personale di reperibilità per emergenze può essere chiamato a lavorare nei fine settimana."',
    "no_pets_service": '"Agli inquilini è vietato tenere animali nell\'appartamento. È '
        'comunque consentito tenere un cane guida per persone non vedenti."',
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


REIFY = re.compile(r"atom\s+\w*(permess|permit|consent|allow|lecit|permitted)\w*", re.I)
SUPER = re.compile(r"^\s*\w+\s*>\s*\w+\s*$", re.M)
PERMOP = re.compile(r"~>O")

for name, prose in CLAUSES.items():
    ddl = ask(prose)
    path = f"/tmp/rep_{name}.ddl"
    open(path, "w").write(ddl)
    loads = "error" not in run(["check", path]).lower()
    uses_perm = bool(PERMOP.search(ddl))
    reifies = bool(REIFY.search(ddl))
    has_super = bool(SUPER.search(ddl))
    print(f"\n===== {name} =====")
    print(ddl.strip())
    print(f"--- loads={loads}  uses_~>={uses_perm}  reifies_permission={reifies}  has_superiority={has_super}")
