"""CPU-only unit tests: config merge, constitution, data, jsonl. No GPU/network."""

from __future__ import annotations

import json

import pytest

from cai.config import load_config
from cai.constitution import load_constitution
from cai.data import load_prompts, read_jsonl, write_jsonl


def test_base_config_loads():
    cfg = load_config()
    assert cfg.model.name
    assert cfg.rl.method in {"dpo", "grpo"}
    assert cfg.lora.target_modules


def test_profile_merge_and_overrides():
    cfg = load_config(profiles=["smoke"], overrides=["rl.method=grpo", "train.max_steps=5"])
    assert cfg.model.name == "Qwen/Qwen3-0.6B"   # from smoke.yaml
    assert cfg.rl.method == "grpo"               # from --set
    assert cfg.train.max_steps == 5              # coerced to int
    assert cfg.lora.r == 16                       # untouched base value


def test_override_type_coercion():
    cfg = load_config(overrides=["lora.enabled=False", "rl.beta=0.2"])
    assert cfg.lora.enabled is False
    assert cfg.rl.beta == pytest.approx(0.2)


def test_constitution_loads():
    cfg = load_config()
    const = load_constitution(cfg.constitution.path)
    assert len(const.principles) >= 1
    p = const.principles[0]
    assert p.critique_request and p.revision_request
    assert const.judge_rubric


def test_seed_prompts_load():
    cfg = load_config(overrides=["data.max_prompts=5"])
    prompts = load_prompts(cfg)
    assert len(prompts) == 5
    assert all(isinstance(p, str) and p for p in prompts)


def test_jsonl_roundtrip(tmp_path):
    rows = [{"prompt": "a", "response": "b"}, {"prompt": "c", "response": "d"}]
    path = tmp_path / "x.jsonl"
    write_jsonl(rows, path)
    assert read_jsonl(path) == rows
    # File is valid line-delimited JSON.
    for line in path.read_text().splitlines():
        json.loads(line)
