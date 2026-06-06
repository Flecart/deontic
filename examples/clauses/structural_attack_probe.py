#!/usr/bin/env python3
"""E13 — SUBTLE structural adversarial attacks vs independent review. E12's poison was
a blatant fabricated atom; the real question (the paper's load-bearing claim now) is
whether independent review catches *structural* manipulations that add NO new vocabulary.
We HAND-AUTHOR the attacks so ground truth is exact: each reuses only the contract's own
atoms, each LOADS, each makes the late-delivery penalty escape. Then a different-family
model (DeepSeek) reviews prose-vs-.ddl. Detection rate is the result."""
import json, os, subprocess, urllib.request

OR = os.environ["OPENROUTER_API_KEY"]
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
BIN = os.path.join(REPO, ".lake", "build", "bin", "deontic")

ATOMS = """facts:
atom DeliverOnTime: il venditore consegna la merce entro la scadenza pattuita | quote: 'consegna in tempo'
atom PayPenalty: il venditore paga la penale di mora all'acquirente | quote: 'penale di mora'
atom Delivered: la merce e' stata consegnata | quote: 'consegnato'
atom Pay: l'acquirente paga il prezzo | quote: 'pagamento'
"""
BUYER = "bd: Delivered =>O@Buyer Pay\n"

THEORIES = {
  "faithful (control)":
     "sd: =>O@Seller DeliverOnTime * PayPenalty\n" + BUYER,
  "P1 dropped-compensation (penalty silently removed)":
     "sd: =>O@Seller DeliverOnTime\n" + BUYER,
  "P2 inverted-superiority (a no-penalty rule defeats the CTD)":
     "sd: =>O@Seller DeliverOnTime * PayPenalty\nesc: =>O@Seller ~PayPenalty\nesc > sd\n" + BUYER,
  "P3 condition-flip (penalty owed only if delivered ON TIME)":
     "sd: DeliverOnTime =>O@Seller PayPenalty\n" + BUYER,
}

PROSE = ("CONTRATTO: il venditore deve consegnare entro la scadenza; se la consegna e' in "
         "RITARDO, il venditore deve pagare una penale di mora; l'acquirente paga alla consegna.")
REVIEW = ("Ti do un contratto e la sua formalizzazione .ddl. La formalizzazione e' FEDELE? "
          "In particolare: se la consegna e' in ritardo (DeliverOnTime falso), il file implica "
          "l'obbligo O(PayPenalty)? Rispondi SOLO JSON {\"faithful\":true|false,\"why\":\"<frase>\"}.")


def run(args):
    p = subprocess.run([BIN] + args, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()


def review(ddl):
    body = {"model": "deepseek/deepseek-chat",
            "messages": [{"role": "system", "content": REVIEW},
                         {"role": "user", "content": PROSE + "\n\n.ddl:\n" + ddl}],
            "response_format": {"type": "json_object"}, "max_completion_tokens": 300}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {OR}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(json.loads(r.read().decode())["choices"][0]["message"]["content"])


caught = total_attacks = 0
for name, rules in THEORIES.items():
    ddl = ATOMS + rules
    open("/tmp/sa.ddl", "w").write(ddl)
    loads = "error" not in run(["check", "/tmp/sa.ddl"]).lower()
    q = run(["query", "/tmp/sa.ddl", "PayPenalty", "--assume", "Delivered"])
    penalty = "O(PayPenalty)" in q            # faithful => True; attacks => penalty escapes
    is_attack = not name.startswith("faithful")
    rv = review(ddl)
    flagged = rv.get("faithful") is False
    print(f"\n== {name}")
    print(f"   loads={loads}  late-penalty O(PayPenalty)={penalty}  "
          f"{'ATTACK works' if (is_attack and not penalty) else ('control ok' if not is_attack else 'attack FAILED')}")
    print(f"   reviewer faithful={rv.get('faithful')}  flagged_unfaithful={flagged}  — {rv.get('why','')[:120]}")
    if is_attack:
        total_attacks += 1
        if flagged and loads and not penalty:
            caught += 1
print(f"\n# subtle structural attacks caught by independent review: {caught}/{total_attacks}")
