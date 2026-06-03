#!/usr/bin/env python3
"""Generate a large ambiguous ContractNLI-style benchmark.

The examples are synthetic but legal-flavoured: each clause contains defaults,
exceptions, exception-to-exception rules, priority language, and irrelevant
distractor facts. Gold labels are derived from the companion DDL theory for the
same clause, so every item has an auditable formal source of truth.
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import random
from dataclasses import dataclass


DISTRACTORS = {
    "UrgentReview": "the matter is being reviewed urgently",
    "QuarterEnd": "it is near quarter-end",
}


@dataclass(frozen=True)
class Template:
    tid: str
    target: str
    act: str
    gerund: str
    atoms: dict[str, str]
    rules: str
    clause: str

    def ddl(self) -> str:
        atoms = {self.target: self.act, **self.atoms, **DISTRACTORS}
        decls = "\n".join(f"atom {name}: {desc}" for name, desc in atoms.items())
        return decls + "\n" + self.rules.strip() + "\n"

    @property
    def facts(self) -> list[str]:
        return list(self.atoms)


TEMPLATES = [
    Template(
        "disclosure", "Disclose", "disclose confidential information",
        "disclosing confidential information",
        {
            "EmployeeNeed": "the recipient is an employee with a need to know",
            "PublicDomain": "the information is already public through no breach",
            "RegulatorDemand": "a regulator has demanded disclosure",
            "CompetitorRecipient": "the recipient is a competitor",
        },
        """
default_no: =>O ~Disclose
employee_ok: EmployeeNeed ~>O Disclose
public_ok: PublicDomain ~>O Disclose
regulator_must: RegulatorDemand =>O Disclose
competitor_no: CompetitorRecipient =>O ~Disclose
superiority: employee_ok > default_no, public_ok > default_no, regulator_must > default_no, competitor_no > employee_ok, regulator_must > competitor_no
""",
        "The Receiving Party shall not disclose Confidential Information. It may disclose it to employees with a need to know, and information already public through no breach is excepted. Notwithstanding the employee exception, disclosure to a competitor is prohibited. If a regulator demands disclosure, the Receiving Party shall disclose notwithstanding the foregoing restrictions.",
    ),
    Template(
        "retention", "Retain", "retain covered materials", "retaining covered materials",
        {
            "Terminated": "the agreement has terminated",
            "BackupCopy": "the copy is an automated backup copy",
            "LegalHold": "a legal hold applies",
            "DeletionRequest": "the disclosing party requested deletion",
        },
        """
term_no: Terminated =>O ~Retain
backup_ok: BackupCopy ~>O Retain
hold_must: LegalHold =>O Retain
delete_no: DeletionRequest =>O ~Retain
superiority: backup_ok > term_no, hold_must > term_no, delete_no > backup_ok, hold_must > delete_no
""",
        "Upon termination, the Recipient shall not retain covered materials. Automated backup copies may be retained temporarily. If a deletion request is made, backup retention is not permitted. Notwithstanding any deletion request, materials subject to a legal hold shall be retained.",
    ),
    Template(
        "assignment", "Assign", "assign the agreement", "assigning the agreement",
        {
            "Affiliate": "the assignee is an affiliate",
            "ChangeControl": "the assignment occurs in a change of control",
            "Consent": "the counterparty has given written consent",
            "Competitor": "the assignee is a competitor",
        },
        """
default_no: =>O ~Assign
affiliate_ok: Affiliate ~>O Assign
change_ok: ChangeControl ~>O Assign
consent_ok: Consent ~>O Assign
competitor_no: Competitor =>O ~Assign
superiority: affiliate_ok > default_no, change_ok > default_no, consent_ok > default_no, competitor_no > affiliate_ok, competitor_no > change_ok, consent_ok > competitor_no
""",
        "Neither party may assign this Agreement without written consent. Assignment to an affiliate or in connection with a change of control is permitted. However, assignment to a competitor is prohibited notwithstanding those exceptions, unless the counterparty gives written consent.",
    ),
    Template(
        "subcontracting", "Subcontract", "subcontract the service", "subcontracting the service",
        {
            "BoundByNDA": "the subcontractor is bound by equivalent confidentiality duties",
            "CriticalService": "the service is business-critical",
            "Offshore": "the subcontractor will perform offshore",
            "CustomerConsent": "the customer has approved the subcontractor",
        },
        """
