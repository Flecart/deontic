"""Task definitions + dataset loading for the eval harness.

Examples are dicts: {text, hypothesis, answer, task}. Load from JSONL (our
sample format) or a LegalBench-style TSV. Real LegalBench data:
`datasets.load_dataset("nguha/legalbench", "<task>")` (online) or download the
task's test.tsv and point --data at it.
"""
from __future__ import annotations
import json
import os

# Per-task framing. `labels` is the allowed answer set; `answer_map` normalizes
# raw gold labels (e.g. LegalBench "Yes"/"No") to our label set.
TASKS = {
    "contract_nli": {
        "name": "contract_nli",
        "labels": ["Yes", "No"],
        "instructions": ("Decide whether the contract supports the stated hypothesis. "
                         "Answer Yes if the contract entails it, No otherwise."),
        "question": "Does the contract support the hypothesis? Answer Yes or No.",
        "answer_map": {"yes": "Yes", "no": "No", "entailment": "Yes",
                       "contradiction": "No", "notmentioned": "No", "not mentioned": "No"},
    },
    # generic statutory/contract yes-no duty question (cuad, privacy, fdcpa, ...)
    "duty_qa": {
        "name": "duty_qa",
        "labels": ["Yes", "No"],
        "instructions": ("Decide whether, under the quoted rule/contract, the stated "
                         "obligation/permission/prohibition holds. Answer Yes or No."),
        "question": "Under the rule, is the hypothesis correct? Answer Yes or No.",
        "answer_map": {"yes": "Yes", "no": "No"},
    },
    "ambiguous_contracts": {
        "name": "ambiguous_contracts",
        "labels": ["Yes", "No"],
        "instructions": ("Decide whether the contract clause and described facts entail "
                         "the stated permission, obligation, or prohibition. Answer Yes "
                         "only when the hypothesis follows from the clause; answer No "
                         "for contradictions, unresolved conflicts, or silence."),
        "question": "Does the clause entail the hypothesis in this scenario? Answer Yes or No.",
        "answer_map": {"yes": "Yes", "no": "No"},
    },
}


# LegalBench contract_nli configs -> the hypothesis (matches our formalizations
# in examples/legalbench/contract-nli/). Gold answers in the data are Yes/No.
LEGALBENCH_HYPOTHESES = {
    "contract_nli_confidentiality_of_agreement":
        "The Receiving Party shall not disclose the fact that the Agreement was agreed or negotiated.",
    "contract_nli_explicit_identification":
        "All Confidential Information shall be expressly identified by the Disclosing Party.",
    "contract_nli_inclusion_of_verbally_conveyed_information":
        "Confidential Information may include verbally conveyed information.",
    "contract_nli_limited_use":
        "The Receiving Party shall not use any Confidential Information for any purpose other than the purposes stated in the Agreement.",
    "contract_nli_no_licensing":
        "The Agreement shall not grant the Receiving Party any right to Confidential Information.",
    "contract_nli_notice_on_compelled_disclosure":
        "The Receiving Party shall notify the Disclosing Party in case it is required by law, regulation or judicial process to disclose any Confidential Information.",
    "contract_nli_permissible_acquirement_of_similar_information":
        "The Receiving Party may acquire information similar to Confidential Information from a third party.",
    "contract_nli_permissible_copy":
        "The Receiving Party may create a copy of some Confidential Information in some circumstances.",
    "contract_nli_permissible_development_of_similar_information":
        "The Receiving Party may independently develop information similar to Confidential Information.",
    "contract_nli_permissible_post-agreement_possession":
        "The Receiving Party may retain some Confidential Information even after the return or destruction of Confidential Information.",
    "contract_nli_return_of_confidential_information":
        "The Receiving Party shall destroy or return some Confidential Information upon the termination of the Agreement.",
    "contract_nli_sharing_with_employees":
        "The Receiving Party may share some Confidential Information with some of the Receiving Party's employees.",
    "contract_nli_sharing_with_third-parties":
        "The Receiving Party may share some Confidential Information with some third parties (including consultants, agents and professional advisors).",
    "contract_nli_survival_of_obligations":
        "Some obligations of the Agreement may survive termination of the Agreement.",
}


def load_legalbench(lb_task: str, split: str = "test") -> list[dict]:
    """Load a real LegalBench task split from HuggingFace (`nguha/legalbench`)."""
    from datasets import load_dataset
    if lb_task not in LEGALBENCH_HYPOTHESES:
        raise SystemExit(f"unmapped LegalBench task '{lb_task}'. Known: "
                         + ", ".join(sorted(LEGALBENCH_HYPOTHESES)))
    hyp = LEGALBENCH_HYPOTHESES[lb_task]
    ds = load_dataset("nguha/legalbench", lb_task)[split]
    return [{"text": r["text"], "hypothesis": hyp, "answer": r["answer"]} for r in ds]


def get_task(name: str) -> dict:
    if name not in TASKS:
        raise SystemExit(f"unknown task '{name}'. Known: {list(TASKS)}")
    return TASKS[name]


def normalize_answer(task: dict, raw: str) -> str:
    return task["answer_map"].get(str(raw).strip().lower(), str(raw).strip())


def load_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_tsv(path: str, text_col="text", answer_col="answer",
             hypothesis_col=None, hypothesis=None) -> list[dict]:
    import csv
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rows.append({
                "text": r.get(text_col, ""),
                "hypothesis": (r.get(hypothesis_col) if hypothesis_col else hypothesis) or "",
                "answer": r.get(answer_col, ""),
            })
    return rows


def load_examples(args, task: dict) -> list[dict]:
    if getattr(args, "legalbench", None):
        rows = load_legalbench(args.legalbench, getattr(args, "split", "test"))
    elif args.data:
        rows = (load_jsonl(args.data) if args.data.endswith(".jsonl")
                else load_tsv(args.data, args.text_col, args.answer_col,
                              args.hypothesis_col, args.hypothesis))
    else:
        sample = os.path.join(os.path.dirname(__file__), "sample", f"{task['name']}.jsonl")
        if not os.path.exists(sample):
            raise SystemExit(f"no --data given and no sample at {sample}")
        rows = load_jsonl(sample)
    # fill defaults + normalize gold
    for r in rows:
        r.setdefault("hypothesis", args.hypothesis or "")
        r["gold"] = normalize_answer(task, r.get("answer", ""))
    # LegalBench splits are sorted by label; shuffle so a --limit slice is balanced.
    if getattr(args, "shuffle", False):
        import random
        random.Random(getattr(args, "seed", 0)).shuffle(rows)
    if args.limit:
        rows = rows[: args.limit]
    return rows
