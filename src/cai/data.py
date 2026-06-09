"""Red-team prompt loading: bundled seed JSONL or a configurable HF dataset."""

from __future__ import annotations

import json
from pathlib import Path

from .config import Config, resolve_path


def _from_seed(path: str | Path) -> list[str]:
    prompts: list[str] = []
    for line in resolve_path(path).read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        prompts.append(json.loads(line)["prompt"])
    return prompts


def _from_hf(cfg: Config) -> list[str]:
    from datasets import load_dataset  # imported lazily; heavy + optional

    ds = load_dataset(cfg.data.hf_name, cfg.data.get("hf_config"), split=cfg.data.hf_split)

    field = cfg.data.get("hf_text_field")
    if field:
        return [row[field] for row in ds]

    # Heuristic fallback: first string-like column, else first column.
    column = next(
        (c for c in ds.column_names if c.lower() in {"prompt", "question", "instruction", "text"}),
        ds.column_names[0],
    )
    out = []
    for value in ds[column]:
        out.append(value if isinstance(value, str) else str(value))
    return out


def load_prompts(cfg: Config) -> list[str]:
    """Return the list of red-team prompts per the data config."""
    source = cfg.data.source
    if source == "seed":
        prompts = _from_seed(cfg.data.seed_path)
    elif source == "hf":
        prompts = _from_hf(cfg)
    else:
        raise ValueError(f"Unknown data.source: {source!r} (expected 'seed' or 'hf')")

    limit = cfg.data.get("max_prompts")
    if limit:
        prompts = prompts[:limit]
    if not prompts:
        raise ValueError("No prompts loaded")
    return prompts


def write_jsonl(rows: list[dict], path: str | Path) -> Path:
    out = resolve_path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return out


def read_jsonl(path: str | Path) -> list[dict]:
    rows = []
    for line in resolve_path(path).read_text().splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows
