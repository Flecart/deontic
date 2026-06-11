"""Shared asyncio helpers for corpus evaluation pipelines (FOIA, EIR, tax, …).

Pipelines fan work out with ``asyncio.gather``; :class:`AsyncLLM` caps in-flight
OpenAI calls with a semaphore. Blocking engine (subprocess) work goes through
:class:`EngineGate` so a cached :class:`deontic_py.Deontic` stays safe.

Typical wiring::

    EXPERIMENTS = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(EXPERIMENTS))
    from corpus_async import RunLog, AsyncLLM, EngineGate, parse_json_reply

    log = RunLog(RUNS_DIR)
    llm = AsyncLLM(args.model, log, concurrency=args.concurrency)
    engine = EngineGate(d)

    async def ground_batch(...):
        reply = await llm.chat(GROUND_SYSTEM, user, meta)
        ...

    results = await asyncio.gather(*[ground_batch(...) for ...])
    pred = await engine.call(engine_result, d, facts, ...)
"""
from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import re
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


class RunLog:
    """Append-only JSONL run log."""

    def __init__(self, runs_dir: Path) -> None:
        self._runs_dir = runs_dir
        self._path: Path | None = None
        self._lock = asyncio.Lock()

    @property
    def path(self) -> Path | None:
        return self._path

    def start(self, tag: str) -> Path:
        self._runs_dir.mkdir(exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self._path = self._runs_dir / f"run_{stamp}_{tag}.jsonl"
        return self._path

    async def event(self, record: dict) -> None:
        if self._path is None:
            return
        record = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
                  **record}
        line = json.dumps(record, ensure_ascii=False) + "\n"
        async with self._lock:
            with self._path.open("a") as fh:
                fh.write(line)


class AsyncLLM:
    """Async OpenAI chat: gather schedules freely; semaphore limits concurrency."""

    def __init__(self, model: str, log: RunLog, *, concurrency: int = 1) -> None:
        self.model = model
        self._log = log
        self.concurrency = max(1, concurrency)
        self._sem = asyncio.Semaphore(self.concurrency)
        self._client = None

    def _client_lazy(self):
        if self._client is None:
            from openai import AsyncOpenAI
            self._client = AsyncOpenAI()
        return self._client

    async def chat(self, system: str, user: str, meta: dict | None = None) -> str:
        async with self._sem:
            t0 = time.time()
            resp = await self._client_lazy().chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
            )
            reply = resp.choices[0].message.content or ""
            usage = resp.usage
            await self._log.event({
                "type": "llm_call",
                **(meta or {}),
                "model": self.model,
                "system": system,
                "user": user,
                "reply": reply,
                "seconds": round(time.time() - t0, 2),
                "prompt_tokens": getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
            })
            return reply


class EngineGate:
    """Run blocking engine calls off the loop; serialize when the client is cached."""

    def __init__(self, engine, *, cached: bool = True) -> None:
        self._engine = engine
        self._lock = asyncio.Lock() if cached else None

    async def call(self, func: Callable[..., T], /, *args, **kwargs) -> T:
        async def _run() -> T:
            return await asyncio.to_thread(func, *args, **kwargs)

        if self._lock is None:
            return await _run()
        async with self._lock:
            return await _run()


async def run_all(*aws: Awaitable[T]) -> list[T]:
    """Schedule every awaitable at once; return results in submission order."""
    return list(await asyncio.gather(*aws))


def parse_json_reply(text: str) -> dict:
    """Tolerate code fences / prose around the JSON object."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON object in model reply:\n{text}")
    return json.loads(m.group(0))


def add_concurrency_arg(ap: argparse.ArgumentParser, default: int = 1) -> None:
    ap.add_argument("--concurrency", type=int, default=default, metavar="N",
                    help="max simultaneous OpenAI API calls (default: %(default)s)")


def concurrency_error(n: int) -> str | None:
    if n < 1:
        return "error: --concurrency must be >= 1"
    return None