default_no: =>O ~Subcontract
nda_ok: BoundByNDA ~>O Subcontract
critical_no: CriticalService =>O ~Subcontract
offshore_no: Offshore =>O ~Subcontract
consent_ok: CustomerConsent ~>O Subcontract
superiority: nda_ok > default_no, critical_no > nda_ok, offshore_no > nda_ok, consent_ok > critical_no, consent_ok > offshore_no
""",
        "Supplier shall not subcontract the service. A subcontractor bound by equivalent confidentiality obligations may be used. That permission does not apply to business-critical services or offshore performance. Customer approval overrides the critical-service and offshore restrictions.",
    ),
    Template(
        "data_use", "UseData", "use customer data", "using customer data",
        {
            "PurposeFit": "the use is necessary for the contracted purpose",
            "Aggregated": "the data is aggregated and non-identifying",
            "Marketing": "the use is for marketing",
            "OptIn": "the customer opted in",
        },
        """
default_no: =>O ~UseData
purpose_ok: PurposeFit ~>O UseData
aggregate_ok: Aggregated ~>O UseData
marketing_no: Marketing =>O ~UseData
optin_ok: OptIn ~>O UseData
superiority: purpose_ok > default_no, aggregate_ok > default_no, marketing_no > purpose_ok, marketing_no > aggregate_ok, optin_ok > marketing_no
""",
        "Processor shall not use Customer Data except as necessary for the contracted purpose or in aggregated non-identifying form. Marketing use is prohibited notwithstanding those exceptions, unless the customer has opted in.",
    ),
    Template(
        "termination", "Terminate", "terminate the agreement", "terminating the agreement",
        {
            "MaterialBreach": "the other party committed a material breach",
            "CureExpired": "the cure period has expired",
            "Waiver": "the terminating party signed a waiver",
            "Insolvency": "the other party is insolvent",
        },
        """
default_no: =>O ~Terminate
breach_ok: MaterialBreach, CureExpired ~>O Terminate
waiver_no: Waiver =>O ~Terminate
insolvency_ok: Insolvency ~>O Terminate
superiority: breach_ok > default_no, insolvency_ok > default_no, waiver_no > breach_ok, insolvency_ok > waiver_no
""",
        "A party may not terminate this Agreement for breach unless the breach is material and the cure period has expired. A written waiver bars termination for that breach. Notwithstanding a waiver, insolvency permits immediate termination.",
    ),
    Template(
        "price_change", "IncreasePrice", "increase the price", "increasing the price",
        {
            "RenewalWindow": "the change occurs at renewal",
            "Notice30": "thirty days' notice was given",
            "FixedTerm": "the price is in a fixed-term order",
            "TaxChange": "the increase passes through a tax change",
        },
        """
default_no: =>O ~IncreasePrice
renewal_ok: RenewalWindow, Notice30 ~>O IncreasePrice
fixed_no: FixedTerm =>O ~IncreasePrice
tax_ok: TaxChange ~>O IncreasePrice
superiority: renewal_ok > default_no, fixed_no > renewal_ok, tax_ok > fixed_no, tax_ok > default_no
""",
        "Vendor shall not increase prices except at renewal with at least thirty days' notice. Fixed-term order prices may not be increased even at renewal. Tax pass-through increases are permitted notwithstanding the fixed-term restriction.",
    ),
    Template(
        "audit", "Audit", "audit the systems", "auditing the systems",
        {
            "SecurityIncident": "a security incident occurred",
            "CustomerRequest": "the customer requested an audit",
            "ConfidentialRisk": "the audit would expose third-party confidential data",
            "RegulatorOrder": "a regulator ordered the audit",
        },
        """
