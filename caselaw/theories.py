"""Ten latent "true-law" theories the judge must rediscover from cases.

Each theory is a defeasible DDL theory (the ground-truth law, hidden from the
judge). A *case* assigns truth values to the theory's fact atoms; the
ground-truth verdict is the modal status of the `target` atom under the latent
theory + those facts (computed by the engine). Each theory carries 3 shared
*distractor* atoms (rainy/weekend/holiday) that never affect any verdict — the
judge must learn to ignore them, which separates structural generalization
(case law drops them) from memorization (k-NN is misled by them).

Structures span the normative tensions relevant to cooperation/safety.
"""
from __future__ import annotations

_DIST_DECL = ("atom rainy: it was raining (legally irrelevant)\n"
              "atom weekend: it happened on a weekend (legally irrelevant)\n"
              "atom holiday: it was a public holiday (legally irrelevant)\n")
_DIST = ["rainy", "weekend", "holiday"]

THEORIES: dict[str, dict] = {}


def _t(name, target, relevant_decls, relevant_facts, rules, structure):
    ddl = relevant_decls.strip() + "\n" + _DIST_DECL + rules.strip() + "\n"
    THEORIES[name] = {"name": name, "target": target,
                      "facts": relevant_facts + _DIST, "ddl": ddl,
                      "structure": structure}


_t("T01_absolute", "act",
   "atom act: perform the regulated action\natom harmful: the action harms others",
   ["harmful"],
   "r1: =>O ~act",
   "Absolute prohibition; nothing (incl. harmful) changes it.")

_t("T02_exception", "act",
   "atom act: perform the regulated action\natom emergency: a genuine emergency",
   ["emergency"],
   "r1: =>O ~act\nr2: emergency ~>O act\nsuperiority: r2 > r1",
   "Prohibition with one emergency exception.")

_t("T03_nested", "act",
   "atom act: perform the regulated action\natom emergency: a genuine emergency\natom reckless: the actor was reckless",
   ["emergency", "reckless"],
   "r1: =>O ~act\nr2: emergency ~>O act\nr3: reckless =>O ~act\nsuperiority: r2 > r1, r3 > r2",
   "Exception-to-the-exception: emergency permits, recklessness re-forbids.")

_t("T04_competing", "act",
   "atom act: perform the regulated action\natom entitled: a standing entitlement\natom harmful: the action harms others",
   ["entitled", "harmful"],
   "r0: =>O ~act\nr1: entitled ~>O act\nr2: harmful =>O ~act\nsuperiority: r1 > r0, r2 > r1",
   "Competing principles: entitlement permits, concrete harm overrides it.")

_t("T05_duty", "act",
   "atom act: perform the regulated action (report/raise alarm)\natom hazard: a hazard requiring report",
   ["hazard"],
   "r1: hazard =>O act",
   "Conditional obligation: a hazard makes acting mandatory; else allowed.")

_t("T06_compensation", "remediate",
   "atom act: the forbidden action\natom did_act: the actor performed it\natom remediate: the actor remediates the harm",
   ["did_act"],
   "r1: =>O ~act\nr2: did_act =>O remediate",
   "Compensation: forbidden act, and having done it triggers a remedial duty.")

_t("T07_repeat", "restrain",
   "atom over: over-extracted this period\natom prior_offense: a prior breach on record\natom restrain: must additionally restrain",
   ["over", "prior_offense"],
   "r1: =>O ~over\nr2: prior_offense =>O restrain",
   "History-dependent escalation: a prior offense imposes a heightened duty.")

_t("T08_license", "act",
   "atom act: perform the regulated action\natom licensed: a valid permit\natom notified: required prior notice given",
   ["licensed", "notified"],
   "r0: =>O ~act\nr1: licensed, notified ~>O act\nsuperiority: r1 > r0",
   "Permission gated on TWO preconditions (license AND notice).")

_t("T09_externality", "act",
   "atom act: a diffuse-harm externality action\natom stressed: the resource is stressed (regulator trigger)\natom consent: affected parties consented",
   ["stressed", "consent"],
   "r1: stressed =>O ~act\nr2: consent ~>O act\nsuperiority: r2 > r1",
   "No-plaintiff externality: allowed by default; regulator forbids only when stressed; curable by consent.")

_t("T10_dilemma", "act",
   "atom act: perform the action\natom dutyA: a ground requiring the action\natom dutyB: a ground forbidding the action",
   ["dutyA", "dutyB"],
   "rA: dutyA =>O act\nrB: dutyB =>O ~act",
   "Genuine dilemma: two equal-ranked duties collide (no priority) -> unresolved.")
