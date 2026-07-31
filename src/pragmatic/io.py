from __future__ import annotations

import os
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DATA = Path(__file__).resolve().parent / "_data"
REPO_METHOD = ROOT / "method" / "inteligencia-pragmatica.yaml"
REPO_TEMPLATE = ROOT / "templates" / "objective.yaml"
DEFAULT_METHOD = (
    REPO_METHOD
    if REPO_METHOD.exists()
    else PACKAGE_DATA / "method" / "inteligencia-pragmatica.yaml"
)
DEFAULT_TEMPLATE = (
    REPO_TEMPLATE if REPO_TEMPLATE.exists() else PACKAGE_DATA / "templates" / "objective.yaml"
)


class DocumentError(ValueError):
    """Raised when a YAML document cannot be loaded safely."""


def load_yaml(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise DocumentError(f"Não foi possível ler {target}: {exc}") from exc
    if not isinstance(data, dict):
        raise DocumentError(f"{target} deve conter um objeto YAML na raiz")
    return data


def dump_yaml(data: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    rendered = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)
    target.write_text(rendered, encoding="utf-8")


def load_method(path: str | Path | None = None) -> dict[str, Any]:
    selected = path or os.environ.get("PRAGMATIC_METHOD") or DEFAULT_METHOD
    return load_yaml(selected)


def load_template() -> dict[str, Any]:
    return deepcopy(load_yaml(DEFAULT_TEMPLATE))