incident_must: SecurityIncident =>O Audit
request_ok: CustomerRequest ~>O Audit
risk_no: ConfidentialRisk =>O ~Audit
regulator_must: RegulatorOrder =>O Audit
superiority: risk_no > request_ok, regulator_must > risk_no, incident_must > risk_no
""",
        "Customer may audit the systems on request. If a security incident occurs, Supplier shall permit an audit. An audit that would expose third-party confidential data is prohibited, except where required by a regulator or by the security-incident audit obligation.",
    ),
    Template(
        "deletion", "DeleteData", "delete personal data", "deleting personal data",
        {
            "DeletionRequest": "the data subject requested deletion",
            "LegalHold": "a legal hold applies",
            "BackupCopy": "the data is held only in backups",
            "RetentionExpired": "the retention period has expired",
        },
        """
request_must: DeletionRequest =>O DeleteData
expired_must: RetentionExpired =>O DeleteData
hold_no: LegalHold =>O ~DeleteData
backup_ok: BackupCopy ~>O DeleteData
superiority: hold_no > request_must, hold_no > expired_must, request_must > backup_ok, expired_must > backup_ok
""",
        "Provider shall delete personal data on a valid deletion request and when the retention period expires. Data subject to a legal hold shall not be deleted notwithstanding those duties. Backup-only data may be deleted in the ordinary backup cycle.",
    ),
    Template(
        "copying", "Copy", "copy the materials", "copying the materials",
        {
            "InternalUse": "the copy is for internal use",
            "Archival": "the copy is archival",
            "SourceCode": "the materials include source code",
            "WrittenConsent": "written consent was obtained",
        },
        """
default_no: =>O ~Copy
internal_ok: InternalUse ~>O Copy
archive_ok: Archival ~>O Copy
source_no: SourceCode =>O ~Copy
consent_ok: WrittenConsent ~>O Copy
superiority: internal_ok > default_no, archive_ok > default_no, source_no > internal_ok, source_no > archive_ok, consent_ok > source_no
""",
        "Licensee shall not copy the materials. Internal-use and archival copies are permitted. Copies containing source code are prohibited notwithstanding those permissions, unless Licensor gives written consent.",
    ),
    Template(
        "customer_contact", "ContactCustomer", "contact the customer", "contacting the customer",
        {
            "ExistingRelationship": "there is an existing customer relationship",
            "OptOut": "the customer opted out",
            "TransactionalNotice": "the contact is a transactional notice",
            "Emergency": "the contact concerns an emergency",
        },
        """
default_no: =>O ~ContactCustomer
relationship_ok: ExistingRelationship ~>O ContactCustomer
optout_no: OptOut =>O ~ContactCustomer
transaction_must: TransactionalNotice =>O ContactCustomer
emergency_must: Emergency =>O ContactCustomer
superiority: relationship_ok > default_no, optout_no > relationship_ok, transaction_must > optout_no, emergency_must > optout_no
""",
        "Partner shall not contact customers directly. Contact is permitted where an existing customer relationship exists. If a customer has opted out, contact is prohibited. Transactional notices and emergency notices shall be sent notwithstanding an opt-out.",
    ),
    Template(
        "reverse_engineering", "ReverseEngineer", "reverse engineer the software",
        "reverse engineering the software",
        {
            "Interoperability": "the activity is necessary for interoperability",
            "RequiredByLaw": "applicable law requires allowing the activity",
            "SecurityResearch": "the activity is good-faith security research",
            "NoticeGiven": "advance notice was given",
        },
        """
