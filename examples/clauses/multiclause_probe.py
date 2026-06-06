#!/usr/bin/env python3
"""C2 benchmark piece 5 (E10) — the scale/falsification test. A 5-clause contract
with INTERACTING defeasibility (non-payment defeats the service duty; a security
incident triggers a contrary-to-duty notify->compensate chain). Tests whether the
model keeps a consistent atom vocabulary across many rules, wires superiorities
correctly, and yields right verdicts on cross-clause scenarios. This is the only
remaining experiment that could FALSIFY (not merely tighten) the paper's thesis."""
import json, os, subprocess, urllib.request

PROVIDER = os.environ.get("DEONTIC_LLM_PROVIDER", "openai")
if PROVIDER == "openrouter":
    KEY = os.environ["OPENROUTER_API_KEY"]; ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = os.environ.get("DEONTIC_LLM_MODEL", "deepseek/deepseek-chat")
else:
    KEY = os.environ["OPENAI_API_KEY"]; ENDPOINT = "https://api.openai.com/v1/chat/completions"
    MODEL = os.environ.get("DEONTIC_LLM_MODEL", "gpt-4.1")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
BIN = os.path.join(REPO, ".lake", "build", "bin", "deontic")

GRAMMAR = """Sei un esperto di logica deontica defeasible. Formalizza il CONTRATTO (piu' clausole) in .ddl.
SINTASSI (esatta): prima riga `facts:`; `atom Nome: descrizione | quote: ...`; congiunzione = VIRGOLA;
obbligo `et: CORPO =>O@Bearer C`, permesso `et: CORPO ~>O@Bearer C`, negazione `~A`; etichette UNICHE;
superiorita' fra etichette `etB > etA`; catena contrary-to-duty `=>O@X A * B` (O(A); se A violato, O(B)).
Usa lo STESSO nome di atomo ovunque (coerenza lessicale). Rispondi SOLO con JSON:
{"ddl":"<file>","atoms":{"provide":"<atomo erogare servizio>","pay":"<atomo pagamento>",
"suspend":"<atomo sospendere>","notify":"<atomo notificare>","compensate":"<atomo compensare>"},
"assume_overdue":["<atomi veri nello scenario: cliente NON paga / pagamento scaduto>"],
"assume_incident_unnotified":["<atomi veri: incidente di sicurezza, NON notificato>"]}"""

CONTRACT = """CONTRATTO SaaS (5 clausole):
1. Il fornitore deve erogare il servizio.
2. Il cliente deve pagare il canone mensile.
3. Se il pagamento e' scaduto (non pagato), il fornitore PUO' sospendere il servizio,
   e in tal caso viene meno l'obbligo di erogare il servizio (questa clausola prevale sulla clausola 1).
4. Se si verifica un incidente di sicurezza, il fornitore deve notificarlo al cliente;
   se non lo notifica, deve compensare il cliente (obbligo secondario).
5. In caso di forza maggiore, il fornitore e' esonerato dall'obbligo di erogare il servizio
   (questa clausola prevale sulla clausola 1)."""


def ask():
    body = {"model": MODEL, "messages": [{"role": "system", "content": GRAMMAR},
            {"role": "user", "content": CONTRACT}],
            "response_format": {"type": "json_object"}, "max_completion_tokens": 1100}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(json.loads(r.read().decode())["choices"][0]["message"]["content"])


def run(args):
    p = subprocess.run([BIN] + args, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()


a = ask()
ddl, atoms = a["ddl"], a.get("atoms", {})
path = "/tmp/multiclause.ddl"
open(path, "w").write(ddl)
print("# LLM-emitted 5-clause .ddl:\n" + ddl.strip() + "\n" + "=" * 60)
chk = run(["check", path]); loads = "error" not in chk.lower()
print(f"# loads? {loads}")
if not loads:
    print("LOAD ERR: " + (chk.splitlines()[0] if chk else ""))

import re
# Parse real atom TOKENS from the ddl (don't trust the model's atoms map, which
# returned descriptions); match concepts by keyword in their descriptions.
decls = dict(re.findall(r"^\s*atom\s+(\w+)\s*:\s*([^|\n]+)", ddl, re.M))
def find(*kw):
    for tok, desc in decls.items():
        if any(k in desc.lower() for k in kw):
            return tok
    return ""
prov = find("eroga", "servizio") or "provide"
comp = find("compens") or "compensate"
# S1: security incident, not notified -> expect O(compensate)
s1 = run(["query", path, comp, "--assume", ",".join(a.get("assume_incident_unnotified", []))]) if comp else "(no atom)"
s1_ok = f"O({comp})" in s1
# S2: payment overdue -> vendor's duty to provide service should be DEFEATED (not O(provide))
s2 = run(["query", path, prov, "--assume", ",".join(a.get("assume_overdue", []))]) if prov else "(no atom)"
s2_ok = f"O({prov})" not in s2
print(f"\n# S1 incident-unnotified → query {comp}: expect O({comp})  | got:")
print("  " + s1.replace(chr(10), chr(10) + "  ")[:220])
print(f"  S1 PASS={s1_ok}")
print(f"\n# S2 payment-overdue → query {prov}: expect service duty DEFEATED (no O({prov}))  | got:")
print("  " + s2.replace(chr(10), chr(10) + "  ")[:220])
print(f"  S2 PASS={s2_ok}")
print(f"\n# MULTI-CLAUSE END-TO-END: loads={loads}  S1={s1_ok}  S2={s2_ok}")
