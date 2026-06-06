#!/usr/bin/env python3
"""C2 benchmark piece 4 (E8) — the decisive OOD test. The grammar spec DEFINES the
contrary-to-duty chain operator `A * B` but the worked example only shows a simple
permission-exception (no `*`). The test clause REQUIRES a CTD chain (late rent ->
rent + penalty), a structure the example never demonstrates. Question: can the model
deploy a *described-but-not-exemplified* deontic construct on a novel clause shape?
Scored end-to-end: in the 'paid late' scenario the engine must derive O(PayPenalty)."""
import json, os, subprocess, urllib.request, re

# Provider switch: default OpenAI; set DEONTIC_LLM_PROVIDER=openrouter for a 2nd model.
PROVIDER = os.environ.get("DEONTIC_LLM_PROVIDER", "openai")
if PROVIDER == "openrouter":
    KEY = os.environ["OPENROUTER_API_KEY"]
    ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = os.environ.get("DEONTIC_LLM_MODEL", "deepseek/deepseek-chat")
else:
    KEY = os.environ["OPENAI_API_KEY"]
    ENDPOINT = "https://api.openai.com/v1/chat/completions"
    MODEL = os.environ.get("DEONTIC_LLM_MODEL", "gpt-4.1")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
BIN = os.path.join(REPO, ".lake", "build", "bin", "deontic")

GRAMMAR = """Sei un esperto di logica deontica defeasible. Formalizza la clausola in .ddl.
SINTASSI (rispettala ESATTAMENTE):
- Prima riga: `facts:`
- Atomi: `atom Nome: descrizione | quote: citazione`
- Congiunzione nel corpo = VIRGOLA. Obbligo `=>O@Bearer`, permesso `~>O@Bearer`, negazione `~A`.
- Etichette uniche; superiorità fra etichette: `et2 > et1`.
- CATENA CONTRARY-TO-DUTY (compensazione): nella conclusione, `A * B` significa
  O(A); se A è violato, sorge l'obbligo secondario O(B). Esempio di forma: `=>O@X A * B`.

ESEMPIO COMPLETO (clausola: "Vietato fumare; ma è permesso fumare nell'area fumatori"):
facts:
atom Fuma: il soggetto fuma | quote: "fumare"
atom AreaFumatori: il soggetto è nell'area fumatori | quote: "area fumatori"
divieto: =>O@Soggetto ~Fuma
eccezione: AreaFumatori ~>O@Soggetto Fuma
eccezione > divieto

Rispondi SOLO con JSON {"ddl":"<file completo>","penalty_atom":"<atomo penale secondario>","late_assume":["<atomi veri nello scenario 'pagato in ritardo'>"]}."""

PROSE = '''Formalizza (NB: struttura diversa dall'esempio):
"L'inquilino deve pagare l'affitto entro il primo del mese. Se paga in ritardo,
deve pagare l'affitto maggiorato di una penale del 10%."'''


def ask():
    body = {"model": MODEL,
            "messages": [{"role": "system", "content": GRAMMAR},
                         {"role": "user", "content": PROSE}],
            "response_format": {"type": "json_object"}, "max_completion_tokens": 800}
    req = urllib.request.Request(ENDPOINT,
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(json.loads(r.read().decode())["choices"][0]["message"]["content"])


def run(args):
    p = subprocess.run([BIN] + args, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()


a = ask()
ddl, pen, late = a["ddl"], a.get("penalty_atom", ""), a.get("late_assume", [])
path = "/tmp/ood_rent.ddl"
open(path, "w").write(ddl)
print("# LLM-emitted .ddl (OOD: CTD chain, only permission-exception was exemplified):\n" + ddl.strip())
uses_star = "*" in ddl
chk = run(["check", path])
loads = "error" not in chk.lower()
print("=" * 60)
print(f"# uses `*` CTD operator? {uses_star}   loads? {loads}")
out = run(["query", path, pen, "--assume", ",".join(late)]) if pen and late else "(no penalty_atom/late_assume)"
print(f"\n# scenario 'paid late' → query {pen} assume={late} (gold: O({pen})):")
print(out[:400])
print(f"\n# OOD end-to-end PASS? {uses_star and loads and ('O(' + pen + ')') in out}")
