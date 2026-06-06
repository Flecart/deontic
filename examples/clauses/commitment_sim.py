#!/usr/bin/env python3
"""C7 commitment-device experiment. Same contract + same facts (seller delivered
LATE, penalty unpaid). Ask gpt-4.1 to argue as each SELF-INTERESTED party whether
the late penalty is owed. If they diverge (each favouring itself), a shared
deterministic referee — the engine — is what lets them pre-commit to one verdict.
The engine's answer (already computed): O(PayPenalty) — the seller owes it."""
import json, os, sys, urllib.request

KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ.get("DEONTIC_LLM_MODEL", "gpt-4.1")

CONTRACT = """CONTRATTO (sintetico):
- Il venditore deve consegnare la merce ENTRO la scadenza pattuita.
- Se la consegna è in ritardo, il venditore deve pagare all'acquirente una PENALE di mora.
- L'acquirente deve pagare il prezzo alla consegna.

FATTI DEL CASO:
- Il venditore HA consegnato la merce, ma DOPO la scadenza (consegna in ritardo).
- La penale non è ancora stata pagata; il prezzo non è ancora stato pagato.

DOMANDA: il venditore deve pagare la penale di mora? Sì o no, e perché (1-2 frasi)."""

ROLES = {
    "SELLER": "Sei l'avvocato del VENDITORE. Il tuo cliente vuole NON pagare la penale. "
              "Difendi i suoi interessi nel modo legalmente più difendibile.",
    "BUYER":  "Sei l'avvocato dell'ACQUIRENTE. Il tuo cliente vuole RISCUOTERE la penale. "
              "Difendi i suoi interessi nel modo legalmente più difendibile.",
    "NEUTRAL":"Sei un arbitro NEUTRALE e imparziale. Decidi secondo il contratto, senza favorire nessuno.",
}


def ask(system):
    body = {"model": MODEL,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": CONTRACT}],
            "response_format": {"type": "json_object"},
            "max_completion_tokens": 300}
    sys_json = system + '\n\nRispondi SOLO con JSON: {"penale_dovuta": true|false, "motivo": "..."}'
    body["messages"][0]["content"] = sys_json
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode())
    return json.loads(d["choices"][0]["message"]["content"])


print("# C7 commitment-device sim — same contract, same facts, 3 stances\n")
verdicts = {}
for role, sysmsg in ROLES.items():
    a = ask(sysmsg)
    verdicts[role] = a["penale_dovuta"]
    print(f"{role:<8} penale_dovuta={str(a['penale_dovuta']):<6} — {a['motivo']}")

print("\nENGINE   penale_dovuta=True   — O(PayPenalty): primary duty DeliverOnTime violated, CTD activates (deterministic)")
diverge = len(set(verdicts.values())) > 1
print(f"\n# self-interested parties diverge? {diverge}  (seller={verdicts['SELLER']}, buyer={verdicts['BUYER']})")
print("# the engine is the shared referee both can pre-commit to regardless of who argues.")
