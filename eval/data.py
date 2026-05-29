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
}


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
    if args.data:
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
    if args.limit:
        rows = rows[: args.limit]
    return rows
