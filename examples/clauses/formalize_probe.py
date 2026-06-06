#!/usr/bin/env python3
"""C2 formalization-fidelity probe. Give gpt-4.1 a prose contract + a compact DDL
grammar, ask it to emit a .ddl, then LOAD it in the engine and check it reproduces
the gold verdict O(PayPenalty) on the late-delivery scenario. Tests (a) round-trip
fidelity and (b) whether a wrong formalization surfaces as a load error / wrong
verdict (auditability, C3) rather than silently."""
import json, os, subprocess, urllib.request

KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ.get("DEONTIC_LLM_MODEL", "gpt-4.1")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
BIN = os.path.join(REPO, ".lake", "build", "bin", "deontic")

GRAMMAR = """GRAMMATICA DDL (defeasible deontic logic), minimale:
- Inizia con una riga `facts:` (può essere vuota).
- Ogni atomo USATO va dichiarato: `atom Nome: descrizione in chiaro | quote: una citazione`
- Regola prescrittiva di obbligo:  `etichetta: CORPO =>O@Bearer  CONCLUSIONE`
    * CORPO = lista di atomi separati da virgola (può essere vuoto).
    * `~Atomo` = negazione.
    * CONCLUSIONE può essere una catena compensatoria (contrary-to-duty):
      `Primario * Secondario` significa O(Primario); se violato, O(Secondario).
- `@Bearer` indica chi porta il dovere (es. @Seller, @Buyer).
Esempio:  seller_duty: =>O@Seller DeliverOnTime * PayPenalty"""

PROSE = """CONTRATTO da formalizzare in DDL:
1. Il venditore (Seller) deve consegnare la merce ENTRO la scadenza pattuita
   (atomo suggerito: DeliverOnTime). Se NON la consegna in tempo, sorge il dovere
   secondario di pagare una penale di mora (atomo: PayPenalty).
2. Una volta che la merce è stata consegnata (atomo: Delivered), l'acquirente
   (Buyer) deve pagare il prezzo (atomo: Pay).

Produci SOLO il testo del file .ddl, niente altro."""


def ask():
    body = {"model": MODEL,
            "messages": [{"role": "system", "content": GRAMMAR},
                         {"role": "user", "content": PROSE}],
            "max_completion_tokens": 500}
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode())
    return d["choices"][0]["message"]["content"]


ddl = ask()
# strip markdown fences if present
ddl = ddl.replace("```ddl", "```").split("```")[1] if "```" in ddl else ddl
path = "/tmp/llm_formalized.ddl"
open(path, "w").write(ddl)
print("# LLM-emitted .ddl:\n" + ddl.strip() + "\n" + "=" * 60)

def run(args):
    p = subprocess.run([BIN] + args, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()

print("\n# engine LOAD (deontic check):")
print(run(["check", path]) or "(ok, no errors)")
print("\n# scenario: Delivered but late (query PayPenalty Pay --assume Delivered):")
out = run(["query", path, "PayPenalty", "Pay", "--assume", "Delivered"])
print(out)
gold_ok = "O(PayPenalty)" in out
print(f"\n# reproduces gold O(PayPenalty)? {gold_ok}")
