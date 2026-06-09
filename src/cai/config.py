"""Configuration: nested dataclasses loaded by deep-merging YAML layers + CLI sets.

Layering order (lowest precedence first):
    configs/base.yaml  <-  profile/stage yaml (e.g. smoke.yaml)  <-  --set k=v

Access is attribute-style (cfg.model.name) but everything is ultimately a plain
dict under the hood, so unknown keys are preserved and round-trip cleanly.
"""

from __future__ import annotations

import ast
import copy
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE = REPO_ROOT / "configs" / "base.yaml"


class Config(dict):
    """A dict with attribute access; nested dicts are wrapped lazily."""

    def __getattr__(self, key: str) -> Any:
        try:
            value = self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc
        if isinstance(value, dict) and not isinstance(value, Config):
            value = Config(value)
            self[key] = value
        return value

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value

    def get_path(self, dotted: str, default: Any = None) -> Any:
        node: Any = self
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge ``override`` into a copy of ``base``."""
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _coerce(raw: str) -> Any:
    """Turn a CLI string into a Python scalar (int/float/bool/None/list/...)."""
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return raw


def _apply_set(cfg: dict, dotted: str, raw: str) -> None:
    """Apply one ``a.b.c=value`` override in place."""
    parts = dotted.split(".")
    node = cfg
    for part in parts[:-1]:
        node = node.setdefault(part, {})
        if not isinstance(node, dict):
            raise ValueError(f"Cannot set '{dotted}': '{part}' is not a mapping")
    node[parts[-1]] = _coerce(raw)


def load_config(
    profiles: list[str] | None = None,
    overrides: list[str] | None = None,
    base: str | Path | None = None,
) -> Config:
    """Build the effective config.

    Args:
        profiles: paths to YAML files merged (in order) on top of base.
        overrides: ``key.path=value`` strings applied last.
        base: base YAML path (defaults to configs/base.yaml).
    """
    base_path = Path(base) if base else DEFAULT_BASE
    merged: dict = yaml.safe_load(base_path.read_text()) or {}

    for profile in profiles or []:
        path = Path(profile)
        if not path.exists():  # allow bare profile names: configs/<name>.yaml
            path = REPO_ROOT / "configs" / f"{profile}.yaml"
        merged = _deep_merge(merged, yaml.safe_load(path.read_text()) or {})

    for item in overrides or []:
        if "=" not in item:
            raise ValueError(f"--set expects key=value, got: {item!r}")
        key, raw = item.split("=", 1)
        _apply_set(merged, key.strip(), raw.strip())

    return Config(merged)


def resolve_path(value: str | Path) -> Path:
    """Resolve a possibly-relative path against the repo root."""
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path
