# Cross-statute aggregate (3 families: gpt-4.1, deepseek, qwen)

## Atom-level accuracy by regime x tier (per statute + pooled)

| statute | closed T0/T1/T2 | open T0/T1/T2 | open-closed gap T2 |
|---|---|---|---|
Traceback (most recent call last):
  File "/home/flecart/Desktop/work/deontic/eval/aggregate.py", line 70, in <module>
    rows = load(rf, cf, ov)
  File "/home/flecart/Desktop/work/deontic/eval/aggregate.py", line 31, in load
    lk = leaky(cases_file)
  File "/home/flecart/Desktop/work/deontic/eval/aggregate.py", line 27, in leaky
    return {json.loads(l)["case_id"] for l in open(cases_file) if json.loads(l).get("leak_flags")}
                                              ~~~~^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'expA/cases_stage2_memo.jsonl'
