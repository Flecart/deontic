"""Two evaluation conditions over the same model:

  baseline : prompt the model directly for a label (LegalBench-style few-shot-free).
  tool     : give the model the `run_deontic` reasoner tool; it may call it for
             several rounds (formalize -> query -> refine) before answering.

Both return (label, transcript) where transcript is a list of dicts for logging
(the tool transcript is the auditability win this project argues for).
"""
from __future__ import annotations
import json

from deontic_tool import (run_deontic, TOOL_SCHEMA,
                          run_shell, SHELL_TOOL_SCHEMA, load_skill)


def _create(client, spec, messages, tools=None, temperature=0.0):
    kwargs = {"model": spec.model_id, "messages": messages}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    if not spec.reasoning:          # o-series reject custom temperature
        kwargs["temperature"] = temperature
    return client.chat.completions.create(**kwargs)


def parse_answer(text: str, labels: list[str]) -> str | None:
    """Extract the chosen label. Prefer an 'ANSWER: X' line; else substring match."""
    if not text:
        return None
    low = text.lower()
    lab_low = {l.lower(): l for l in labels}
    for line in reversed(text.splitlines()):
        s = line.strip()
        if ":" in s and s.split(":", 1)[0].strip().lower() in ("answer", "final answer", "label"):
            cand = s.split(":", 1)[1].strip().strip(".").strip()
            if cand.lower() in lab_low:
                return lab_low[cand.lower()]
            for l in labels:               # label appears within the answer line
                if l.lower() in cand.lower():
                    return l
    # last resort: last label mentioned anywhere
    best, pos = None, -1
    for l in labels:
        p = low.rfind(l.lower())
        if p > pos:
            best, pos = l, p
    return best


def _sys_baseline(task):
    return (f"You are a legal reasoning assistant for the task '{task['name']}'. "
            f"{task['instructions']} "
            f"Respond with a short rationale, then a final line exactly: ANSWER: <label> "
            f"where <label> is one of: {', '.join(task['labels'])}.")

def _sys_tool(task, max_rounds):
    return (_sys_baseline(task) +
            f"\n\nYou have a tool `run_deontic`: a formal defeasible-deontic-logic "
            f"reasoner. Before answering, you SHOULD formalize the relevant clause as a "
            f"small DDL theory and call the tool (up to {max_rounds} times) to check the "
            f"obligation/prohibition/permission status, then decide. Map the formal result "
            f"to the label set. Always finish with the 'ANSWER: <label>' line.")

def _user_msg(task, ex):
    return (f"Text:\n{ex['text']}\n\nHypothesis: {ex['hypothesis']}\n\n"
            f"{task['question']}")


def run_baseline(client, spec, task, ex, temperature=0.0):
    messages = [{"role": "system", "content": _sys_baseline(task)},
                {"role": "user", "content": _user_msg(task, ex)}]
    resp = _create(client, spec, messages, temperature=temperature)
    content = resp.choices[0].message.content or ""
    return parse_answer(content, task["labels"]), [{"role": "assistant", "content": content}]


def run_tool(client, spec, task, ex, max_rounds=4, temperature=0.0):
    messages = [{"role": "system", "content": _sys_tool(task, max_rounds)},
                {"role": "user", "content": _user_msg(task, ex)}]
    transcript = []
    for _ in range(max_rounds):
        resp = _create(client, spec, messages, tools=[TOOL_SCHEMA], temperature=temperature)
        msg = resp.choices[0].message
        tool_calls = getattr(msg, "tool_calls", None)
        if not tool_calls:
            content = msg.content or ""
            transcript.append({"role": "assistant", "content": content})
            pred = parse_answer(content, task["labels"])
            if pred is not None:
                return pred, transcript
            # no tool call and no parseable answer (e.g. empty content from some
            # tool-enabled models) -> nudge once for a plain answer, then continue
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user",
                             "content": f"Answer now with exactly one line: ANSWER: <one of {task['labels']}>."})
            continue
        # record + execute each tool call
        messages.append({"role": "assistant", "content": msg.content,
                         "tool_calls": [_tc_dump(tc) for tc in tool_calls]})
        for tc in tool_calls:
            try:
                a = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                a = {}
            result = run_deontic(a.get("ddl", ""), a.get("command", "check"),
                                 a.get("args"), a.get("flags"))
            transcript.append({"role": "tool", "call": a, "result": result})
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    # ran out of rounds: force a final answer with no more tools
    messages.append({"role": "user",
                     "content": f"Give your final answer now. ANSWER: <one of {task['labels']}>."})
    resp = _create(client, spec, messages, temperature=temperature)
    content = resp.choices[0].message.content or ""
    transcript.append({"role": "assistant", "content": content})
    return parse_answer(content, task["labels"]), transcript


def run_cli(client, spec, task, ex, max_rounds=4, temperature=0.0):
    """Agentic condition with raw CLI access: a `bash` tool (deontic on PATH)
    plus the skill doc in the system prompt. The model writes .ddl files and runs
    `deontic ...` itself for up to max_rounds rounds, then answers."""
    system = (_sys_baseline(task) +
              "\n\nYou have a `bash` tool: a shell in the project root with the `deontic` "
              f"reasoner on PATH. Before answering you SHOULD use it (up to {max_rounds} "
              "rounds) to formalize the relevant clause as a DDL theory and run the reasoner, "
              "then map the formal result to the label. Always finish with 'ANSWER: <label>'.\n\n"
              "=== deontic skill ===\n" + load_skill())
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": _user_msg(task, ex)}]
    transcript = []
    for _ in range(max_rounds):
        resp = _create(client, spec, messages, tools=[SHELL_TOOL_SCHEMA], temperature=temperature)
        msg = resp.choices[0].message
        tool_calls = getattr(msg, "tool_calls", None)
        if not tool_calls:
            content = msg.content or ""
            transcript.append({"role": "assistant", "content": content})
            pred = parse_answer(content, task["labels"])
            if pred is not None:
                return pred, transcript
            # no tool call and no parseable answer (e.g. empty content from some
            # tool-enabled models) -> nudge once for a plain answer, then continue
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user",
                             "content": f"Answer now with exactly one line: ANSWER: <one of {task['labels']}>."})
            continue
        messages.append({"role": "assistant", "content": msg.content,
                         "tool_calls": [_tc_dump(tc) for tc in tool_calls]})
        for tc in tool_calls:
            try:
                a = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                a = {}
            result = run_shell(a.get("command", ""))
            transcript.append({"role": "tool", "call": a, "result": result})
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    messages.append({"role": "user",
                     "content": f"Give your final answer now. ANSWER: <one of {task['labels']}>."})
    resp = _create(client, spec, messages, temperature=temperature)
    content = resp.choices[0].message.content or ""
    transcript.append({"role": "assistant", "content": content})
    return parse_answer(content, task["labels"]), transcript


def _tc_dump(tc):
    return {"id": tc.id, "type": "function",
            "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