default_no: =>O ~ReverseEngineer
interop_ok: Interoperability ~>O ReverseEngineer
law_ok: RequiredByLaw ~>O ReverseEngineer
research_ok: SecurityResearch, NoticeGiven ~>O ReverseEngineer
superiority: interop_ok > default_no, law_ok > default_no, research_ok > default_no
""",
        "User shall not reverse engineer the software. The restriction does not apply to activity required by law or necessary for interoperability. Good-faith security research is permitted only if advance notice is given.",
    ),
]


def powerset(items: list[str]):
    for r in range(len(items) + 1):
        yield from itertools.combinations(items, r)


def status_from_template(t: Template, facts: set[str]) -> str:
    """Tiny evaluator for the generated benchmark's DDL subset.

    It mirrors the intended deontic pattern: applicable obligations compete,
    defeaters can establish permission, and explicit superiority decides
    exception stacks. This fallback lets the benchmark run on machines without
    Lean/Lake; the experiment script can still call the real binary when present.
    """
    rules = []
    superiority = set()
    for raw in t.rules.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("superiority:"):
            rest = line.split(":", 1)[1]
            for pair in rest.split(","):
                if ">" in pair:
                    l, r = pair.split(">", 1)
                    superiority.add((l.strip(), r.strip()))
            continue
        label, body = line.split(":", 1)
        if "=>O" in body:
            ant, con = body.split("=>O", 1)
            strength = "obligation"
        elif "~>O" in body:
            ant, con = body.split("~>O", 1)
            strength = "defeater"
        else:
            continue
        ants = {a.strip() for a in ant.split(",") if a.strip()}
        con = con.strip()
        side = "neg" if con.startswith("~") else "pos"
        rules.append({"label": label.strip(), "ants": ants, "side": side, "strength": strength})

    applicable = [r for r in rules if r["ants"] <= facts]
    pos = [r for r in applicable if r["side"] == "pos"]
    neg = [r for r in applicable if r["side"] == "neg"]

    def defeated(rule, opponents):
        return any((opp["label"], rule["label"]) in superiority for opp in opponents)

    pos_undefeated = [r for r in pos if not defeated(r, neg)]
    neg_undefeated = [r for r in neg if not defeated(r, pos)]
    pos_obl = [r for r in pos_undefeated if r["strength"] == "obligation"]
    neg_obl = [r for r in neg_undefeated if r["strength"] == "obligation"]
    pos_def = [r for r in pos_undefeated if r["strength"] == "defeater"]

    if pos_obl and neg_obl:
        return "unresolved"
    if pos_obl:
        return "O"
    if neg_obl:
        return "F"
    if pos_def and not neg_undefeated:
        return "P"
    if pos_def and all(any((p["label"], n["label"]) in superiority for p in pos_def) for n in neg_undefeated):
        return "P"
    return "unknown"


def answer_for(mode: str, status: str) -> str:
    if mode == "may":
        return "Yes" if status in {"O", "P", "Ps", "Pw"} else "No"
    if mode == "must":
        return "Yes" if status == "O" else "No"
    if mode == "must_not":
        return "Yes" if status == "F" else "No"
    raise ValueError(mode)


def hypothesis(t: Template, mode: str) -> str:
    if mode == "may":
        return f"The party may {t.act} in the described scenario."
    if mode == "must":
        return f"The party is required to {t.act} in the described scenario."
    return f"The party is prohibited from {t.gerund} in the described scenario."


def scenario(t: Template, facts: set[str]) -> str:
    bits = []
    for atom in [*t.facts, *DISTRACTORS]:
        desc = {**t.atoms, **DISTRACTORS}[atom]
        bits.append(("Present: " if atom in facts else "Absent: ") + desc + ".")
    return " ".join(bits)


def make_examples(seed: int, limit: int | None) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    modes = ["may", "must", "must_not"]
    dist_sets = [set(), {"UrgentReview"}, {"QuarterEnd"}, {"UrgentReview", "QuarterEnd"}]
    for t in TEMPLATES:
        for rel in powerset(t.facts):
            for dist in dist_sets:
                facts = set(rel) | set(dist)
                status = status_from_template(t, facts)
                for mode in modes:
                    rows.append({
                        "id": f"{t.tid}-{len(rows):05d}",
                        "task": "ambiguous_contracts",
                        "template": t.tid,
                        "text": f"Clause: {t.clause}\n\nScenario: {scenario(t, facts)}",
                        "hypothesis": hypothesis(t, mode),
                        "answer": answer_for(mode, status),
                        "mode": mode,
                        "facts": sorted(facts),
                        "target": t.target,
                        "status": status,
                        "ddl": t.ddl(),
                    })
    rng.shuffle(rows)
    return rows[:limit] if limit else rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="eval/sample/ambiguous_contracts.jsonl")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--limit", type=int, default=0, help="0 = all generated rows")
    args = ap.parse_args()
    rows = make_examples(args.seed, args.limit or None)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    yes = sum(r["answer"] == "Yes" for r in rows)
    print(f"wrote {len(rows)} examples -> {args.out}")
    print(f"labels: Yes={yes} No={len(rows) - yes}")
    print(f"templates={len(TEMPLATES)} modes=may/must/must_not")


if __name__ == "__main__":
    main()
